"""최종 예측 추적 및 best/patience 분리의 작은 CPU 합성 검사입니다."""
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
from tests.보조.이전설정 import legacy_config,legacy_manifest_config

class FinalPredictionTest(unittest.TestCase):
    def test_prediction_files_and_small_best_improvement(self):
        import torch
        import legacy.model
        from 지표 import binary_report
        torch.set_num_threads(2)
        class Tiny(torch.nn.Module):
            def __init__(self,**kwargs):
                super().__init__()
                self.front=torch.nn.Module()
                self.front.conv1=torch.nn.Conv2d(3,3,1)
                self.head=torch.nn.Linear(3,1)
            def forward_from_blurred(self,x):
                return self.head(self.front.conv1(x).mean((-2,-1))).squeeze(1)
        config=legacy_config()
        config.update(epochs=2,min_epochs=1,patience=2,samples_per_class=1,reserve_gib=0)
        with tempfile.TemporaryDirectory() as temporary:
            runtime=Path(temporary)
            folder=runtime/'conditions'/'final_fixture'
            folder.mkdir(parents=True)
            rows={}
            for split in ('train','validation','test','test_generated'):
                rows[split]=[]
                for label in (0,1):
                    path=runtime/f'{split}_{label}.ctb'
                    path.write_bytes(engine.encode(np.full((512,512),40+label*170,dtype=np.uint8),2,'블러_축소64_4비트'))
                    rows[split].append({'id':f'{split}_{label}','label':label,'source_id':f'source_{label}',
                        'source_group':f'group_{label}','packet_path':str(path),'packet_sha256':engine.digest(path)})
            original_evaluate=engine.evaluate
            losses=iter([.10000,.09995])
            def controlled_validation(model,records,device,precision,**kwargs):
                report=original_evaluate(model,records,device,precision,**kwargs)
                if not kwargs.get('group_ci',False):
                    report['loss']=next(losses)
                return report
            with patch.object(legacy.model,'SplitResNet50',Tiny),patch.object(engine,'evaluate',side_effect=controlled_validation):
                result=engine.classify(config,folder,{'sigma':2,'splits':rows},'cpu',False,'final-fixture-run')
            self.assertEqual(result['best_epoch'],2)
            self.assertEqual(result['best_validation_loss'],.09995)
            self.assertEqual(torch.load(folder/'best.pth',map_location='cpu',weights_only=False)['epoch'],2)
            last=torch.load(folder/'last.pth',map_location='cpu',weights_only=False)
            self.assertEqual(last['patience_best'],.10000)
            self.assertEqual(last['bad'],1)
            self.assertEqual(engine.read_json(folder/'current.json')['run_id'],'final-fixture-run')
            self.assertTrue(all(row['run_id']=='final-fixture-run' for row in engine.read_json(folder/'history.json')))
            paths=[]
            for split in ('test','test_generated'):
                reference=result[split]['predictions']
                path=runtime/reference['path']
                paths.append(path)
                self.assertEqual(reference['sha256'],engine.digest(path))
                data=engine.read_json(path)
                self.assertEqual(data['split'],split)
                self.assertEqual(data['run_id'],'final-fixture-run')
                self.assertEqual(data['checkpoint_sha256'],engine.digest(folder/'best.pth'))
                self.assertEqual(reference['rows'],2)
                saved=data['rows']
                recomputed=binary_report([r['label'] for r in saved],[r['rawlogit'] for r in saved])
                for key,value in recomputed.items():
                    if key!='interval_note':
                        self.assertEqual(result[split][key],value)
                self.assertIn('유사원본그룹단위재표집구간',result[split]['interval_note'])
                self.assertIn('환자단위구간아님',result[split]['interval_note'])
                for row in saved:
                    self.assertEqual(row['predicted'],int(row['rawlogit']>=0))
                    self.assertTrue(row['row_id'].startswith(split+'_'))
                    self.assertGreaterEqual(row['probability'],0)
                    self.assertLessEqual(row['probability'],1)
            self.assertNotEqual(paths[0],paths[1])

if __name__=='__main__':
    unittest.main()
