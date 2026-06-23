# -*- coding: utf-8 -*-
"""Import SciSan case studies and generate Ubuntu Life Resources pages."""
from __future__ import annotations

import html
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "about.html"
INDEX_URL = "https://www.scisan.co.za/case-studies/"

EMBED_FIXES = """<style id="ulr-scisan-embed-fixes">
  html, body { margin: 0; padding: 0; overflow-x: hidden; background: #fff; }
  body { min-height: 0; }
  .ulr-scisan-source-page { width: 100%; overflow: hidden; }
  .ulr-scisan-source-page img { max-width: 100%; height: auto; }
  .ulr-scisan-source-page .elementor-element,
  .ulr-scisan-source-page .e-con,
  .ulr-scisan-source-page .e-con-inner { box-sizing: border-box; }

  /* Elementor lazy backgrounds need frontend JS on SciSan; show immediately in embed */
  .ulr-scisan-source-page .elementor-invisible {
    visibility: visible !important;
    opacity: 1 !important;
    animation: none !important;
    transform: none !important;
  }
</style>"""

CASE_STUDIES = [
    {
        "file_slug": "the-chirpy-egg-co",
        "scisan_path": "the-chirpy-egg-co/",
        "title": "The Chirpy Egg Co",
        "card_title": "SANI-99™ For AGRI: The Chirpy Egg Co, Lincolnshire, United Kingdom",
        "category": "Agriculture",
        "pillar_href": "pillar-agri-biosecurity.html",
    },
    {
        "file_slug": "makoko-nigeria",
        "scisan_path": "makoko-nigeria-case-study/",
        "title": "Makoko, Nigeria",
        "card_title": "SANI AMANZI™ Case Study: Makoko, Nigeria",
        "category": "Water",
        "pillar_href": "pillar-water-purification.html",
    },
    {
        "file_slug": "mozambique",
        "scisan_path": "mozambique-case-study/",
        "title": "Mozambique, East Africa",
        "card_title": "SANI AMANZI™ Case Study: Mozambique, East Africa",
        "category": "Water",
        "pillar_href": "pillar-water-purification.html",
    },
    {
        "file_slug": "kzn-province",
        "scisan_path": "KZN-Province-case-study/",
        "title": "KZN Province, South Africa",
        "card_title": "SANI-99™ For AGRI Case Study: KZN Province, South Africa",
        "category": "Agriculture",
        "pillar_href": "pillar-agri-biosecurity.html",
    },
    {
        "file_slug": "transforming-poultry-production",
        "scisan_path": "transforming-poultry-production/",
        "title": "Transforming Poultry Production in South Africa",
        "card_title": "CuGROW-99™ & SANI-99 for AGRI™ Case Study: Transforming Poultry Production",
        "category": "Agriculture",
        "pillar_href": "pillar-agri-biosecurity.html",
    },
    {
        "file_slug": "safeguarding-heritage",
        "scisan_path": "safeguarding-heritage/",
        "title": "Safeguarding Heritage: Shakespeare's Globe Workshop",
        "card_title": "Safeguarding Heritage: How SANI-99™ Protected Shakespeare's Globe Workshop from Black Mould",
        "category": "Hygiene",
        "pillar_href": "pillar-hygiene-sanitation.html",
    },
    {
        "file_slug": "north-west-ambulance-service",
        "scisan_path": "north-west-ambulance-service-nwas/",
        "title": "North West Ambulance Service",
        "card_title": "North West Ambulance Service Enhances Hygiene with SANI-99™ Wipes",
        "category": "Hygiene",
        "pillar_href": "pillar-hygiene-sanitation.html",
    },
]

SCI_SAN_BASE = "https://www.scisan.co.za/"


def scisan_url(path: str) -> str:
    return SCI_SAN_BASE + path.lstrip("/")


def local_page(slug: str) -> str:
    return f"case-study-{slug}.html"


def content_file(slug: str) -> str:
    if slug == "index":
        return "scisan-case-studies-content.html"
    return f"scisan-case-study-{slug}-content.html"


def link_map() -> dict[str, str]:
    mapping = {INDEX_URL: "case-studies.html", scisan_url("case-studies/"): "case-studies.html"}
    for study in CASE_STUDIES:
        for variant in (
            scisan_url(study["scisan_path"]),
            scisan_url(study["scisan_path"].rstrip("/")),
            scisan_url(study["scisan_path"].lower()),
        ):
            mapping[variant] = local_page(study["file_slug"])
    return mapping


