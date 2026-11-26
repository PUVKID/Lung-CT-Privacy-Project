"""거친 공간 정보/주변 영역만으로도 분류되는지 확인하는 탐색적 비교입니다."""
import numpy as np
from PIL import Image
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from 전송 import decode
from 지표 import binary_report

def diagnose(rows):
    from pathlib import Path
    import hashlib
    data = {}
    for split in ('train', 'test'):
        features, labels = [], []
        for row in rows[split]:
            raw = Path(row['packet_path']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != row['packet_sha256']:
                raise ValueError('단서진단패킷해시불일치')
            image = Image.fromarray(decode(raw)).resize((16,16),Image.Resampling.BOX)
            features.append(np.asarray(image,dtype=float).ravel()/255)
            labels.append(row['label'])
        data[split] = np.asarray(features), np.asarray(labels)
    center = np.zeros((16,16),dtype=bool)
    center[4:12,4:12] = True
    reports = {}
    for name, mask in [('coarse_full',np.ones(256,dtype=bool)),
                       ('coarse_center',center.ravel()),('coarse_outer',~center.ravel())]:
        model = make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=2000,random_state=42))
        model.fit(data['train'][0][:,mask],data['train'][1])
        reports[name] = binary_report(data['test'][1],model.decision_function(data['test'][0][:,mask]))
    return {'method':'16x16 area downsample, train-only scaling and fixed C1 logistic regression',
            'reports':reports, 'used_for_selection':False,
            'limitations':['이미사용한시험셋의탐색적진단',
                           '중앙정사각형은폐분할마스크가아님',
                           '바깥영역에도폐/신체일부가포함되어배경의존확정불가',
                           '환자ID가없어환자단위독립성미확인']}
