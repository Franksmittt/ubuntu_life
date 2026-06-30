# -*- coding: utf-8 -*-
"""Build pillar-hygiene-sanitation.html matching scisan.co.za/sani-99 layout."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TM = "&trade;"
IMG = "assets/images/pillars/hygiene-sanitation/scisan"
HERO = "assets/images/hero/ulr-hero-hygiene-sanitation.jpg"
PAGE = ROOT / "pillar-hygiene-sanitation.html"
REQUIRED_STYLES = (
    "assets/css/ulr-pillar-brief.css",
    "assets/css/ulr-amanzi-page.css",
    "assets/css/ulr-amanzi-scisan.css",
    "assets/css/ulr-hygiene-scisan.css",
)
DEPRECATED_STYLES = (
    "assets/css/ulr-scisan-embed-shell.css",
    "assets/css/ulr-scisan-embed.css",
)


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


def brochure_btn(label: str, brochure_name: str) -> str:
    return f"""<button type="button" class="tj-primary-btn js-request-brochure" data-brochure-name="{brochure_name}">
<span class="btn-text"><span>{label}</span></span>
<span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
</button>"""


def video_playlist(videos: list[tuple[str, str]]) -> str:
    titles = []
    panels = []
    for i, (title, url) in enumerate(videos, start=1):
        titles.append(
            f"""<div class="e-tab-title e-tab-desktop-title" aria-selected="{"true" if i == 1 else "false"}" data-tab="{i}" role="tab" tabindex="{"0" if i == 1 else "-1"}" aria-controls="ulr-hygiene-tab-{i}">
<h4 class="e-tab-title-text"><button type="button">{title}</button></h4>
</div>"""
        )
        hidden = "" if i == 1 else ' hidden="hidden"'
        active = " ulr-scisan-tab-active" if i == 1 else ""
        panels.append(
            f"""<div id="ulr-hygiene-tab-{i}" class="e-tab-content elementor-clearfix{active}" data-tab="{i}" role="tabpanel" data-video-url="{url}" data-video-type="youtube" data-video-title="{title}"{hidden}>
<div></div>
</div>"""
        )

    return f"""<div class="elementor-widget elementor-widget-video-playlist e-tabs-view-vertical elementor-layout-end">
