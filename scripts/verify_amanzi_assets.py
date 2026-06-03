"""Verify asset paths referenced in pillar-water-purification.html exist."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "pillar-water-purification.html").read_text(encoding="utf-8")
paths = set(re.findall(r'src="([^"]+)"', html))
assets = [p for p in paths if p.startswith("assets/")]
missing = [p for p in sorted(assets) if not (ROOT / p).exists()]
print(f"asset refs: {len(assets)}, missing: {len(missing)}")
for p in missing:
    print(f"  MISSING: {p}")
