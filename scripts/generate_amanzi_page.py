# -*- coding: utf-8 -*-
"""Build pillar-water-purification.html in strict SANI AMANZI.Updated.docx order."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLOW = ROOT / "_docx_flow.txt"
TM = "&trade;"
OPENING = "assets/images/pillars/sani-amanzi/ulr-sani-amanzi-opening.jpg"

# Doc UI notes — not published as copy
SKIP_EXACT = {
    "TEXT",
    "I",
    "1",
    "15",
    "(empty)",
    "Brochure Button (to access Brochure) – Brochure scroll down",
    "Contact us Button: Call / Email",
    "Get Social Linked IN link",
    "Get in touch button: Form",
    "-name",
    "-surname",
    "-email",
    "-contact number",
    "- message",
    "Top of Form",
    "Bottom of Form",
    "Button - Get Social with Us:",
    "Linked In Icon",
    "Button - Get in Touch Form:",
    "Name, surname, number, email and message space",
    "”",
    "is me ans that a significant portion of the global population lacks access to clean and",
    "1According to the World Health Organization (WHO) and UNICEF, approximately 2.2 billion people worldwide do not have access to safely managed drinking water services.",
}

SKIP_PREFIX = (
    "Brochure Button",
    "Contact us Button",
    "Get in touch button",
    "Button -",
)

IMG_RE = re.compile(r"^---IMAGE:\s*media/image(\d+)\.(png|jpe?g|emf)$", re.I)

# Word “Save as HTML” uses 041–044 for the four safety icons (docx refs image38–41.emf).
SAFETY_EMF_TO_PNG = {38: 41, 39: 42, 40: 43, 41: 44}
# Final “Sustainable water purification” banner uses image045 in the HTML export (docx image18.emf).
SUSTAINABLE_BANNER = "assets/images/pillars/sani-amanzi/doc/image045.png"

# Overlay artefacts from the Word layout (not visible copy in the .docx).
SKIP_EXACT_EXTRA = {"iffe", "emicals", "xing d"}


def resolve_image(num: int, ext: str, *, next_text: str | None = None) -> str | None:
    folder = ROOT / "assets/images/pillars/sani-amanzi/doc"
    if ext.lower() == "emf":
        if next_text and next_text.strip().startswith("Sustainable water"):
            p = ROOT / SUSTAINABLE_BANNER
            if p.exists():
                return SUSTAINABLE_BANNER
        if num in SAFETY_EMF_TO_PNG:
            mapped = SAFETY_EMF_TO_PNG[num]
            name = f"image{mapped:03d}.png"
            if (folder / name).exists():
                return f"assets/images/pillars/sani-amanzi/doc/{name}"
    if ext.lower() in ("png", "jpeg", "jpg"):
        for name in (f"image{num:03d}.png", f"image{num:03d}.jpg", f"image{num:03d}.jpeg"):
            if (folder / name).exists():
                return f"assets/images/pillars/sani-amanzi/doc/{name}"
    for name in (f"image{num:03d}.png", f"image{num:03d}.jpg", f"image{num:03d}.jpeg"):
        if (folder / name).exists():
            return f"assets/images/pillars/sani-amanzi/doc/{name}"
    return None


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("™", TM)
        .replace("SANI-AMANZI™", f"SANI-AMANZI{TM}")
        .replace("SANI AMANZI™", f"SANI AMANZI{TM}")
    )


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower().replace("™", ""))
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s[:48] or "section"


def figure(src: str, alt: str = "", extra_class: str = "") -> str:
    cls = "ulr-amanzi-doc-figure"
    if extra_class:
        cls += f" {extra_class}"
    return (
        f'<figure class="{cls}">'
        f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async">'
        f"</figure>"
    )


def is_section_heading(t: str) -> bool:
    if re.match(r"^\d+\s*Trucks?$", t, re.I):
        return False
    if len(t) > 78:
        return False
    if t.endswith(".") and "?" not in t:
        return False
    if re.match(r"^\d+\.", t):
        return False
    skip_starts = (
        "More than",
        "The ",
        "In line",
        "Introducing",
        "Furthermore",
        "Developed",
        "SANI ",
        "Behind ",
        "According",
        "We ",
        "To gain",
        "Scientific",
        "Remember",
        "Use ",
        "No Mixing",
        "Avoid ",
        "Do Not",
        "No Consumption",
        "What is the",
        "Why must",
        "Will ",
        "How ",
        "Does ",
        "Is there",
        "Who is",
        "United ",
        "UNICEF",
        "Email:",
        "Contact",
        "www.",
        "Dedicated",
        "Beyond ",
        "Against ",
        "Central ",
        "Innovative ",
        "Convenient ",
        "Robust ",
        "Exceptional ",
        "Accurate ",
        "Chemical-Free",
        "Premium ",
        "Sustainability ",
        "Designed ",
        "One of ",
        "A ",
        "Additionally",
        "When ",
        "From ",
        "Given ",
        "Its ",
        "Step ",
        "Optimal ",
        "correct ",
        "proper ",
        "full ",
        "flooding",
        "infrastructure",
        "drought",
        "contamination",
        "humanitarian",
        "municipal",
        "rapid ",
        "simplified ",
        "scalable ",
        "emergency ",
        "governments",
        "NGOs",
        "disaster",
        "institutional",
        "distribution",
        "pesticides",
        "iron",
        "Addressing",
        "Antibiotic",
        "In areas",
        "In a market",
        "In a world",
        "In highly",
        "In situations",
        "In recognition",
        "With our",
        "With just",
        "World's Best",
        "Product Range",
        "Transportation",
        "for ",
        "for purifying",
        "bottled",
        "water using",
        "the imperative",
        "This means",
        "Triple Foil",
        "1 Sachet",
        "Point-of-Use",
        "Precise Dosage",
        "Affordable",
        "66 ",
        "1 ",
    )
    if any(t.startswith(s) for s in skip_starts):
        return False
    if len(t) <= 52:
        return True
    keys = (
        "classification",
        "responsible",
        "characteristics",
        "instructions",
        "purifier",
        "range",
        "apart",
        "advantages",
        "pathogens",
        "contaminants",
        "chlorine",
        "drinking water",
        "testing",
        "perform",
        "tds",
        "treatment",
        "scalable",
        "sustainable",
        "questions",
        "associations",
        "readiness",
        "partner",
        "why we do",
        "addressing",
        "shield",
        "shield",
        "disaster",
        "strategic",
        "partner with",
        "simple water",
        "important note",
        "registered",
    )
    low = t.lower()
    return any(k in low for k in keys)


def clean_doc_text(text: str) -> str:
    """Strip Word text-box overlay garbage while keeping document wording."""
    t = text.strip()
    fixes = (
        ("No Mixing with Other DisinfectantsDo not", "No Mixing with Other Disinfectants. Do not"),
        ("Avoid Contact with Eyesxing d", "Avoid Contact with Eyes"),
        ("Do Not Ingest Anhydrous Powderrent ch", "Do Not Ingest Anhydrous Powder"),
        (
            "No Consumption of Coagulants/ Precipitatecan lead",
            "No Consumption of Coagulants/ Precipitate can lead",
        ),
    )
    for old, new in fixes:
        if t.startswith(old):
            t = new + t[len(old) :]
    return t


def para(text: str, *, in_faq: bool = False) -> str:
    t = clean_doc_text(text)
    if not t or t in SKIP_EXACT or t in SKIP_EXACT_EXTRA or any(t.startswith(p) for p in SKIP_PREFIX):
        return ""
    # Title block (doc line 5)
    if "Water Sanitising" in t and "Purification Solution" in t and "SANI" in t:
        return (
            '<header class="ulr-amanzi-doc-title">'
            f'<p class="ulr-amanzi-doc-title__brand">SANI AMANZI{TM}</p>'
            '<p class="ulr-amanzi-doc-title__line">Water Sanitising</p>'
            '<p class="ulr-amanzi-doc-title__line">&amp; Purification Solution</p>'
            "</header>"
        )
    if t == "Caring for Life" or t.startswith("Caring"):
        return '<p class="ulr-amanzi-doc-tagline">Caring for Life</p>'
    if t.lower().startswith("for ") and len(t) < 40:
        return f'<p class="ulr-amanzi-doc-p">{esc(t)}</p>'
    if t == "VS":
        return '<p class="ulr-amanzi-doc-vs" aria-hidden="true">VS</p>'
    if t.startswith("“") or t.startswith('"'):
        return f'<p class="ulr-amanzi-doc-quote">{esc(t)}</p>'
    if t in ("UNICEF/ World Health Organization Report",):
        return f'<p class="ulr-amanzi-doc-quote ulr-amanzi-doc-quote--attrib">{esc(t)}</p>'
    if (
        in_faq
        and "?" in t
        and t.index("?") < 80
        and t.startswith(("What ", "Why ", "Will ", "How ", "Does ", "Is ", "Who "))
    ):
        q = esc(t)
        return f'<div class="ulr-amanzi-doc-faq-item"><p class="ulr-amanzi-doc-p ulr-amanzi-doc-faq-q">{q}</p></div>'
    if is_section_heading(t):
        sid = slugify(t)
        return (
            f'<p id="{sid}" class="ulr-amanzi-doc-heading">{esc(t)}</p>'
        )
    if re.match(r"^\d+\s*Trucks?$", t) or (
        len(t) < 42 and t[0].isdigit() and "Truck" in t
    ):
        return f'<p class="ulr-amanzi-doc-p ulr-amanzi-doc-stat">{esc(t)}</p>'
    return f'<p class="ulr-amanzi-doc-p">{esc(t)}</p>'


def parse_flow() -> list[tuple[str, str]]:
    raw = FLOW.read_text(encoding="utf-8").splitlines()
    blocks: list[tuple[str, str]] = []
    i = 0
    while i < len(raw):
        line = raw[i].strip()
        if line == "---TABLE---":
            rows = []
            i += 1
            while i < len(raw) and raw[i].strip() != "---END---":
                if raw[i].strip() and raw[i].strip() != "---END---":
                    rows.append(raw[i].strip())
                i += 1
            blocks.append(("table", "\n".join(rows)))
            i += 1
            continue
        m = IMG_RE.match(line)
        if m:
            blocks.append(("image", f"{m.group(1)}.{m.group(2)}"))
        elif line:
            blocks.append(("text", line))
        i += 1
    return blocks


def render_table(rows_text: str) -> str:
    rows = rows_text.split("\n")
    if not rows:
        return ""
    head = rows[0].split(" | ")
    body = [r.split(" | ") for r in rows[1:]]
    th = "".join(f"<th>{esc(c)}</th>" for c in head)
    trs = ""
    for row in body:
        trs += "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>"
    return (
        '<div class="ulr-amanzi-doc-table-wrap"><table class="ulr-product-table">'
        f"<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>"
    )


def brochure_actions() -> str:
    return """<div class="ulr-amanzi-doc-cta">
  <p class="ulr-amanzi-doc-cta__title">Get the brochure or speak with our team</p>
  <div class="ulr-amanzi-doc-actions">
  <button type="button" class="tj-primary-btn js-request-brochure" data-brochure-name="SANI AMANZI Brochure"><span class="btn-text"><span>Request a brochure</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></button>
  <a class="tj-primary-btn" href="contact.html"><span class="btn-text"><span>Contact us</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
  <a class="tj-primary-btn" href="tel:+27796588189"><span class="btn-text"><span>Call 079 658 8189</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
  </div>