<div class="e-tabs" role="region" aria-label="SANI-99 video playlist">
<div class="e-tabs-main-area">
<div class="e-tabs-wrapper">
<div class="e-tabs-items-wrapper">
<div class="e-tabs-items" role="tablist">
{"".join(titles)}
</div>
</div>
</div>
<div class="e-tabs-content-wrapper" role="tablist" aria-orientation="vertical">
{"".join(panels)}
</div>
</div>
</div>
</div>"""


def build_main() -> str:
    parts: list[str] = []

    parts.append(f"""        <section class="ulr-amanzi-scisan-hero ulr-hygiene-hero section-gap-x">
          <div class="ulr-amanzi-scisan-hero__bg" style="background-image: url('{HERO}');" aria-hidden="true"></div>
          <div class="ulr-amanzi-scisan-hero__content ulr-hygiene-hero__content">
            <h1 class="ulr-amanzi-scisan-hero__title">
              SANI-<span class="ulr-accent">99</span>{TM}<br>
              <span class="ulr-accent">Medical Grade</span><br>
              Hand &amp; Surface Disinfectant
            </h1>
            <p class="ulr-hygiene-hero__lead">Alcohol and chlorine free hygiene solutions for healthcare, hospitality and industrial settings.</p>
          </div>
        </section>""")

    parts.append(f"""        <section id="better-disinfecting" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Better <span class="ulr-accent">Disinfecting</span></h2>
            <div class="ulr-amanzi-scisan-prose-center">
              <p class="desc"><strong>Most consumers are unaware of the many ways in which disinfectants can harm one&rsquo;s health. By their very nature, all chemical disinfectants are potentially harmful or toxic to living organisms, including humans. While disinfectants are intended to protect us from getting sick, they&rsquo;re a bit of a double-edged sword.</strong></p>
              <p class="desc">Traditional disinfectants often contain volatile organic compounds (VOCs) that have been linked to chronic respiratory problems and other health issues. These compounds can trigger allergies, asthma, and even contribute to the development of cancer and autoimmune diseases. Additionally, they can be harsh on the skin, leading to irritation and damage. In contrast, SANI-99{TM} offers a powerful, medical-grade, and eco-friendly alternative.</p>
              <p class="desc"><strong>&ldquo;SANI-99{TM} targets and eliminates pathogens without alcohol or chlorine. Its potency surpasses bleach by 2,000 times, offering exceptional effectiveness. It is gentle on the skin, and accidents like swallowing or eye contact pose no harm.&rdquo;</strong></p>
              <p class="desc mb-0">With SANI-99{TM}, you have access to an extraordinary level of protection. Achieving a minimum 7-log reduction of 99.99995%, SANI-99{TM} stands as the pinnacle of non-alcohol-based disinfectants. Its unrivaled potency ensures a thorough and effective elimination of pathogens.</p>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section class="ulr-amanzi-band ulr-amanzi-band--tight section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="ulr-amanzi-scisan-wheel">
              {figure(src('SANI-99-BENEFITS-WHEEL-5-1024x1024.png'), 'SANI-99 benefits wheel')}
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="features" class="ulr-amanzi-band ulr-amanzi-scisan-dark section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading"><span>Key</span> Features</h2>
            <div class="ulr-hygiene-kf-strip my-4">
              <img src="{src('Key-features-icon-1024x152-1.png')}" alt="SANI-99 key features icons" loading="lazy" decoding="async">
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="sectors" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="ulr-amanzi-prose ulr-amanzi-prose--wide">
              <p class="desc">SANI-99{TM} plays a pivotal role in ensuring cleanliness and hygiene across various sectors. Its advanced formulation has positioned it as a cornerstone of sanitation protocols in critical industries such as healthcare facilities, food industries, education, hospitality, public transportation, and office spaces.</p>
              <p class="desc mb-0">In healthcare settings, SANI-99{TM} contributes to maintaining sterile and safe environments, safeguarding patients, medical personnel, and visitors from harmful pathogens. In the food industry, it upholds rigorous sanitation standards to prevent foodborne illnesses, ensuring consumer safety. Educational institutions benefit from SANI-99{TM} by creating clean and infection-free environments conducive to learning. Moreover, the hospitality sector relies on its potent disinfection capabilities to provide guests with a reassuringly hygienic experience. Even in high-traffic environments like public transportation, SANI-99{TM} helps curb the spread of germs, fostering safe travel conditions. Offices and fitness centres also implement SANI-99{TM} to cultivate healthy spaces for employees and clients alike.</p>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="standards" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Standards &amp; <span class="ulr-accent">Certifications</span></h2>
            <div class="ulr-amanzi-scisan-flips">
              {flip_card(
                  "BACTERIA",
                  f"SANI-99{TM} is effective in destroying Bacteria, Fungi and Protozoa.",
                  flip_list([
                      "E.coli",
                      "Staphylococcus",
                      "Enterococcus hirae",
                      "Pseudomonas aeruginosa",
                      "Salmonella",
                      "Listeria",
                  ]),
              )}
              {flip_card(
                  "VIRUSES",
                  f"SANI-99{TM} has been tested and proven to be effective in destroying enveloped viruses.",
                  flip_list([
                      "Corona Viruses &amp; SARS-CoV-2",
                      "Ebola",
                      "Influenza",
                      "Measles",
                      "Rabies",
                      "Herpesviridae",
                      "Hepatitis B,C,D",
                      "Flavivirus",
                  ]),
              )}
              {flip_card(
                  "STANDARDS",
                  f"SANI-99{TM} has passed European Standard EN, ilac.MRA/SANAS laboratory tests.",
                  flip_list([
                      "EN1276",
                      "EN13697",
                      "EN14476:2013 + A2:2019",
                      "EN1500",
                      "EN14349",
                      "BS EN 1040:2005",
                      "BS EN 13727:2012 + A2:2015",
                  ]),
              )}
            </div>
            <div class="mt-4">
              {figure(src('Standards-ic.png'), 'SANI-99 standards and certifications', 'ulr-amanzi-figure--flush')}
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="log-reduction" class="ulr-amanzi-band ulr-amanzi-band--alt section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">What is <span class="ulr-accent">Log Reduction?</span></h2>
            <div class="ulr-amanzi-prose ulr-amanzi-prose--wide">
              <p class="desc"><strong>When it comes to infection control, measuring the effectiveness of a product in reducing pathogens is crucial. This effectiveness is often expressed through &lsquo;Log Reductions&rsquo;, which indicate the degree to which bacteria and other infectious agents are eliminated. The higher the log reduction, the more effective the product is at killing these pathogens. With SANI-99{TM}, you can trust in its outstanding performance, as it achieves a remarkable 7-Log reduction, resulting in a pathogenic reduction of 99.99995%.</strong></p>
              <p class="desc">What sets SANI-99{TM} apart is its long-lasting impact. Unlike many other products, SANI-99{TM} doesn&rsquo;t evaporate quickly. Instead, it remains on surfaces and hands for extended periods, ensuring continuous protection. In fact, SANI-99{TM} has been rigorously tested following the European standard EN lab protocol, and the results are impressive. It has been confirmed that SANI-99{TM} effectively eliminates pathogenic bacteria in just 10 seconds, providing rapid and reliable protection. Even for stubborn contaminants, SANI-99{TM} delivers exceptional results within a span of 5 minutes.</p>
            </div>
            {figure(src('Log-Rating-Chart.webp'), 'SANI-99 log reduction chart', 'ulr-amanzi-figure--flush')}
            <p class="desc mt-3 mb-0">With its high log reduction and long-lasting effect, SANI-99{TM} surpasses expectations in infection control. It not only eliminates pathogens effectively but also provides sustained protection, giving you peace of mind in various environments. Trust in SANI-99{TM} to deliver the superior performance you need for a safer and healthier environment.</p>
          </div>
        </section>""")

    parts.append(f"""        <section id="legionella" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Advanced Disinfection for <span class="ulr-accent">Legionella Control</span></h2>
            <div class="ulr-amanzi-prose ulr-amanzi-prose--wide">
              <p class="desc"><strong>SANI-99{TM} offers an innovative solution to tackle Legionella pneumophila</strong>, a dangerous waterborne pathogen responsible for Legionnaires&rsquo; disease. Common in environments like cooling towers, spa pools, and complex plumbing systems, Legionella presents a severe health risk if not managed effectively. Traditional methods such as chlorination often fail to address the bacterium&rsquo;s resilience within biofilms, protective layers that allow Legionella to survive even after treatment.</p>
              <p class="desc"><strong>Why Choose SANI-99{TM} for Legionella Control?</strong></p>
              <ul class="desc">
                <li><strong>Penetrates and Dismantles Biofilms:</strong> Unlike conventional disinfectants, SANI-99{TM} breaks down biofilms, ensuring comprehensive eradication of Legionella bacteria.</li>
                <li><strong>Proven Effectiveness:</strong> Scientific studies demonstrate SANI-99{TM}&rsquo;s capability to eliminate Legionella colonies entirely, achieving complete disinfection in as little as 10 days.</li>
                <li><strong>Residual Protection:</strong> The unique formula prevents bacterial regrowth, offering long-lasting safety for water systems.</li>
                <li><strong>Environmentally Friendly:</strong> Free from harsh chemicals, SANI-99{TM} is biodegradable and safe for both users and the environment.</li>
                <li><strong>Cost-Effective:</strong> Its high efficacy and long-lasting effects reduce the need for frequent applications, lowering maintenance costs.</li>
              </ul>
            </div>
            {figure(src('banner-with-images-1024x527.jpg'), 'SANI-99 Legionella control applications', 'ulr-amanzi-figure--flush my-4')}
            <p class="desc"><strong>Applications for Legionella Treatment</strong></p>
            <p class="desc">SANI-99{TM} can be seamlessly integrated into various water systems, including:</p>
            <ul class="desc">
              <li><strong>Cooling Towers:</strong> Removes biofilms and ensures optimal water quality.</li>
              <li><strong>Cold &amp; Hot Water Storage Tanks:</strong> Maintains safe water supplies by eliminating contamination risks.</li>
              <li><strong>Spas, Pools, and Commercial Water Systems:</strong> Provides peace of mind with effective pathogen control.</li>
            </ul>
            <p class="desc"><strong>Certified Compliance</strong></p>
            <p class="desc">SANI-99{TM} meets stringent European standards, including EN1276, EN13697, and EN13727, ensuring its effectiveness and safety for use in healthcare, hospitality, and industrial settings.</p>
            <p class="desc">For detailed guidance, applications, and compliance information, request the full brochure below:</p>
            <div class="ulr-amanzi-actions mt-3">
              {brochure_btn("Request the SANI-99 Legionella Control Brochure", "SANI-99 Legionella Control Brochure")}
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="black-mould" class="ulr-amanzi-band ulr-amanzi-band--alt section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Unmatched Treatment for <span class="ulr-accent">Black Mould Control</span></h2>
            <div class="ulr-amanzi-prose ulr-amanzi-prose--wide">
              <p class="desc">SANI-99{TM} provides an innovative solution to tackle black mould, a persistent and harmful problem in damp and poorly ventilated environments. Common in areas like basements, bathrooms, kitchens, and HVAC systems, black mould poses serious health risks, including respiratory issues and allergies, while also compromising structural integrity. Traditional methods often fail to eliminate mould spores completely or prevent regrowth, leaving spaces vulnerable to recurring contamination.</p>
              <p class="desc"><strong>Why Choose SANI-99{TM} for Black Mould Treatment?</strong></p>
              <ul class="desc">
                <li><strong>Deep Penetration and Spore Elimination:</strong> SANI-99{TM} targets and eradicates mould at its source, breaking down spores to ensure thorough treatment.</li>
                <li><strong>Prevents Regrowth:</strong> Its unique formula creates a protective barrier, stopping mould from returning even in damp conditions.</li>
                <li><strong>Proven Effectiveness:</strong> Scientifically validated to eliminate 99.99995% of mould spores, SANI-99{TM} delivers superior results in both residential and commercial environments.</li>
                <li><strong>Residue-Free and Safe:</strong> Unlike harsh chemical treatments, SANI-99{TM} leaves no harmful residues, protecting surfaces and maintaining a safe space for occupants.</li>
                <li><strong>Eco-Friendly Solution:</strong> Chlorine-free, alcohol-free, and biodegradable, SANI-99{TM} is designed to minimise environmental impact while delivering powerful results.</li>
                <li><strong>Cost-Effective:</strong> Long-lasting protection reduces the need for frequent applications, lowering maintenance costs and improving efficiency.</li>
              </ul>
            </div>
            {figure(src('housekeeper-s-hand-with-glove-cleaning-mold-from-w-2023-11-27-04-54-12-utc-scaled-1-1024x576.jpg'), 'Black mould treatment with SANI-99', 'ulr-amanzi-figure--flush my-4')}
            <p class="desc"><strong>Applications for Black Mould Treatment</strong></p>
            <p class="desc">SANI-99{TM} is ideal for mould-prone environments, including:</p>
            <ul class="desc">
              <li><strong>Bathrooms and Wet Areas:</strong> Eradicates mould from tiles, grout, and fixtures to maintain hygiene and safety.</li>
              <li><strong>Basements and Crawl Spaces:</strong> Addresses mould in poorly ventilated areas, preventing damage to infrastructure and stored items.</li>
              <li><strong>HVAC Systems:</strong> Cleans ducts and vents to stop the spread of mould spores and improve air quality.</li>
              <li><strong>Commercial Kitchens and Food Storage:</strong> Maintains safe conditions in damp environments where mould threatens health and hygiene.</li>
            </ul>
            <p class="desc"><strong>Certified Compliance</strong></p>
            <p class="desc">SANI-99{TM} meets stringent European standards, including EN 13697 and EN 1656, certifying its fungicidal efficacy and safety for use in a wide range of settings.</p>
            <p class="desc">For detailed guidance, applications, and compliance information, request the full brochure below:</p>
            <div class="ulr-amanzi-actions mt-3">
              {brochure_btn("Request the SANI-99 Black Mould Treatment Brochure", "SANI-99 Black Mould Treatment Brochure")}
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="environment" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Environmentally <span class="ulr-accent">Responsible</span></h2>
            <div class="ulr-amanzi-prose ulr-amanzi-prose--wide">
              <p class="desc"><strong>Traditional alcohol-based disinfectants and sanitisers have contributed significantly to the global plastic bottle pollution crisis. Recognising this issue, SANI-99{TM} was purposefully developed in powder form to address the environmental impact. With SANI-99{TM}, we have taken a proactive approach to minimise plastic waste.</strong></p>
              <p class="desc">By formulating SANI-99{TM} as a powder, we eliminate the need for pre-mixed solutions in single-use plastic bottles. Instead, our innovative approach allows for easy preparation by simply mixing a 6g sachet with water using our specially designed 1-litre &ldquo;One bottle for Life&rdquo;. This means there is no need to purchase a new bottle each time the disinfectant is replenished &mdash; you can simply refill and reuse the existing bottle.</p>
              <p class="desc">The benefits of SANI-99{TM} extend beyond reducing plastic waste. Compared to transporting pre-mixed disinfectants and sanitisers, the compact size and lightweight nature of our sachets significantly reduce transportation requirements. For instance, transporting 2 million litres of pre-mixed disinfectant would typically require sixty-six 30-ton trucks. In contrast, the same quantity of SANI-99{TM}, equivalent to 2 million litres, can be transported using just one 30-ton truck. This substantial reduction in transportation needs contributes to a significant decrease in carbon emissions and fuel consumption.</p>
            </div>
            <div class="ulr-amanzi-compare mt-4">
              <div class="ulr-amanzi-compare__col">
                {figure(src('sani-truck-2.png'), '66 trucks for pre-mixed disinfectant transport')}
                <h3 class="sec-title h4 text-center mt-2">66 <span class="ulr-accent">Trucks</span></h3>
                <p class="desc text-center mb-0">Transportation requirements for <strong>2 million litres</strong> of <strong>pre-mixed disinfectant</strong></p>
              </div>
              <div class="ulr-amanzi-compare__vs" aria-hidden="true">VS</div>
              <div class="ulr-amanzi-compare__col">
                {figure(src('sani-truck-1.png'), '1 truck for SANI-99 transport')}
                <h3 class="sec-title h4 text-center mt-2">1 <span class="ulr-accent">Truck</span></h3>
                <p class="desc text-center mb-0">Transportation requirements for <strong>2 million litres</strong> of <strong>SANI-99{TM}</strong> disinfectant</p>
              </div>
            </div>
            <p class="desc mt-4">The COVID-19 pandemic has led to an alarming five-fold increase in plastic bottle contamination, resulting in hundreds of millions of additional bottles polluting our planet in just one year. At our organisation, we acknowledge the severity of the climate crisis and our responsibility to take action against the harmful effects of plastic waste on our environment. That&rsquo;s why we have taken deliberate steps to design our medical-grade hand and surface disinfectant with a focus on reducing and, wherever possible, eliminating plastic bottle contamination.</p>
            <p class="desc mb-0">With our <strong>&ldquo;One bottle for Life&rdquo;</strong> principle, we are committed to both caring for people and preserving the environment. This achievement is a source of immense pride for us. By embracing this principle, you can ensure that as long as you possess a SANI-99{TM} disinfectant sachet and access to water, you will always have a powerful and effective disinfectant at your disposal.</p>
          </div>
        </section>""")

    chars = [
        ("SANI-Sachet-Lable-2-150x150.webp", "Triple foil sachet", ["Triple Foil", "HIGH QUALITY", "SACHET"]),
        ("1-Litre-Lable-1-146x150.webp", "1 litre treatment", ["1 Sachet =", "1 LITRE"]),
        ("Medical-Grade-Lable-150x150.webp", "Medical grade disinfectant", ["Medical Grade", "DISINFECTANT"]),
        ("LOG-7-Lable-1.webp", "7 log efficacy", ["Unbeatable", "EFFICACY"]),
        ("Affordable-label.webp", "Affordable pricing", ["Affordable", "COMPETITIVELY", "PRICED"]),
        ("Carbon-Footprint-Label-1-150x150.webp", "Lightweight powder", ["Powder Solution", "LIGHTWEIGHT", "TO TRANSPORT"]),
    ]
    parts.append(f"""        <section id="characteristics" class="ulr-amanzi-band ulr-amanzi-scisan-dark section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading"><span>Key</span> Characteristics</h2>
            <div class="ulr-amanzi-scisan-kf">
              {"".join(kf_item(*item) for item in chars)}
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="instructions" class="ulr-amanzi-band ulr-amanzi-band--tint section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Instructions <span class="ulr-accent">for Use</span></h2>
            <p class="desc ulr-amanzi-prose--wide">To prepare the solution, use the &ldquo;One Bottle for Life&rdquo; and dilute the contents of one sachet (6g) in 1 litre of water. After use, remember to turn the nozzle to the OFF position to prevent any accidental leakage or spills. For proper storage, keep the container upright in a cool, dry place away from direct sunlight. Avoid exposing to high temperatures; store at room temperature to maintain effectiveness.</p>
            <div class="my-4">
              {figure(src('Instructions-for-Use-June-23-white-bg-2-1024x307.webp'), 'SANI-99 instructions for use', 'ulr-amanzi-figure--flush')}
            </div>
            <p class="desc mb-0"><em>*Human error accounts for approximately 85% of low disinfecting efficacy results. When applying a disinfectant, the user must carefully follow instructions to ensure optimum results. For other dosages please refer to packaging.</em></p>
          </div>
        </section>""")

    videos = [
        ("Dental Practice Disinfection with SANI-99", "https://youtu.be/YD9NO4fp2Ao"),
        ("SANI-99 Food Processing Disinfection Demo with Marzelle", "https://youtu.be/iqwii9eqxIM"),
        ("How to Disinfect Surfaces and Carcasses in a Butchery", "https://youtu.be/Spj4-URaZPA"),
        ("SANI-99 — Food-Safe Disinfection for Every Home", "https://youtu.be/x_g518tHiT0"),
    ]
    parts.append(f"""        <section id="videos" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner ulr-hygiene-video">
            <h2 class="sec-title ulr-amanzi-heading">Video <span class="ulr-accent">Playlist</span></h2>
            {video_playlist(videos)}
          </div>
        </section>""")

    parts.append(f"""        <section id="comparison" class="ulr-amanzi-band ulr-amanzi-band--alt section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="ulr-amanzi-scisan-vs-head">
              <h3 class="sec-title h5 mb-0">Alcohol Based <span class="ulr-accent">Disinfectants</span></h3>
              <div class="ulr-amanzi-scisan-vs-head__mid">VS</div>
              <div class="d-flex align-items-center gap-3">
                <img src="{src('sani-logo-199x300-1.png')}" alt="SANI-99" width="80" height="120" loading="lazy" decoding="async">
                <h3 class="sec-title h5 mb-0">SANI-99{TM}</h3>
              </div>
            </div>
            {figure(src('Vs-graphic.webp'), 'Alcohol based disinfectants versus SANI-99 comparison', 'ulr-amanzi-figure--flush')}
          </div>
        </section>""")

    parts.append(f"""        <section id="products" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Product <span class="ulr-accent">Range</span></h2>
            <p class="desc text-center ulr-amanzi-scisan-prose-center">Take a moment to explore our range of SANI-99{TM} products. We continuously update our brochure to ensure you have the latest information on our offerings. Stay connected by visiting this page and following us on social media, as we frequently introduce new products and promotions to keep you informed and engaged.</p>
            <p class="desc text-center ulr-amanzi-scisan-prose-center">If you have any questions or need further information, our FAQ section is a valuable resource that provides detailed answers to common queries. Alternatively, feel free to reach out to us directly. Our team is ready to assist you and demonstrate how SANI-99{TM} can revolutionise your disinfectant and sanitation requirements.</p>
            <div class="ulr-amanzi-scisan-product-banner my-4">
              <img src="{src('sani-all-products-222-1.jpg')}" alt="SANI-99 product range" loading="lazy" decoding="async">
            </div>
            <div class="ulr-amanzi-actions">
              <button type="button" class="tj-primary-btn js-request-brochure" data-brochure-name="SANI-99 Brochure">
                <span class="btn-text"><span>Request a brochure</span></span>
                <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
              </button>
              <a class="tj-primary-btn tj-primary-btn--outline" href="contact.html">
                <span class="btn-text"><span>Contact us</span></span>
                <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
              </a>
            </div>
          </div>
        </section>""")

    return "\n".join(parts)


def ensure_body_classes(head: str) -> str:
    match = re.search(r'<body class="([^"]*)">', head)
    if not match:
        return head

    classes = [
        cls
        for cls in match.group(1).split()
        if cls not in {"ulr-rich-subpage", "ulr-scisan-embed-page", "ulr-amanzi-scisan"}
    ]
    for required in ("ulr-pillar-page", "ulr-amanzi-page", "ulr-hygiene-scisan"):
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
    for marker in (
        '        <section class="ulr-scisan-exact-page"',
        '        <section class="ulr-amanzi-scisan-hero section-gap-x"',
        '        <section class="ulr-amanzi-scisan-hero ulr-hygiene-hero section-gap-x"',
        '        <section class="tj-page-header section-gap-x"',
    ):
        if marker in text:
            start = text.index(marker)
            break
    else:
        raise ValueError("Could not find hygiene page content start")
    end = text.index('      </main>')
    head, tail = text[:start], text[end:]

    head = ensure_body_classes(ensure_styles(head))

    tail = re.sub(
        r'\s*<script src="assets/js/ulr-scisan-embed\.js" defer></script>\n?',
        "\n",
        tail,
    )
    tail = re.sub(
        r'\s*<script src="assets/js/ulr-hygiene-scisan\.js" defer></script>\n?',
        "\n",
        tail,
    )
    tail = re.sub(
        r'\s*<script src="assets/js/ulr-amanzi-scisan\.js" defer></script>\n?',
        "\n",
        tail,
    )
    tail = re.sub(
        r'\s*<script src="assets/js/ulr-scisan-playlist\.js" defer></script>\n?',
        "\n",
        tail,
    )
    script = (
        '  <script src="assets/js/ulr-amanzi-scisan.js" defer></script>\n'
        '  <script src="assets/js/ulr-scisan-playlist.js" defer></script>'
    )
    tail = tail.replace("</body>", f"{script}\n</body>", 1)

    path.write_text(head + main_html + "\n" + tail, encoding="utf-8")


def main() -> None:
    main_html = build_main()
    splice_page(PAGE, main_html)
    print(f"Updated {PAGE.name} (native hygiene layout).")


if __name__ == "__main__":
    main()
