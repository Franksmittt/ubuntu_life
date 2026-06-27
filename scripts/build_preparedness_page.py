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
        "banner": "Banner — environmental hygiene & infection-control readiness",
    },
    "water": {
        "id": "water-security",
        "nav": "Water security",
        "eyebrow": "Brief 2",
        "heroes": (
            "assets/images/pillars/preparedness/water/hero1.jpeg",
            "assets/images/pillars/preparedness/water/hero2.jpeg",
        ),
        "hero_alt": "Water security and humanitarian response preparedness",
    },
    "nutrition": {
        "id": "nutrition-reserves",
        "nav": "Protein food reserves",
        "eyebrow": "Brief 3",
        "banner": "Banner — strategic protein food reserves",
    },
}

NAV_ITEM = '<li><a href="pillar-preparedness.html">Preparedness</a></li>'
NAV_AFTER = '<li><a href="pillar-hygiene-sanitation.html">Hygiene</a></li>'
NAV_CURRENT = (
    '<li class="current-menu-item"><a href="pillar-preparedness.html">Preparedness</a></li>'
)

HYGIENE_HERO_REL = "assets/images/pillars/preparedness/water/hero1.jpeg"
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


def is_meta_paragraph(html: str) -> bool:
    text = re.sub(r"<[^>]+>", "", html).strip()
    if text in {"Ubuntu Life Resources", "Ubuntu\u00a0Life\u00a0Resources"}:
        return True
    if text.startswith("Registration Number:"):
        return True
    if text.startswith("Prepared by"):
        return True
    return False


def ensure_hygiene_hero_image() -> str:
    return HYGIENE_HERO_REL


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


def parse_docx_blocks(path: Path) -> tuple[str, str, list[dict]]:
    from docx import Document

    doc = Document(str(path))
    title = ""
    subtitle = ""
    blocks: list[dict] = []
    pending_list: list[str] = []
    pending_checks = False

    def flush_list() -> None:
        nonlocal pending_list, pending_checks
        if not pending_list:
            return
        blocks.append(
            {
                "type": "ul",
                "items": pending_list[:],
                "checks": pending_checks,
            }
        )
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

        if bold and len(text) < 120 and "\n" not in text:
            blocks.append({"type": "h3", "text": text})
        else:
            blocks.append({"type": "p", "html": render_paragraph(text, bold)})

    flush_list()

    if not title:
        title = path.stem

    return title, subtitle, blocks


def render_list(items: list[str], checks: bool = False, cols: bool = False) -> str:
    cls = "desc ulr-preparedness-list"
    if checks:
        cls += " ulr-preparedness-list--checks"
    if cols and len(items) >= 6:
        cls += " ulr-preparedness-list--cols"
    lis = "".join(f"<li>{linkify(item)}</li>" for item in items)
    return f'<ul class="{cls}">{lis}</ul>'


def collect_until(blocks: list[dict], start: int, stop_types: set[str]) -> tuple[list[dict], int]:
    chunk: list[dict] = []
    i = start
    while i < len(blocks) and blocks[i]["type"] not in stop_types:
        chunk.append(blocks[i])
        i += 1
    return chunk, i


def collect_h3_pairs_until(
    blocks: list[dict], start: int, stop_titles: set[str]
) -> tuple[list[tuple[str, str]], int]:
    pairs: list[tuple[str, str]] = []
    i = start
    while i < len(blocks) - 1:
        if blocks[i]["type"] == "h3" and blocks[i]["text"] in stop_titles:
            break
        if blocks[i]["type"] == "h3" and blocks[i + 1]["type"] == "p":
            pairs.append((blocks[i]["text"], blocks[i + 1]["html"]))
            i += 2
        else:
            break
    return pairs, i


def split_contact_chunk(chunk: list[dict]) -> tuple[list[dict], list[dict]]:
    band: list[dict] = []
    contact: list[dict] = []
    found = False
    for block in chunk:
        if not found and block["type"] == "p" and "Contact Us" in block["html"]:
            found = True
            continue
        if found:
            contact.append(block)
        else:
            band.append(block)
    return band, contact


