"""저장 로짓과 정답에서 계산하며, 정의되지 않는 지표를 숫자로 꾸미지 않습니다."""
import math
import numpy as np
from scipy.special import expit
from sklearn.metrics import roc_auc_score, average_precision_score, matthews_corrcoef

def grouped_accuracy_interval(labels, logits, groups, seed=20261125, draws=2000):
    """유사 원본 그룹을 통째로 재표집합니다. 환자ID 부재를 대체하지 않습니다."""
    y = np.asarray(labels).reshape(-1)
    z = np.asarray(logits).reshape(-1)
    g = np.asarray(groups).reshape(-1)
    if not len(y) or len(y) != len(z) or len(y) != len(g) or not np.isfinite(z).all():
        raise ValueError('그룹구간입력길이/유한값오류')
    unique, inverse = np.unique(g, return_inverse=True)
    if len(unique) < 2:
        return {'accuracy_ci95_group':None,'n_similarity_groups':len(unique),
                'interval_reason':'유사그룹이2개미만이어서구간을산출하지않음'}
    correct = np.bincount(inverse, weights=(y == (z >= 0)))
    counts = np.bincount(inverse)
    indexes = np.random.default_rng(seed).integers(0,len(unique),size=(draws,len(unique)))
    values = correct[indexes].sum(axis=1)/counts[indexes].sum(axis=1)
    degenerate = bool(np.allclose(values, values[0], rtol=0, atol=1e-15))
    reason = ('현재 표본의 재표집 정확도가 모두 같아 구간이 퇴화함. '
              '모집단 정확도가 이 값으로 확정된다는 뜻이 아님') if degenerate else None
    return {'accuracy_ci95_group':np.quantile(values,[.025,.975]).tolist(),
            'n_similarity_groups':len(unique),'group_bootstrap_draws':draws,
            'interval_degenerate':degenerate, 'interval_degenerate_reason':reason,
            'interval_note':'유사원본그룹단위재표집구간;환자단위구간아님;이미사용한시험셋의탐색평가'}

def binary_report(labels, logits):
    y = np.asarray(labels, dtype=float).reshape(-1)
    z = np.asarray(logits, dtype=float).reshape(-1)
    if not len(y) or len(y) != len(z) or not np.isfinite(z).all() or not np.isin(y, [0, 1]).all():
        raise ValueError("정답/로짓 길이·범위·유한값을 확인하십시오.")
    y = y.astype(int)
    pred = (z >= 0).astype(int)
    p = expit(z)
    tn = int(((y == 0) & (pred == 0)).sum())
    fp = int(((y == 0) & (pred == 1)).sum())
    fn = int(((y == 1) & (pred == 0)).sum())
    tp = int(((y == 1) & (pred == 1)).sum())
    reasons = {}
    def ratio(a, b, name):
        if not b:
            reasons[name] = "분모가0이어서정의되지않음"
            return None
        return a / b
    ok = ratio(tn, tn+fp, "ok_accuracy")
    ng = ratio(tp, tp+fn, "ng_accuracy")
    precision = ratio(tp, tp+fp, "precision")
    npv = ratio(tn, tn+fn, "npv")
    f1 = ratio(2*tp, 2*tp+fp+fn, "f1")
    both = len(np.unique(y)) == 2
    auc = float(roc_auc_score(y, z)) if both else None
    ap = float(average_precision_score(y, p)) if both else None
    if not both:
        reasons.update(auc="실제정답에두클래스가모두필요함", pr_auc="실제정답에두클래스가모두필요함")
    mcc_den = (tp+fp)*(tp+fn)*(tn+fp)*(tn+fn)
    mcc = float(matthews_corrcoef(y, pred)) if mcc_den else None
    if mcc is None:
        reasons['mcc'] = "혼동행렬의MCC분모가0이어서정의되지않음"
    ece = 0.0
    for i in range(10):
        mask = (p >= i/10) & ((p < (i+1)/10) if i < 9 else (p <= 1))
        if mask.any():
            ece += float(mask.mean() * abs(p[mask].mean()-y[mask].mean()))
    n = len(y)
    correct = tn+tp
    accuracy = correct/n
    q = 1.959963984540054
    den = 1+q*q/n
    center = (accuracy+q*q/(2*n))/den
    margin = q*math.sqrt(accuracy*(1-accuracy)/n+q*q/(4*n*n))/den
    return dict(loss=float(np.mean(np.logaddexp(0, z)-y*z)), accuracy=accuracy,
                correct=correct, total=n, n_correct=correct, n_images=n, n_errors=n-correct,
                ok_accuracy=ok, ng_accuracy=ng, sensitivity=ng, specificity=ok,
                ok_support=tn+fp, ng_support=tp+fn,
                balanced_accuracy=(ok+ng)/2 if ok is not None and ng is not None else None,
                auc=auc, pr_auc=ap, pr_auc_definition="average_precision",
                precision=precision, npv=npv, f1=f1, mcc=mcc,
                brier_score=float(np.mean((p-y)**2)), ece_10_bins=ece,
                ece_definition="ten equal-width probability bins: absolute mean predicted NG probability minus observed NG frequency",
                confusion_matrix=[[tn,fp],[fn,tp]], threshold_probability=.5,
                wilson95=[max(0,center-margin),min(1,center+margin)],
                interval_note="영상독립을가정한기술적구간이며환자단위독립성을입증하지않음",
                undefined_reasons=reasons)
