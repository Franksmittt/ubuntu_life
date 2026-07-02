# -*- coding: utf-8 -*-
"""Build scisan-sani-99-content.html from scisan.co.za/sani-99/."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = "https://www.scisan.co.za/sani-99/"
SOURCE_HTML = ROOT / "scripts" / ".cache" / "scisan-sani-99.html"
OUTPUT = ROOT / "scisan-sani-99-content.html"
PAGE_ID = "1959"
HERO_BG = (
    "/assets/vendor/scisan-mirror/www.scisan.co.za/wp-content/uploads/2024/06/"
    "SANI-99-Stater-Pack.185de69a25.webp"
)

EMBED_FIXES = f"""
<style id="ulr-scisan-embed-fixes">
  html, body {{ margin: 0; padding: 0; overflow-x: hidden; background: #fff; }}
  body {{ min-height: 0; }}
  .ulr-scisan-source-page {{ width: 100%; max-width: 100%; overflow-x: hidden; }}
  .ulr-scisan-source-page img {{ max-width: 100%; height: auto; }}
  .ulr-scisan-source-page .elementor-element,
  .ulr-scisan-source-page .e-con,
  .ulr-scisan-source-page .e-con-inner {{ box-sizing: border-box; max-width: 100%; }}

  .ulr-scisan-source-page .wd-section-stretch-content,
  .ulr-scisan-source-page .wd-section-stretch {{
    width: 100% !important;
    max-width: 100% !important;
    left: 0 !important;
    right: 0 !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
  }}

  .ulr-scisan-source-page .elementor-widget-text-editor {{
    width: 100% !important;
    max-width: 100% !important;
  }}

  .ulr-scisan-source-page .elementor-widget-text-editor > .elementor-widget-container,
  .ulr-scisan-source-page .elementor-widget-heading > .elementor-widget-container {{
    width: 80% !important;
    max-width: 80% !important;
    margin-left: auto;
    margin-right: auto;
  }}

  .ulr-scisan-source-page .elementor-widget-image > .elementor-widget-container,
  .ulr-scisan-source-page .elementor-widget-eael-flip-box > .elementor-widget-container {{
    width: 100% !important;
    max-width: 100% !important;
    margin-left: auto;
    margin-right: auto;
  }}

  .ulr-scisan-source-page .elementor-widget-video-playlist {{
    width: 80% !important;
    max-width: 80% !important;
    margin-left: auto;
    margin-right: auto;
  }}

  .ulr-scisan-source-page .elementor-element-76af5ff,
  .ulr-scisan-source-page .elementor-element-76af5ff > .elementor-motion-effects-container > .elementor-motion-effects-layer {{
    background-image: url('{HERO_BG}') !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-size: cover !important;
  }}

  .ulr-scisan-source-page .elementor-element-76af5ff .elementor-widget-heading > .elementor-widget-container {{
    width: 100% !important;
    max-width: 100% !important;
    text-align: center;
  }}

  .ulr-scisan-source-page .elementor-element-f39fde8 .elementor-widget-heading > .elementor-widget-container {{
    width: 100% !important;
    max-width: 100% !important;
  }}

  /* Elementor scroll animations do not run in the iframe — show content immediately */
  .ulr-scisan-source-page .elementor-invisible {{
    visibility: visible !important;
    opacity: 1 !important;
    animation: none !important;
    transform: none !important;
  }}

  /* Disable load animations that cause flip-card text overlap */
  .ulr-scisan-source-page .eael-animate-zoom-in,
  .ulr-scisan-source-page .eael-animate-flip {{
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
  }}

  .ulr-scisan-source-page .eael-elements-flip-box-container {{
    overflow: hidden !important;
    perspective: 1200px;
  }}

  .ulr-scisan-source-page .eael-elements-flip-box-flip-card {{
    position: relative;
    width: 100%;
    min-height: 280px;
    transform-style: preserve-3d;
    transition: transform 0.55s ease;
  }}

  .ulr-scisan-source-page .eael-elements-flip-box-front-container,
  .ulr-scisan-source-page .eael-elements-flip-box-rear-container {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    overflow: hidden;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
  }}

  .ulr-scisan-source-page .eael-elements-flip-box-rear-container {{
    transform: rotateY(180deg);
  }}

  .ulr-scisan-source-page .eael-flip-box-hover:hover .eael-elements-flip-box-flip-card {{
    transform: rotateY(180deg);
  }}

  .ulr-scisan-source-page .eael-elements-flip-box-heading,
  .ulr-scisan-source-page .eael-elements-flip-box-content,
  .ulr-scisan-source-page .flipcontent {{
    position: relative;
    z-index: 1;
  }}

  .ulr-scisan-source-page .eael-elements-flip-box-content .flipcontent {{
    margin: 0;
    padding-left: 1.1rem;
    text-align: left;
  }}

  .ulr-scisan-source-page .eael-elements-flip-box-content .flipcontent li + li {{
    margin-top: 0.2rem;
  }}

  .ulr-scisan-source-page .ulr-scisan-video-embed,
  .ulr-scisan-source-page .e-tab-content-video {{
    width: 100%;
  }}

  .ulr-scisan-source-page .ulr-scisan-video-embed .elementor-wrapper,
  .ulr-scisan-source-page .e-tab-content-video .elementor-wrapper {{
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    background: #000;
  }}

  .ulr-scisan-source-page .ulr-scisan-video-embed iframe,
  .ulr-scisan-source-page .e-tab-content-video iframe {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: 0;
  }}

  .ulr-scisan-source-page .elementor-widget-video-playlist .e-tabs-main-area {{
    min-height: 434px;
  }}

  .ulr-scisan-source-page .elementor-widget-video-playlist .e-tabs-content-wrapper {{
    background: #000;
  }}

  .ulr-scisan-source-page .elementor-widget-video-playlist .e-tabs-content-wrapper .e-tab-content {{
    display: none !important;
    height: 100%;
    background: #000;
  }}

  .ulr-scisan-source-page .elementor-widget-video-playlist .e-tabs-content-wrapper .e-tab-content.ulr-scisan-tab-active {{
    display: block !important;
  }}

  .ulr-scisan-source-page .elementor-widget-video-playlist .e-tabs-content-wrapper .e-tab-content.ulr-scisan-tab-active > div,
  .ulr-scisan-source-page .elementor-widget-video-playlist .ulr-scisan-video-embed,
  .ulr-scisan-source-page .elementor-widget-video-playlist .e-tab-content-video {{
    height: 100%;
    min-height: 100%;
  }}

  .ulr-scisan-source-page .elementor-widget-video-playlist .ulr-scisan-video-embed .elementor-wrapper,
  .ulr-scisan-source-page .elementor-widget-video-playlist .e-tab-content-video .elementor-wrapper {{
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 320px;
    aspect-ratio: auto;
    background: #000;
  }}

  @media (max-width: 1024px) {{
    .ulr-scisan-source-page .elementor-widget-video-playlist.e-tabs-view-vertical .e-tabs-main-area {{
      flex-direction: column !important;
      min-height: 0 !important;
    }}

    .ulr-scisan-source-page .elementor-widget-video-playlist .e-tabs-content-wrapper {{
      min-height: 240px;
    }}
  }}

  @media (max-width: 767px) {{
    .ulr-scisan-source-page .elementor-widget-text-editor > .elementor-widget-container,
    .ulr-scisan-source-page .elementor-widget-heading > .elementor-widget-container,
    .ulr-scisan-source-page .elementor-widget-video-playlist {{
      width: 100% !important;
      max-width: 100% !important;
    }}

    .ulr-scisan-source-page .eael-elements-flip-box-flip-card {{
      min-height: 240px;
    }}

    .ulr-scisan-source-page .elementor-widget-video-playlist .e-tabs-main-area {{
      min-height: 0 !important;
    }}

    .ulr-scisan-source-page .elementor-widget-video-playlist .ulr-scisan-video-embed .elementor-wrapper,
    .ulr-scisan-source-page .elementor-widget-video-playlist .e-tab-content-video .elementor-wrapper {{
      min-height: 200px;
    }}
  }}
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
    SOURCE_HTML.parent.mkdir(parents=True, exist_ok=True)
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
    head = re.sub(
        r"<style>\s*\.e-con\.e-parent:nth-of-type.*?background-image:\s*none\s*!important;.*?</style>",
        "",
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


def remove_element_by_data_id(content: str, data_id: str) -> str:
    marker = f'data-id="{data_id}"'
    start = content.find(marker)
    if start == -1:
        return content

    open_tag_start = content.rfind("<div", 0, start)
    if open_tag_start == -1:
        return content

    depth = 0
    index = open_tag_start
    length = len(content)
    while index < length:
        next_open = content.find("<div", index)
        next_close = content.find("</div>", index)
        if next_close == -1:
            return content
        if next_open != -1 and next_open < next_close:
            depth += 1
            index = next_open + 4
            continue
        depth -= 1
        index = next_close + 6
        if depth == 0:
            return content[:open_tag_start] + content[index:]
    return content


def apply_brochure_copy(content: str) -> str:
    updated = content.replace("Download the ", "Request the ")
    updated = updated.replace(
        "download the full brochure below",
        "request the full brochure below",
    )
    updated = updated.replace(
        '<span class="elementor-button-text">BROCHURE</span>',
        '<span class="elementor-button-text">REQUEST BROCHURE</span>',
    )
    return updated


def apply_ulr_fixes(content: str) -> str:
    updated = remove_element_by_data_id(content, "cffe84c")
    updated = updated.replace(
        "elementor-element-dc63de8 elementor-invisible elementor-widget",
        "elementor-element-dc63de8 elementor-widget",
    )
    updated = updated.replace(
        "elementor-element-b3fc7f5 elementor-invisible elementor-widget",
        "elementor-element-b3fc7f5 elementor-widget",
    )
    updated = updated.replace("eael-animate-flip eael-animate-zoom-in ", "")
    updated = updated.replace("eael-animate-zoom-in eael-animate-flip ", "")
    return apply_brochure_copy(updated)


def mark_elementor_lazyloaded(body: str) -> str:
    def add_lazyloaded(match: re.Match[str]) -> str:
        tag = match.group(0)
        if "e-lazyloaded" in tag:
            return tag
        return re.sub(r'\bclass="', 'class="e-lazyloaded ', tag, count=1, flags=re.I)

    return re.sub(
        r'<div\b[^>]*\bclass="[^"]*\be-con[^"]*\be-parent[^"]*"[^>]*>',
        add_lazyloaded,
        body,
        flags=re.I,
    )


def wire_brochure_links(content: str) -> str:
    updated = content
    for old, new in BROCHURE_REPLACEMENTS:
        updated = updated.replace(old, new)
    return updated


def build_document(html: str) -> str:
    head = extract_head(html)
    elementor = mark_elementor_lazyloaded(
        apply_ulr_fixes(wire_brochure_links(extract_elementor_content(html)))
    )
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
        + "\n\t\t\n  </main>\n"
        + '  <script src="assets/js/ulr-scisan-playlist.js" defer></script>\n'
        + "</body>\n</html>\n"
    )


def main() -> None:
    html = fetch_source()
    OUTPUT.write_text(build_document(html), encoding="utf-8")
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
