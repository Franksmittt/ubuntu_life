"""Copy scisan reference images from saved webpage folder into assets."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "SANI Amanzi – Scientific Sanitation Solutions_files"
DEST = ROOT / "assets/images/pillars/sani-amanzi/scisan"
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    copied = 0
    for path in sorted(SRC.iterdir()):
        if path.suffix.lower() in EXTS and path.is_file():
            target = DEST / path.name
            if not target.exists() or path.stat().st_mtime > target.stat().st_mtime:
                shutil.copy2(path, target)
                copied += 1
    total = len(list(DEST.glob("*")))
    print(f"Scisan assets: {total} files ({copied} copied/updated)")


if __name__ == "__main__":
    main()
