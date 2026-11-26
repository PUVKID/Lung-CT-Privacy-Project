"""CPU 실제 특징 역복원·사진 결과 분리·Windows 프로세스 잠금 검사입니다."""
import importlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
engine=importlib.import_module('실행')
attack=importlib.import_module('공격')
feature=importlib.import_module('특징노출')

def checkpoint(path,actual=False,deficient=False):
    import torch
    torch.set_num_threads(2)
    std=torch.tensor([.229,.224,.225]).reshape(1,3,1,1)
    if actual:
        config=engine.read_json(ROOT/'config.json')
        if engine.digest(config['initial_weights_path'])!=config['initial_weights_sha256']:
            raise ValueError('고정 초기 가중치 SHA 불일치')
        weights=torch.load(config['initial_weights_path'],map_location='cpu',weights_only=True)['conv1.weight']
    else:
        generator=torch.Generator().manual_seed(71)
        kernel=torch.zeros(64,49) if deficient else torch.randn(64,49,generator=generator)
        weights=torch.zeros(64,3,7,7)
        weights[:,0]=kernel.reshape(64,7,7)*std[0,0]
    engine.save_torch(path,{'model':{'front.conv1.weight':weights,'rgb_mean':torch.tensor([.485,.456,.406]).reshape(1,3,1,1),'rgb_std':std}})

