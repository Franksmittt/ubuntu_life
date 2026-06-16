# -*- coding: utf-8 -*-
"""Build pillar-preparedness.html from brief docx files (when present) and patch site nav."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "pillar-institutional-supply.html"
OUTPUT = ROOT / "pillar-preparedness.html"
KNOWLEDGE = ROOT / "knowledge"

DOCX_SOURCES = (
    "Environmental Hygiene Biosecurity & Infection-Control Readiness.docx",
    "Supporting Nutritional Resilience Through Strategic Protein Food Reserves.docx",
    "Strategic Water Security Planning for Disaster, Outbreak & Humanitarian Response Across Africa.docx",
)

NAV_ITEM = '<li><a href="pillar-preparedness.html">Preparedness</a></li>'
NAV_AFTER = '<li><a href="pillar-hygiene-sanitation.html">Hygiene</a></li>'
NAV_CURRENT = (
    '<li class="current-menu-item"><a href="pillar-preparedness.html">Preparedness</a></li>'
)


def placeholder(label: str, modifier: str = "") -> str:
    cls = "ulr-preparedness-placeholder"
    if modifier:
        cls += f" {modifier}"
    return (
        f'<figure class="{cls}" role="img" aria-label="Image placeholder: {label}">'
        f'<span class="ulr-preparedness-placeholder__label">{label}</span>'
        "</figure>"
    )


def split_section(text: str, image_label: str, flip: bool = False, bg: bool = False) -> str:
    """Render alternating text + placeholder image blocks from plain paragraphs."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return ""

    title = paragraphs[0]
    body_parts = paragraphs[1:]
    body_html = "".join(f"<p class='desc'>{p}</p>" for p in body_parts)

    cls = "section-gap ulr-brief-section"
    if bg:
        cls += " bg-light"

    img_col = f'<div class="col-lg-6">{placeholder(image_label)}</div>'
    txt_col = (
        f'<div class="col-lg-6"><div class="ulr-brief-copy">'
        f"<h2 class=\"sec-title h3 mb-3\">{title}</h2>{body_html}</div></div>"
    )
    row = (txt_col + img_col) if flip else (img_col + txt_col)

    return (
        f'<section class="{cls}"><div class="container">'
        f'<div class="row g-4 g-lg-5 align-items-center">{row}</div>'
        "</div></section>"
    )


def load_docx_paragraphs(path: Path) -> list[str]:
    try:
        from docx import Document
    except ImportError:
        return []

    if not path.exists():
        return []

    doc = Document(str(path))
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


def paragraphs_to_html(paragraphs: list[str]) -> str:
    if not paragraphs:
        return ""
    chunks: list[str] = []
    for para in paragraphs:
        if para.isupper() and len(para) < 120:
            chunks.append(f"<h3 class=\"h5 sec-title mb-3\">{para}</h3>")
        elif para.startswith("•") or para.startswith("- "):
            if not chunks or not chunks[-1].endswith("</ul>"):
                chunks.append('<ul class="desc">')
            item = para.lstrip("•- ").strip()
            chunks.append(f"<li>{item}</li>")
        else:
            if chunks and chunks[-1] == '<ul class="desc">':
                chunks.append("</ul>")
            elif chunks and chunks[-1].startswith("<li>"):
                chunks.append("</ul>")
            chunks.append(f"<p class=\"desc\">{para}</p>")
    if chunks and chunks[-1].startswith("<li>"):
        chunks.append("</ul>")
    return "".join(chunks)


def section_block(
    section_id: str,
    eyebrow: str,
    title: str,
    lead: str,
    body_html: str,
    banner_label: str,
    side_label: str,
    flip: bool = False,
    bg: bool = False,
) -> str:
    cls = "section-gap ulr-brief-section ulr-preparedness-section"
    if bg:
        cls += " bg-light"

    img_col = f'<div class="col-lg-5">{placeholder(side_label)}</div>'
    txt_col = (
        f'<div class="col-lg-7"><div class="ulr-brief-copy">'
        f'<span class="ulr-preparedness-section__eyebrow">{eyebrow}</span>'
        f'<h2 class="sec-title h3 mb-3" id="{section_id}">{title}</h2>'
        f'<p class="desc"><strong>{lead}</strong></p>'
        f"{body_html}</div></div>"
    )
    row = (txt_col + img_col) if flip else (img_col + txt_col)

    return f"""        <section class="{cls}" aria-labelledby="{section_id}">
          <div class="container">
            <div class="mb-4 mb-lg-5">{placeholder(banner_label, "ulr-preparedness-placeholder--banner")}</div>
            <div class="row g-4 g-lg-5 align-items-center">{row}</div>
          </div>
        </section>"""