def collect_card_pairs(blocks: list[dict], start: int) -> tuple[list[tuple[str, str]], int]:
    stop_titles = (
        BAND_HEADINGS
        | CONTACT_HEADINGS
        | TIER_PARENTS
        | SPLIT_HEADINGS
        | STAKEHOLDER_HEADINGS
        | {"Vision", "Tuna", "Sardines", "Pilchards", "Why Tonno Bonno", "Products include:"}
    )
    pairs: list[tuple[str, str]] = []
    i = start
    while i < len(blocks) - 1:
        if blocks[i]["type"] == "h3" and blocks[i]["text"] in stop_titles:
            break
        if blocks[i]["type"] == "h3" and blocks[i + 1]["type"] == "p":
            pairs.append((blocks[i]["text"], blocks[i + 1]["html"]))
            i += 2
        else:
            break
    return pairs, i


def is_tier_heading(text: str) -> bool:
    return text in {
        "High-Risk Population Centres & International Gateways",
        "High-Risk Countries",
        "Medium-Risk Regions",
        "Medium-Risk Countries",
        "Lower-Risk Countries",
        "Districts, Municipalities & Institutional Facilities",
    }


def render_card_grid(title: str, pairs: list[tuple[str, str]], triple: bool = False) -> str:
    grid_cls = "ulr-preparedness-card-grid"
    if triple or len(pairs) == 3:
        grid_cls += " ulr-preparedness-card-grid--triple"
    cards = "".join(
        f'<article class="ulr-preparedness-mini-card"><h4>{linkify(h)}</h4>{body}</article>'
        for h, body in pairs
    )
    return (
        f'<div class="ulr-preparedness-block">'
        f'<div class="ulr-preparedness-block__title"><h3 class="h5 sec-title">{linkify(title)}</h3></div>'
        f'<div class="{grid_cls}">{cards}</div></div>'
    )


def render_split_section(title: str, chunk: list[dict]) -> str:
    prose: list[str] = []
    lists: list[dict] = []
    tail: list[str] = []
    seen_list = False

    for block in chunk:
        if block["type"] == "p":
            if not seen_list:
                prose.append(block["html"])
            else:
                tail.append(block["html"])
        elif block["type"] == "ul":
            if not seen_list:
                seen_list = True
            else:
                tail.append(render_list(block["items"], cols=True))
            lists.append(block)
        elif block["type"] == "figure":
            prose.insert(
                0,
                f'<figure class="ulr-preparedness-figure m-0">'
                f'<img src="{block["src"]}" alt="" class="w-100" loading="lazy" decoding="async"></figure>',
            )

    list_html = ""
    if lists:
        list_html = (
            f'<div class="ulr-preparedness-panel ulr-preparedness-panel--on-tint">'
            f"{render_list(lists[0]['items'], cols=len(lists[0]['items']) >= 6)}</div>"
        )

    prose_col = "".join(prose)
    tail_html = "".join(tail)
    tail_block = (
        f'<div class="ulr-preparedness-prose mt-4">{tail_html}</div>' if tail_html else ""
    )
    if list_html:
        body = (
            f'<div class="row g-4 g-lg-5 align-items-start ulr-preparedness-split">'
            f'<div class="col-lg-7"><div class="ulr-preparedness-prose">{prose_col}</div></div>'
            f'<div class="col-lg-5">{list_html}</div></div>'
            f"{tail_block}"
        )
    else:
        body = f'<div class="ulr-preparedness-prose">{prose_col}{tail_html}</div>'

    return (
        f'<div class="ulr-preparedness-block">'
        f'<div class="ulr-preparedness-block__title"><h3 class="h5 sec-title">{linkify(title)}</h3></div>'
        f"{body}</div>"
    )


