"""실행 문맥 불변성과 CUDA를 초기화하지 않는 버전 조회 검사입니다."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import 실행 as engine

class ContextTests(unittest.TestCase):
    def test_binding_reuses_identical_context_and_refuses_changes(self):
        version=['fixed-package-version']
        def context(device):
            return {'device':device,'precision':'cuda_bf16' if device=='cuda' else 'cpu_fp32','package_version':version[0]}
        with tempfile.TemporaryDirectory() as temporary,patch.object(engine,'fixed_test_plan',return_value={'rows':[]}),\
             patch.object(engine,'source_binding',return_value={'source':'fixed-sha'}),patch.object(engine,'runtime_context',side_effect=context):
            runtime=Path(temporary)
            first=engine.bind({},runtime,'cpu')
            original=engine.digest(runtime/'run.json')
            self.assertEqual(engine.bind({},runtime,'cpu'),first)
            with self.assertRaises(ValueError):
                engine.bind({},runtime,'cuda')
            version[0]='changed-package-version'
            with self.assertRaises(ValueError):
                engine.bind({},runtime,'cpu')
            self.assertEqual(engine.digest(runtime/'run.json'),original)
    def test_real_context_keeps_cuda_uninitialized(self):
        import torch
        self.assertFalse(torch.cuda.is_initialized())
        context=engine.runtime_context('cpu')
        self.assertFalse(torch.cuda.is_initialized())
        self.assertEqual(context['precision'],'cpu_fp32')
        self.assertIsNone(context['cudnn_runtime_version'])
        self.assertGreater(len(context['cudnn_installed_files']),0)
        with patch.dict(engine.os.environ,{},clear=False):
            engine.os.environ.pop('CUDA_VISIBLE_DEVICES',None)
            absent=engine.runtime_context('cpu')['environment']['CUDA_VISIBLE_DEVICES']
            engine.os.environ['CUDA_VISIBLE_DEVICES']=''
            empty=engine.runtime_context('cpu')['environment']['CUDA_VISIBLE_DEVICES']
        self.assertEqual(absent,{'present':False,'value':None})
        self.assertEqual(empty,{'present':True,'value':''})

if __name__=='__main__':
    unittest.main()