def hygiene_content() -> str:
  docx = KNOWLEDGE / DOCX_SOURCES[0]
  paras = load_docx_paragraphs(docx)
  if paras:
      return paragraphs_to_html(paras)

  return """
<p class="desc">Environmental hygiene, biosecurity, and infection-control readiness are not optional add-ons to a crisis plan — they are the operational layer that keeps facilities, supply chains, and communities functioning when pressure rises.</p>
<p class="desc">Ubuntu Life Resources supports preparedness programmes that combine evidence-based disinfection with practical deployment models for healthcare, hospitality, food processing, institutional settings, and agricultural biosecurity corridors.</p>
<h3 class="h5 sec-title mb-3">Why readiness matters before an outbreak</h3>
<ul class="desc">
  <li>Pathogen transmission accelerates when cleaning protocols, product selection, and staff training are improvised under stress.</li>
  <li>Healthcare-associated infections and zoonotic spillover both demand disciplined environmental hygiene — not reactive deep cleans alone.</li>
  <li>Reserve stock, dilution discipline, and surface-contact mapping must be agreed before an event, not negotiated during one.</li>
</ul>
<h3 class="h5 sec-title mb-3">Representative solution lines</h3>
<ul class="desc">
  <li><strong>SANI-99&trade;</strong> — medical-grade hand and surface disinfection for clinics, hospitality, and high-touch environments.</li>
  <li><strong>SANI-99&trade; for AGRI</strong> — veterinary-grade biosecurity for farms, abattoirs, transport, and outbreak containment zones.</li>
  <li>Structured engagement for governments, NGOs, distributors, and institutional buyers building IPC-ready supply postures.</li>
</ul>
<p class="desc mb-0">Explore the full hygiene portfolio on our <a href="pillar-hygiene-sanitation.html">Hygiene &amp; Sanitation</a> page and <a href="pillar-agri-biosecurity.html">Agricultural Biosecurity</a> pillar.</p>
"""


def water_content() -> str:
  docx = KNOWLEDGE / DOCX_SOURCES[2]
  paras = load_docx_paragraphs(docx)
  if paras:
      return paragraphs_to_html(paras)

  return """
<p class="desc">Water security planning for disaster, outbreak, and humanitarian response must assume infrastructure failure, contamination events, and sudden population displacement — often simultaneously.</p>
<p class="desc">Strategic preparedness means maintaining lightweight, shelf-stable treatment capacity that can move from central reserves to household and community level without re-engineering the method at each deployment.</p>
<h3 class="h5 sec-title mb-3">Crisis scenarios we plan for</h3>
<ul class="desc">
  <li>Flooding, drought, and municipal supply interruptions that cut safe drinking water access.</li>
  <li>Disease outbreaks where WASH infrastructure and infection control must work together.</li>
  <li>Humanitarian corridors, camps, and rural off-grid communities beyond conventional piped networks.</li>
</ul>
<h3 class="h5 sec-title mb-3">SANI AMANZI&trade; in a preparedness architecture</h3>
<ul class="desc">
  <li>Point-of-use powder treatment — 6&nbsp;g sachets calibrated for 20&nbsp;L batches, scaling to bulk humanitarian volumes.</li>
  <li>Compact storage and rapid transport compared with bottled-water logistics at scale.</li>
  <li>Suitable for governments, NGOs, disaster-response organisations, and institutional reserve programmes.</li>
</ul>
<p class="desc mb-0">Read the full water pillar at <a href="pillar-water-purification.html">Water Purification Solutions</a> and our field narrative on <a href="blog-sani-amanzi-point-of-use-water.html">point-of-use water programmes</a>.</p>
"""