def render_water_capacity(title: str, chunk: list[dict]) -> str:
    stats = [
        ("1 Million Sachets", "20 Million Litres Safe Drinking Water"),
        ("5 Million Sachets", "100 Million Litres Safe Drinking Water"),
        ("10 Million Sachets", "200 Million Litres Safe Drinking Water"),
    ]
    cards = "".join(
        f'<div class="ulr-preparedness-stat-card">'
        f'<span class="ulr-preparedness-stat-card__value">{linkify(label)}</span>'
        f'<span class="ulr-preparedness-stat-card__label">{linkify(cap)}</span></div>'
        for label, cap in stats
    )
    return (
        f'<div class="ulr-preparedness-block">'
        f'<div class="ulr-preparedness-block__title"><h3 class="h5 sec-title">{linkify(title)}</h3></div>'
        f'<p class="desc"><strong>1 Sachet = 20 Litres Safe Drinking Water</strong></p>'
        f'<div class="ulr-preparedness-stat-grid mt-3">{cards}</div></div>'
    )


def render_tier_group(title: str, blocks: list[dict], start: int) -> tuple[str, int]:
    i = start
    intro_parts: list[str] = []

    while i < len(blocks) and not (
        blocks[i]["type"] == "h3" and is_tier_heading(blocks[i]["text"])
    ):
        if blocks[i]["type"] == "p":
            intro_parts.append(blocks[i]["html"])
        elif blocks[i]["type"] == "ul":
            intro_parts.append(render_list(blocks[i]["items"], cols=True))
        elif blocks[i]["type"] == "h3":
            break
        i += 1

    cards: list[str] = []
    while i < len(blocks) and blocks[i]["type"] == "h3" and is_tier_heading(blocks[i]["text"]):
        tier = blocks[i]["text"]
        i += 1
        parts: list[str] = []
        while i < len(blocks) and blocks[i]["type"] != "h3":
            if blocks[i]["type"] == "p":
                parts.append(blocks[i]["html"])
            elif blocks[i]["type"] == "ul":
                parts.append(render_list(blocks[i]["items"], cols=True))
            i += 1
        cards.append(
            f'<article class="ulr-preparedness-mini-card">'
            f'<h4>{linkify(tier)}</h4>{"".join(parts)}</article>'
        )

    tail_parts: list[str] = []
    while i < len(blocks) and blocks[i]["type"] != "h3":
        if blocks[i]["type"] == "p":
            tail_parts.append(blocks[i]["html"])
        elif blocks[i]["type"] == "ul":
            tail_parts.append(render_list(blocks[i]["items"], cols=True))
        i += 1

    if not cards:
        chunk, i = collect_until(blocks, start, {"h3"})
        return render_default_block(title, chunk), i

    grid_cls = "ulr-preparedness-card-grid"
    if len(cards) == 3:
        grid_cls += " ulr-preparedness-card-grid--triple"
    intro_html = (
        f'<div class="ulr-preparedness-prose mb-4">{"".join(intro_parts)}</div>'
        if intro_parts
        else ""
    )
    tail_html = (
        f'<div class="ulr-preparedness-prose mt-4">{"".join(tail_parts)}</div>'
        if tail_parts
        else ""
    )
    html = (
        f'<div class="ulr-preparedness-block">'
        f'<div class="ulr-preparedness-block__title"><h3 class="h5 sec-title">{linkify(title)}</h3></div>'
        f"{intro_html}"
        f'<div class="{grid_cls}">{"".join(cards)}</div>'
        f"{tail_html}</div>"
    )
    return html, i


