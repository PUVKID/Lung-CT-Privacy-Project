import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from 지표 import binary_report

perfect = binary_report([0,0,1,1], [-10,-2,2,10])
assert perfect['correct'] == perfect['total'] == 4
assert perfect['accuracy'] == perfect['auc'] == perfect['f1'] == 1
assert perfect['confusion_matrix'] == [[2,0],[0,2]]
assert 0 < perfect['wilson95'][0] < 1
wrong = binary_report([0,1], [2,-2])
assert wrong['correct'] == 0 and wrong['auc'] == 0
single = binary_report([0,0], [-1,-1])
assert single['auc'] is None and single['ng_accuracy'] is None and single['precision'] is None
assert single['undefined_reasons']
for y,z in [([],[]),([0],[float('nan')]),([2],[0]),([0],[1,2])]:
    try:
        binary_report(y,z)
    except ValueError:
        pass
    else:
        raise AssertionError('잘못된입력수락')
print('PASS:실제정답수/0점/완전정답/정의불가/실패입력')
