# -*- coding: utf-8 -*-
"""Generate SANI AMANZI blog listing and article pages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "about.html"
POST_SLUG = "blog-sani-amanzi-point-of-use-water.html"
HERO = "assets/images/pillars/sani-amanzi/ulr-sani-amanzi-opening.jpg"
WHEEL = "assets/images/pillars/sani-amanzi/scisan/SANI-AMANZI-Benefits-Wheel-1.png"
TRUCKS = "assets/images/pillars/sani-amanzi/scisan/amazi-trusk-2.png"


def shell_parts() -> tuple[str, str]:
    text = SHELL.read_text(encoding="utf-8")
    main_start = text.index('      <main id="primary" class="site-main">')
    footer_start = text.index("      <!-- start: Footer Section -->")
    head = text[:main_start]
    tail = text[footer_start:]
    tail = tail.replace(
        '<li><a href="about.html">Company profile</a></li>',
        '<li><a href="about.html">Company profile</a></li>\n                    <li><a href="blog.html">Insights</a></li>',
    )
    head = head.replace(
        'body class="ulr-rich-subpage"',
        'body class="ulr-rich-subpage ulr-blog-page"',
    )
    if "ulr-blog.css" not in head:
        head = head.replace(
            '  <link rel="stylesheet" href="assets/css/ulr-phase-gate.css">',
            '  <link rel="stylesheet" href="assets/css/ulr-phase-gate.css">\n  <link rel="stylesheet" href="assets/css/ulr-blog.css">',
        )
    return head, tail


def page_header(title: str, lead: str, crumb: str, bg: str = HERO) -> str:
    return f"""        <div class="space-for-header"></div>
        <section class="tj-page-header section-gap-x" data-bg-image="{bg}">
          <div class="container position-relative" style="z-index:2;">
            <div class="row">
              <div class="col-lg-12">
                <div class="tj-page-header-content text-center">
                  <h1 class="tj-page-title">{title}</h1>
                  <p class="pillar-header-lead">{lead}</p>
                  <div class="tj-page-link">
                    <span><i class="tji-home"></i></span>
                    <span><a href="index.html">Home</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><a href="blog.html">Insights</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><span>{crumb}</span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="page-header-overlay ulr-pheader-overlay" aria-hidden="true"></div>
        </section>"""


def build_listing() -> str:
    head, tail = shell_parts()
    head = head.replace(
        "<title>Company profile | Ubuntu Life Resources</title>",
        "<title>Insights | Ubuntu Life Resources</title>",
    ).replace(
        'content="Contact Ubuntu Life Resources for market entry, commercial representation, and partnership enquiries across Africa."',
        'content="Insights on water purification, food security, and agricultural biosecurity from Ubuntu Life Resources."',
    )
    main = f"""      <main id="primary" class="site-main">
{page_header("Insights", "Practical perspectives on clean water, food security, and biosecurity across Africa.", "Insights", "assets/images/about/ulr-about-field-operations.jpg")}

        <section class="tj-blog-section section-gap">
          <div class="container">
            <div class="row mb-4">
              <div class="col-lg-8">
                <div class="sec-heading">
                  <span class="sub-title"><i class="tji-strategy"></i> Latest</span>
                  <h2 class="sec-title">From the <span>field</span></h2>
                  <p class="desc mb-0">Updates, explainers, and programme notes from the Ubuntu Life Resources team.</p>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-4 col-md-6">
                <article class="blog-item wow fadeInUp" data-wow-delay=".1s">
                  <div class="blog-thumb">
                    <a href="{POST_SLUG}"><img src="{HERO}" alt="Hands holding clean water after SANI AMANZI treatment."></a>
                  </div>
                  <div class="blog-content">
                    <div class="blog-meta mb-2">
                      <span>3 June 2026</span>
                      <span class="categories"><a href="{POST_SLUG}">Water purification</a></span>
                    </div>
                    <h3 class="title"><a href="{POST_SLUG}">SANI AMANZI&trade;: point-of-use water purification when piped supply is not enough</a></h3>
                    <p class="desc">Why chlorine-free powder sachets matter for households, NGOs, and emergency programmes — and how one 6&nbsp;g sachet treats 20&nbsp;litres at the point of use.</p>
                    <a class="text-btn" href="{POST_SLUG}">
                      <span class="btn-text"><span>Read article</span></span>
                      <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                    </a>
                  </div>
                </article>
              </div>
            </div>
          </div>
        </section>

        <section class="tj-cta-section section-gap-x">
          <div class="container">
            <div class="row">
              <div class="col-12">
                <div class="cta-area">
                  <div class="cta-content text-center">
                    <h2 class="title">Need a water programme conversation?</h2>
                    <p class="desc">Speak to Ubuntu Life Resources about SANI AMANZI&trade; supply, documentation, and deployment support.</p>
                    <a class="tj-primary-btn" href="contact.html">
                      <span class="btn-text"><span>Contact us</span></span>
                      <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
