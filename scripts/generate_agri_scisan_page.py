# -*- coding: utf-8 -*-
"""Build agriculture pages matching scisan.co.za/sani-99-for-agri layout."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TM = "&trade;"
IMG = "assets/images/pillars/agri-biosecurity/scisan"
HERO = "assets/images/pillars/agri-biosecurity/0001.jpg"
SUSTAINABILITY_SECTION = Path(__file__).resolve().parent / "agri_sustainability_section.html"
DEPLOY_CLOSING_SECTION = Path(__file__).resolve().parent / "agri_deploy_closing_section.html"
PAGES = (
    ROOT / "pillar-agri-biosecurity.html",
    ROOT / "product-sani-99-agri.html",
)
REQUIRED_STYLES = (
    "assets/css/ulr-scisan-embed-shell.css",
    "assets/css/ulr-scisan-embed.css",
)
DEPRECATED_STYLES = (
    "assets/css/ulr-pillar-brief.css",
    "assets/css/ulr-amanzi-page.css",
    "assets/css/ulr-amanzi-scisan.css",
    "assets/css/ulr-agri-scisan.css",
)
EMBED_BODY_CLASSES = ("ulr-pillar-page", "ulr-agri-scisan", "ulr-scisan-embed-page")


def sustainability_section() -> str:
    return SUSTAINABILITY_SECTION.read_text(encoding="utf-8").replace("&trade;", TM)


def deploy_closing_section() -> str:
    return DEPLOY_CLOSING_SECTION.read_text(encoding="utf-8").replace("&trade;", TM)


def src(name: str) -> str:
    return f"{IMG}/{name}"


def figure(path: str, alt: str = "", extra: str = "") -> str:
    cls = "ulr-amanzi-figure"
    if extra:
        cls += f" {extra}"
    return (
        f'<figure class="{cls}">'
        f'<img src="{path}" alt="{alt}" loading="lazy" decoding="async">'
        f"</figure>"
    )


def kf_item(img_name: str, alt: str, lines: list[str]) -> str:
    label = "".join(
        f'<span class="muted">{line}</span>' if i else line
        for i, line in enumerate(lines)
    )
    return f"""<div class="ulr-amanzi-scisan-kf__item">
<img src="{src(img_name)}" alt="{alt}" loading="lazy" decoding="async">
<p class="ulr-amanzi-scisan-kf__label">{label}</p>
</div>"""


def flip_card(title: str, front: str, back_html: str) -> str:
    return f"""<button type="button" class="ulr-amanzi-scisan-flip" aria-label="{title} — tap to flip">