def render_product_block(blocks: list[dict], start: int) -> tuple[str, int]:
    i = start
    if i >= len(blocks) or blocks[i]["type"] != "h3":
        return "", start

    product_title = blocks[i]["text"]
    i += 1
    chunk, i = collect_until(blocks, i, {"h3"})
    prose: list[str] = []
    checks: list[str] = []
    for block in chunk:
        if block["type"] == "p":
            prose.append(block["html"])
        elif block["type"] == "ul" and block.get("checks"):
            checks.extend(block["items"])
        elif block["type"] == "ul":
            prose.append(render_list(block["items"]))

    check_html = ""
    if checks:
        half = (len(checks) + 1) // 2
        check_html = (
            f'<div class="ulr-preparedness-check-grid mt-3">'
            f"{render_list(checks[:half], checks=True)}"
            f"{render_list(checks[half:], checks=True)}</div>"
        )

    html = (
        f'<div class="ulr-preparedness-panel">'
        f'<h4 class="h5 sec-title mb-3">{linkify(product_title)}</h4>'
        f'{"".join(prose)}{check_html}</div>'
    )
    return html, i


def render_stakeholder_block(title: str, chunk: list[dict]) -> str:
    body_parts: list[str] = []
    for block in chunk:
        if block["type"] == "p":
            body_parts.append(block["html"])
        elif block["type"] == "ul":
            body_parts.append(render_list(block["items"], cols=True))
    return (
        f'<div class="ulr-preparedness-block">'
        f'<div class="ulr-preparedness-panel">'
        f'<div class="ulr-preparedness-block__title"><h3 class="h5 sec-title">{linkify(title)}</h3></div>'
        f'{"".join(body_parts)}</div></div>'
    )


def render_band(title: str, chunk: list[dict]) -> str:
    body = "".join(
        b["html"] if b["type"] == "p" else render_list(b["items"])
        for b in chunk
        if b["type"] in {"p", "ul"}
    )
    return (
        f'<div class="ulr-preparedness-block">'
        f'<div class="ulr-preparedness-band">'
        f'<h3 class="h5 sec-title mb-3">{linkify(title)}</h3>{body}</div></div>'
    )


def render_contact(title: str, chunk: list[dict]) -> str:
    body = "".join(b["html"] for b in chunk if b["type"] == "p")
    return (
        f'<div class="ulr-preparedness-block">'
        f'<div class="ulr-preparedness-contact">'
        f'<h3 class="h5 sec-title mb-3">{linkify(title)}</h3>{body}</div></div>'
    )


def render_default_block(title: str, chunk: list[dict]) -> str:
    parts: list[str] = []
    for block in chunk:
        if block["type"] == "p":
            parts.append(block["html"])
        elif block["type"] == "ul":
            parts.append(render_list(block["items"], block.get("checks", False), cols=True))
        elif block["type"] == "figure":
            parts.append(
                f'<figure class="ulr-preparedness-figure m-0 mb-3">'
                f'<img src="{block["src"]}" alt="" class="w-100" loading="lazy" decoding="async"></figure>'
            )
    return (
        f'<div class="ulr-preparedness-block">'
        f'<div class="ulr-preparedness-block__title"><h3 class="h5 sec-title">{linkify(title)}</h3></div>'
        f'<div class="ulr-preparedness-prose">{"".join(parts)}</div></div>'
    )


def render_intro(
    blocks: list[dict], start: int, *, hygiene_hero: str | None = None
) -> tuple[str, int]:
    chunk, end = collect_until(blocks, start, {"h3"})
    if not chunk:
        return "", start

    paras = [b["html"] for b in chunk if b["type"] == "p"]
    if hygiene_hero:
        body_paras = [p for p in paras if not is_meta_paragraph(p)]
        hero_html = (
            f'<figure class="ulr-preparedness-figure ulr-preparedness-hero m-0 mb-4 mb-lg-5">'
            f'<img src="{hygiene_hero}" alt="Environmental hygiene and infection-control readiness" '
            f'class="w-100" loading="eager" decoding="async"></figure>'
        )
        html = (
            f"{hero_html}"
            f'<div class="ulr-preparedness-prose">{"".join(body_paras)}</div>'
        )
    else:
        html = f'<div class="ulr-preparedness-prose">{"".join(paras)}</div>'

    return f'<div class="ulr-preparedness-block">{html}</div>', end


CARD_GRID_PARENTS = {
    "Areas of Support",
    "Strategic Applications",
    "Benefits",
}

