"""최적 모델 포인터 저장 사이 중단을 실제 CPU 학습 경로에서 재현합니다."""
import copy,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import torch
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import SCI실행 as engine
import SCI공격 as attacks
from 실행 import read_json,save_json,save_torch,digest
ROOT=Path(__file__).resolve().parents[1]
torch.set_num_threads(2)
class Tiny(torch.nn.Module):
 def __init__(self,*args,**kwargs):
  super().__init__();self.conv=torch.nn.Conv2d(1,1,1);self.fc=torch.nn.Linear(1,1)
 def forward(self,x):return self.fc(self.conv(x).mean((2,3))).squeeze(1)
 def observed(self,x):return x
 def features_from_observed(self,x,layer):return torch.nn.functional.avg_pool2d(x,4).repeat(1,3,1,1)
def fixture(root):
 c=read_json(ROOT/'SCIconfig.json');c.update(runtime=str(root),fixed_samples_root=str(root/'fixed'),image_size=32,samples_per_class=1,validation_samples_per_class=1,test_samples_per_class=1,batch_size=2,accumulation=1,reserve_gib=0,epochs=1,min_epochs=1)
 c['reconstruction']={**c['reconstruction'],'epochs':1,'min_epochs':1}
 rows={}
 for split in ('train','validation','test'):
  rows[split]=[]
  for label in (0,1):
   p=root/f'{split}_{label}.png';Image.fromarray(np.full((32,32),40+label*160,dtype=np.uint8)).save(p)
   rows[split].append(dict(id=split+str(label),patient_id=split+str(label),cohort='LUNA25',label=label,image_path=str(p),image_sha256=digest(p),metadata={}))
 return c,rows
