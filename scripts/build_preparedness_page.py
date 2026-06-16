# -*- coding: utf-8 -*-
"""Build pillar-preparedness.html from the three preparedness brief docx files."""
from __future__ import annotations

import html
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "pillar-institutional-supply.html"
OUTPUT = ROOT / "pillar-preparedness.html"
IMG_DIR = ROOT / "assets/images/pillars/preparedness"

DOCX_FILES = {
    "hygiene": ROOT / "Environmental Hygiene Biosecurity & Infection-Control Readiness.docx",
    "water": ROOT
    / "Strategic Water Security Planning for Disaster, Outbreak & Humanitarian Response Across Africa.docx",
    "nutrition": ROOT
    / "Supporting Nutritional Resilience Through Strategic Protein Food Reserves.docx",
}

SECTION_META = {
    "hygiene": {
        "id": "hygiene-readiness",
        "nav": "Hygiene &amp; infection control",
        "eyebrow": "Brief 1",
    },
    "water": {
        "id": "water-security",
        "nav": "Water security",
        "eyebrow": "Brief 2",
    },
    "nutrition": {
        "id": "nutrition-reserves",
        "nav": "Protein food reserves",
        "eyebrow": "Brief 3",
    },
}

NAV_ITEM = '<li><a href="pillar-preparedness.html">Preparedness</a></li>'
NAV_AFTER = '<li><a href="pillar-hygiene-sanitation.html">Hygiene</a></li>'
NAV_CURRENT = (
    '<li class="current-menu-item"><a href="pillar-preparedness.html">Preparedness</a></li>'
)

BULLET_RE = re.compile(r"^[\u2022\u2713\u2714•✔\-]\s*")
EMAIL_RE = re.compile(r"([\w.+-]+@[\w.-]+\.\w+)")
PHONE_RE = re.compile(r"(\+?\d[\d\s]{8,}\d)")


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def linkify(text: str) -> str:
    text = esc(text)
    text = EMAIL_RE.sub(r'<a href="mailto:\1">\1</a>', text)
    text = text.replace("📧 ", "")
    if "WhatsApp:" in text:
        text = text.replace(
            "WhatsApp: +27 79 658 8189",
            'WhatsApp: <a href="https://wa.me/27796588189">+27 79 658 8189</a>',
        )
    return text


def paragraph_bold(paragraph) -> bool:
    runs = [r for r in paragraph.runs if r.text.strip()]
    if not runs:
        return False
    return all(r.bold for r in runs)


def paragraph_has_image(paragraph) -> bool:
    for run in paragraph.runs:
        if run._element.xpath(".//a:blip"):
            return True
    return False


def extract_hygiene_cover_image() -> str | None:
    docx_path = DOCX_FILES["hygiene"]
    if not docx_path.exists():
        return None

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    out = IMG_DIR / "hygiene-readiness-cover.png"

    with zipfile.ZipFile(docx_path) as archive:
        names = [n for n in archive.namelist() if n.startswith("word/media/")]
        if not names:
            return None
        with archive.open(names[0]) as src, out.open("wb") as dst:
            shutil.copyfileobj(src, dst)

    return "assets/images/pillars/preparedness/hygiene-readiness-cover.png"


