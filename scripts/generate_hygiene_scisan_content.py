# -*- coding: utf-8 -*-
"""Build scisan-sani-99-content.html from scisan.co.za/sani-99/."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = "https://www.scisan.co.za/sani-99/"
SOURCE_HTML = Path("/tmp/scisan-sani-99.html")
OUTPUT = ROOT / "scisan-sani-99-content.html"
PAGE_ID = "1959"

EMBED_FIXES = """
<style id="ulr-scisan-embed-fixes">
  html, body { margin: 0; padding: 0; overflow-x: hidden; background: #fff; }
  body { min-height: 0; }
  .ulr-scisan-source-page { width: 100%; overflow: hidden; }
  .ulr-scisan-source-page img { max-width: 100%; height: auto; }
  .ulr-scisan-source-page .elementor-element,
  .ulr-scisan-source-page .e-con,
  .ulr-scisan-source-page .e-con-inner { box-sizing: border-box; }
</style>
"""

BROCHURE_REPLACEMENTS = (
    (
        'href="https://www.scisan.co.za/wp-content/uploads/2024/11/SANI-99-Legionella-Brochure-2024.pdf" target="_blank"',
        'href="#request-brochure" data-ulr-brochure-name="SANI-99 Legionella Control Brochure"',
    ),
    (
        'href="https://www.scisan.co.za/wp-content/uploads/2024/12/SANI-99-for-Black-Mould-2024.pdf" target="_blank"',
        'href="#request-brochure" data-ulr-brochure-name="SANI-99 Black Mould Treatment Brochure"',
    ),
    (
        'href="https://www.scisan.co.za/wp-content/uploads/2024/02/SANI-99-Brochure-2023.pdf" target="_blank"',
        'href="#request-brochure" data-ulr-brochure-name="SANI-99 Brochure"',
    ),
)


def fetch_source() -> str:
    if SOURCE_HTML.exists() and SOURCE_HTML.stat().st_size > 10000:
        return SOURCE_HTML.read_text(encoding="utf-8", errors="replace")
    print(f"Fetching {SOURCE_URL}")
    with urllib.request.urlopen(SOURCE_URL, timeout=120) as response:
        html = response.read().decode("utf-8", errors="replace")
    SOURCE_HTML.write_text(html, encoding="utf-8")
    return html


def extract_head(html: str) -> str:
    match = re.search(r"<head[^>]*>(.*)</head>", html, re.DOTALL | re.IGNORECASE)
    if not match:
        raise ValueError("Could not find <head> in source page")
    head = match.group(1).strip()
    head = re.sub(
        r"<title>.*?</title>",
        "<title>SANI-99 &#8211; Scientific Sanitation Solutions</title>",
        head,
        count=1,
        flags=re.DOTALL,
    )
    return head


def extract_elementor_content(html: str) -> str:
    marker = f'data-elementor-type="wp-page" data-elementor-id="{PAGE_ID}"'
    start = html.find(marker)
    if start == -1:
        raise ValueError(f"Could not find elementor page {PAGE_ID}")

    open_tag_start = html.rfind("<div", 0, start)
    if open_tag_start == -1:
        raise ValueError("Could not find elementor wrapper start")

    depth = 0
    index = open_tag_start
    length = len(html)
    while index < length:
        next_open = html.find("<div", index)
        next_close = html.find("</div>", index)
        if next_close == -1:
            raise ValueError("Unbalanced div tags in elementor content")
        if next_open != -1 and next_open < next_close:
            depth += 1
            index = next_open + 4
            continue
        depth -= 1
        index = next_close + 6
        if depth == 0:
            return html[open_tag_start:index].strip()
    raise ValueError("Could not close elementor wrapper")


def wire_brochure_links(content: str) -> str:
    updated = content
    for old, new in BROCHURE_REPLACEMENTS:
        updated = updated.replace(old, new)
    return updated


def build_document(html: str) -> str:
    head = extract_head(html)
    elementor = wire_brochure_links(extract_elementor_content(html))
    body_class = (
        "wp-singular page-template-default page page-id-1959 wp-theme-woodmart "
        "wp-child-theme-woodmart-child ehf-header ehf-footer ehf-template-woodmart "
        "ehf-stylesheet-woodmart-child wrapper-custom categories-accordion-on "
        "woodmart-ajax-shop-on elementor-default elementor-kit-6 elementor-page "
        "elementor-page-1959"
    )
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        + head
        + EMBED_FIXES
        + "\n</head>\n<body class=\""
        + body_class
        + "\">\n"
        + '  <main class="ulr-scisan-source-page" aria-label="SANI-99 SciSan source content">\n\t\t'
        + elementor
        + "\n\t\t\n  </main>\n</body>\n</html>\n"
    )


def main() -> None:
    html = fetch_source()
    OUTPUT.write_text(build_document(html), encoding="utf-8")
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
