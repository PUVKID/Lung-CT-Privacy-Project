"""완료한 실험만 CPU에서 읽어 참고 자료와 같은 폴더·패널 구성으로 저장합니다."""
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import traceback

PROJECT = Path(__file__).resolve().parents[2]
HERE = PROJECT / '블러 강도별 대표 특징맵' / '7차'
TRAIN = PROJECT / '7차'
REFERENCE = PROJECT.parent / '블러 엣지' / '블러 피쳐맵 저장 파일'
RUN = None
SIGMAS = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
CLASSES = [('Bengin_cases', 'Bengin cases', '양성 · OK'),
           ('Malignant_cases', 'Malignant cases', '악성 · NG'),
           ('Normal_cases', 'Normal cases', '정상 · OK')]
LAYERS = ['입력 회색조 CT', 'conv1 → GaussianDCTBlur 직후',
          'cloud.layer1 출력', 'cloud.layer2 출력', 'cloud.layer3 출력', 'cloud.layer4 출력']
MEANINGS = ['실제 입력 CT를 512×512 회색조로 맞춘 영상입니다. 3채널에 같은 값을 복제해 모델에 입력합니다.',
            '첫 합성곱이 추출한 윤곽·질감 반응에 블러를 적용한 전송 특징입니다. 아직 BN·ReLU·최대 풀링을 거치지 않았습니다.',
            '전송 특징이 BN·ReLU·최대 풀링과 첫 잔차 블록 묶음을 통과한 결과입니다.',
            '두 번째 잔차 블록 묶음이 공간 크기를 줄이며 조합한 특징입니다.',
            '세 번째 잔차 블록 묶음이 더 넓은 영역의 반응을 조합한 특징입니다.',
            '마지막 잔차 블록 묶음의 출력입니다. 이후 전역 평균 풀링과 분류기로 OK·NG를 계산합니다.']

def now():
    return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec='seconds')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read_json(path):
    # 확인한 Windows 공유·접근 잠금만 합계 0.63초 이내로 재시도합니다.
    # 잘못된 JSON·공간 부족·지속 오류는 감추지 않고 감시를 종료합니다.
    delays = (0.01, 0.02, 0.04, 0.08, 0.16, 0.32)
    for attempt in range(len(delays) + 1):
        try:
            return json.loads(Path(path).read_text(encoding='utf-8'))
        except PermissionError as error:
            if getattr(error, 'winerror', None) not in {5, 32} or attempt == len(delays):
                raise
            time.sleep(delays[attempt])

def atomic_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    # 대시보드의 짧은 읽기 핸들과 충돌하면 제한된 횟수만 재시도합니다.
    for attempt in range(6):
        try:
            os.replace(temporary, path)
            return
        except PermissionError:
            if attempt == 5:
                raise
            time.sleep(0.1 * (attempt + 1))

def prepare():
    paths = sorted(p.relative_to(REFERENCE).as_posix() for p in REFERENCE.rglob('*.png'))
    if len(paths) != 180:
        raise ValueError('참고 자료의 PNG 180개 계약이 다릅니다.')
    template_path = HERE / '참고_폴더구성_비공개.json'
    template = {'reference': str(REFERENCE), 'relative_paths': paths}
    if template_path.exists():
        if read_json(template_path) != template:
            raise ValueError('동결한 참고 폴더 구성과 현재 구성이 다릅니다.')
    else:
        atomic_json(template_path, template)
    for relative in paths:
        (HERE / '블러 피쳐맵 저장 파일' / relative).parent.mkdir(parents=True, exist_ok=True)
    return paths

