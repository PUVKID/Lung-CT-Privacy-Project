"""작은 CPU 합성 공격·계보 검사. 실제 의료영상 성능 검사가 아닙니다."""
import copy,inspect,sys,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import SCI공격 as attack
from legacy.model import GaussianDCTBlur
torch.set_num_threads(2)

class Tiny(torch.nn.Module):
    def __init__(self,sigma):
        super().__init__();self.weight=torch.nn.Parameter(torch.tensor(1.),requires_grad=False)
        self.blur=GaussianDCTBlur(sigma);self.preblurred=True
    def observed(self,x): raise AssertionError('원본공격은 observed 우회 금지')
    def features_from_observed(self,x,layer): return x*self.weight

class 검사(unittest.TestCase):
    def test_raw_objective_and_frozen(self):
        model=Tiny(1.5);raw=torch.linspace(0,1,256).reshape(1,1,16,16)
        target=model.blur(raw);mean=np.full((16,16),.5,dtype=np.float32)
        before=model.weight.clone()
        result,audit=attack._raw_gradient_inverse(model,target,'conv1',mean,90,0.,'f32',['train_mean','flat_0.5'])
        reconstructed=torch.from_numpy(result)[None,None]
        self.assertLess(float((model.blur(reconstructed)-target).square().mean()),1e-4)
        self.assertEqual(audit['selected_objective'],min(r['objective'] for r in audit['candidates']))
        self.assertFalse(model.weight.requires_grad);self.assertIsNone(model.weight.grad)
        torch.testing.assert_close(before,model.weight)
        self.assertNotIn('raw_target',inspect.signature(attack._raw_gradient_inverse).parameters)

    def test_sigma_zero_deterministic_initializations(self):
        model=Tiny(0);mean=np.full((8,8),.2,dtype=np.float32);target=torch.full((1,1,8,8),.5)
        a,first=attack._raw_gradient_inverse(model,target,'conv1',mean,0,0.,'f32',['train_mean','flat_0.5'])
        np.random.seed(937);torch.manual_seed(14)
        b,second=attack._raw_gradient_inverse(model,target,'conv1',mean,0,0.,'f32',['train_mean','flat_0.5'])
        np.testing.assert_array_equal(a,b);np.testing.assert_array_equal(a,np.full((8,8),.5))
        self.assertEqual(first,second);self.assertEqual(first['selected_initialization'],'flat_0.5')

    def test_dtype_forward_and_gradient(self):
        for dtype in ('f32','f16','i8'):
            value=torch.tensor([-.37,.123,.98],requires_grad=True)
            actual=attack._feature_forward_ste(value,dtype)
            torch.testing.assert_close(actual,attack.FeatureCodec(dtype).transfer(value,False))
            actual.sum().backward();torch.testing.assert_close(value.grad,torch.ones_like(value))

    def test_source_shuffle_preserves_source_distribution(self):
        rows=[{'id':str(i),'source_id':s,'label':y} for i,(s,y) in enumerate([('a',0),('a',0),('b',0),('c',1),('c',1),('c',1)])]
        original=copy.deepcopy(rows)
        result,audit=attack._shuffle_source_labels(rows,42)
        self.assertEqual(rows,original);self.assertEqual(audit['source_counts_before'],audit['source_counts_after'])
        for source in ('a','b','c'): self.assertEqual(len({r['label'] for r in result if r['source_id']==source}),1)
        again,_=attack._shuffle_source_labels(list(reversed(rows)),42)
        self.assertEqual({r['id']:r['label'] for r in result},{r['id']:r['label'] for r in again})
        self.assertEqual(sum(audit['row_counts_after'].values()),6)

    def test_conflicting_source_fails(self):
        with self.assertRaisesRegex(ValueError,'불일치'):
            attack._shuffle_source_labels([{'source_id':'a','label':0},{'source_id':'a','label':1}],42)

    def test_integration_contract(self):
        source=inspect.getsource(attack.attack_exposure)
        self.assertIn('_raw_gradient_inverse(',source);self.assertIn("if split=='validation':",source)
        diagnostics=inspect.getsource(attack.run_diagnostics)
        self.assertIn('_shuffle_source_labels(',diagnostics);self.assertIn('label_shuffle_mapping.json',diagnostics)
        self.assertFalse(torch.cuda.is_initialized())

if __name__=='__main__': unittest.main(verbosity=2)
