"""GPU·원본 영상 변경 없이 확인하는 엔진 경계 검사입니다."""
import importlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
engine=importlib.import_module('실행')
attack=importlib.import_module('공격')

class EngineTests(unittest.TestCase):
    def test_all_conditions(self):
        self.assertEqual(len(set(engine.conditions(engine.read_json(ROOT/'config.json')))),60)
    def test_canonical_actual_manifest(self):
        rows=engine.canonical(engine.read_json(ROOT/'config.json'))
        self.assertEqual([len(rows[s]) for s in ('train','validation','test')],[769,164,164])
    def test_balanced_sampling(self):
        rows=[{'label':0},{'label':1}]
        result=engine.train_rows(rows,3000,42)
        self.assertEqual(result,engine.train_rows(rows,3000,42))
        self.assertEqual(sum(r['label']==1 for r in result),3000)
        self.assertEqual(len(result),6000)
    def test_atomic_failure_preserves_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'state.json'
            engine.save_json(path,{'before':True})
            def broken(temp):
                temp.write_text('incomplete',encoding='utf-8')
                raise OSError('제어된 쓰기 실패')
            with self.assertRaises(OSError):
                engine.atomic(path,broken)
            self.assertEqual(engine.read_json(path),{'before':True})
            self.assertEqual(len(list(Path(tmp).glob('*.tmp'))),1)
    def test_live_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            with engine.lock(Path(tmp)):
                with self.assertRaises(RuntimeError):
                    with engine.lock(Path(tmp)):
                        pass
    def test_cuda_guard_refuses_foreign_process(self):
        class Process:
            stdout='123456, active_training.exe\n'
        with patch.object(engine.subprocess,'run',return_value=Process()):
            with self.assertRaises(RuntimeError):
                engine.cuda_guard()
    def test_metrics(self):
        x=np.zeros((512,512),dtype=np.float32)
        self.assertEqual(attack.metrics(x,x)['ssim'],1.)
        self.assertTrue(attack.metrics(x,x)['psnr_infinite'])
        self.assertTrue(np.isfinite(attack.deblur(x,256,1e-12)).all())
    def test_cpu_packet_optimizer_resume_attack(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine.smoke(Path(tmp))
            result=engine.read_json(Path(tmp)/'smoke.json')
            self.assertTrue(result['resume_equal'])
            self.assertEqual([r['bytes'] for r in result['profiles']],[262153,16393,2057])
            self.assertIsInstance(result['reconstruction']['ssim'],float)
    def test_classifier_and_attack_epoch_resume(self):
        import torch
        import legacy.model
        from PIL import Image
        torch.set_num_threads(2)
        class Tiny(torch.nn.Module):
            def __init__(self,**kwargs):
                super().__init__()
                self.front=torch.nn.Module()
                self.front.conv1=torch.nn.Conv2d(3,3,1)
                self.head=torch.nn.Linear(3,1)
            def forward_from_blurred(self,x):
                return self.head(self.front.conv1(x).mean((-2,-1))).squeeze(1)
        config=engine.read_json(ROOT/'config.json')
        config.update(epochs=2,min_epochs=1,patience=2,samples_per_class=1,reserve_gib=0)
        config['reconstruction'].update(epochs=1,min_epochs=1,patience=1)
        with tempfile.TemporaryDirectory() as tmp:
            runtime=Path(tmp)
            folder=runtime/'conditions'/'sigma_002_블러_축소64_4비트'
            folder.mkdir(parents=True)
            rows={}
            for split in ('train','validation','test'):
                rows[split]=[]
                for label in (0,1):
                    pixels=np.full((512,512),40+label*170,dtype=np.uint8)
                    original=runtime/f'{split}_{label}.png'
                    Image.fromarray(pixels).save(original)
                    packet=runtime/f'{split}_{label}.ctb'
                    packet.write_bytes(engine.encode(pixels,2,'블러_축소64_4비트'))
                    rows[split].append({'id':f'{split}_{label}','label':label,'source_id':f'{split}{label}','source_group':f'{split}_group{label}','unblurred_path':str(original),
                        'unblurred_sha256':engine.digest(original),'packet_path':str(packet),'packet_sha256':engine.digest(packet)})
            rows['test_generated']=[dict(r) for r in rows['test']]
            data={'sigma':2,'profile':'블러_축소64_4비트','splits':rows}
            save=engine.save_json
            interrupted=False
            def stop_after_checkpoint(path,value):
                nonlocal interrupted
                if Path(path).name=='current.json' and not interrupted:
                    interrupted=True
                    raise RuntimeError('제어된 epoch 경계 중단')
                save(path,value)
            with patch.object(legacy.model,'SplitResNet50',Tiny):
                with patch.object(engine,'save_json',side_effect=stop_after_checkpoint):
                    with self.assertRaisesRegex(RuntimeError,'제어된'):
                        engine.classify(config,folder,data,'cpu',False,'test-run')
                result=engine.classify(config,folder,data,'cpu',True,'test-run')
            self.assertEqual(result['test']['total'],2)
            self.assertEqual(result['test_generated']['total'],2)
            self.assertEqual(result['test']['n_similarity_groups'],2)
            self.assertEqual(result['test_generated']['n_similarity_groups'],2)
            self.assertIn('accuracy_ci95_group',result['test'])
            self.assertEqual(set(result['feature_maps']),{'OK','NG'})
            for feature in result['feature_maps'].values():
                self.assertEqual(feature['settings']['layer'],'front.conv1')
                self.assertTrue((runtime/feature['path']).is_file())
            self.assertEqual(len(engine.read_json(folder/'history.json')),2)
            recovered=attack.run_attack(config,folder,data,'cpu',True,'test-run')
            self.assertEqual(len(recovered['candidate_metrics']),9)
            self.assertEqual(recovered['test']['count'],2)
            self.assertEqual(recovered['test_generated']['count'],2)
            self.assertEqual(len(recovered['examples']),2)
            self.assertTrue((runtime/recovered['examples'][0]['original']).is_file())
            for candidate in recovered['candidate_metrics'].values():
                for split in ('validation','test'):
                    self.assertEqual(candidate[split]['count'],2)
                    for label in ('OK','NG'):
                        report=candidate[split+'_by_class'][label]
                        self.assertEqual(report['count'],1)
                        self.assertGreater(report['mean_baseline_mse'],0)
                        self.assertGreaterEqual(report['privacy_error_score'],0)
                        self.assertLessEqual(report['privacy_error_score'],100)
                        self.assertAlmostEqual(report['privacy_error_ratio_raw'],report['mse']/report['mean_baseline_mse'])
            # 실제 0분모: 학습·검증·시험 전체를 같은 검정영상으로 바꾼 별도 조건입니다.
            zero_folder=runtime/'conditions'/'zero_prior'
            zero_folder.mkdir()
            for records in rows.values():
                for row in records:
                    path=Path(row['unblurred_path'])
                    Image.fromarray(np.zeros((512,512),dtype=np.uint8)).save(path)
                    row['unblurred_sha256']=engine.digest(path)
                    packet=Path(row['packet_path'])
                    packet.write_bytes(engine.encode(np.zeros((512,512),dtype=np.uint8),2,'블러_축소64_4비트'))
                    row['packet_sha256']=engine.digest(packet)
            zero=attack.run_attack(config,zero_folder,data,'cpu',False,'zero-run')
            self.assertIsNone(zero['privacy_score'])
            self.assertIsNotNone(zero['undefined_reason'])
            for candidate in zero['candidate_metrics'].values():
                self.assertIsNone(candidate['test']['privacy_error_score'])
                self.assertIsNotNone(candidate['test']['undefined_reason'])
    def test_generated_test_ancestry_and_row_ids(self):
        canonical=[{'source_id':'a','source_group':'g'}]
        records=[{'id':'first','source_id':'a','source_group':'g','split':'test'},
                 {'id':'second','source_id':'a','source_group':'g','split':'test'}]
        self.assertEqual(len(engine.validate_generated(records,canonical)),2)
        wrong=[dict(records[0],source_group='training_group')]
        with self.assertRaises(ValueError):
            engine.validate_generated(wrong,canonical)
        with self.assertRaises(ValueError):
            engine.validate_generated([records[0],records[0]],canonical)
    def test_fixed_2000_test_plan(self):
        config=engine.read_json(ROOT/'config.json')
        first=engine.fixed_test_plan(config)
        self.assertEqual(first,engine.fixed_test_plan(config))
        self.assertEqual(len(first['rows']),2000)
        self.assertEqual(sum(r['label']==0 for r in first['rows']),1000)
        self.assertEqual(sum(r['canonical'] for r in first['rows']),164)
        engine.validate_generated(first['rows'],engine.canonical(config)['test'])
        for row in first['rows']:
            if row['canonical']:
                self.assertEqual(row['fixed_transform'],{'hflip':False,'contrast':1.,'brightness':0.})
    def test_existing_packets_need_no_duplicate_disk_space(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime=Path(tmp)
            selected=[(2,'블러_축소64_4비트')]
            folder=runtime/'conditions'/engine.condition_id(*selected[0])
            path=folder/'packets'/'test'/'first.ctb'
            path.parent.mkdir(parents=True)
            path.write_bytes(engine.encode(np.zeros((512,512),dtype=np.uint8),2,'블러_축소64_4비트'))
            engine.save_json(path.with_suffix('.json'),{'sha256':engine.digest(path),'source_sha256':'fixed-source','encode_seconds':0.})
            engine.save_json(folder/'data.json',{'run_id':'reuse-run'})
            rows={'test':[{'id':'first','unblurred_sha256':'fixed-source'}]}
            self.assertEqual(engine.required_packet_bytes(rows,runtime,selected,'reuse-run'),0)
            rows['test'].append({'id':'missing','unblurred_sha256':'fixed-source'})
            self.assertEqual(engine.required_packet_bytes(rows,runtime,selected,'reuse-run'),2057)
            path.write_bytes(b'corrupt')
            with self.assertRaises(ValueError):
                engine.required_packet_bytes(rows,runtime,selected,'reuse-run')

if __name__=='__main__':
    unittest.main()