class 검사(unittest.TestCase):
 def classifier_interruption(self,epochs,remaining=False):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);c,rows=fixture(root);c.update(epochs=epochs+int(remaining),min_epochs=epochs+int(remaining));condition=engine.experiment_plan(c)[20];folder=root/'conditions'/condition['id'];original=engine.save_json
   def stop(path,value):
    original(path,value)
    if Path(path).name=='last.json' and value['epoch']==epochs:raise RuntimeError('last 저장 직후 중단')
   real_evaluate=engine.evaluate;losses=iter([.8,.6])
   def evaluate(model,rs,*args,**kwargs):
    result=real_evaluate(model,rs,*args,**kwargs)
    if len(args)<3 and kwargs.get('path') is None:result['loss']=next(losses)
    return result
   protection={'attack':{'privacy_score':None},'examples':[]}
   with patch('SCI모델.SCIResNet',Tiny),patch('SCI공격.run_protection',return_value=protection),patch('SCI공격.run_diagnostics',return_value={'fixture':True}):
    with patch.object(engine,'save_json',side_effect=stop),patch.object(engine,'evaluate',side_effect=evaluate):
     with self.assertRaisesRegex(RuntimeError,'직후 중단'):engine.train_condition(c,{'splits':rows,'external':{}},condition,'fixture','cpu')
    committed=read_json(folder/'last.json');self.assertEqual(committed['epoch'],epochs)
    if epochs==1:self.assertFalse((folder/'best.json').exists())
    else:self.assertEqual(read_json(folder/'best.json')['epoch'],epochs-1)
    with patch.object(engine,'evaluate',side_effect=lambda model,rs,*args,**kwargs: {**real_evaluate(model,rs,*args,**kwargs),**({'loss':.9} if len(args)<3 and kwargs.get('path') is None else {})}):
     engine.train_condition(c,{'splits':rows,'external':{}},condition,'fixture','cpu',True)
   result=read_json(folder/'result.json');self.assertEqual(result['classifier']['checkpoint']['sha256'],committed['sha256']);self.assertEqual(result['classifier']['checkpoint']['epoch'],epochs)
 def test_classifier_first_best_missing(self):self.classifier_interruption(1)
 def test_classifier_best_marker_stale(self):self.classifier_interruption(2)
 def test_classifier_repairs_before_next_nonimproving_epoch(self):self.classifier_interruption(2,True)
 def test_decoder_first_best_missing(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);c,rows=fixture(root);folder=root/'decoder';original=attacks.save_json
   def stop(path,value):
    original(path,value)
    if Path(path).name=='last.json':raise RuntimeError('last 저장 직후 중단')
   def image(row):
    with Image.open(row['image_path']) as im:return np.asarray(im,dtype=np.float32)/255
   with patch.object(engine,'image',side_effect=image):
    with patch.object(attacks,'save_json',side_effect=stop):
     with self.assertRaisesRegex(RuntimeError,'직후 중단'):attacks._fit(Tiny(),rows,'stem',attacks.FeatureCodec('f32'),c,folder,'fixture',False)
    self.assertFalse((folder/'best.json').exists());committed=read_json(folder/'last.json')
    actual=attacks._fit(Tiny(),rows,'stem',attacks.FeatureCodec('f32'),c,folder,'fixture',True)
   self.assertEqual(read_json(folder/'best.json'),committed)
   saved=torch.load(folder/committed['path'],map_location='cpu',weights_only=False)['model']
   for key,value in actual.state_dict().items():torch.testing.assert_close(value,saved[key])
 def test_decoder_stale_best(self):
  class Decoder(torch.nn.Module):
   def __init__(self,*args):super().__init__();self.bias=torch.nn.Parameter(torch.tensor(-2.))
   def forward(self,x):return torch.sigmoid(self.bias).expand(x.shape[0],1,32,32)
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);c,rows=fixture(root);c['reconstruction'].update(epochs=2,min_epochs=2);folder=root/'decoder';original=attacks.save_json
   def stop(path,value):
    original(path,value)
    if Path(path).name=='last.json' and value['epoch']==2:raise RuntimeError('중단')
   def image(row):
    with Image.open(row['image_path']) as im:return np.asarray(im,dtype=np.float32)/255
   with patch.object(engine,'image',side_effect=image),patch.object(attacks,'FeatureDecoder',Decoder):
    with patch.object(attacks,'save_json',side_effect=stop):
     with self.assertRaisesRegex(RuntimeError,'중단'):attacks._fit(Tiny(),rows,'stem',attacks.FeatureCodec('f32'),c,folder,'fixture',False)
    self.assertEqual(read_json(folder/'best.json')['epoch'],1)
    attacks._fit(Tiny(),rows,'stem',attacks.FeatureCodec('f32'),c,folder,'fixture',True)
   self.assertEqual(read_json(folder/'best.json')['epoch'],2)
   self.assertEqual(read_json(folder/'best.json'),read_json(folder/'last.json'))
 def test_prior_best_is_preserved_and_mismatch_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp);history=[{'epoch':1,'run_id':'fixture','validation_mse':.2},{'epoch':2,'run_id':'fixture','validation_mse':.3}]
   old={'epoch':1,'run_id':'fixture','best':.2,'history':history[:1]};state={'epoch':2,'run_id':'fixture','best':.2,'history':history}
   refs=[]
   for record in (old,state):
    path=folder/f"epoch_{record['epoch']}.pth";save_torch(path,record);refs.append(dict(path=path.name,sha256=digest(path),epoch=record['epoch']))
   save_json(folder/'best.json',refs[0]);before=digest(folder/'best.json')
   self.assertEqual(engine.reconcile_best_reference(folder,refs[1],state,'validation_mse'),refs[0]);self.assertEqual(digest(folder/'best.json'),before)
   save_json(folder/'best.json',refs[1])
   with self.assertRaisesRegex(ValueError,'epoch'):engine.reconcile_best_reference(folder,refs[1],state,'validation_mse')
   bad={**refs[0],'sha256':'0'*64};save_json(folder/'best.json',bad)
   with self.assertRaisesRegex(ValueError,'SHA'):engine.reconcile_best_reference(folder,refs[1],state,'validation_mse')
   wrong={**old,'run_id':'other'};save_torch(folder/refs[0]['path'],wrong);save_json(folder/'best.json',{**refs[0],'sha256':digest(folder/refs[0]['path'])})
   with self.assertRaisesRegex(ValueError,'계보'):engine.reconcile_best_reference(folder,refs[1],state,'validation_mse')
   invalid=copy.deepcopy(state);invalid['best']=.1
   with self.assertRaisesRegex(ValueError,'손실'):engine.reconcile_best_reference(folder,refs[1],invalid,'validation_mse')
if __name__=='__main__':unittest.main(verbosity=2)
