# -*- coding: utf-8 -*-
"""Download scisan.co.za/sani-99 images into assets folder."""
from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "pillars" / "hygiene-sanitation" / "scisan"
BASE = "https://www.scisan.co.za/wp-content/uploads"

FILES = [
    "2024/06/SANI-99-BENEFITS-WHEEL-5-1024x1024.png",
    "2024/05/Key-features-icon-1024x152-1.png",
    "2025/02/Standards-ic.png",
    "2023/11/Log-Rating-Chart.webp",
    "2024/11/banner-with-images-1024x527.jpg",
    "2024/12/housekeeper-s-hand-with-glove-cleaning-mold-from-w-2023-11-27-04-54-12-utc-scaled-1-1024x576.jpg",
    "2023/11/sani-truck-2.png",
    "2023/11/sani-truck-1.png",
    "2023/11/SANI-Sachet-Lable-2-150x150.webp",
    "2023/11/1-Litre-Lable-1-146x150.webp",
    "2023/11/Medical-Grade-Lable-150x150.webp",
    "2023/11/LOG-7-Lable-1.webp",
    "2023/11/Affordable-label.webp",
    "2023/11/Carbon-Footprint-Label-1-150x150.webp",
    "2023/11/Instructions-for-Use-June-23-white-bg-2-1024x307.webp",
    "2024/03/sani-logo-199x300-1.png",
    "2023/11/Vs-graphic.webp",
    "2024/06/sani-all-products-222-1.jpg",
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for rel in FILES:
        url = f"{BASE}/{rel}"
        name = Path(rel).name
        dest = OUT / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"skip {name}")
            continue
        print(f"get {name}")
        urllib.request.urlretrieve(url, dest)
    print(f"Done -> {OUT}")


if __name__ == "__main__":
    main()