</div>"""


def nav_filter(headings: list[tuple[str, str]]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for label, sid in headings:
        low = label.lower().strip()
        if low in {"arsenic", "fluorides", "nitrates", "iron", "pesticides", "drinking water"}:
            continue
        if low.islower() and len(label) < 22:
            continue
        out.append((label, sid))
    return out[:12]


def render_nav(headings: list[tuple[str, str]]) -> str:
    filtered = nav_filter(headings)
    if len(filtered) < 3:
        return ""
    items = "".join(
        f'<li><a href="#{sid}">{esc(label)[:42]}</a></li>'
        for label, sid in filtered
    )
    return (
        '<nav class="ulr-amanzi-doc-nav" aria-label="On this page">'
        '<span class="ulr-amanzi-doc-nav__label">On this page</span>'
        f'<ul class="ulr-amanzi-doc-nav__list">{items}</ul></nav>'
    )


def next_text_block(blocks: list[tuple[str, str]], start: int) -> str | None:
    for j in range(start + 1, len(blocks)):
        if blocks[j][0] == "text":
            return blocks[j][1]
    return None


def ensure_opening_image() -> None:
    dest = ROOT / "assets/images/pillars/sani-amanzi/ulr-sani-amanzi-opening.jpg"
    for src in (ROOT / "water.jpeg", ROOT / "cleanwater.jpg"):
        if src.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(src.read_bytes())
            return


def emit_figure(
    parts: list[str],
    src: str,
    num: int,
    *,
    hero: bool = False,
    banner: bool = False,
    figure_row: list[str] | None = None,
) -> None:
    extra = ""
    if hero:
        extra = "ulr-amanzi-doc-figure--hero"
    elif banner:
        extra = "ulr-amanzi-doc-figure--banner"
    fig = figure(src, f"Document illustration {num}.", extra)
    if figure_row is not None:
        figure_row.append(fig)
    else:
        parts.append(fig)


def flush_figure_row(parts: list[str], row: list[str]) -> None:
    if not row:
        return
    if len(row) >= 2:
        parts.append('<div class="ulr-amanzi-doc-figure-row">')
        parts.extend(row)
        parts.append("</div>")
    else:
        parts.extend(row)
    row.clear()


def build_main() -> str:
    ensure_opening_image()
    blocks = parse_flow()
    parts: list[str] = []
    nav_headings: list[tuple[str, str]] = []

    parts.append('        <section class="ulr-amanzi-doc section-gap-x">')
    parts.append('          <div class="ulr-amanzi-doc__inner">')
    parts.append('<div class="ulr-amanzi-doc-hero">')
    parts.append(
        figure(OPENING, "Hands holding clean water.", "ulr-amanzi-doc-figure--hero")
    )
    parts.append('<div class="ulr-amanzi-doc-hero__panel">')

    started = False
    skip_leading_doc_images = True
    hero_open = True
    hero_closed = False
    in_compare = False
    compare_col: list[str] = []
    in_safety = False
    in_faq = False
    in_contact = False
    figure_row: list[str] = []
    icon_grid_cells: list[dict[str, str]] = []
    icon_grid_cols = 0
    icon_grid_mode = ""  # char (with labels), instr, plain
    instr_grid_armed = False

    def close_icon_grid() -> None:
        nonlocal icon_grid_cols, icon_grid_mode
        if not icon_grid_cells:
            icon_grid_cols = 0
            icon_grid_mode = ""
            return
        parts.append(
            f'<div class="ulr-amanzi-doc-icon-grid ulr-amanzi-doc-icon-grid--{icon_grid_cols}">'
        )
        for cell in icon_grid_cells:
            parts.append('<div class="ulr-amanzi-doc-icon-grid__item">')
            parts.append(cell["figure"])
            if cell.get("caption"):
                parts.append(cell["caption"])
            parts.append("</div>")
        parts.append("</div>")
        icon_grid_cells.clear()
        icon_grid_cols = 0
        icon_grid_mode = ""

    def add_icon_grid_image(src: str, num: int, cols: int, mode: str) -> None:
        nonlocal icon_grid_cols, icon_grid_mode
        flush_figure_row(parts, figure_row)
        if icon_grid_cells and (icon_grid_cols != cols or icon_grid_mode != mode):
            close_icon_grid()
        icon_grid_cols = cols
        icon_grid_mode = mode
        icon_grid_cells.append(
            {
                "figure": figure(
                    src,
                    f"Document illustration {num}.",
                    "ulr-amanzi-doc-figure--icon",
                )
            }
        )

    def grid_spec_for_image(num: int) -> tuple[int, str] | None:
        if 9 <= num <= 12:
            return 4, "char"
        if instr_grid_armed and num in (13, 14, 15):
            return 4, "instr"
        if num in (30, 31, 32):
            return 3, "plain"
        if num in (36, 37):
            return 2, "plain"
        if num in (38, 39, 40, 41):
            return 4, "plain"
        return None

    def close_icon_grid_on_text(t: str) -> bool:
        """Return True if this line closes the active icon grid."""
        if not icon_grid_cells:
            return False
        if icon_grid_mode == "char" and "Affordable" in t and "PRICED" in t:
            if icon_grid_cells:
                icon_grid_cells[-1]["caption"] = (
                    f'<p class="ulr-amanzi-doc-icon-grid__label">{esc(t)}</p>'
                )
            close_icon_grid()
            return True
        if icon_grid_mode == "instr" and (
            "World's Best" in t or "Water Purifier" in t
        ):
            close_icon_grid()
            return True
        if icon_grid_mode == "plain" and icon_grid_cols == 3 and t.startswith(
            "Additionally"
        ):
            close_icon_grid()
            return True
        if icon_grid_mode == "plain" and icon_grid_cols == 2 and (
            "Simple Water Treatment" in t
        ):
            close_icon_grid()
            return True
        if icon_grid_mode == "plain" and icon_grid_cols == 4 and t.startswith(
            "No Mixing"
        ):
            close_icon_grid()
            return True
        return False

    def close_hero() -> None:
        nonlocal hero_open, hero_closed
        if hero_open:
            parts.append("</div></div>")
            hero_open = False
            hero_closed = True

    def close_compare() -> None:
        nonlocal in_compare, compare_col
        if not in_compare:
            return
        if compare_col:
            parts.extend(compare_col)
            compare_col = []
        parts.append("</div>")
        parts.append("</div>")
        in_compare = False

    def close_safety() -> None:
        nonlocal in_safety
        if in_safety:
            parts.append("</div>")
            in_safety = False

    for i, (kind, payload) in enumerate(blocks):
        if kind == "image":
            num_s, ext = payload.rsplit(".", 1)
            num = int(num_s)
            if skip_leading_doc_images and num <= 3:
                continue
            src = resolve_image(num, ext, next_text=next_text_block(blocks, i))
            if not src:
                continue
            if not started:
                started = True
            if hero_open and num == 4:
                close_hero()
            nxt = next_text_block(blocks, i) or ""
            banner = nxt.strip().startswith("Sustainable water")
            if num == 6 and not in_compare:
                flush_figure_row(parts, figure_row)
                parts.append('<div class="ulr-amanzi-doc-compare">')
                parts.append('<div class="ulr-amanzi-doc-compare__col">')
                in_compare = True
                compare_col = []
                compare_col.append(figure(src, f"Document illustration {num}."))
                continue
            if in_compare:
                compare_col.append(figure(src, f"Document illustration {num}."))
                continue
            spec = grid_spec_for_image(num)
            if spec:
                cols, mode = spec
                add_icon_grid_image(src, num, cols, mode)
                continue
            if banner:
                flush_figure_row(parts, figure_row)
                emit_figure(parts, src, num, banner=True)
                continue
            if i + 1 < len(blocks) and blocks[i + 1][0] == "image":
                emit_figure(parts, src, num, figure_row=figure_row)
            else:
                flush_figure_row(parts, figure_row)
                emit_figure(parts, src, num)
            continue

        if kind == "table":
            flush_figure_row(parts, figure_row)
            close_compare()
            parts.append(render_table(payload))
            continue

        if skip_leading_doc_images:
            if "SANI" in payload and "Water Sanitising" in payload:
                skip_leading_doc_images = False
                started = True
            else:
                continue

        t = clean_doc_text(payload)

        if close_icon_grid_on_text(t):
            if "Affordable" in t and "PRICED" in t:
                continue

        if icon_grid_mode == "char" and icon_grid_cells and "Triple Foil" not in t:
            if not t or t in SKIP_EXACT or t in SKIP_EXACT_EXTRA:
                continue
            for cell in reversed(icon_grid_cells):
                if not cell.get("caption"):
                    cell["caption"] = (
                        f'<p class="ulr-amanzi-doc-icon-grid__label">{esc(t)}</p>'
                    )
                    break
            continue

        if "Instructions for use" in t:
            instr_grid_armed = True

        if t == "VS" and in_compare:
            if compare_col:
                parts.extend(compare_col)
                compare_col = []
            parts.append("</div>")
            parts.append('<p class="ulr-amanzi-doc-vs" aria-hidden="true">VS</p>')
            parts.append('<div class="ulr-amanzi-doc-compare__col">')
            continue

        if in_compare and t.startswith("We do not only believe"):
            if compare_col:
                parts.extend(compare_col)
                compare_col = []
            close_compare()

        if t.startswith("No Mixing with Other Disinfectants"):
            flush_figure_row(parts, figure_row)
            close_icon_grid()
            close_safety()
            parts.append('<div class="ulr-amanzi-doc-safety-grid">')
            in_safety = True

        if t == "Frequently asked questions)":
            close_safety()
            flush_figure_row(parts, figure_row)
            parts.append('<div class="ulr-amanzi-doc-faq">')
            in_faq = True
            parts.append(
                '<p id="faq" class="ulr-amanzi-doc-heading">Frequently asked questions</p>'
            )
            nav_headings.append(("FAQ", "faq"))
            continue

        if t == "Contact Us":
            if in_faq:
                parts.append("</div>")
                in_faq = False
            flush_figure_row(parts, figure_row)
            parts.append('<div class="ulr-amanzi-doc-contact">')
            in_contact = True

        if t.startswith("Partner With Ubuntu"):
            if in_contact:
                parts.append("</div>")
                in_contact = False

        html = para(payload, in_faq=in_faq)
        if not html:
            continue

        if in_safety:
            if t.startswith(("No ", "Avoid ", "Do Not", "use SANI")):
                parts.append(f'<p class="ulr-amanzi-doc-safety-item">{esc(t)}</p>')
                if "compromise the effectiveness" in t:
                    close_safety()
                continue

        if hero_open and not hero_closed:
            parts.append(html)
        else:
            flush_figure_row(parts, figure_row)
            if in_compare and t not in ("VS",) and not t.startswith("66"):
                compare_col.append(html)
            else:
                parts.append(html)
                if "ulr-amanzi-doc-heading" in html and t not in (
                    "Frequently asked questions",
                ):
                    nav_headings.append((t, slugify(t)))

        if payload.startswith("Brochure Button"):
            parts.append(brochure_actions())

        if payload == "Contact Us":
            parts.append(
                '<p class="ulr-amanzi-doc-p"><a href="mailto:sanchia@ubuntuliferesources.co.za">sanchia@ubuntuliferesources.co.za</a></p>'
            )
        if payload.startswith("Email:"):
            parts.append(
                '<p class="ulr-amanzi-doc-p"><a href="mailto:sanchia@ubuntuliferesources.co.za">sanchia@ubuntuliferesources.co.za</a></p>'
            )
        if "Contact No:" in payload or payload.startswith("Contact No"):
            parts.append(
                '<p class="ulr-amanzi-doc-p"><a href="tel:+27796588189">079 658 8189</a></p>'
            )
        if "www.linkedin.com" in payload:
            parts.append(
                '<p class="ulr-amanzi-doc-p"><a href="https://www.linkedin.com/in/sanchia-lynn-smit-935a44404" target="_blank" rel="noopener noreferrer">www.linkedin.com/in/sanchia-lynn-smit-935a44404</a></p>'
            )

    flush_figure_row(parts, figure_row)
    close_icon_grid()
    close_compare()
    close_safety()
    if in_faq:
        parts.append("</div>")
    if in_contact:
        parts.append("</div>")
    if hero_open:
        close_hero()

    nav_html = render_nav(nav_headings)
    if nav_html:
        for idx, line in enumerate(parts):
            if line == "</div></div>":
                parts.insert(idx + 1, nav_html)
                break

    parts.append("          </div>")
    parts.append("        </section>")
    return "\n".join(parts)


def splice_page(main_html: str) -> None:
    path = ROOT / "pillar-water-purification.html"
    text = path.read_text(encoding="utf-8")
    for marker in (
        '        <section class="ulr-amanzi-doc section-gap-x"',
        '        <section class="ulr-amanzi-hero section-gap-x"',
        '        <section class="tj-page-header section-gap-x"',
    ):
        if marker in text:
            start = text.index(marker)
            break
    else:
        raise ValueError("Could not find water page content start")
    end = text.index('        <section class="section-gap ulr-pillar-leadership-section">')
    head, tail = text[:start], text[end:]
    head = head.replace(
        'body class="ulr-pillar-page ulr-amanzi-page"',
        'body class="ulr-pillar-page ulr-amanzi-page ulr-amanzi-doc-flow"',
    )
    head = head.replace(
        'body class="ulr-pillar-page"',
        'body class="ulr-pillar-page ulr-amanzi-page ulr-amanzi-doc-flow"',
    )
    if "ulr-amanzi-doc.css" not in head:
        head = head.replace(
            '<link rel="stylesheet" href="assets/css/ulr-amanzi-page.css">',
            '<link rel="stylesheet" href="assets/css/ulr-amanzi-page.css">\n  <link rel="stylesheet" href="assets/css/ulr-amanzi-doc.css">',
        )
        if "ulr-amanzi-doc.css" not in head:
            head = head.replace(
                '<link rel="stylesheet" href="assets/css/ulr-pillar-brief.css">',
                '<link rel="stylesheet" href="assets/css/ulr-pillar-brief.css">\n  <link rel="stylesheet" href="assets/css/ulr-amanzi-doc.css">',
            )
    script = '<script src="assets/js/ulr-amanzi-doc.js" defer></script>'
    if "ulr-amanzi-doc.js" not in tail:
        tail = tail.replace("</body>", f"  {script}\n</body>", 1)
    path.write_text(head + main_html + "\n" + tail, encoding="utf-8")


def main() -> None:
    splice_page(build_main())
    print("Updated pillar-water-purification.html (strict doc flow).")


if __name__ == "__main__":
    main()
