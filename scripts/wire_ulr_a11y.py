"""Add ulr-a11y.css after ulr-layout.css on every HTML page."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNIPPET = '\n  <link rel="stylesheet" href="assets/css/ulr-a11y.css">'
ANCHOR = '  <link rel="stylesheet" href="assets/css/ulr-layout.css">'

for path in sorted(ROOT.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    if "ulr-a11y.css" in text:
        print(f"skip {path.name}")
        continue
    if ANCHOR not in text:
        print(f"skip {path.name} (no layout css)")
        continue
    text = text.replace(ANCHOR, ANCHOR + SNIPPET, 1)
    path.write_text(text, encoding="utf-8")
    print(f"updated {path.name}")
