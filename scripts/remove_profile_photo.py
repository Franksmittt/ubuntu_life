"""Remove Sanchia profile photo block from all HTML pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(
    r'\s*<div class="ulr-pillar-leadership-visual">\s*'
    r'<img class="ulr-pillar-leadership-photo"[^>]*>\s*'
    r'</div>\s*',
    re.IGNORECASE | re.DOTALL,
)

for path in sorted(ROOT.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    new_text, count = BLOCK.subn("", text)
    if count:
        path.write_text(new_text, encoding="utf-8")
        print(f"removed {count} from {path.name}")