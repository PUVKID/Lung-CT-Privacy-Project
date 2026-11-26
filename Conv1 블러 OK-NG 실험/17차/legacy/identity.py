"""고정 1만장 연구의 설정·설치·실행 식별자. Torch 없이 사용할 수 있습니다."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

PROTOCOL = 'input-blur-fixed10000-resnet50-multimetric-v12'
SIGMAS = [0,1,2,4,6,8,10,12,16,20,24,32,40,48,64,80,96,128,192,256]
REGIMES = ['split_trainable', 'full_finetune']
PIPELINE_IDENTITY = {
    'blur_domain': 'input_image', 'sigma_unit': 'resized_image_pixels', 'image_size': 512,
    'transform_order': 'copied_source_fixed_oversample_sigma0_png8_copy_blur_png8_load_normalize_conv1',
    'exposed_feature_dtype': 'float32', 'classifier_input': 'materialized_png8',
    'classifier_applies_blur_again': False, 'split_unit': 'source_image_lineage_group',
    'stage12_training': 'microbatch2_accum4_bn_running_stats_frozen_trainonly_hflip25_validation_best200',
    'batch_norm_running_stats_policy': 'freeze_running_stats_train_gamma_beta',
}
DEFAULTS = {
    'protocol': PROTOCOL, 'image_size': 512, 'batch_size': 2, 'gradient_accumulation_steps': 4, 'batch_norm_running_stats_frozen': True, 'samples_per_class': 5000,
    'seed': 42, 'sigmas': SIGMAS, 'regimes': REGIMES, 'epochs': 200, 'precision': 'bf16',
    'early_stopping_enabled': True, 'early_stopping_min_epochs': 30,
    'early_stopping_patience': 25, 'min_delta': 1e-4, 'dropout': .3,
    'learning_rate': 1e-4, 'weight_decay': 1e-4, 'scheduler_patience': 8,
    'scheduler_factor': .5, 'min_learning_rate': 1e-6, 'label_smoothing': .02, 'train_flip_probability': .25,
    'split_boundary': 'conv1', 'num_workers': 2, 'eval_num_workers': 0,
    'prefetch_factor': 2, 'persistent_workers': True, 'pin_memory': True,
    'worker_timeout_seconds': 120, 'cpu_threads': 4, 'validation_ratio': .15,
    'test_ratio': .15, 'gradient_clip_norm': 1.0,
    'retain_completed_last_checkpoints': False,
}


def file_sha256(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def json_digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def safe_path(root, value):
    root = Path(root).absolute()
    path = Path(value)
    path = path if path.is_absolute() else root / path
    for part in (path, *path.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('연결 경로를 연구 파일로 사용하지 않습니다: ' + str(part))
        if part == root:
            break
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('실험 폴더 밖의 결과 파일입니다: ' + str(path))
    return path


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def validate_config(config):
    for key in ('protocol', 'image_size', 'batch_size', 'samples_per_class', 'seed',
                'sigmas', 'regimes', 'epochs', 'early_stopping_enabled', 'early_stopping_min_epochs',
                'early_stopping_patience', 'dropout', 'weight_decay', 'label_smoothing', 'split_boundary', 'gradient_accumulation_steps', 'train_flip_probability', 'batch_norm_running_stats_frozen'):
        expected = DEFAULTS[key]
        if type(config.get(key)) is not type(expected) or config[key] != expected:
            raise ValueError('고정 1만장 연구 설정이 다릅니다: ' + key)
    instance = config.get('experiment_instance_id')
    if (not isinstance(instance, str) or len(instance) != 32
            or any(c not in '0123456789abcdef' for c in instance)):
        raise ValueError('설치 식별자가 올바르지 않습니다.')
    if type(config.get('gradient_accumulation_steps')) is not int or not 1 <= config['gradient_accumulation_steps'] <= 16:
        raise ValueError('누적 미니배치 횟수가 올바르지 않습니다.')
    if not 0 <= config.get('train_flip_probability', -1) <= 1:
        raise ValueError('학습 전용 좌우 반전 확률이 유효하지 않습니다.')
    if config.get('precision') != 'bf16':
        raise ValueError('학습 정밀도는 명시한 BF16 조건이어야 합니다.')
    for key in ('initial_weights_path', 'initial_weights_sha256', 'dataset_root'):
        if not isinstance(config.get(key), str) or not config[key]:
            raise ValueError('필수 설정이 없습니다: ' + key)
    for key in ('learning_rate', 'min_learning_rate', 'min_delta', 'gradient_clip_norm'):
        value = config.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 < float(value) < float('inf'):
            raise ValueError('양의 유한한 설정이 필요합니다: ' + key)
    if not 0 < config.get('scheduler_factor', 0) < 1:
        raise ValueError('학습률 감소 비율이 유효하지 않습니다.')
    for key in ('num_workers', 'eval_num_workers'):
        if type(config.get(key, 0)) is not int or not 0 <= config.get(key, 0) <= 16:
            raise ValueError('데이터 워커 설정이 유효하지 않습니다: ' + key)
    return config


def source_hashes(root):
    root = Path(root)
    paths = [root / 'run_training.py', root / 'config.json']
    paths += sorted((root / 'src').glob('*.py'))
    paths += sorted((root / 'tools').glob('*.py'))
    config = read_json(root / 'config.json')
    reference = config.get('expected_reference_manifest')
    if reference:
        paths.append(safe_path(root, reference))
    return {path.relative_to(root).as_posix(): file_sha256(safe_path(root, path)) for path in paths}


def verify_installation(root):
    root = Path(root)
    marker = read_json(safe_path(root, 'installation.json'))
    if marker.get('protocol') != PROTOCOL:
        raise ValueError('고정 1만장 설치 기록이 아닙니다.')
    fingerprints = marker.get('code_sha256')
    if not isinstance(fingerprints, dict) or not fingerprints:
        raise ValueError('설치 파일 지문이 없습니다.')
    for name, expected in fingerprints.items():
        path = safe_path(root, name)
        if not path.is_file() or file_sha256(path) != expected:
            raise ValueError('설치 이후 연구 파일이 달라졌습니다: ' + name)
    return marker


def read_config(root, verify=True):
    root = Path(root)
    marker = verify_installation(root) if verify else None
    config = validate_config(read_json(safe_path(root, 'config.json')))
    if marker is not None and marker.get('experiment_instance_id') != config['experiment_instance_id']:
        raise ValueError('설정과 설치 식별자가 다릅니다.')
    return config


def get_run_id(root, config):
    return json_digest({'config': config, 'source_hashes': source_hashes(root)})[:16]


def prepare_run(root, config, source_hashes=None):
    from .state import atomic_json, now_kst
    root = Path(root)
    hashes = source_hashes if source_hashes is not None else globals()['source_hashes'](root)
    run_id = json_digest({'config': config, 'source_hashes': hashes})[:16]
    path = safe_path(root, 'work/results/run_' + run_id + '/run_metadata.json')
    metadata = {'protocol': PROTOCOL, 'run_id': run_id,
                'experiment_instance_id': config['experiment_instance_id'],
                'config': config, 'source_hashes': hashes, 'pipeline': PIPELINE_IDENTITY,
                'created_at': now_kst(), 'test_use': 'fixed generated split; model selection only by validation loss',
                'evaluation_unit': 'generated_image_and_source_image', 'patient_grouping': False}
    if path.exists():
        old = read_json(path)
        for key in ('protocol', 'run_id', 'experiment_instance_id', 'config', 'source_hashes', 'pipeline'):
            if old.get(key) != metadata[key]:
                raise ValueError('기존 실행과 현재 코드/설정이 다릅니다: ' + key)
        metadata = old
    else:
        atomic_json(path, metadata)
    return run_id, metadata


def condition_binding(config, run_id, manifest, sigma, regime):
    return {'protocol': PROTOCOL, 'experiment_instance_id': config['experiment_instance_id'],
            'run_id': run_id, 'sigma': sigma, 'regime': regime,
            'condition_id': f'{regime}:sigma_{sigma}',
            'data_manifest_sha256': manifest['manifest_sha256'],
            'plan_sha256': manifest['plan_sha256'],
            'source_copy_manifest_sha256': manifest['source_copy_manifest_sha256'],
            'classifier_input': 'actual_saved_png8', 'double_blur': False}


def assert_binding(value, binding):
    if not isinstance(value, dict) or any(value.get(k) != v for k, v in binding.items()):
        raise ValueError('결과/체크포인트가 현재 실행·강도·데이터와 다릅니다.')


def load_selection(root, run_id, sigma, regime='split_trainable'):
    value = read_json(safe_path(root, f'work/results/run_{run_id}/{regime}/sigma_{sigma}_selection.json'))
    if value.get('run_id') != run_id or value.get('sigma') != sigma or value.get('regime') != regime:
        raise ValueError('선정 모델 기록이 요청 조건과 다릅니다.')
    return value