class FeatureTests(unittest.TestCase):
    def test_random_and_actual_512_feature_inverse(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'best.pth'
            x=np.random.default_rng(42).integers(0,256,(512,512),dtype=np.uint8).astype(np.float32)/255
            for actual in (False,True):
                checkpoint(path,actual=actual)
                inverter=feature.FeatureExposure(path,engine.digest(path))
                recovered=inverter.transform(x)
                metadata=inverter.metadata()
                self.assertEqual(metadata['rank'],49)
                self.assertLess(np.max(np.abs(recovered[0.]-x)),1e-4)
                self.assertEqual(metadata['lambda_ratios'],[0.,1e-8,1e-6])
                self.assertFalse(metadata['full_feature_files_saved'])
                self.assertEqual(recovered[0.].dtype,np.float32)
                self.assertLess(metadata['diagnostics']['unspecified']['0.0']['means']['forward_relative_mse'],1e-9)
    def test_deficient_nan_and_checkpoint_tamper(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'best.pth'
            checkpoint(path,deficient=True)
            inverter=feature.FeatureExposure(path,engine.digest(path))
            inverter.transform(np.zeros((32,32),dtype=np.float32))
            self.assertEqual(inverter.metadata()['rank'],0)
            self.assertIsNotNone(inverter.metadata()['rank_reason'])
            with self.assertRaises(ValueError):
                inverter.transform(np.full((32,32),np.nan,dtype=np.float32))
            path.write_bytes(b'tampered')
            with self.assertRaises(ValueError):
                inverter.verify_checkpoint()
            with self.assertRaises(ValueError):
                feature.FeatureExposure(path,'wrong-sha')
    def test_photo_and_feature_results_are_separate(self):
        import torch
        from PIL import Image
        with tempfile.TemporaryDirectory() as temporary:
            runtime=Path(temporary)
            folder=runtime/'conditions'/'feature_fixture'
            folder.mkdir(parents=True)
            checkpoint(folder/'best.pth')
            rows={}
            for split in ('train','validation','test','test_generated'):
                rows[split]=[]
                for label in (0,1):
                    pixels=np.full((512,512),40+label*170,dtype=np.uint8)
                    source=runtime/f'{split}_{label}.png'
                    Image.fromarray(pixels).save(source)
                    packet=runtime/f'{split}_{label}.ctb'
                    packet.write_bytes(engine.encode(pixels,2,'블러_축소64_4비트'))
                    rows[split].append({'label':label,'unblurred_path':str(source),'unblurred_sha256':engine.digest(source),
                        'packet_path':str(packet),'packet_sha256':engine.digest(packet)})
            config=engine.read_json(ROOT/'config.json')
            data={'sigma':2,'profile':'블러_축소64_4비트','splits':rows}
            with patch.object(attack,'fit_decoder',return_value=torch.nn.Identity()):
                photo=attack.run_attack(config,folder,data,'cpu',False,'feature-fixture-run')
                before=engine.digest(folder/'attack.json')
                inverter=feature.FeatureExposure(folder/'best.pth',engine.digest(folder/'best.pth'))
                exposed=attack.run_attack(config,folder,data,'cpu',False,'feature-fixture-run',exposure=inverter)
            self.assertEqual(engine.digest(folder/'attack.json'),before)
            self.assertEqual(len(photo['candidate_metrics']),9)
            self.assertEqual(len(exposed['candidate_metrics']),27)
            self.assertTrue((folder/'feature_exposure'/'attack.json').exists())
            self.assertNotEqual(photo['examples'][0]['reconstructed'],exposed['examples'][0]['reconstructed'])
            self.assertEqual(exposed['test_generated']['count'],2)
            self.assertTrue(exposed['photo_decoder_reused'])
            self.assertEqual(exposed['exposure']['rank'],49)
    def test_process_guard_and_stale_pid_preservation(self):
        import psutil
        with tempfile.TemporaryDirectory() as temporary:
            runtime=Path(temporary)
            code="import sys; from pathlib import Path; import 실행; p=Path(sys.argv[1]);\nwith 실행.lock(p):\n print('held',flush=True); sys.stdin.readline()"
            process=subprocess.Popen([sys.executable,'-B','-X','utf8','-c',code,str(runtime)],cwd=ROOT,
                                     stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
            worker=None
            try:
                self.assertEqual(process.stdout.readline().strip(),'held')
                with self.assertRaises(RuntimeError):
                    with engine.lock(runtime):
                        pass
                process.communicate('\n',timeout=15)
                self.assertEqual(process.returncode,0)
                with engine.lock(runtime):
                    pass
                # 비정상 종료의 PID 기록은 삭제하지 않고 이력으로 보존합니다.
                crash_code=code.replace('sys.stdin.readline()',"__import__('time').sleep(60)")
                process=subprocess.Popen([sys.executable,'-B','-X','utf8','-c',crash_code,str(runtime)],cwd=ROOT,
                                         stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
                self.assertEqual(process.stdout.readline().strip(),'held')
                saved=(runtime/'실행.lock').read_bytes()
                owner=engine.read_json(runtime/'실행.lock')
                worker=psutil.Process(owner['pid'])
                self.assertAlmostEqual(worker.create_time(),owner['created'],places=2)
                self.assertIn(crash_code,worker.cmdline())
                self.assertIn(str(runtime),worker.cmdline())
                worker.kill()
                worker.wait(timeout=15)
                process.wait(timeout=15)
                self.assertNotEqual(process.returncode,0)
                self.assertEqual((runtime/'실행.lock').read_bytes(),saved)
                process.communicate(timeout=15)
                with engine.lock(runtime):
                    self.assertEqual(len(list(runtime.glob('실행.stale.*.json'))),1)
                    self.assertEqual(next(runtime.glob('실행.stale.*.json')).read_bytes(),saved)
                self.assertTrue((runtime/'실행.guard').exists())
                (runtime/'실행.lock').write_bytes(b'{partial')
                with engine.lock(runtime):
                    preserved=list(runtime.glob('실행.stale.*.json'))
                    self.assertEqual(len(preserved),2)
                    self.assertTrue(any(path.read_bytes()==b'{partial' for path in preserved))
                    self.assertEqual(len(list(runtime.glob('*.reason.txt'))),2)
            finally:
                if worker is not None:
                    try:
                        if worker.is_running() and abs(worker.create_time()-owner['created'])<.01 and crash_code in worker.cmdline():
                            worker.kill()
                            worker.wait(timeout=15)
                    except psutil.NoSuchProcess:
                        pass
                if process.poll() is None:
                    process.kill()
                    process.communicate(timeout=15)

if __name__=='__main__':
    unittest.main()
