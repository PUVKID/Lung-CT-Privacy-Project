"""연결 원본 식별·다른 run 캐시 거부·공격 진행 CPU 합성 검사."""
import sys,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import SCI공격 as a
import SCI실행 as runner
class Tiny(torch.nn.Module):
 def __init__(self): super().__init__();self.p=torch.nn.Parameter(torch.tensor(1.))
 def observed(self,x): return x
 def features_from_observed(self,x,layer): return x
class Tests(unittest.TestCase):
 def test_duplicate_sources_share_gallery_identity(self):
  rows=[{'id':f'copy{i}','source_id':'a','patient_id':'p','materialized':True,'preblurred':True,'canonical':i==0} for i in range(4)]
  with patch('SCI실행.image',return_value=np.ones((4,4),dtype=np.float32)),patch('SCI고정표본.read_raw',return_value=np.ones((4,4),dtype=np.float32)):
   result=a.linking(Tiny(),rows,'conv1',[1,5])
  self.assertEqual(result['topk_source']['1']['correct'],4)
  self.assertEqual(result['gallery_size'],1)
  self.assertEqual(result['count'],4)
 def test_cache_rejects_other_or_missing_run(self):
  with tempfile.TemporaryDirectory() as tmp:
   for value in [{'run_id':'other'},{}]:
    p=Path(tmp);(p/'result.json').write_text(json.dumps(value),encoding='utf-8')
    with self.assertRaisesRegex(ValueError,'run_id'):
     a.attack_exposure(None,{}, {},p,'current')
   (p/'result.json').write_text(json.dumps({'run_id':'current','value':3}),encoding='utf-8')
   self.assertEqual(a.attack_exposure(None,{}, {},p,'current')['value'],3)
 def test_progress_preserves_classifier_epoch_and_rejects_stale(self):
  with tempfile.TemporaryDirectory() as tmp:
   config={'runtime':tmp,'sigmas':[],'roi_pixel_spacing_mm':.1,'data_status':'fixture'}
   condition=runner.experiment_plan(config)[0];p=Path(tmp)/'conditions'/condition['id'];p.mkdir(parents=True)
   (p/'current.json').write_text(json.dumps({'run_id':'r','epoch':41,'state':'classifying'}),encoding='utf-8')
   report=runner.attack_progress_reporter(config,'r',condition,min_interval=0)
   report({'phase':'reconstruction','layer':'conv1','dtype':'f16','processed':7,'total':20})
   current=json.loads((p/'current.json').read_text(encoding='utf-8'))
   status=json.loads((Path(tmp)/'status.json').read_text(encoding='utf-8'))
   self.assertEqual(current['epoch'],41);self.assertEqual(current['state'],'protecting')
   self.assertEqual(status['attack_progress']['processed'],7)
   self.assertEqual(status['attack_progress']['total'],20)
   self.assertNotIn('patient_id',status['attack_progress'])
   (p/'current.json').write_text(json.dumps({'run_id':'other','epoch':1}),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'run_id'): report({'phase':'done'})
 def test_linking_progress_is_actual_count(self):
  rows=[{'id':'a','patient_id':'p'}];events=[]
  with patch('SCI실행.image',return_value=np.ones((4,4),dtype=np.float32)):
   a.linking(Tiny(),rows,'conv1',[1],progress=events.append)
  self.assertEqual(events[-1]['processed'],1);self.assertEqual(events[-1]['total'],1)
if __name__=='__main__':unittest.main()