def nutrition_content() -> str:
  docx = KNOWLEDGE / DOCX_SOURCES[1]
  paras = load_docx_paragraphs(docx)
  if paras:
      return paragraphs_to_html(paras)

  return """
<p class="desc">Nutritional resilience depends on protein and micronutrient access that does not collapse when cold chains fail, borders slow, or budgets are stretched across extended response seasons.</p>
<p class="desc">Strategic protein food reserves — built around shelf-stable, retorted seafood — give governments, NGOs, and institutional buyers a dependable buffer between normal supply and emergency feeding demand.</p>
<h3 class="h5 sec-title mb-3">Why shelf-stable protein reserves</h3>
<ul class="desc">
  <li>Ambient storage removes refrigeration dependency in rural, disaster-affected, and logistics-constrained corridors.</li>
  <li>Canned tuna, pilchards, and sardines deliver complete protein, Omega-3, and calcium (from edible bone) in formats familiar to African households.</li>
  <li>Case-level pallet logic supports both retail continuity and large-scale humanitarian rotation stock.</li>
</ul>
<h3 class="h5 sec-title mb-3">Tonno Bonno portfolio for reserve programmes</h3>
<ul class="desc">
  <li>Multiple pack sizes (155&nbsp;g / 170&nbsp;g / 400&nbsp;g) and sauce variants for cultural preference and caloric targets.</li>
  <li>Manufactured under strict canned-fish compulsory specifications for institutional acceptance.</li>
  <li>Ubuntu Life Resources acts as strategic agent for structured supply into Southern Africa and selected Sub-Saharan markets.</li>
</ul>
<p class="desc mb-0">See the <a href="pillar-shelf-stable-nutrition.html">Strategic Food Supply</a> pillar and <a href="products.html">product catalogue</a> for SKU-level detail.</p>
"""


