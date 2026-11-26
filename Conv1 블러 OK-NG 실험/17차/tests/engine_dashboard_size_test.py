"""실제 평가 행수 규모의 전체 결과 보존과 작은 화면 자료 투영 검사입니다."""
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import 실행 as engine

class DashboardSizeTest(unittest.TestCase):
    def test_full_metrics_and_compact_projection(self):
        record={'mse':.123456789012345,'ssim':.234567890123456,'psnr':9.87654321012345,'psnr_infinite':False}
        report={**record,'count':164,'mean_baseline_mse':.23456789012345,'privacy_error_ratio_raw':.52631578,
            'privacy_error_ratio_clipped':.52631578,'privacy_error_score':52.631578,'privacy_error_clipping_applied':False,
            'privacy_structure_ratio_raw':.7654321,'privacy_structure_ratio_clipped':.7654321,
            'privacy_structure_score':76.54321,'privacy_structure_clipping_applied':False,'undefined_reason':None,'psnr_infinite_count':0}
        def attack(candidates):
            result={'selected_family':'candidate_0','test':dict(report),'test_per_source_metrics':[record]*164,'candidate_metrics':{}}
            for index in range(candidates):
                candidate={}
                for split,count in [('validation',164),('test',164),('test_generated',2000)]:
                    candidate[split]={**report,'count':count}
                    candidate[split+'_by_class']={label:{**report,'count':count//2} for label in ('OK','NG')}
                    candidate[split+'_per_source']=[record]*count
                result['candidate_metrics'][f'candidate_{index}']=candidate
            return result
        result={'run_id':'size-fixture','classifier':{'test':{'predictions':{'path':'predictions/test.json','sha256':'fixed','rows':164}}},
                'attack':attack(9),'feature_attack':attack(27),'examples':[{'label':'OK','original':'examples/OK.png'}]}
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary)/'conditions'/'size_fixture'
            engine.save_json(folder/'result.json',result)
            original_hash=engine.digest(folder/'result.json')
            engine.save_dashboard(folder,result)
            compact=engine.read_json(folder/'dashboard.json')
            self.assertGreater((folder/'result.json').stat().st_size,4*1024**2)
            self.assertLess((folder/'dashboard.json').stat().st_size,1024**2)
            self.assertEqual(engine.digest(folder/'result.json'),original_hash)
            self.assertEqual(compact['full_result']['sha256'],original_hash)
            self.assertEqual(compact['attack']['test'],result['attack']['test'])
            self.assertEqual(compact['feature_attack']['candidate_metrics']['candidate_26']['test_generated_by_class'],
                             result['feature_attack']['candidate_metrics']['candidate_26']['test_generated_by_class'])
            self.assertEqual(compact['examples'],result['examples'])
            self.assertNotIn('test_per_source_metrics',compact['attack'])
            self.assertNotIn('test_generated_per_source',compact['feature_attack']['candidate_metrics']['candidate_26'])
            print('전체 결과 바이트', (folder/'result.json').stat().st_size,'화면 자료 바이트',(folder/'dashboard.json').stat().st_size)

if __name__=='__main__':
    unittest.main()
