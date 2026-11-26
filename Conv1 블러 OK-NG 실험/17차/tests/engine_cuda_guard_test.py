"""CUDA 초기화 없이 실제 프로세스 판별 분기만 검사합니다."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import psutil
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import 실행 as engine

class FakeProcess:
    def __init__(self,exe,created=7.):
        self.path,self.created=exe,created
    def create_time(self):
        return self.created
    def exe(self):
        return self.path
    def cmdline(self):
        return [self.path,'--fixture']

class Query:
    def __init__(self,text):
        self.stdout=text

class CudaGuardTests(unittest.TestCase):
    def test_known_windows_gui_is_allowed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            exe=r'C:\Windows\explorer.exe'
            with patch.object(engine.subprocess,'run',return_value=Query('101, '+exe+'\n')),patch.object(psutil,'Process',return_value=FakeProcess(exe)):
                report=engine.cuda_guard(root/'audit.json',root/'missing_status.json')
            self.assertEqual(report['decision'],'allowed')
            self.assertEqual(report['processes'][0]['decision'],'allowed_gui')
            self.assertEqual(engine.read_json(root/'audit.json')['decision'],'allowed')
            self.assertIsNone(engine.gui_process_reason(r'C:\Unknown\explorer.exe'))
    def test_live_stage12_owner_is_always_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            engine.save_json(root/'status.json',{'pid':8920,'process_created':7.})
            with patch.object(psutil,'Process',return_value=FakeProcess(r'C:\Windows\explorer.exe')),patch.object(engine.subprocess,'run') as query:
                with self.assertRaisesRegex(RuntimeError,'기존12차'):
                    engine.cuda_guard(root/'audit.json',root/'status.json')
                query.assert_not_called()
            self.assertEqual(engine.read_json(root/'audit.json')['decision'],'blocked')
    def test_python_and_unknown_compute_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            for exe in (r'C:\Tools\python.exe',r'C:\Tools\custom_compute.exe'):
                with self.subTest(exe=exe),patch.object(engine.subprocess,'run',return_value=Query('101, '+exe)),patch.object(psutil,'Process',return_value=FakeProcess(exe)):
                    with self.assertRaises(RuntimeError):
                        engine.cuda_guard(status_path=Path(temporary)/'none.json')
    def test_exited_query_and_reused_pid_are_distinguished(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            exe=r'C:\Windows\explorer.exe'
            with patch.object(engine.subprocess,'run',return_value=Query('101, '+exe)),patch.object(psutil,'Process',side_effect=psutil.NoSuchProcess(101)):
                report=engine.cuda_guard(status_path=root/'none.json')
                self.assertIn('조회 중 종료',report['processes'][0]['decision'])
            with patch.object(engine.subprocess,'run',return_value=Query('101, '+exe)),patch.object(psutil,'Process',side_effect=[FakeProcess(exe,7.),FakeProcess(exe,8.)]):
                with self.assertRaisesRegex(RuntimeError,'재사용'):
                    engine.cuda_guard(status_path=root/'none.json')
    def test_access_denied_and_path_mismatch_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            with patch.object(engine.subprocess,'run',return_value=Query('101, C:\\Windows\\explorer.exe')),patch.object(psutil,'Process',side_effect=psutil.AccessDenied(101)):
                with self.assertRaises(RuntimeError):
                    engine.cuda_guard(status_path=root/'none.json')
            with patch.object(engine.subprocess,'run',return_value=Query('101, C:\\Windows\\explorer.exe')),patch.object(psutil,'Process',return_value=FakeProcess(r'C:\Tools\unknown.exe')):
                with self.assertRaises(RuntimeError):
                    engine.cuda_guard(status_path=root/'none.json')

if __name__=='__main__':
    unittest.main()