SPLIT_HEADINGS = {
    "Why Preparedness Matters",
    "The Challenge",
    "Why Strategic Food Reserves Matter",
}

TIER_PARENTS = {
    "Continental Preparedness Model",
    "Scalable Preparedness Model",
}

STAKEHOLDER_HEADINGS = {
    "Potential Stakeholders",
    "Distribution Pathways",
    "Transport Efficiency",
    "Public Health Relevance",
    "What This Means",
    "Africa Planning Assumption",
}

BAND_HEADINGS = {"Vision", "Let's Strengthen Preparedness Together"}

CONTACT_HEADINGS = {"Contact Us", "Contact Ubuntu Life Resources"}

PRODUCT_CATALOG_HEADINGS = {"Tuna", "Sardines", "Pilchards"}


def render_product_catalog(blocks: list[dict], start: int) -> tuple[str, int]:
    cards: list[str] = []
    i = start
    while i < len(blocks) and blocks[i]["type"] == "h3" and blocks[i]["text"] in PRODUCT_CATALOG_HEADINGS:
        name = blocks[i]["text"]
        i += 1
        parts: list[str] = []
        while i < len(blocks) and blocks[i]["type"] != "h3":
            if blocks[i]["type"] == "p":
                parts.append(blocks[i]["html"])
            elif blocks[i]["type"] == "ul":
                parts.append(render_list(blocks[i]["items"]))
            i += 1
        cards.append(
            f'<article class="ulr-preparedness-mini-card">'
            f'<h4>{linkify(name)}</h4>{"".join(parts)}</article>'
        )
    html = (
        f'<div class="ulr-preparedness-card-grid ulr-preparedness-card-grid--triple">'
        f'{"".join(cards)}</div>'
    )
    return html, i


def render_why_tonno_block(title: str, blocks: list[dict], start: int) -> tuple[str, int]:
    chunk, i = collect_until(blocks, start, {"h3"})
    lead = "".join(
        b["html"] if b["type"] == "p" else render_list(b["items"], cols=True)
        for b in chunk
        if b["type"] in {"p", "ul"}
    )
    catalog_html, i = render_product_catalog(blocks, i)
    html = (
        f'<div class="ulr-preparedness-block">'
        f'<div class="ulr-preparedness-block__title"><h3 class="h5 sec-title">{linkify(title)}</h3></div>'
        f'<div class="ulr-preparedness-prose mb-4">{lead}</div>{catalog_html}</div>'
    )
    return html, i


def layout_blocks(blocks: list[dict], *, hygiene_hero: str | None = None) -> str:
    parts: list[str] = []
    i = 0

    intro_html, i = render_intro(blocks, i, hygiene_hero=hygiene_hero)
    if intro_html:
        parts.append(intro_html)

    while i < len(blocks):
        block = blocks[i]
        if block["type"] != "h3":
            i += 1
            continue

        title = block["text"]
        i += 1

        if title in CARD_GRID_PARENTS:
            if title == "Benefits":
                pairs, i = collect_h3_pairs_until(blocks, i, BAND_HEADINGS | CONTACT_HEADINGS)
            else:
                pairs, i = collect_card_pairs(blocks, i)
            parts.append(render_card_grid(title, pairs))
            continue

        if title in TIER_PARENTS:
            html, i = render_tier_group(title, blocks, i)
            parts.append(html)
            continue

        if title == "Environmental Hygiene Solutions":
            product_html, i = render_product_block(blocks, i)
            parts.append(
                f'<div class="ulr-preparedness-block">'
                f'<div class="ulr-preparedness-block__title"><h3 class="h5 sec-title">{linkify(title)}</h3></div>'
                f"{product_html}</div>"
            )
            continue

        if title == "Sani Amanzi Emergency Water Capacity":
            chunk, i = collect_until(blocks, i, {"h3"})
            parts.append(render_water_capacity(title, chunk))
            continue

        if title in CONTACT_HEADINGS:
            chunk, i = collect_until(blocks, i, {"h3"})
            parts.append(render_contact(title, chunk))
            continue

        if title in BAND_HEADINGS:
            chunk, i = collect_until(blocks, i, {"h3"})
            if title == "Let's Strengthen Preparedness Together":
                band_chunk, contact_chunk = split_contact_chunk(chunk)
                parts.append(render_band(title, band_chunk))
                if contact_chunk:
                    parts.append(render_contact("Contact Us", contact_chunk))
            else:
                parts.append(render_band(title, chunk))
            continue

        if title in SPLIT_HEADINGS:
            chunk, i = collect_until(blocks, i, {"h3"})
            parts.append(render_split_section(title, chunk))
            continue

        if title in STAKEHOLDER_HEADINGS or title.startswith("Stakeholder"):
            chunk, i = collect_until(blocks, i, {"h3"})
            parts.append(render_stakeholder_block(title, chunk))
            continue

        if title == "Why Tonno Bonno":
            html, i = render_why_tonno_block(title, blocks, i)
            parts.append(html)
            continue

        chunk, i = collect_until(blocks, i, {"h3"})
        parts.append(render_default_block(title, chunk))

    return "".join(parts)