<div class="ulr-amanzi-scisan-flip__inner">
<div class="ulr-amanzi-scisan-flip__face ulr-amanzi-scisan-flip__face--front">
<h3 class="ulr-amanzi-scisan-flip__title">{title}</h3>
<p>{front}</p>
</div>
<div class="ulr-amanzi-scisan-flip__face ulr-amanzi-scisan-flip__face--back">
<h3 class="ulr-amanzi-scisan-flip__title">{title}</h3>
<div class="ulr-amanzi-scisan-flip__back">{back_html}</div>
</div>
</div>
</button>"""


def flip_list(items: list[str]) -> str:
    lis = "".join(f"<li>{item}</li>" for item in items)
    return f'<ul class="ulr-scisan-flip-list">{lis}</ul>'


def build_main() -> str:
    parts: list[str] = []

    parts.append(f"""        <section class="ulr-amanzi-scisan-hero ulr-agri-hero section-gap-x">
          <div class="ulr-amanzi-scisan-hero__bg" style="background-image: url('{HERO}');" aria-hidden="true"></div>
          <div class="ulr-amanzi-scisan-hero__content ulr-agri-hero__content">
            <h1 class="ulr-amanzi-scisan-hero__title">Agricultural Biosecurity Starts Here</h1>
            <p class="ulr-agri-hero__lead">Advanced Veterinary Grade Disinfection Solutions For Modern Agriculture</p>
            <p class="ulr-agri-hero__desc">Ubuntu Life Resources delivers scalable agricultural biosecurity solutions through SANI-99{TM} for AGRI &mdash; helping farms, poultry operations, abattoirs, dairies, hatcheries and food processing environments reduce pathogen risks and improve hygiene standards.</p>
            <p class="ulr-agri-hero__pillars">Agricultural Biosecurity &middot; Clean Water &middot; Food Security</p>
          </div>
        </section>""")

    parts.append(f"""        <section id="what-is" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="row g-4 g-lg-5 align-items-center ulr-agri-split">
              <div class="col-lg-6">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0002.png" alt="SANI-99 for AGRI agricultural disinfectant" loading="lazy" decoding="async">
                </figure>
              </div>
              <div class="col-lg-6">
                <div class="ulr-agri-split__copy">
                  <h2 class="sec-title ulr-amanzi-heading h3 mb-3">What is SANI-99{TM} for AGRI?</h2>
                  <p class="desc">SANI-99{TM} for AGRI is a veterinary and food grade agricultural disinfectant designed to support biosecurity across multiple agricultural sectors.</p>
                  <p class="desc">The solution has been developed to assist farms and agricultural facilities in reducing pathogen exposure while supporting hygiene, operational safety and disease prevention protocols.</p>
                  <p class="desc mb-2"><strong>SANI-99{TM} for AGRI provides:</strong></p>
                  <ul class="desc mb-3">
                    <li>Broad-spectrum disinfection</li>
                    <li>360&deg; biosecurity support</li>
                    <li>High efficacy pathogen control</li>
                    <li>Long-lasting residual activity</li>
                    <li>Food and veterinary grade applications</li>
                    <li>Agricultural equipment sanitation</li>
                    <li>Facility and livestock area disinfection</li>
                  </ul>
                  <p class="desc mb-0">Designed for modern agriculture, SANI-99{TM} for AGRI supports operations ranging from poultry and livestock farming to abattoirs, dairies, aquaculture and food processing facilities.</p>
                </div>
              </div>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="key-features-intro" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="row g-4 g-lg-5 align-items-center ulr-agri-split">
              <div class="col-lg-6 order-2 order-lg-2">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0003.png" alt="SANI-99 for AGRI key features" loading="lazy" decoding="async">
                </figure>
              </div>
              <div class="col-lg-6 order-1 order-lg-1">
                <div class="ulr-agri-split__copy">
                  <h2 class="sec-title ulr-amanzi-heading h3 mb-4">Key Features</h2>
                  <div class="ulr-agri-feature-list">
                    <div class="ulr-agri-feature-item">
                      <h3 class="ulr-agri-feature-item__title">360&deg; Agricultural Biosecurity</h3>
                      <p class="desc mb-0">SANI-99{TM} for AGRI supports comprehensive agricultural disinfection across livestock facilities, poultry housing, food processing environments, equipment sanitation and operational hygiene protocols.</p>
                    </div>
                    <div class="ulr-agri-feature-item">
                      <h3 class="ulr-agri-feature-item__title">Alcohol &amp; Chlorine Free</h3>
                      <p class="desc mb-0">The formulation is alcohol-free and chlorine-free, helping reduce harsh chemical exposure while maintaining strong disinfection performance.</p>
                    </div>
                    <div class="ulr-agri-feature-item">
                      <h3 class="ulr-agri-feature-item__title">Safe Around Livestock</h3>
                      <p class="desc mb-0">Designed for agricultural environments where animal welfare remains essential.</p>
                    </div>
                    <div class="ulr-agri-feature-item">
                      <h3 class="ulr-agri-feature-item__title">Food &amp; Veterinary Grade</h3>
                      <p class="desc mb-0">Suitable for use across multiple agricultural and food-related applications.</p>
                    </div>
                    <div class="ulr-agri-feature-item">
                      <h3 class="ulr-agri-feature-item__title">Halal Certified</h3>
                      <p class="desc mb-0">Supports diverse agricultural and food production requirements.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="industries-applications" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="row g-4 g-lg-5 align-items-center ulr-agri-split">
              <div class="col-lg-6">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0004.png" alt="SANI-99 for AGRI industries and applications" loading="lazy" decoding="async">
                </figure>
              </div>
              <div class="col-lg-6">
                <div class="ulr-agri-split__copy">
                  <p class="ulr-agri-discover-quote mb-3">&#9989; &ldquo;Discover the diverse applications and uses of SANI-99{TM} for AGRI&rdquo;</p>
                  <h2 class="sec-title ulr-amanzi-heading h3 mb-3">Industries &amp; Applications</h2>
                  <p class="desc">SANI-99{TM} for AGRI supports a wide range of agricultural industries and operational environments including:</p>
                  <ul class="desc ulr-agri-apps-list mb-3">
                    <li>Poultry Farming</li>
                    <li>Livestock Facilities</li>
                    <li>Dairy Operations</li>
                    <li>Hatcheries</li>
                    <li>Abattoirs</li>
                    <li>Cold Storage Facilities</li>
                    <li>Food Processing Areas</li>
                    <li>Aquaculture</li>
                    <li>Crop Production</li>
                    <li>Horticulture</li>
                    <li>Agricultural Machinery</li>
                    <li>Water Systems &amp; Foot Baths</li>
                  </ul>
                  <p class="desc mb-0">The solution can be integrated into both preventative hygiene protocols and active biosecurity management systems.</p>
                </div>
              </div>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section class="ulr-amanzi-band ulr-amanzi-band--tight section-gap">
          <div class="ulr-amanzi-band__inner">
            <figure class="ulr-amanzi-figure ulr-amanzi-figure--flush ulr-agri-fit-image m-0">
              <img src="assets/images/pillars/agri-biosecurity/0005.png" alt="SANI-99 for AGRI applications overview" loading="lazy" decoding="async">
            </figure>
          </div>
        </section>""")

    parts.append(f"""        <section id="eliminating-pathogens" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="row g-4 g-lg-5 align-items-center ulr-agri-split">
              <div class="col-lg-6 order-2 order-lg-2">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0006.png" alt="SANI-99 for AGRI pathogen control" loading="lazy" decoding="async">
                </figure>
              </div>
              <div class="col-lg-6 order-1 order-lg-1">
                <div class="ulr-agri-split__copy">
                  <p class="ulr-agri-discover-quote mb-3">&#9989; &ldquo;Eliminating Pathogens, Viruses and Diseases&rdquo;</p>
                  <h2 class="sec-title ulr-amanzi-heading h3 mb-3">Eliminating Pathogens, Viruses &amp; Diseases</h2>
                  <p class="desc">SANI-99{TM} for AGRI has been formulated to assist in controlling and reducing exposure to a broad spectrum of pathogens affecting agricultural environments.</p>
                  <p class="desc mb-2">This includes support against:</p>
                  <ul class="desc ulr-agri-apps-list mb-3">
                    <li>E.coli</li>
                    <li>Salmonella</li>
                    <li>Listeria monocytogenes</li>
                    <li>Newcastle Disease</li>
                    <li>Avian Influenza</li>
                    <li>Swine Flu</li>
                    <li>Foot &amp; Mouth Disease</li>
                    <li>Poxviridae</li>
                    <li>Staphylococcus aureus</li>
                    <li>Enterococcus hirae</li>
                    <li>Pseudomonas aeruginosa</li>
                  </ul>
                  <p class="desc mb-0">Its broad-spectrum disinfection capabilities support improved operational hygiene across agricultural sectors.</p>
                </div>
              </div>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="poultry-biosecurity" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="row g-4 mb-4 mb-lg-5 ulr-agri-duo-images">
              <div class="col-md-6">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0007.png" alt="Advanced poultry biosecurity application" loading="lazy" decoding="async">
                </figure>
              </div>
              <div class="col-md-6">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0008.png" alt="SANI-99 for AGRI poultry fogging" loading="lazy" decoding="async">
                </figure>
              </div>
            </div>
            <div class="ulr-agri-poultry-copy">
              <h2 class="sec-title ulr-amanzi-heading h3 mb-3 text-center">Advanced Poultry Biosecurity</h2>
              <p class="desc">The poultry industry faces increasing pressure from airborne disease transmission, Avian Influenza outbreaks and operational hygiene risks.</p>
              <p class="desc mb-2">SANI-99{TM} for AGRI supports poultry biosecurity protocols through:</p>
              <ul class="desc ulr-agri-apps-list mb-3">
                <li>Poultry housing disinfection</li>
                <li>Fogging applications</li>
                <li>Airborne pathogen reduction support</li>
                <li>Surface sanitation</li>
                <li>Dust suppression support</li>
                <li>Foot bath applications</li>
                <li>Equipment sanitation</li>
              </ul>
              <p class="desc mb-0">The fogging application process assists in improving coverage throughout poultry facilities while supporting operational hygiene standards.</p>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="abattoirs-food-processing" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="row g-4 mb-4 mb-lg-5 ulr-agri-trio-images">
              <div class="col-md-4">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0011.png" alt="Abattoir hygiene management" loading="lazy" decoding="async">
                </figure>
              </div>
              <div class="col-md-4">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0010.png" alt="Food processing sanitation" loading="lazy" decoding="async">
                </figure>
              </div>
              <div class="col-md-4">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0009.png" alt="SANI-99 for AGRI abattoir applications" loading="lazy" decoding="async">
                </figure>
              </div>
            </div>
            <div class="ulr-agri-block-copy">
              <h2 class="sec-title ulr-amanzi-heading h3 mb-3 text-center">Abattoirs &amp; Food Processing</h2>
              <p class="desc mb-2">SANI-99{TM} for AGRI supports hygiene management within:</p>
              <ul class="desc ulr-agri-apps-list mb-3">
                <li>Abattoirs</li>
                <li>Meat processing facilities</li>
                <li>Carcass washing systems</li>
                <li>Equipment sanitation</li>
                <li>Biosecurity control areas</li>
                <li>Food processing environments</li>
              </ul>
              <p class="desc">The solution assists facilities in maintaining high hygiene standards while supporting contamination reduction strategies and operational sanitation protocols.</p>
              <p class="desc mb-2">Applications include:</p>
              <ul class="desc ulr-agri-apps-list mb-0">
                <li>Equipment disinfection</li>
                <li>Surface sanitation</li>
                <li>Carcass dipping</li>
                <li>Processing area disinfection</li>
                <li>Worker hygiene support</li>
                <li>Facility sanitation</li>
              </ul>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="certifications-approvals" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="row g-4 mb-4 mb-lg-5 ulr-agri-duo-images">
              <div class="col-md-6">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0013.png" alt="SANI-99 for AGRI certifications" loading="lazy" decoding="async">
                </figure>
              </div>
              <div class="col-md-6">
                <figure class="ulr-amanzi-figure ulr-agri-split__figure m-0">
                  <img src="assets/images/pillars/agri-biosecurity/0012.png" alt="SANI-99 for AGRI approvals and standards" loading="lazy" decoding="async">
                </figure>
              </div>
            </div>
            <div class="ulr-agri-block-copy">
              <h2 class="sec-title ulr-amanzi-heading h3 mb-3 text-center">Certifications &amp; Approvals</h2>
              <p class="desc mb-2">SANI-99{TM} for AGRI aligns with multiple international and agricultural disinfection standards and approvals including:</p>
              <ul class="desc ulr-agri-apps-list mb-3">
                <li>DEFRA Approval</li>
                <li>ECHA Approval</li>
                <li>BEIC Approval</li>
                <li>EN1276</li>
                <li>EN13697</li>
                <li>EN14476</li>
                <li>EN1040</li>
                <li>EN13727</li>
                <li>SANS 51276</li>
                <li>SANS 53697</li>
              </ul>
              <p class="desc mb-0">These certifications support its use across veterinary hygiene, agricultural biosecurity and food-related operational environments.</p>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="application-methods" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <figure class="ulr-amanzi-figure ulr-amanzi-figure--flush ulr-agri-fit-image m-0 mb-4 mb-lg-5">
              <img src="assets/images/pillars/agri-biosecurity/0014.png" alt="SANI-99 for AGRI flexible application methods" loading="lazy" decoding="async">
            </figure>
            <div class="ulr-agri-block-copy">
              <h2 class="sec-title ulr-amanzi-heading h3 mb-3 text-center">Flexible Application Methods</h2>
              <p class="desc mb-2">SANI-99{TM} for AGRI supports multiple agricultural application methods including:</p>
              <ul class="desc ulr-agri-apps-list mb-3">
                <li>Fogging</li>
                <li>Pressure Washers</li>
                <li>Sprayers</li>
                <li>Foot Baths</li>
                <li>Dip Tanks</li>
                <li>Handheld Sprayers</li>
                <li>Soaking Tubs</li>
                <li>Surface Wipes</li>
                <li>Agricultural Machinery Sanitation</li>
              </ul>
              <p class="desc mb-0">This flexibility allows integration into both small-scale and industrial agricultural operations.</p>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="product-formats" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <figure class="ulr-amanzi-figure ulr-amanzi-figure--flush ulr-agri-fit-image m-0 mb-4 mb-lg-5">
              <img src="assets/images/pillars/agri-biosecurity/0015.png" alt="SANI-99 for AGRI product formats" loading="lazy" decoding="async">
            </figure>
            <h2 class="sec-title ulr-amanzi-heading h3 mb-4 text-center">Available Product Formats</h2>
            <div class="row g-4 g-lg-5 ulr-agri-format-grid">
              <div class="col-md-6">
                <div class="ulr-agri-format-card">
                  <h3 class="ulr-agri-feature-item__title">96g Sachets</h3>
                  <p class="desc mb-2">Ideal for:</p>
                  <ul class="desc mb-0">
                    <li>Backpack sprayers</li>
                    <li>Fogging systems</li>
                    <li>Foot baths</li>
                    <li>Small-scale sanitation</li>
                    <li>Portable applications</li>
                  </ul>
                </div>
              </div>
              <div class="col-md-6">
                <div class="ulr-agri-format-card">
                  <h3 class="ulr-agri-feature-item__title">1kg &ndash; 25kg Tubs</h3>
                  <p class="desc mb-2">Ideal for:</p>
                  <ul class="desc mb-0">
                    <li>Pressure washers</li>
                    <li>Large agricultural operations</li>
                    <li>IBC systems</li>
                    <li>Industrial sanitation</li>
                    <li>Commercial agricultural deployment</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>""")

    parts.append(sustainability_section())

    parts.append(deploy_closing_section())

    return "\n".join(parts)


def build_exact_embed_main() -> str:
    return """        <div class="space-for-header"></div>
        <section class="ulr-scisan-exact-page" aria-labelledby="ulr-scisan-agri-title">
          <h1 id="ulr-scisan-agri-title" class="visually-hidden">SANI-99 for AGRI</h1>
          <iframe id="ulr-scisan-agri-frame" class="ulr-scisan-exact-page__frame" src="scisan-agri-content.html" title="SANI-99 for AGRI SciSan page content" loading="eager" scrolling="no"></iframe>
        </section>"""


def ensure_body_classes(head: str) -> str:
    match = re.search(r'<body class="([^"]*)">', head)
    if not match:
        return head

    classes = [cls for cls in match.group(1).split() if cls not in {
        "ulr-rich-subpage",
        "ulr-amanzi-page",
        "ulr-amanzi-scisan",
    }]
    for required in EMBED_BODY_CLASSES:
        if required not in classes:
            classes.append(required)

    return head[: match.start(1)] + " ".join(classes) + head[match.end(1) :]


def ensure_styles(head: str) -> str:
    for href in DEPRECATED_STYLES:
        head = re.sub(
            rf'\s*<link rel="stylesheet" href="{re.escape(href)}">\n?',
            "\n",
            head,
        )

    missing = [
        href
        for href in REQUIRED_STYLES
        if f'href="{href}"' not in head
    ]
    if not missing:
        return head

    links = "".join(f'  <link rel="stylesheet" href="{href}">\n' for href in missing)
    return head.replace("</head>", links + "</head>", 1)


def splice_page(path: Path, main_html: str) -> None:
    text = path.read_text(encoding="utf-8")
    marker = '        <div class="space-for-header"></div>'
    if marker in text:
        start = text.index(marker)
    else:
        for fallback in (
            '        <section class="ulr-scisan-exact-page"',
            '        <section class="ulr-amanzi-scisan-hero ulr-agri-hero section-gap-x"',
            '        <section class="ulr-amanzi-scisan-hero section-gap-x"',
            '        <section class="tj-page-header section-gap-x"',
        ):
            if fallback in text:
                start = text.index(fallback)
                break
        else:
            raise ValueError("Could not find agri page content start")
    end = text.index('      </main>')
    head, tail = text[:start], text[end:]

    head = ensure_body_classes(ensure_styles(head))

    head = head.replace(
        "<title>Agricultural Biosecurity | SANI-99 for AGRI | Ubuntu Life Resources</title>",
        "<title>SANI-99&trade; for AGRI | Agricultural Biosecurity | Ubuntu Life Resources</title>",
    )

    tail = re.sub(
        r'\s*<script src="assets/js/ulr-agri-scisan\.js" defer></script>\n?',
        "\n",
        tail,
    )
    tail = re.sub(
        r'\s*<script src="assets/js/ulr-amanzi-scisan\.js" defer></script>\n?',
        "\n",
        tail,
    )
    if "ulr-scisan-embed.js" not in tail:
        tail = tail.replace(
            "</body>",
            '  <script src="assets/js/ulr-scisan-embed.js" defer></script>\n</body>',
            1,
        )

    path.write_text(head + main_html + "\n" + tail, encoding="utf-8")


def main() -> None:
    main_html = build_exact_embed_main()
    for page in PAGES:
        splice_page(page, main_html)
        print(f"Updated {page.name} (SciSan iframe embed).")


if __name__ == "__main__":
    main()
