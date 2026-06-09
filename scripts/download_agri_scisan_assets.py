# -*- coding: utf-8 -*-
"""Download scisan.co.za/sani-99-for-agri images into assets folder."""
from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "pillars" / "agri-biosecurity" / "scisan"
BASE = "https://www.scisan.co.za/wp-content/uploads"

FILES = [
    "2024/01/qq.webp",
    "2024/06/SANI-99-FOR-AGRI-BENEFITS-WHEEL-1.png",
    "2024/05/Key-Features-Trt-1024x175-1.png",
    "2023/11/Log-Rating-Chart.webp",
    "2023/11/sani-truck-2.png",
    "2023/11/agri-truck.png",
    "2023/11/SANI-Sachet-Lable-2-150x150.webp",
    "2023/11/1-Litre-Lable-1-146x150.webp",
    "2023/11/Medical-Grade-Lable-150x150.webp",
    "2023/11/LOG-7-Lable-1.webp",
    "2023/11/Affordable-label.webp",
    "2023/11/Carbon-Footprint-Label-1.webp",
    "2024/06/4pictures-1024x256-1.png",
    "2024/06/view-1024x682-1.jpg",
    "2024/01/SANI-AGRI-Worlds-Best-Disinfectant-1024x728.webp",
    "2023/11/bottom-agri-1024x512.png",
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