def fetch(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "UbuntuLifeResources/1.0 (case-study-import)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def rewrite_links(text: str) -> str:
    for source, target in sorted(link_map().items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(f'href="{source}"', f'href="{target}"')
        text = text.replace(f"href='{source}'", f"href='{target}'")
    text = re.sub(
        r'href="https://www\.scisan\.co\.za/contact-us/?"',
        'href="contact.html"',
        text,
        flags=re.I,
    )
    return tag_parent_navigation(text)


def tag_parent_navigation(text: str) -> str:
  def fix_anchor(match: re.Match[str]) -> str:
      tag = match.group(0)
      href_match = re.search(r'href=(["\'])(.*?)\1', tag, flags=re.I)
      if not href_match:
          return tag
      href = href_match.group(2)
      if href.startswith(("#", "mailto:", "tel:", "javascript:")):
          return tag
      if re.match(r"^https?://", href, flags=re.I):
          if "ubuntuliferesources.co.za" not in href.lower():
              return tag
      elif ".html" not in href:
          return tag
      if re.search(r'\btarget=', tag, flags=re.I):
          return re.sub(r'\btarget=(["\'])[^"\']*\1', 'target="_parent"', tag, flags=re.I)
      return tag[:-1] + ' target="_parent">'

  return re.sub(r"<a\b[^>]*>", fix_anchor, text, flags=re.I)


def extract_head_assets(page_html: str) -> str:
    styles: list[str] = []
    for match in re.finditer(
        r'<link[^>]+rel=["\']stylesheet["\'][^>]*>',
        page_html,
        flags=re.I,
    ):
        tag = match.group(0)
        if "scisan.co.za" in tag:
            styles.append(tag)
    for match in re.finditer(r"<style[^>]*>.*?</style>", page_html, flags=re.I | re.S):
        block = match.group(0)
        if "ulr-scisan-embed-fixes" in block:
            continue
        if "e-lazyloaded" in block and "background-image: none" in block:
            continue
        styles.append(block)
    return "\n".join(styles)


def clean_embed_body(body: str) -> str:
    body = re.sub(r"\s*</article>\s*", "\n", body, flags=re.I)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return mark_elementor_lazyloaded(body.strip())


def mark_elementor_lazyloaded(body: str) -> str:
    def add_lazyloaded(match: re.Match[str]) -> str:
        tag = match.group(0)
        if "e-lazyloaded" in tag:
            return tag
        return re.sub(
            r'\bclass="',
            'class="e-lazyloaded ',
            tag,
            count=1,
            flags=re.I,
        )

    return re.sub(
        r'<div\b[^>]*\bclass="[^"]*\be-con[^"]*\be-parent[^"]*"[^>]*>',
        add_lazyloaded,
        body,
        flags=re.I,
    )


def extract_elementor_html(page_html: str) -> str:
    match = re.search(
        r'(<div[^>]+data-elementor-type="wp-page"[^>]*>.*?</div>\s*)(?=<script|<div class="wd-prefooter|<footer|\Z)',
        page_html,
        flags=re.I | re.S,
    )
    if not match:
        raise ValueError("Could not find Elementor page content")
    return match.group(1).strip()


def build_content_document(page_html: str, aria_label: str) -> str:
    head_assets = extract_head_assets(page_html)
    body = rewrite_links(clean_embed_body(extract_elementor_html(page_html)))
    title_match = re.search(r"<title>([^<]+)</title>", page_html, flags=re.I)
    title = html.escape(title_match.group(1).strip() if title_match else aria_label)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
{head_assets}
{EMBED_FIXES}
</head>
<body>
  <main class="ulr-scisan-source-page" aria-label="{html.escape(aria_label, quote=True)}">
{body}
  </main>
</body>
</html>
"""


def import_content_files() -> None:
    print("Fetching case studies index…")
    index_html = fetch(INDEX_URL)
    (ROOT / content_file("index")).write_text(
        build_content_document(index_html, "SciSan case studies listing"),
        encoding="utf-8",
    )

    for study in CASE_STUDIES:
        url = scisan_url(study["scisan_path"])
        print(f"Fetching {url}")
        page_html = fetch(url)
        out = ROOT / content_file(study["file_slug"])
        out.write_text(
            build_content_document(page_html, study["title"]),
            encoding="utf-8",
        )


def shell_parts() -> tuple[str, str]:
    text = SHELL.read_text(encoding="utf-8")
    main_start = text.index('      <main id="primary" class="site-main">')
    footer_start = text.index("      <!-- start: Footer Section -->")
    head = text[:main_start]
    tail = text[footer_start:]

    if "ulr-scisan-embed.css" not in head:
        head = head.replace(
            '  <link rel="stylesheet" href="assets/css/ulr-phase-gate.css">',
            '  <link rel="stylesheet" href="assets/css/ulr-phase-gate.css">\n'
            '  <link rel="stylesheet" href="assets/css/ulr-scisan-embed-shell.css">\n'
            '  <link rel="stylesheet" href="assets/css/ulr-scisan-embed.css">',
        )

    head = head.replace(
        'body class="ulr-rich-subpage"',
        'body class="ulr-rich-subpage ulr-scisan-embed-page"',
    )
    return head, tail


def embed_main(title: str, src: str, frame_id: str) -> str:
    return f"""      <main id="primary" class="site-main">
        <div class="space-for-header"></div>
        <section class="ulr-scisan-exact-page" aria-labelledby="{frame_id}-title">
          <h1 id="{frame_id}-title" class="visually-hidden">{html.escape(title)}</h1>
          <iframe id="{frame_id}" class="ulr-scisan-exact-page__frame" src="{src}" title="{html.escape(title)} SciSan content" loading="eager" scrolling="no"></iframe>
        </section>
      </main>
"""


def ensure_embed_script(tail: str) -> str:
    script = '  <script src="assets/js/ulr-scisan-embed.js" defer></script>'
    if "ulr-scisan-embed.js" not in tail:
        tail = tail.replace("</body>", f"{script}\n</body>", 1)
    return tail


def inject_header_nav(head: str, current_page: str | None = None) -> str:
    if 'href="case-studies.html">Case studies</a></li>' in head:
        if current_page == "case-studies.html":
            head = head.replace(
                '<li><a href="case-studies.html">Case studies</a></li>',
                '<li class="current-menu-item"><a href="case-studies.html">Case studies</a></li>',
                2,
            )
        return head

    if current_page == "case-studies.html":
        case_item = '                  <li class="current-menu-item"><a href="case-studies.html">Case studies</a></li>\n'
    else:
        case_item = '                  <li><a href="case-studies.html">Case studies</a></li>\n'

    preparedness_marker = '                  <li><a href="pillar-preparedness.html">Preparedness</a></li>\n'
    if preparedness_marker in head:
        return head.replace(preparedness_marker, preparedness_marker + case_item, 2)

    hygiene_marker = '                  <li><a href="pillar-hygiene-sanitation.html">Hygiene</a></li>\n'
    fallback_marker = '                  <li><a href="products.html#hygiene-sanitation">Hygiene</a></li>\n'
    preparedness_item = '                  <li><a href="pillar-preparedness.html">Preparedness</a></li>\n'
    block = hygiene_marker + preparedness_item + case_item
    fallback_block = fallback_marker + preparedness_item + case_item

    if hygiene_marker in head:
        return head.replace(hygiene_marker, block, 2)
    if fallback_marker in head:
        return head.replace(fallback_marker, fallback_block, 2)
    return head


def write_shell_page(
    path: Path,
    *,
    page_title: str,
    meta_description: str,
    visible_title: str,
    iframe_src: str,
    frame_id: str,
    current_href: str | None = None,
) -> None:
    head, tail = shell_parts()
    head = head.replace(
        "<title>Company profile | Ubuntu Life Resources</title>",
        f"<title>{page_title}</title>",
    )
    head = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{html.escape(meta_description, quote=True)}">',
        head,
        count=1,
    )
    head = inject_header_nav(head, current_href)

    main = embed_main(visible_title, iframe_src, frame_id)
    tail = ensure_embed_script(tail)
    path.write_text(head + main + "\n" + tail, encoding="utf-8")


def generate_shell_pages() -> None:
    write_shell_page(
        ROOT / "case-studies.html",
        page_title="Case studies | Ubuntu Life Resources",
        meta_description="Real-world SANI-99, SANI AMANZI, and CuGROW-99 case studies across agriculture, water, and hygiene programmes.",
        visible_title="Case studies",
        iframe_src=content_file("index"),
        frame_id="ulr-scisan-case-studies-frame",
        current_href="case-studies.html",
    )

    for study in CASE_STUDIES:
        slug = study["file_slug"]
        write_shell_page(
            ROOT / local_page(slug),
            page_title=f"{study['title']} | Case study | Ubuntu Life Resources",
            meta_description=f"{study['card_title']} — case study from Ubuntu Life Resources.",
            visible_title=study["title"],
            iframe_src=content_file(slug),
            frame_id=f"ulr-scisan-case-study-{slug.replace('-', '_')}",
        )


def patch_footer_nav() -> None:
    footer_link = '<li><a href="case-studies.html">Case studies</a></li>'
    skip = {"pillar-hygiene-sanitation.html", "pillar-preparedness.html"}
    for path in ROOT.glob("*.html"):
        if path.name.startswith("scisan-") or path.name in skip:
            continue
        text = path.read_text(encoding="utf-8")
        if footer_link in text:
            continue
        marker = '<li><a href="blog.html">Insights</a></li>'
        if marker not in text:
            marker = '<li><a href="about.html">Company profile</a></li>'
        if marker not in text:
            continue
        updated = text.replace(marker, marker + "\n                    " + footer_link, 1)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"Patched footer nav in {path.name}")


def patch_header_nav() -> None:
    skip = {"pillar-hygiene-sanitation.html", "pillar-preparedness.html"}
    for path in ROOT.glob("*.html"):
        if path.name.startswith("scisan-") or path.name in skip:
            continue
        text = path.read_text(encoding="utf-8")
        if 'href="case-studies.html">Case studies</a></li>' in text:
            continue
        updated = inject_header_nav(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"Patched header nav in {path.name}")


def main() -> None:
    import_content_files()
    generate_shell_pages()
    patch_footer_nav()
    patch_header_nav()
    print("Done.")


if __name__ == "__main__":
    main()
