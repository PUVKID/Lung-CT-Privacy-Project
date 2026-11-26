"""동일 소스의 실제 CPU·화면 검사 근거를 재사용하며 변경·누락은 거부합니다."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(name):
    return json.loads((ROOT / 'evidence' / name).read_text(encoding='utf-8'))


def source(name, expected):
    path = (ROOT / name).resolve(strict=True)
    if not path.is_relative_to(ROOT) or sha(path) != expected.lower():
        raise ValueError('검사 이후 소스 변경 또는 경로 오류: ' + name)


def log(name, expected):
    path = Path(name)
    if not path.is_absolute():
        path = ROOT / path
    path = path.resolve(strict=True)
    if not path.is_relative_to(ROOT / 'evidence') or sha(path) != expected.lower():
        raise ValueError('검사 원출력 무결성 오류: ' + name)


def main():
    engine = read('SCI_엔진_CPU_최종검사.json')
    if engine['exit_code'] != 0 or engine['test_count'] != 9 or not engine['unchanged']:
        raise ValueError('SCI 엔진 검사 미완료')
    if engine['sources_before'] != engine['sources_after']:
        raise ValueError('엔진 검사 도중 소스 변경')
    for name, expected in engine['sources_after'].items():
        source(name, expected)
    log(engine['log_path'], engine['log_sha256'])

    data = read('SCI데이터_소스동결.json')
    if data['tests']['exit_code'] != 0 or data['tests']['test_methods'] != 10:
        raise ValueError('SCI 데이터 검사 미완료')
    for item in data['sources']:
        source(item['path'], item['sha256'])
    log(data['tests']['log'], data['tests']['log_sha256'])

    ui = read('SCI_화면_표시수정후_최종검사.json')
    if not ui['unchanged'] or ui['sources_before'] != ui['sources_after'] or len(ui['checks']) != 2:
        raise ValueError('현재 SCI 화면 검사 근거 부족')
    for name, expected in ui['sources_after'].items():
        source(name, expected)
    for check in ui['checks']:
        if check['exit_code'] != 0:
            raise ValueError('SCI 화면 검사 실패')
        log(check['log'], check['log_sha256'])
    rust = read('SCI_Rust_최종검사.json')
    source('rust/src/main.rs', rust['source_sha256'])
    source('rust/전송엔진.exe', rust['engine_sha256'])
    print('SCI 데이터10·엔진9·화면2 검사 소스/원출력 SHA 연결 확인. GPU·실자료 전체 준비·브라우저 검증은 별도입니다.')


if __name__ == '__main__':
    main()