def docx_body_html(path: Path) -> tuple[str, str, str]:
    title, subtitle, blocks = parse_docx_blocks(path)
    hero = ensure_hygiene_hero_image() if path == DOCX_FILES["hygiene"] else None
    return title, subtitle, layout_blocks(blocks, hygiene_hero=hero)


def render_placeholder(label: str, variant: str = "") -> str:
    cls = "ulr-preparedness-placeholder"
    if variant:
        cls += f" ulr-preparedness-placeholder--{variant}"
    safe = esc(label)
    return (
        f'<figure class="{cls}" role="img" aria-label="Image placeholder: {safe}">'
        f'<span class="ulr-preparedness-placeholder__label">{safe}</span></figure>'
    )


def render_section_heroes(images: tuple[str, ...], alt: str) -> str:
    parts: list[str] = []
    for i, src in enumerate(images):
        margin = "mb-4 mb-lg-5" if i == len(images) - 1 else "mb-3 mb-lg-4"
        loading = "eager" if i == 0 else "lazy"
        parts.append(
            f'<figure class="ulr-preparedness-figure ulr-preparedness-hero m-0 {margin}">'
            f'<img src="{src}" alt="{esc(alt)}" class="w-100" loading="{loading}" '
            f'decoding="async"></figure>'
        )
    return "".join(parts)


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

    header_html = (
        f'<div class="ulr-preparedness-section__header">'
        f'<span class="ulr-preparedness-section__eyebrow">{meta["eyebrow"]}</span>'
        f'<h2 class="sec-title h3 mb-2" id="{meta["id"]}">{linkify(title)}</h2>'
        f"{subtitle_html}</div>"
    )

    heroes = meta.get("heroes")
    if heroes:
        banner_html = render_section_heroes(heroes, meta.get("hero_alt", meta["eyebrow"]))
    elif meta.get("banner"):
        banner_html = (
            f'<div class="mb-4 mb-lg-5">{render_placeholder(meta["banner"], "banner")}</div>'
        )
    else:
        banner_html = ""

    inner = (
        f"{banner_html}"
        f"{header_html}"
        f'<div class="ulr-preparedness-layout ulr-brief-copy">{body}</div>'
    )

    return f"""        <section class="{cls}" aria-labelledby="{meta['id']}">
          <div class="container">
            {inner}
          </div>
        </section>"""


