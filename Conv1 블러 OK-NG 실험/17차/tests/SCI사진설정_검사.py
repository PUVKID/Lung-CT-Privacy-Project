"""실제 결과 생성 경로의 모델 SHA와 위협모형 메타데이터 CPU 합성 검사."""
import sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import SCI공격 as attack
class Model(torch.nn.Module):
 def __init__(self):
  super().__init__();self.p=torch.nn.Parameter(torch.tensor(1.));self.name='fixture';self.blur=type('Blur',(),{'sigma':2})()
 def observed(self,x):return x
 def features_from_observed(self,x,layer):return x
class Tests(unittest.TestCase):
 def test_generated_settings_link_selected_checkpoint_and_threat(self):
  rows=[{'id':str(y),'patient_id':str(y),'cohort':'LUNA25','label':y,'metadata':{}} for y in (0,1)]
  def exposure(*args,**kwargs):return {'selected_family':'chosen','examples':[{'label':g,'reconstructed':'fake.png'} for g in ['OK','NG']]}
  with tempfile.TemporaryDirectory() as tmp,patch.object(attack,'attack_exposure',side_effect=exposure),patch.object(attack,'linking',return_value={}),patch.object(attack,'membership',return_value={}),patch('SCI실행.image',return_value=np.ones((4,4),dtype=np.float32)):
   result=attack.run_protection(Model(),{'validation':rows,'test':rows}, {'feature_layers':['conv1'],'feature_dtypes':['f32'],'connection_topk':[1]},Path(tmp)/'conditions'/'c','r',{'sha256':'a'*64},'cpu',False)
  for item in result['examples']:
   settings=item['settings']['feature_reconstruction']
   self.assertEqual(settings['checkpoint_sha256'],'a'*64)
   self.assertEqual(settings['selected_attack'],'chosen')
   self.assertIn('서버 내부 특징 노출 가정',settings['threat_model'])
if __name__=='__main__':unittest.main()
