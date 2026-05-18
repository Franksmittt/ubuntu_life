import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
pat = re.compile(
    r'\n        <section class="tj-cta-section">\s*<div class="container">.*?Start the conversation.*?</section>\n      </main>',
    re.S,
)
for fn in [
    "pillar-agri-biosecurity.html",
    "pillar-shelf-stable-nutrition.html",
    "pillar-water-purification.html",
]:
    p = ROOT / fn
    t = p.read_text(encoding="utf-8")
    t2, n = pat.subn("\n      </main>", t, count=1)
    if n:
        p.write_text(t2, encoding="utf-8")
        print("removed duplicate CTA from", fn)
    else:
        print("no duplicate found in", fn)