def render(array, stage, sigma, label, destination):
    channels = array.shape[0]
    shape = list(array.shape)
    caption = MEANINGS[stage]
    if stage:
        caption += ' 색은 특징의 상대적인 반응을 뜻하며 병변 위치나 프라이버시 보장을 뜻하지 않습니다.'
        indices = [i * channels // 8 for i in range(8)]
        panels = [array.mean(axis=0), array.max(axis=0)] + [array[i] for i in indices]
        titles = ['전체 채널 평균', '채널별 최댓값'] + [f'채널 {i} / {channels}' for i in indices]
        fig, axes = plt.subplots(2, 5, figsize=(20, 11), dpi=120)
        for i, (axis, panel, title) in enumerate(zip(axes.flat, panels, titles)):
            axis.imshow(panel, cmap='hot' if i == 1 else 'viridis', interpolation='nearest')
            axis.set_title(title, fontproperties=FONT, fontsize=13, pad=10)
            axis.axis('off')
        fig.subplots_adjust(left=.025, right=.975, top=.83, bottom=.17, wspace=.12, hspace=.20)
        caption += ' 각 패널은 자기 최솟값·최댓값으로 정규화하므로 서로 다른 패널의 색 크기를 직접 비교할 수 없습니다.'
        note = '전체 채널 평균 · 채널별 최댓값 · 균등 간격의 개별 채널 8개 (총 10패널)'
    else:
        caption += ' 회색조의 밝기는 입력 픽셀 밝기이며 악성 확률이 아닙니다.'
        indices = []
        panels = [array[0]]
        fig, axis = plt.subplots(figsize=(9, 10), dpi=120)
        axis.imshow(array[0], cmap='gray', vmin=0, vmax=1)
        axis.axis('off')
        fig.subplots_adjust(top=.83, bottom=.21, left=.08, right=.92)
        note = '원본 입력 1장 · 평가 전처리 · 증강 없음'
    fig.suptitle(f'{label}  |  블러 강도 {sigma}  |  단계 {stage}: {LAYERS[stage]}', fontproperties=FONT, fontsize=18, y=.965)
    fig.text(.5, .90, f'{note}\n텐서: {shape[0]}채널 × {shape[1]} × {shape[2]} · 완료한 최적 체크포인트 · FP32 평가',
             ha='center', va='center', fontproperties=FONT, fontsize=12, linespacing=1.6)
    import textwrap
    wrapped = '\n'.join(textwrap.wrap(caption, width=103 if stage else 57))
    fig.text(.035, .11 if stage else .14, wrapped, va='top', fontproperties=FONT, fontsize=12, linespacing=1.7)
    if stage == 1:
        fig.text(.035, .025, '추출 지점 안내: 참고 자료와 프레임워크·전송 경계가 달라 현재 모델의 실제 추출 지점을 표시했습니다.', fontproperties=FONT, fontsize=11)
    temporary = destination.with_suffix('.tmp')
    fig.savefig(temporary, format='png', facecolor='white')
    plt.close(fig)
    os.replace(temporary, destination)
    return caption, indices, [{'min': float(p.min()), 'max': float(p.max())} for p in panels]

def validate_inputs(root, run_id):
    from src.identity import validate_run, load_selection
    metadata = validate_run(root, run_id)
    manifest = read_json(Path(root) / 'work/results/dataset_manifest_private.json')
    return metadata['config'], manifest, load_selection(root, run_id)


def run_once(paths):
    from src.identity import validate_fixed_result
    from src.training import tensor_state_digest
    selection_path = TRAIN / f'work/results/run_{RUN}/fixed_model_selection.json'
    if not selection_path.exists():
        return False
    config, manifest, selection = validate_inputs(TRAIN, RUN)
    state = read_json(TRAIN / 'work/runtime/status.json')
    if state.get('run_id') != RUN or state.get('training_status') != 'completed':
        raise ValueError('학습100회 완료 상태와 현재 실행이 일치하지 않습니다.')
    samples = [sorted((r for r in manifest['splits']['train'] if r['source_class'] == source), key=lambda r: r['relative_path'])[0]
               for _, source, _ in CLASSES]
    index_path = HERE / 'export_index_private.json'
    bound = {'schema_version': 2, 'run_id': RUN, 'protocol': 'fixed-model-sigma0-v1', 'protocol_fixed_model': True,
             'training_sigma': 0, 'checkpoint_sha256': selection['checkpoint_sha256'], 'model_state_sha256': selection['model_state_sha256'],
             'checkpoint_epoch': selection['checkpoint_epoch'], 'selected_checkpoint': selection['selected_checkpoint'],
             'source_manifest_sha256': digest(TRAIN / 'work/results/dataset_manifest_private.json'),
             'manifest_records_sha256': manifest['manifest_sha256'], 'model_source_sha256': digest(TRAIN / 'src/model.py'),
             'data_source_sha256': digest(TRAIN / 'src/data.py'), 'generator_sha256': digest(Path(__file__)), 'samples_private': samples}
    index = read_json(index_path) if index_path.exists() else {
        **bound, 'items': [], 'completed_sigmas': [], 'pending_sigmas': SIGMAS,
        'sample_selection': '학습 분할에서 원본 클래스별 상대경로 정렬 첫 영상',
        'reference_panel_layout': '2행5열 채널 평균·최대·균등 간격8채널',
        'stage1_boundary_note': '모든 블러는 동일한 σ0 선정 모델의 conv1 직후에 적용합니다.'}
    if any(index.get(key) != value for key, value in bound.items()):
        raise ValueError('기존 그림의 단일 모델·소스·원본 연결이 현재 실행과 다릅니다.')
    for item in index['items']:
        if digest(HERE / item['relative_path']) != item['sha256'] or item.get('checkpoint_sha256') != selection['checkpoint_sha256']:
            raise ValueError('기존 그림 또는 단일 모델 연결이 변했습니다.')
    checkpoint = torch.load(TRAIN / selection['selected_checkpoint'], map_location='cpu', weights_only=True)
    model = SplitResNet50(sigma=0, pretrained=False).eval().requires_grad_(False)
    model.load_state_dict(checkpoint['model'], strict=True)
    if tensor_state_digest(model.state_dict()) != selection['model_state_sha256']:
        raise ValueError('그림 모델이 동결된 전체 state와 다릅니다.')
    for sigma in SIGMAS:
        if sigma in index['completed_sigmas']:
            continue
        metrics_path = TRAIN / f'work/results/run_{RUN}/sigma_{sigma}_metrics.json'
        eligible = any(q['sigma'] == sigma and q['status'] == 'completed' for q in state['sigma_queue'])
        if not eligible or not metrics_path.exists():
            continue
        validate_fixed_result(TRAIN, read_json(metrics_path), RUN)
        model.blur = GaussianDCTBlur(sigma)
        items = []
        for (key, source, label), row in zip(CLASSES, samples):
            if digest(row['path']) != row['byte_sha256']:
                raise ValueError('그림 입력 원영상이 저장된 SHA와 다릅니다.')
            x, _ = CTDataset([row], image_size=512, training=False)[0]
            stages = [x.numpy().copy()]
            with torch.inference_mode():
                y = model.blur(model.edge((x[None] - model.rgb_mean) / model.rgb_std))
                stages.append(y[0].numpy().copy())
                y = model.cloud.maxpool(model.cloud.relu(model.cloud.bn1(y)))
                for layer in [model.cloud.layer1, model.cloud.layer2, model.cloud.layer3, model.cloud.layer4]:
                    y = layer(y)
                    stages.append(y[0].numpy().copy())
            for stage, array in enumerate(stages):
                if not np.isfinite(array).all():
                    raise ValueError('그림 특징 텐서가 비유한 값입니다.')
                folder = '원본 파일 생성' if sigma == 0 else f'sigma{sigma} 블러 파일 생성'
                matches = [p for p in paths if p.startswith(folder + '/피쳐맵/' + key + '/') and Path(p).name.startswith(f'stage{stage}_')]
                if len(matches) != 1:
                    raise ValueError('참고 경로의 단계별 한 개 계약이 다릅니다.')
                relative = '블러 피쳐맵 저장 파일/' + matches[0]
                destination = HERE / relative
                if destination.exists():
                    raise FileExistsError('색인 밖의 그림은 덮어쓰지 않습니다: ' + relative)
                caption, selected, ranges = render(array, stage, sigma, label, destination)
                with Image.open(destination) as picture:
                    width, height = picture.size
                items.append({'id': f'{sigma}-{key}-{stage}', 'sigma': sigma, 'class_key': key, 'class_label': label,
                              'stage': stage, 'relative_path': relative, 'sha256': digest(destination), 'width': width, 'height': height,
                              'caption': caption, 'layer': LAYERS[stage], 'shape': list(array.shape), 'panel_indices': selected,
                              'panel_count': 1 if stage == 0 else 10, 'panel_minmax': ranges, 'source_sha256': row['byte_sha256'],
                              'run_id': RUN, 'protocol_fixed_model': True, 'training_sigma': 0,
                              'checkpoint_sha256': selection['checkpoint_sha256'], 'checkpoint_epoch': selection['checkpoint_epoch'],
                              'model_state_sha256': selection['model_state_sha256'], 'selected_checkpoint': selection['selected_checkpoint']})
        if len(items) != 18 or tensor_state_digest(model.state_dict()) != selection['model_state_sha256']:
            raise ValueError('동일 가중치와 강도별18그림 계약이 다릅니다.')
        index['items'].extend(items)
        index['completed_sigmas'].append(sigma)
        index['pending_sigmas'] = [s for s in SIGMAS if s not in index['completed_sigmas']]
        index['updated_at'] = now()
        atomic_json(index_path, index)
        print(json.dumps({'sigma': sigma, 'saved_png': 18, 'checkpoint_sha256': selection['checkpoint_sha256']}, ensure_ascii=False), flush=True)
    return not index['pending_sigmas']


def main():
    global TRAIN, HERE, REFERENCE, RUN, torch, np, plt, FONT, Image, SplitResNet50, GaussianDCTBlur, CTDataset
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--once', action='store_true')
    modes.add_argument('--watch', action='store_true')
    parser.add_argument('--experiment-root', type=Path, default=TRAIN)
    parser.add_argument('--output-root', type=Path, default=HERE)
    parser.add_argument('--reference-root', type=Path, default=REFERENCE)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    TRAIN, HERE, REFERENCE, RUN = args.experiment_root.resolve(), args.output_root.resolve(), args.reference_root.resolve(), args.run_id
    if TRAIN != (PROJECT / '7차').resolve() or HERE != (PROJECT / '블러 강도별 대표 특징맵' / '7차').resolve():
        parser.error('7차 학습과 새7차 그림 폴더만 사용합니다.')
    if len(RUN) != 16 or any(c not in '0123456789abcdef' for c in RUN):
        parser.error('확인한 실행 식별자16자리가 필요합니다.')
    try:
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        sys.path.insert(0, str(TRAIN))
        import torch
        torch.set_num_threads(2)
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.font_manager import FontProperties
        from PIL import Image
        from src.model import SplitResNet50, GaussianDCTBlur
        from src.data import CTDataset
        FONT = FontProperties(fname=str(TRAIN / 'web/fonts/NanumGothic-Bold.ttf'), weight='bold')
        HERE.mkdir(parents=True, exist_ok=True)
        paths = prepare()
        while True:
            complete = run_once(paths)
            if args.once or complete:
                break
            time.sleep(30)
    except Exception:
        failure = {'time_kst': now(), 'argv': [sys.executable, *sys.orig_argv[1:]], 'cwd': os.getcwd(), 'exit_code': 1, 'error': traceback.format_exc()}
        HERE.mkdir(parents=True, exist_ok=True)
        with (HERE / '실패기록_비공개.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(failure, ensure_ascii=False) + '\n')
        raise
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
