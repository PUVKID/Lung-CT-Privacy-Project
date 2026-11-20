"""핵심 소스·문서의 UTF-8·대체 문자·Python 문법을 검사합니다."""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paths = [ROOT / "run_training.py", ROOT / "안전_학습.py", ROOT / "config.json"]
paths += list((ROOT / "src").glob("*.py")) + list((ROOT / "tools").glob("*.py")) + list((ROOT / "docs").glob("*.md"))
for path in paths:
    text = path.read_bytes().decode("utf-8", errors="strict")
    if "\ufffd" in text:
        raise ValueError("대체 문자가 있습니다: " + str(path))
    if path.suffix == ".py":
        ast.parse(text, filename=str(path))
print(f"엄격 UTF-8·대체 문자·해당 Python 문법 검사 통과: {len(paths)}파일")