"""
    return head + main + tail


def build_article() -> str:
    head, tail = shell_parts()
    head = head.replace(
        "<title>Company profile | Ubuntu Life Resources</title>",
        "<title>SANI AMANZI&trade; Point-of-Use Water Purification | Ubuntu Life Resources</title>",
    ).replace(
        'content="Contact Ubuntu Life Resources for market entry, commercial representation, and partnership enquiries across Africa."',
        'content="SANI AMANZI is a chlorine-free point-of-use water purifier: one 6g sachet treats 20 litres. Learn how it supports safe drinking water in Africa."',
    )
    article = f"""      <main id="primary" class="site-main">
{page_header(
    "SANI AMANZI&trade;: point-of-use water purification when piped supply is not enough",
    "A practical look at safe drinking water where infrastructure gaps, contamination events, and emergency response all meet the same household bucket.",
    "SANI AMANZI&trade;",
)}

        <section class="section-gap pt-0">
          <div class="container">
            <div class="row justify-content-center">
              <div class="col-lg-10">
                <article class="post-details-wrapper">
                  <div class="ulr-blog-meta">
                    <time datetime="2026-06-03">3 June 2026</time>
                    <span class="ulr-blog-tag">Water purification</span>
                    <span>By Ubuntu Life Resources</span>
                  </div>

                  <div class="blog-images">
                    <img src="{HERO}" alt="Clean water held in cupped hands after treatment." class="w-100">
                  </div>

                  <div class="blog-text">
                    <p class="lead desc"><strong>More than two billion people live in water-stressed countries. Nearly 900 million still lack reliable access to clean drinking water.</strong> That is not a distant statistic — it is the daily reality in many of the communities, municipalities, and humanitarian corridors Ubuntu Life Resources works in across Southern Africa and selected Sub-Saharan markets.</p>

                    <p>Contaminated water remains one of the most preventable killers on the planet. Cholera, diarrhoea, dysentery, hepatitis A, typhoid, and polio still travel through unsafe sources long after a pipeline map says a village is "connected." When boreholes fail, trucks are late, or floods overwhelm treatment works, the last metre of protection often happens at the <strong>point of use</strong> — in the home, the clinic, the school, or the emergency camp.</p>

                    <p>That is where <strong>SANI AMANZI&trade;</strong> is designed to perform: a chlorine-free powder water purifier packaged in a triple-foil sachet, built for field conditions where simplicity, traceability, and transport efficiency matter as much as laboratory efficacy.</p>

                    <blockquote>
                      "Everyone has the right to sufficient, continuous, safe, acceptable, physically accessible, and affordable water for personal and domestic use."
                      <cite>United Nations — resolution on the human right to water and sanitation</cite>
                    </blockquote>

                    <h3>What SANI AMANZI&trade; is — and what problem it solves</h3>
                    <p>SANI AMANZI&trade; is a point-of-use (POU) water sanitising and purification solution. One <strong>6&nbsp;g powder sachet treats 20&nbsp;litres</strong> of contaminated water using a blend of safe active ingredients that target waterborne pathogenic bacteria — including strains associated with antibiotic resistance — without relying on chlorine.</p>
                    <p>For programme managers, the format matters as much as the chemistry:</p>
                    <ul class="ulr-blog-highlight">
                      <li><strong>Lightweight sachets</strong> reduce transport volume compared with bottled water or liquid purifiers — one truck of SANI AMANZI&trade; can support purification at a scale that would require dozens of trucks if the same volume were moved as bottled water.</li>
                      <li><strong>Precise dosing</strong> helps prevent overdose and supports repeatable field protocols across large volunteer networks.</li>
                      <li><strong>Plastic-free packaging philosophy</strong> aligns with climate-conscious procurement — powder replaces liquid bottles wherever possible.</li>
                    </ul>

                    <figure class="ulr-blog-figure">
                      <img src="{WHEEL}" alt="Diagram of SANI AMANZI benefits including pathogen reduction, affordability, and environmental impact.">
                      <figcaption>SANI AMANZI&trade; combines pathogen control, affordability, and lower transport footprint in a single point-of-use format.</figcaption>
                    </figure>

                    <h3>Tested to recognised drinking-water standards</h3>
                    <p>SANI AMANZI&trade; has been evaluated by accredited SANAS laboratories against <strong>SANS 241-1:2015</strong> drinking water requirements and the <strong>WRC Domestic Use Standard</strong> classification framework. Treated samples demonstrated physical, chemical, and bacteriological qualities suitable for potable and domestic use. The Water Research Commission classified treated water as <strong>"Good Water Quality" (Class 1)</strong> — suitable for lifetime use with rare sub-clinical effects.</p>
                    <p>Ubuntu Life Resources shares this transparently because no point-of-use product can honestly promise perfect clarification on every source, every time, regardless of pH and local chemistry. What SANI AMANZI&trade; is engineered for — and what field testing across highly contaminated South African sources supports — is a core goal of eliminating <strong>99.99% of waterborne pathogenic bacteria</strong> when used as directed.</p>

                    <h3>Five steps in the field</h3>
                    <p>Training teams and community health workers on a consistent protocol builds trust faster than handing out anonymous bottles:</p>
                    <ol>
                      <li>Use a <strong>clean container</strong> and fill with up to 20&nbsp;litres of source water.</li>
                      <li>Add <strong>one 6&nbsp;g sachet</strong> and stir thoroughly until the powder is dissolved.</li>
                      <li>Allow the water to <strong>stand for 30 minutes</strong> so active ingredients can neutralise pathogens.</li>
                      <li>Filter through a <strong>clean, tightly woven cloth</strong> — do not disturb sediment at the bottom of the container.</li>
                      <li>Decant the treated water for drinking and cooking; <strong>do not consume coagulants or precipitate</strong> that settle out during treatment.</li>
                    </ol>
                    <p><em>Safety reminder:</em> do not mix SANI AMANZI&trade; with other disinfectants, acids, ammonia, or sanitisers. Avoid eye contact with dry powder and never ingest undiluted product.</p>

                    <figure class="ulr-blog-figure">
                      <img src="{TRUCKS}" alt="Illustration comparing transport efficiency of SANI AMANZI sachets versus bottled water.">
                      <figcaption>Powder sachets dramatically reduce the number of truck movements required to deliver equivalent purification capacity.</figcaption>
                    </figure>

                    <h3>Who should be planning with SANI AMANZI&trade; on the shelf</h3>
                    <p>SANI AMANZI&trade; is intended for governments, NGOs, humanitarian agencies, and institutional buyers running household- or community-level water programmes — including disaster response when flooding, drought, infrastructure failure, or municipal interruptions cut safe supply.</p>
                    <p>Reserve stock logic is straightforward: lightweight units store compactly, ship quickly, and scale from a single household bucket to regional emergency depots without re-engineering the treatment method.</p>

                    <h3>Working with Ubuntu Life Resources</h3>
                    <p>Ubuntu Life Resources connects SANI AMANZI&trade; with the commercial and documentation layer programme teams actually need — named product lines, brochure and technical packs, stakeholder introductions, and supply conversations aligned to Southern Africa and selected Sub-Saharan procurement realities.</p>
                    <p>For the full product story — features, certifications, instructions, FAQs, and product range — visit our <a href="pillar-water-purification.html">water purification solutions</a> page or request the SANI AMANZI brochure using the button below.</p>

                    <div class="p-4 p-md-5 mt-4 border rounded-3 bg-light">
                      <h4 class="mb-3">Partner on clean water programmes</h4>
                      <p class="mb-2"><strong>Sanchia-Lynn Smit</strong> · CEO / Founder</p>
                      <p class="mb-1"><a href="mailto:sanchia@ubuntuliferesources.co.za">sanchia@ubuntuliferesources.co.za</a></p>
                      <p class="mb-3"><a href="tel:+27796588189">+27 79 658 8189</a></p>
                      <div class="d-flex flex-wrap gap-3">
                        <button type="button" class="tj-primary-btn js-request-brochure" data-brochure-name="SANI AMANZI Brochure">
                          <span class="btn-text"><span>Request a brochure</span></span>
                          <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                        </button>
                        <a class="tj-primary-btn" href="contact.html">
                          <span class="btn-text"><span>Get in touch</span></span>
                          <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                        </a>
                        <a class="tj-primary-btn tj-primary-btn--outline" href="pillar-water-purification.html">
                          <span class="btn-text"><span>Explore SANI AMANZI&trade;</span></span>
                          <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                        </a>
                      </div>
                    </div>

                    <p class="ulr-blog-back mb-0"><a class="text-btn" href="blog.html"><span class="btn-text"><span>Back to insights</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a></p>
                  </div>
                </article>
              </div>
            </div>
          </div>
        </section>
      </main>
"""
    return head + article + tail


def main() -> None:
    (ROOT / "blog.html").write_text(build_listing(), encoding="utf-8")
    (ROOT / POST_SLUG).write_text(build_article(), encoding="utf-8")
    print(f"Wrote blog.html and {POST_SLUG}")


if __name__ == "__main__":
    main()
