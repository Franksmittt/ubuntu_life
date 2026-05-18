"""Add ulr-brand.css + ulr-layout.css to every HTML page (main.css @import at EOF is invalid)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNIPPET = (
    '\n  <link rel="stylesheet" href="assets/css/ulr-brand.css">'
    '\n  <link rel="stylesheet" href="assets/css/ulr-layout.css">'
)
MAIN = '  <link rel="stylesheet" href="assets/css/main.css">'

for path in sorted(ROOT.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    if "ulr-layout.css" in text:
        print(f"skip {path.name} (already wired)")
        continue
    if MAIN not in text:
        print(f"skip {path.name} (no main.css)")
        continue
    text = text.replace(MAIN, MAIN + SNIPPET, 1)
    path.write_text(text, encoding="utf-8")
    print(f"updated {path.name}")