def intro_section() -> str:
    return """        <section class="section-gap ulr-brief-section bg-light">
          <div class="container">
            <div class="ulr-preparedness-intro mb-4">
              <span class="sub-title d-inline-block mb-2"><i class="tji-strategy"></i> One readiness framework</span>
              <p class="desc mb-3">Three preparedness briefs — environmental hygiene, emergency drinking water, and strategic protein food reserves — aligned for governments, institutions, humanitarian programmes, and emergency-response agencies across Africa.</p>
              <ul class="ulr-preparedness-nav" aria-label="Preparedness sections">
                <li><a href="#hygiene-readiness">Hygiene &amp; infection control</a></li>
                <li><a href="#water-security">Water security</a></li>
                <li><a href="#nutrition-reserves">Protein food reserves</a></li>
              </ul>
            </div>
            <div class="row g-4 g-lg-5 align-items-stretch">
              <div class="col-md-5 col-lg-4">
                <figure class="ulr-preparedness-placeholder ulr-preparedness-placeholder--square h-100" role="img" aria-label="Image placeholder: Hero — integrated preparedness collage"><span class="ulr-preparedness-placeholder__label">Hero — integrated preparedness collage</span></figure>
              </div>
              <div class="col-md-7 col-lg-8">
                <div class="ulr-preparedness-pillar-cards h-100">
                  <article class="ulr-preparedness-pillar-card">
                    <h3>Environmental hygiene</h3>
                    <p class="desc small mb-0">Biosecurity, IPC discipline, and disinfection reserves for healthcare, food, and agricultural settings.</p>
                  </article>
                  <article class="ulr-preparedness-pillar-card">
                    <h3>Water security</h3>
                    <p class="desc small mb-0">Point-of-use treatment stockpiles for disaster, outbreak, and humanitarian corridors.</p>
                  </article>
                  <article class="ulr-preparedness-pillar-card">
                    <h3>Nutritional resilience</h3>
                    <p class="desc small mb-0">Shelf-stable protein reserves that hold without cold chain dependency.</p>
                  </article>
                </div>
              </div>
            </div>
          </div>
        </section>"""


def engagement_band_section() -> str:
    return """        <section class="section-gap ulr-preparedness-engagement-band">
          <div class="container">
            <div class="row g-4 g-lg-5 align-items-center">
              <div class="col-lg-6">
                <h2 class="sec-title">Integrated <span>readiness</span> engagement</h2>
                <p class="desc">Ubuntu Life Resources helps programme sponsors translate preparedness briefs into supplier-aligned plans — reserve levels, documentation, training collateral, and phased roll-out that respects procurement reality.</p>
                <ul class="desc ulr-preparedness-list mb-0">
                  <li>Multi-pillar baskets spanning hygiene, water, and nutrition where programmes overlap</li>
                  <li>Evidence and product truth aligned to supplier documentation and lab reports</li>
                  <li>Single accountable commercial interface: <strong>Sanchia-Lynn Smit</strong>, CEO / Founder</li>
                </ul>
              </div>
              <div class="col-lg-6">
                <figure class="ulr-preparedness-placeholder ulr-preparedness-placeholder--side" role="img" aria-label="Image placeholder: Integrated readiness — programme planning / stakeholder briefing"><span class="ulr-preparedness-placeholder__label">Integrated readiness — programme planning / stakeholder briefing</span></figure>
              </div>
            </div>
          </div>
        </section>"""


def cta_section() -> str:
    return """        <section class="tj-cta-section section-gap-x">
          <div class="container">
            <div class="row">
              <div class="col-12">
                <div class="cta-area">
                  <div class="cta-content">
                    <h2 class="title title-anim">Plan preparedness with Ubuntu Life Resources</h2>
                    <p class="desc">Whether you are scoping hygiene reserves, water-security stockpiles, or protein food reserves — start with a structured conversation on scope, territories, and deployment timelines.</p>
                    <div class="cta-btn mt-3 d-flex flex-wrap gap-2">
                      <a class="tj-primary-btn" href="contact.html">
                        <span class="btn-text"><span>Contact us</span></span>
                        <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                      </a>
                      <a class="tj-primary-btn transparent-btn" href="pillars.html">
                        <span class="btn-text"><span>All pillars</span></span>
                        <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
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
        engagement_band_section(),
        cta_section(),
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
        r'<li><a href="pillar-preparedness\.html">Preparedness</a></li>',
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
