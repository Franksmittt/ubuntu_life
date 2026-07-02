# -*- coding: utf-8 -*-
"""Strip hardcoded header nav active states and include ulr-nav.js."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_STUDIES_ACTIVE = (
    '<li class="current-menu-item"><a href="case-studies.html">Case studies</a></li>'
)
CASE_STUDIES_LINK = '<li><a href="case-studies.html">Case studies</a></li>'
NAV_SCRIPT = '  <script src="assets/js/ulr-nav.js"></script>\n'
MAIN_SCRIPT = '  <script src="assets/js/main.js"></script>'


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = text.replace(CASE_STUDIES_ACTIVE, CASE_STUDIES_LINK)
    if NAV_SCRIPT.strip() not in updated and MAIN_SCRIPT in updated:
        updated = updated.replace(MAIN_SCRIPT, NAV_SCRIPT + MAIN_SCRIPT, 1)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for path in sorted(ROOT.glob("*.html")):
        if path.name.startswith("scisan-"):
            continue
        if patch_file(path):
            print(f"Patched {path.name}")
            changed += 1
    print(f"Done. Updated {changed} file(s).")


if __name__ == "__main__":
    main()
