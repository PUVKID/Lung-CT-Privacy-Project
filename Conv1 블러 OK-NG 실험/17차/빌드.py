"""설치된 E Rust 도구와 Windows MSVC로 실제 전송 엔진을 빌드합니다."""
import os
import json
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = Path('E:/2026/개발 도구 및 캐시/Rust Astryx')

def main():
    toolchain = TOOLS/'rustup/toolchains/stable-x86_64-pc-windows-msvc'
    compiler = toolchain/'bin/rustc.exe'
    vc = Path('C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC')
    versions = sorted(p for p in vc.glob('*/lib/x64') if (p/'msvcrt.lib').is_file())
    if not versions or not compiler.is_file():
        raise RuntimeError('기존Rust/MSVC환경을찾을수없습니다. 임의설치나정책변경은하지않습니다.')
    # 설치된 정식 MSVC 링커를 사용하여 generic rust-lld 실행 모드 추론을 피합니다.
    linker = versions[-1].parents[1]/'bin/Hostx64/x64/link.exe'
    if not linker.is_file():
        raise RuntimeError('설치된 MSVC link.exe가 없습니다.')
    sdk = TOOLS/'windows-sdk/x64'
    libs = sorted({str(p.parent) for p in sdk.rglob('*.lib')})
    env = os.environ.copy()
    env['LIB'] = ';'.join([str(versions[-1]), *libs])
    # 원본 경로의 컴파일 대기 현상을 격리합니다. 동일 바이트 사본의 메타데이터 검사는 통과했습니다.
    # 원인을 보안 프로그램 등으로 단정하지 않으며 원본과 입력의 SHA 일치를 먼저 확인합니다.
    source = ROOT/'rust/src/main.rs'
    build_input = ROOT/'evidence'/'Rust_빌드입력'/'ct_transport.rs'
    build_input.parent.mkdir(parents=True,exist_ok=True)
    build_input.write_bytes(source.read_bytes())
    if hashlib.sha256(source.read_bytes()).digest()!=hashlib.sha256(build_input.read_bytes()).digest():
        raise RuntimeError('Rust 빌드 입력 사본 불일치')
    args = [str(compiler), '--edition=2024', '--crate-name', 'ct_transport_v2', '-O', '-C', f'linker={linker}', '-C', 'linker-flavor=msvc',
            str(build_input), '-o', str(ROOT/'rust/전송엔진.exe')]
    try:
        result = subprocess.run(args, env=env, cwd=ROOT, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired as error:
        report={'argv':args,'exit_code':None,'error':'빌드 제한시간 120초 초과',
                'stdout':(error.stdout or b'').decode('utf-8',errors='replace'),
                'stderr':(error.stderr or b'').decode('utf-8',errors='replace')}
        (ROOT/'evidence'/'Rust_빌드_시간초과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        raise
    report = {'argv':args,'exit_code':result.returncode,
              'stdout':result.stdout.decode('utf-8',errors='replace'),
              'stderr':result.stderr.decode('utf-8',errors='replace')}
    if result.returncode == 0:
        report['engine_sha256'] = hashlib.sha256((ROOT/'rust/전송엔진.exe').read_bytes()).hexdigest()
        report['source_sha256'] = hashlib.sha256((ROOT/'rust/src/main.rs').read_bytes()).hexdigest()
    (ROOT/'docs/Rust_빌드결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    if result.returncode:
        raise RuntimeError(report['stderr'])
    print('전송엔진빌드완료',report['engine_sha256'])

if __name__ == '__main__':
    main()
