#!/usr/bin/env python3
"""Add phase-gate CSS/JS to all public HTML pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_LINK = '  <link rel="stylesheet" href="assets/css/ulr-phase-gate.css">'
JS_SCRIPT = '  <script src="assets/js/ulr-phase-gate.js"></script>'
SKIP = {"test.html"}


def wire(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    if "ulr-phase-gate.css" not in text:
        marker = '  <link rel="stylesheet" href="assets/css/ulr-a11y.css">'
        if marker in text:
            text = text.replace(marker, marker + "\n" + CSS_LINK, 1)
            changed = True
        else:
            marker = '  <link rel="stylesheet" href="assets/css/ulr-footer.css">'
            if marker in text:
                text = text.replace(marker, marker + "\n" + CSS_LINK, 1)
                changed = True

    if "ulr-phase-gate.js" not in text:
        marker = '  <script src="assets/js/main.js"></script>'
        if marker in text:
            text = text.replace(marker, JS_SCRIPT + "\n" + marker, 1)
            changed = True

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    updated = []
    for html in sorted(ROOT.glob("*.html")):
        if html.name in SKIP:
            continue
        if wire(html):
            updated.append(html.name)
    print("Wired phase gate on", len(updated), "files:")
    for name in updated:
        print(" ", name)


if __name__ == "__main__":
    main()