def main_content() -> str:
    parts = [
        """        <section class="tj-page-header section-gap-x" data-bg-image="assets/images/hero/ulr-hero-route-to-market-southern-africa.jpg">
          <div class="container position-relative" style="z-index:2;">
            <div class="row">
              <div class="col-lg-12">
                <div class="tj-page-header-content text-center">
                  <h1 class="tj-page-title">Preparedness</h1>
                  <p class="pillar-header-lead">Integrated readiness across <strong>environmental hygiene</strong>, <strong>water security</strong>, and <strong>nutritional resilience</strong> — structured for governments, institutions, and humanitarian programmes across Africa.</p>
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
        f"""        <section class="section-gap ulr-brief-section">
          <div class="container">
            <div class="ulr-preparedness-intro mb-4">
              <span class="sub-title d-inline-block mb-2"><i class="tji-strategy"></i> One readiness framework</span>
              <p class="desc mb-3">Crises rarely isolate a single risk vector. Outbreaks stress hygiene systems. Disasters interrupt water. Prolonged emergencies deplete protein reserves. This page brings together the three preparedness briefs that shape how Ubuntu Life Resources supports buyers building <strong>reserve capacity</strong>, <strong>deployment playbooks</strong>, and <strong>supplier alignment</strong> before the event.</p>
              <ul class="ulr-preparedness-nav" aria-label="Preparedness sections">
                <li><a href="#hygiene-readiness">Hygiene &amp; infection control</a></li>
                <li><a href="#water-security">Water security</a></li>
                <li><a href="#nutrition-reserves">Protein food reserves</a></li>
              </ul>
            </div>
            <div class="row g-4">
              <div class="col-md-4">
                {placeholder("Hero — integrated preparedness collage", "ulr-preparedness-placeholder--square")}
              </div>
              <div class="col-md-8">
                <div class="ulr-preparedness-cards h-100">
                  <article class="ulr-preparedness-card">
                    <h3>Environmental hygiene</h3>
                    <p class="desc small mb-0">Biosecurity, IPC discipline, and disinfection reserves for healthcare, food, and agricultural settings.</p>
                  </article>
                  <article class="ulr-preparedness-card">
                    <h3>Water security</h3>
                    <p class="desc small mb-0">Point-of-use treatment stockpiles for disaster, outbreak, and humanitarian corridors.</p>
                  </article>
                  <article class="ulr-preparedness-card">
                    <h3>Nutritional resilience</h3>
                    <p class="desc small mb-0">Shelf-stable protein reserves that hold without cold chain dependency.</p>
                  </article>
                </div>
              </div>
            </div>
          </div>
        </section>""",
        section_block(
            "hygiene-readiness",
            "Brief 1",
            "Environmental Hygiene, Biosecurity &amp; Infection-Control Readiness",
            "Build IPC and environmental hygiene capacity before transmission pathways accelerate.",
            hygiene_content(),
            "Banner — environmental hygiene &amp; infection-control readiness",
            "Side image — healthcare / facility disinfection",
            flip=False,
            bg=True,
        ),
        section_block(
            "water-security",
            "Brief 2",
            "Strategic Water Security Planning for Disaster, Outbreak &amp; Humanitarian Response Across Africa",
            "Plan reserve water-treatment capacity that moves as fast as the crisis.",
            water_content(),
            "Banner — water security &amp; humanitarian response",
            "Side image — community water treatment deployment",
            flip=True,
            bg=False,
        ),
        section_block(
            "nutrition-reserves",
            "Brief 3",
            "Supporting Nutritional Resilience Through Strategic Protein Food Reserves",
            "Anchor feeding programmes with shelf-stable protein that survives logistics stress.",
            nutrition_content(),
            "Banner — strategic protein food reserves",
            "Side image — shelf-stable food reserve stock",
            flip=False,
            bg=True,
        ),
        f"""        <section class="section-gap ulr-preparedness-band">
          <div class="container">
            <div class="row g-4 g-lg-5 align-items-center">
              <div class="col-lg-6">
                <h2 class="sec-title">Integrated <span>readiness</span> engagement</h2>
                <p class="desc">Ubuntu Life Resources helps programme sponsors translate preparedness briefs into supplier-aligned plans — reserve levels, documentation, training collateral, and phased roll-out that respects procurement reality.</p>
                <ul class="desc mb-0">
                  <li>Multi-pillar baskets spanning hygiene, water, and nutrition where programmes overlap</li>
                  <li>Evidence and product truth aligned to supplier documentation and lab reports</li>
                  <li>Single accountable commercial interface: <strong>Sanchia-Lynn Smit</strong>, CEO / Founder</li>
                </ul>
              </div>
              <div class="col-lg-6">
                {placeholder("Integrated readiness — programme planning / stakeholder briefing")}
              </div>
            </div>
          </div>
        </section>""",
        """        <section class="tj-cta-section section-gap-x">
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
        </section>""",
        """        <section class="section-gap pt-0">
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
        </section>""",
    ]
    return "\n".join(parts)


def build_page() -> None:
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
        'content="Preparedness across environmental hygiene, water security, and nutritional resilience — reserve planning for governments, institutions, and humanitarian programmes in Africa."',
    )
    head = head.replace(
        '<body class="ulr-pillar-page">',
        '<body class="ulr-pillar-page ulr-preparedness-page">',
    )
    if "ulr-pillar-brief.css" not in head:
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


def patch_nav_in_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "pillar-preparedness.html" in text:
        return False

    patterns = (
        NAV_AFTER,
        '<li class="current-menu-item"><a href="pillar-hygiene-sanitation.html">Hygiene</a></li>',
    )
    for pattern in patterns:
        if pattern in text:
            updated = text.replace(pattern, pattern + "\n                  " + NAV_ITEM)
            path.write_text(updated, encoding="utf-8")
            return True
    return False


def patch_site_nav() -> None:
    count = 0
    for path in ROOT.glob("*.html"):
        if path.name == OUTPUT.name:
            continue
        if patch_nav_in_file(path):
            count += 1
            print(f"Patched nav: {path.name}")
    print(f"Nav updated in {count} files")


def patch_pillars_overview() -> None:
    path = ROOT / "pillars.html"
    text = path.read_text(encoding="utf-8")
    if "pillar-preparedness.html" in text:
        return

    card = """
              <div class="col-md-6">
                <a class="text-decoration-none text-reset" href="pillar-preparedness.html">
                  <div class="pillar-related-card h-100 overflow-hidden rounded-3 border">
                    <div class="ratio ratio-4x3 ulr-preparedness-placeholder">
                      <span class="ulr-preparedness-placeholder__label">Image — preparedness overview</span>
                    </div>
                    <div class="p-3">
                      <h3 class="h5 mb-1">Preparedness</h3>
                      <span class="small text-muted">Hygiene, water security, and protein reserves for crisis readiness.</span>
                    </div>
                  </div>
                </a>
              </div>"""

    anchor = '              <div class="col-md-6">\n                <a class="text-decoration-none text-reset" href="pillar-institutional-supply.html">'
    if anchor not in text:
        return
    text = text.replace(anchor, card + anchor, 1)
    text = text.replace(
        "<h2 class=\"sec-title\">The four <span>pillars</span></h2>",
        "<h2 class=\"sec-title\">Core <span>pillars</span></h2>",
    )
    path.write_text(text, encoding="utf-8")
    print("Patched pillars.html overview card")


def main() -> None:
    build_page()
    patch_site_nav()
    patch_pillars_overview()


if __name__ == "__main__":
    main()