def split_bullet_block(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    items: list[str] = []
    for line in lines:
        if BULLET_RE.match(line):
            items.append(BULLET_RE.sub("", line).strip())
        elif line.startswith("✔"):
            items.append(line.lstrip("✔").strip())
        else:
            items.append(line)
    return items


def is_bullet_block(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return False
    hits = sum(1 for line in lines if BULLET_RE.match(line) or line.startswith("✔"))
    return hits >= max(1, len(lines) // 2)


def render_bullet_list(text: str, checkmarks: bool = False) -> str:
    items = split_bullet_block(text)
    tag = "ul"
    cls = "desc ulr-preparedness-list"
    if checkmarks or any("✔" in text for _ in [0]):
        cls += " ulr-preparedness-list--checks"
    lis = "".join(f"<li>{linkify(item)}</li>" for item in items)
    return f"<{tag} class=\"{cls}\">{lis}</{tag}>"


def render_paragraph(text: str, bold: bool) -> str:
    if is_bullet_block(text):
        return render_bullet_list(text)

    if bold:
        if len(text) < 90 and "\n" not in text:
            return f'<h3 class="h5 sec-title mb-3">{linkify(text)}</h3>'
        parts = [p.strip() for p in text.split("\n\n") if p.strip()]
        if len(parts) > 1:
            return "".join(
                f'<p class="desc"><strong>{linkify(part)}</strong></p>' for part in parts
            )
        return f'<p class="desc"><strong>{linkify(text)}</strong></p>'

    if "@" in text and "sanchia" in text.lower():
        return f'<p class="desc">{linkify(text)}</p>'

    parts = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    if len(parts) > 1:
        return "".join(render_paragraph(part, False) for part in parts)

    if "\n" in text and is_bullet_block(text):
        return render_bullet_list(text)

    if "\n" in text:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if all(len(line) < 80 for line in lines) and len(lines) <= 6:
            return "".join(f'<p class="desc mb-1">{linkify(line)}</p>' for line in lines)

    return f'<p class="desc">{linkify(text)}</p>'


def docx_body_html(path: Path) -> tuple[str, str, str | None]:
    from docx import Document

    doc = Document(str(path))
    cover_image: str | None = None
    chunks: list[str] = []
    title = ""
    subtitle = ""
    pending_list: list[str] = []
    pending_checks = False

    def flush_list() -> None:
        nonlocal pending_list, pending_checks
        if not pending_list:
            return
        joined = "\n".join(f"• {item}" for item in pending_list)
        chunks.append(render_bullet_list(joined, checkmarks=pending_checks))
        pending_list = []
        pending_checks = False

    def is_list_paragraph(text: str, bold: bool) -> bool:
        if bold:
            return False
        if text.startswith("✔"):
            return True
        return is_bullet_block(text)

    for paragraph in doc.paragraphs:
        if paragraph_has_image(paragraph):
            flush_list()
            if path == DOCX_FILES["hygiene"]:
                cover_image = extract_hygiene_cover_image()
                if cover_image:
                    chunks.append(
                        f'<figure class="ulr-preparedness-figure m-0 mb-4">'
                        f'<img src="{cover_image}" alt="Environmental hygiene and infection-control readiness" '
                        f'class="w-100 rounded-3 shadow-sm" loading="lazy" decoding="async"></figure>'
                    )
            continue

        text = paragraph.text.strip()
        if not text:
            flush_list()
            continue

        bold = paragraph_bold(paragraph)

        if not title and bold:
            title = text
            continue
        if not subtitle and bold and text != title:
            subtitle = text
            continue

        if is_list_paragraph(text, bold):
            if text.startswith("✔"):
                pending_checks = True
                pending_list.append(text.lstrip("✔").strip())
            else:
                pending_list.extend(split_bullet_block(text))
            continue

        flush_list()
        chunks.append(render_paragraph(text, bold))

    flush_list()

    if not title:
        title = path.stem

    return title, subtitle, "".join(chunks)


def section_html(key: str, bg: bool = False) -> str:
    path = DOCX_FILES[key]
    meta = SECTION_META[key]
    title, subtitle, body = docx_body_html(path)

    cls = "section-gap ulr-brief-section ulr-preparedness-section"
    if bg:
        cls += " bg-light"

    subtitle_html = (
        f'<p class="desc ulr-preparedness-section__subtitle"><strong>{linkify(subtitle)}</strong></p>'
        if subtitle
        else ""
    )

    return f"""        <section class="{cls}" aria-labelledby="{meta['id']}">
          <div class="container">
            <div class="ulr-preparedness-section__header mb-4">
              <span class="ulr-preparedness-section__eyebrow">{meta['eyebrow']}</span>
              <h2 class="sec-title h3 mb-2" id="{meta['id']}">{linkify(title)}</h2>
              {subtitle_html}
            </div>
            <div class="ulr-preparedness-doc-body ulr-brief-copy">
              {body}
            </div>
          </div>
        </section>"""


def intro_section() -> str:
    return """        <section class="section-gap ulr-brief-section">
          <div class="container">
            <div class="ulr-preparedness-intro mb-4">
              <span class="sub-title d-inline-block mb-2"><i class="tji-strategy"></i> One readiness framework</span>
              <p class="desc mb-3">This page reproduces the full Ubuntu Life Resources preparedness briefs for environmental hygiene, emergency drinking water, and strategic protein food reserves — aligned for governments, institutions, humanitarian programmes, and emergency-response agencies across Africa.</p>
              <ul class="ulr-preparedness-nav" aria-label="Preparedness sections">
                <li><a href="#hygiene-readiness">Hygiene &amp; infection control</a></li>
                <li><a href="#water-security">Water security</a></li>
                <li><a href="#nutrition-reserves">Protein food reserves</a></li>
              </ul>
            </div>
          </div>
        </section>"""


def related_pillars_section() -> str:
    return """        <section class="section-gap pt-0">
          <div class="container">
            <div class="sec-heading text-center mb-4">
              <h3 class="sec-title">Related <span>pillars</span></h3>
            </div>
            <div class="row g-4">
              <div class="col-md-4">
                <a class="text-decoration-none text-reset" href="pillar-hygiene-sanitation.html">
                  <div class="pillar-related-card h-100 overflow-hidden rounded-3 border">
                    <div class="ratio ratio-4x3">
                      <img src="assets/images/hero/ulr-hero-hygiene-sanitation.jpg" class="w-100 h-100" style="object-fit:cover;" alt="">
                    </div>
                    <div class="p-3">
                      <h4 class="h6 mb-0">Hygiene &amp; sanitation</h4>
                      <span class="small text-muted">SANI-99&trade; disinfection solutions</span>
                    </div>
                  </div>
                </a>
              </div>
              <div class="col-md-4">
                <a class="text-decoration-none text-reset" href="pillar-water-purification.html">
                  <div class="pillar-related-card h-100 overflow-hidden rounded-3 border">
                    <div class="ratio ratio-4x3">
                      <img src="assets/images/service/ulr-service-water-treatment-programme.jpg" class="w-100 h-100" style="object-fit:cover;" alt="">
                    </div>
                    <div class="p-3">
                      <h4 class="h6 mb-0">Water purification</h4>
                      <span class="small text-muted">SANI AMANZI&trade; programmes</span>
                    </div>
                  </div>
                </a>
              </div>
              <div class="col-md-4">
                <a class="text-decoration-none text-reset" href="pillar-shelf-stable-nutrition.html">
                  <div class="pillar-related-card h-100 overflow-hidden rounded-3 border">
                    <div class="ratio ratio-4x3">
                      <img src="assets/images/hero/ulr-hero-food-security.jpg" class="w-100 h-100" style="object-fit:cover;" alt="">
                    </div>
                    <div class="p-3">
                      <h4 class="h6 mb-0">Strategic food supply</h4>
                      <span class="small text-muted">Tonno Bonno shelf-stable protein</span>
                    </div>
                  </div>
                </a>
              </div>
            </div>
          </div>
        </section>"""


def main_content() -> str:
    parts = [
        """        <section class="tj-page-header section-gap-x" data-bg-image="assets/images/hero/ulr-hero-route-to-market-southern-africa.jpg">
          <div class="container position-relative" style="z-index:2;">
            <div class="row">
              <div class="col-lg-12">
                <div class="tj-page-header-content text-center">
                  <h1 class="tj-page-title">Preparedness</h1>
                  <p class="pillar-header-lead">Environmental hygiene, emergency drinking water, and strategic protein food reserves — full preparedness briefs for disaster, outbreak, and humanitarian response across Africa.</p>
                  <div class="tj-page-link">
                    <span><i class="tji-home"></i></span>
                    <span><a href="index.html">Home</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><a href="pillars.html">Core pillars</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><span>Preparedness</span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="page-header-overlay ulr-pheader-overlay" aria-hidden="true"></div>
        </section>""",
        intro_section(),
        section_html("hygiene", bg=True),
        section_html("water", bg=False),
        section_html("nutrition", bg=True),
        related_pillars_section(),
    ]
    return "\n".join(parts)


def build_page() -> None:
    for path in DOCX_FILES.values():
        if not path.exists():
            raise FileNotFoundError(f"Missing source document: {path}")

    text = TEMPLATE.read_text(encoding="utf-8")
    start = text.index('        <section class="tj-page-header')
    end = text.index("      </main>")
    head = text[:start]
    tail = text[end:]

    head = head.replace(
        "<title>Institutional supply | Ubuntu Life Resources</title>",
        "<title>Preparedness | Ubuntu Life Resources</title>",
    )
    head = head.replace(
        'content="Institutional supply, RFQs, and audited representation for government and large buyers from Ubuntu Life Resources."',
        'content="Full preparedness briefs: environmental hygiene, water security, and protein food reserves for disaster, outbreak, and humanitarian response across Africa."',
    )
    head = head.replace(
        '<body class="ulr-pillar-page">',
        '<body class="ulr-pillar-page ulr-preparedness-page">',
    )
    if "ulr-preparedness-page.css" not in head:
        head = head.replace(
            '  <link rel="stylesheet" href="assets/css/ulr-phase-gate.css">',
            '  <link rel="stylesheet" href="assets/css/ulr-phase-gate.css">\n'
            '  <link rel="stylesheet" href="assets/css/ulr-pillar-brief.css">\n'
            '  <link rel="stylesheet" href="assets/css/ulr-preparedness-page.css">',
        )

    head = re.sub(
        r'<li><a href="pillar-hygiene-sanitation\.html">Hygiene</a></li>',
        NAV_CURRENT,
        head,
        count=2,
    )

    OUTPUT.write_text(head + main_content() + "\n" + tail, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


def main() -> None:
    build_page()


if __name__ == "__main__":
    main()
