# -*- coding: utf-8 -*-
"""Build pillar-water-purification.html matching scisan.co.za/sani-amanzi layout."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TM = "&trade;"
IMG = "assets/images/pillars/sani-amanzi/scisan"
HERO = "assets/images/pillars/sani-amanzi/cleanwater.jpg"


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


def flip_card(title: str, front: str, back_title: str, back: str) -> str:
    return f"""<button type="button" class="ulr-amanzi-scisan-flip" aria-label="{title} — tap to flip">
<div class="ulr-amanzi-scisan-flip__inner">
<div class="ulr-amanzi-scisan-flip__face ulr-amanzi-scisan-flip__face--front">
<h3 class="ulr-amanzi-scisan-flip__title">{title}</h3>
<p>{front}</p>
</div>
<div class="ulr-amanzi-scisan-flip__face ulr-amanzi-scisan-flip__face--back">
<h3 class="ulr-amanzi-scisan-flip__title">{back_title}</h3>
<p>{back}</p>
</div>
</div>
</button>"""


def faq_item(q: str, a: str) -> str:
    return f"""<details class="ulr-amanzi-faq__item">
<summary class="ulr-amanzi-faq__question">{q}</summary>
<div class="ulr-amanzi-faq__answer">
<p>{a}</p>
</div>
</details>"""


def build_main() -> str:
    parts: list[str] = []

    parts.append(f"""        <section class="ulr-amanzi-scisan-hero section-gap-x">
          <div class="ulr-amanzi-scisan-hero__bg" style="background-image: url('{HERO}');" aria-hidden="true"></div>
          <div class="ulr-amanzi-scisan-hero__content">
            <h1 class="ulr-amanzi-scisan-hero__title">
              SANI <span class="ulr-accent">AMANZI</span>{TM}<br>
              <span class="ulr-accent">Water Sanitising</span><br>
              &amp; Purification Solution
            </h1>
          </div>
        </section>""")

    parts.append("""        <section id="caring" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Caring <span class="ulr-accent">for Life</span></h2>
            <div class="ulr-amanzi-scisan-prose-center">
              <p class="desc"><strong>More than 2 billion people are currently trapped in water-stressed countries, while shockingly, a staggering 900 million individuals continue to endure the daily torment of lacking access to clean drinking water. This grim reality signifies that over 1 in every 8 people across the globe is living without this basic necessity.</strong></p>
              <p class="desc">The gravity of this crisis cannot be overstated. Access to safe drinking water is not a luxury but a fundamental human right, essential for our very survival and well-being. What adds to the shock is the stark fact that contaminated water claims more lives than the combined toll of diseases like Malaria, COVID-19, and AIDS. Contaminated water breeds and spreads deadly diseases like Cholera, Diarrhoea, Dysentery, Hepatitis A, Typhoid, and Polio, leaving a trail of suffering and death in its wake.</p>
              <p class="desc"><strong>In line with the United Nations' declaration that "Everyone has the right to sufficient, continuous, safe, acceptable, physically accessible, and affordable water for personal and domestic use," this ongoing water crisis should serve as a resounding wake-up call. It highlights the urgent need for immediate and concerted action to address this dire global issue.</strong></p>
              <p class="desc">Introducing SANI AMANZI&trade;, a cutting-edge point-of-use solution that is not only affordable but also highly practical for all those exposed to contaminated water sources. This innovative product effectively eliminates waterborne pathogenic bacteria through a unique blend of safe active ingredients. Developed by a team of experts deeply knowledgeable about the challenges posed by contaminated water, SANI AMANZI&trade; stands out as the ultimate solution to the clean water crisis. Furthermore, SANI AMANZI&trade; demonstrates exceptional effectiveness against antibiotic-resistant bacteria and successfully eradicates a wide spectrum of pathogenic microbes. What sets this product apart is its ingenious design, incorporating an inorganic, natural, and non-polluting reagent. SANI AMANZI&trade; is poised to revolutionise access to clean water and make a significant impact on global health.</p>
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section class="ulr-amanzi-band ulr-amanzi-band--tight section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="ulr-amanzi-scisan-wheel">
              {figure(src('SANI-AMANZI-Benefits-Wheel-1.png'), 'SANI AMANZI benefits wheel')}
            </div>
          </div>
        </section>""")

    kf = [
        ("f16414_ae1ad229a5e641b5a3805d1e41f8fdc6mv2.webp", "Chlorine free", ["Chlorine", "FREE"]),
        ("f16414_c6013c91828247088426efc4045437camv2.webp", "Kills pathogenic bacteria", ["Kills", "PATHOGENIC", "BACTERIA"]),
        ("q1.png", "Safe for human consumption", ["Safe for Grade", "HUMAN", "CONSUMPTION"]),
        ("q2.png", "Antibiotic resistant bacteria", ["Effective against", "ANTI-BIOTIC", "RESISTANT BACTERIA"]),
        ("q3.png", "Fresh tasting water", ["Fresh", "TASTING", "WATER"]),
        ("q5.png", "One sachet sanitises 20L", ["1 Sachet", "SANITISES", "20L OF WATER"]),
    ]
    parts.append(f"""        <section id="features" class="ulr-amanzi-band ulr-amanzi-scisan-dark section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading"><span>Key</span> Features</h2>
            <div class="ulr-amanzi-scisan-kf">
              {"".join(kf_item(*item) for item in kf)}
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="standards" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Standards &amp; <span class="ulr-accent">Certifications</span></h2>
            <div class="ulr-amanzi-scisan-flips">
              {flip_card(
                  "PATHOGENS",
                  f"SANI-AMANZI{TM} is effective in neutralising Salmonella, Shigella and Cholera in the water and has a sanitising efficacy of 0 (ZERO) E.coli/p/p 100ml.",
                  "PATHOGENS",
                  f"SANI-AMANZI{TM} is effective in neutralising Salmonella, Shigella and Cholera in the water and has a sanitising efficacy of 0 (ZERO) E.coli/p/p 100ml.",
              )}
              {flip_card(
                  "INGREDIENTS",
                  f"SANI-AMANZI{TM} with its technical and scientific formula consists of some ground-breaking ingredients.",
                  "DISEASES",
                  f"SANI-AMANZI{TM} fuels the beneficial bacteria in your gut and has also been proven to have a detoxifying effect that can improve your body's pH balance. It is also safe for human consumption once correctly diluted.",
              )}
              {flip_card(
                  "STANDARDS",
                  f"SANI-AMANZI{TM} has passed the SANS 241-1:2015 – the South African National Standard for Drinking Water.",
                  "STANDARDS",
                  f'SANI-AMANZI{TM} was classified as being of "Good Water Quality" meaning that it is fit for use as potable water and domestic use purposes. It has also been approved by the FDA for use as a household chemical substance.',
              )}
            </div>
          </div>
        </section>""")

    parts.append(f"""        <section id="classification" class="ulr-amanzi-band ulr-amanzi-band--alt section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Water Quality <span class="ulr-accent">Classification</span></h2>
            <div class="ulr-amanzi-prose ulr-amanzi-prose--wide">
              <p class="desc"><strong>SANI AMANZI{TM} has been tested by accredited SANAS laboratories using the SANS 241-1:2015 Drinking Water Standards and the WRC Domestic Use Standard classification system (*see diagram below).</strong></p>
              <p class="desc">After vigorous testing of SANI AMANZI{TM} it was determined that the samples collected and treated displayed physical, chemical and bacteriological qualities that were deemed as fit for use as potable water and for domestic use purposes. The WRC classified SANI AMANZI{TM} as being of "Good Water Quality" (class one); meaning treated water was suitable for life-time use, with rare instances of sub-clinical effects.</p>
              <p class="desc">To gain more insight into the WRC Domestic Use Standard classification system please visit <a href="https://www.wrc.org.za/" target="_blank" rel="noopener noreferrer">www.wrc.org.za</a>.</p>
            </div>
            {figure(src('Catalogue-SANI-AMANZI-5-copy-1-1024x399.webp'), 'WRC Domestic Use Standard classification diagram', 'ulr-amanzi-figure--flush')}
            <p class="desc mt-3"><strong>*The WRC Domestic Use Standard classification system</strong></p>
            <p class="desc">Ubuntu Life Resources and our partners are always striving to achieve breakthrough discoveries in chemistry, to make effective clarification possible every time. Any Point-of-Use product claiming to be 100% successful in the clarification of water every time, irrespective of pH and other chemistry influences, are misleading and false.</p>
            <p class="desc">We take great pride in providing our customers with full transparency, and have tested SANI-AMANZI{TM} on the most contaminated of water sources in South Africa to ensure we meet our efficacy standard goals of eliminating <strong>99.99% of waterborne pathogenic bacteria</strong> and this remains our core goal to this very day.</p>
          </div>
        </section>""")

    parts.append(f"""        <section id="environment" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Environmentally <span class="ulr-accent">Responsible</span></h2>
            <div class="ulr-amanzi-prose ulr-amanzi-prose--wide">
              <p class="desc"><strong>In recognition of the climate crisis and our responsibility to do all we can to reduce the amount of plastic waste harming our environment, SANI AMANZI{TM} has been purposefully designed to reduce, and wherever possible, stop plastic bottle contamination.</strong></p>
              <p class="desc">With our "plastic-free" principle in mind, SANI AMANZI{TM} has been packaged via powder sachet as an alternative to liquid purifiers on the market. All you need is a sachet of SANI AMANZI{TM} and water to fill your bucket and you will have a powerful and environmentally friendly water purifier.</p>
            </div>
            <div class="ulr-amanzi-compare mt-4">
              <div class="ulr-amanzi-compare__col">
                {figure(src('amazi-trusk.png'), '66 trucks for bottled water transport')}
                <h3 class="sec-title h4 text-center mt-2">66 <span class="ulr-accent">Trucks</span></h3>
                <p class="desc text-center mb-0">Transportation requirements for <strong>2 million litres</strong> of <strong>bottled water</strong></p>
              </div>
              <div class="ulr-amanzi-compare__vs" aria-hidden="true">VS</div>
              <div class="ulr-amanzi-compare__col">
                {figure(src('amazi-trusk-2.png'), '1 truck for SANI AMANZI transport')}
                <h3 class="sec-title h4 text-center mt-2">1 <span class="ulr-accent">Truck</span></h3>
                <p class="desc text-center mb-0">Transportation requirements for purifying <strong>40 million litres</strong> of water using <strong>SANI AMANZI{TM}</strong></p>
              </div>
            </div>
            <p class="desc mt-4 mb-0">We do not only believe in eradicating pathogens but also reducing our carbon footprint. By using a SANI AMANZI{TM} sachet as an alternative to bottled water or liquid water purifiers this means that less trucks are required for transportation, thus being more friendly on the environment.</p>
          </div>
        </section>""")

    chars = [
        ("SANI-Sachet-Lable-2-150x150.webp", "Triple foil sachet", ["Triple Foil", "HIGH QUALITY", "SACHET"]),
        ("20-Litre-Lable-1-150x150.webp", "20 litre treatment", ["1 Sachet =", "20 LITRES"]),
        ("POU-Lable-1-150x150.webp", "Point of use purifier", ["Point-of-Use", "PURIFIER"]),
        ("Overdose-lable-150x150.webp", "Precise dosage", ["Precise Dosage", "PREVENTS", "OVERDOSE"]),
        ("Affordable-label-2.webp", "Affordable pricing", ["Affordable", "COMPETITIVELY", "PRICED"]),
        ("Carbon-Footprint-Label-2-150x150.webp", "Lightweight powder", ["Powder Solution", "LIGHTWEIGHT", "TO TRANSPORT"]),
    ]
    parts.append(f"""        <section id="characteristics" class="ulr-amanzi-band ulr-amanzi-scisan-dark section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading"><span>Key</span> Characteristics</h2>
            <div class="ulr-amanzi-scisan-kf">
              {"".join(kf_item(*item) for item in chars)}
            </div>
          </div>
        </section>""")

    instr = [
        ("SANI-AMANZI-Instructions-1.webp", "SANI AMANZI instructions step 1"),
        ("SANI-AMANZI-Instructions-2.webp", "SANI AMANZI instructions step 2"),
        ("SANI-AMANZI-Instructions-3.webp", "SANI AMANZI instructions step 3"),
        ("SANI-AMANZI-Instructions-4.webp", "SANI AMANZI instructions step 4"),
    ]
    instr_html = "".join(
        f'<img src="{src(name)}" alt="{alt}" loading="lazy" decoding="async">'
        for name, alt in instr
    )
    parts.append(f"""        <section id="instructions" class="ulr-amanzi-band ulr-amanzi-band--tint section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Instructions <span class="ulr-accent">for Use</span></h2>
            <p class="desc ulr-amanzi-prose--wide">To treat contaminated water using SANI AMANZI{TM} mix one 6g powder sachet with 20 litres of water, following the instructions provided below. Ensure you use a clean container and thoroughly stir the powder into the contaminated water. Once treatment is complete, use a clean and tightly woven cloth to filter the water. It is important not to filter the sedimentation that has settled at the bottom of the container.</p>
            <div class="ulr-amanzi-scisan-instructions my-4">
              {instr_html}
            </div>
            <p class="desc"><em>Do not combine with other disinfectants, sanitisers, acids, or ammonia. Avoid direct contact with anhydrous powder with your eyes, and never ingest it. Refrain from consuming coagulants or precipitates generated during the sanitization process. It's important to note that every water source possesses its unique chemical composition. The pH level of the water plays a pivotal role in the coagulation process. Additionally, factors like particle size, particle density, liquid density, surface charge, and water chemistry exert significant influences on the settling of fine particles.</em></p>
          </div>
        </section>""")

    parts.append(f"""        <section id="comparison" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">World's Best <span class="ulr-accent">Water Purifier?</span></h2>
            <div class="ulr-amanzi-scisan-vs-head">
              <h3 class="sec-title h5 mb-0">Chlorine Based <span class="ulr-accent">Purifiers</span></h3>
              <div class="ulr-amanzi-scisan-vs-head__mid">VS</div>
              <h3 class="sec-title h5 mb-0">SANI AMANZI{TM} <span class="ulr-accent">Purifier</span></h3>
            </div>
            {figure(src('Catalogue-SANI-AMANZI-3-copy-1-1024x768.webp'), 'SANI AMANZI versus chlorine-based purifiers comparison', 'ulr-amanzi-figure--flush')}
          </div>
        </section>""")

    parts.append(f"""        <section id="products" class="ulr-amanzi-band ulr-amanzi-band--alt section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Product <span class="ulr-accent">Range</span></h2>
            <p class="desc text-center ulr-amanzi-scisan-prose-center">Please take your time to browse our range of SANI AMANZI{TM} products. Our catalogue is constantly being updated so please keep an eye on this page and our social media platforms to be sure you stay in the loop with new products and promotions.</p>
            <div class="ulr-amanzi-scisan-product-banner my-4">
              <img src="{src('amanzi-bottom-1024x477.jpg')}" alt="SANI AMANZI product range" loading="lazy" decoding="async">
            </div>
            <div class="ulr-amanzi-actions">
              <button type="button" class="tj-primary-btn js-request-brochure" data-brochure-name="SANI AMANZI Brochure">
                <span class="btn-text"><span>Request a brochure</span></span>
                <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
              </button>
              <a class="tj-primary-btn tj-primary-btn--outline" href="#faq">
                <span class="btn-text"><span>FAQ</span></span>
                <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
              </a>
              <a class="tj-primary-btn tj-primary-btn--outline" href="contact.html">
                <span class="btn-text"><span>Contact us</span></span>
                <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
              </a>
            </div>
          </div>
        </section>""")

    faqs = [
        (
            f"What is the main function of SANI AMANZI{TM}?",
            f"The primary purpose of SANI AMANZI{TM} is two-fold. Firstly, it effectively eliminates waterborne pathogens that can lead to infectious diseases in humans. Secondly, it facilitates water clarification through a flocculation process.",
        ),
        (
            f"Why must the water sit for 30 minutes after treatment?",
            f"Allowing the treated water to sit for 30 minutes is essential to provide sufficient time for the chemicals in SANI AMANZI{TM} to effectively neutralise the pathogens present in the water.",
        ),
        (
            f"Will water always become clear through flocculation with SANI AMANZI{TM}?",
            "No. While we lead in successful water clarity, claims of any product making water clear every time, regardless of pH, are often misleading. We continue to research and develop new formulas to enhance clarity.",
        ),
        (
            "How much water can be treated with 1 6g sachet?",
            f"One 6g sachet of SANI AMANZI{TM} is suitable for treating 20 litres of contaminated water, ensuring its safety for consumption.",
        ),
        (
            f"What influences solids in water not to settle with SANI AMANZI{TM}?",
            "The diverse water sources across South Africa result in varying water chemistries. While water chemistry affects water clarity (flocculation), it does not impact the sanitation process.",
        ),
        (
            "Does the clarity of water pose a health risk to people?",
            f"Water clarity itself is not a health threat. The presence of waterborne pathogens in clear water, however, can be dangerous. SANI AMANZI{TM} is designed to eliminate these pathogens.",
        ),
        (
            f"Is there a chemical taste in the water when using SANI AMANZI{TM}?",
            f"In highly contaminated water, SANI AMANZI{TM} might result in a slight chemical taste. When used in clear tap water without significant contamination, residual chemicals might lead to a mild taste. This taste, while not harmful, indicates the presence of protective agents against waterborne pathogens.",
        ),
        (
            f"Will SANI AMANZI{TM} remove sea salt from water?",
            f"No, SANI AMANZI{TM} is not designed to remove sea salt from water.",
        ),
        (
            f"Who is SANI-AMANZI{TM} intended for?",
            f"SANI AMANZI{TM} serves as a Point-of-Use (POU) solution for governments, NGOs, and concerned companies dedicated to providing safe drinking water for all individuals.",
        ),
    ]
    parts.append(f"""        <section id="faq" class="ulr-amanzi-band section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Frequently <span class="ulr-accent">Asked Questions</span></h2>
            <div class="ulr-amanzi-faq ulr-amanzi-faq--accordion">
              {"".join(faq_item(q, a) for q, a in faqs)}
            </div>
          </div>
        </section>""")

    parts.append("""        <section id="readiness" class="ulr-amanzi-band ulr-amanzi-band--deep section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Disaster Response &amp; <span>Government Readiness</span></h2>
            <div class="ulr-amanzi-readiness__grid">
              <div>
                <p class="desc">In situations such as flooding, infrastructure failure, drought, contamination events, humanitarian emergencies and municipal water interruptions, SANI AMANZI&trade; provides an immediate portable solution to support safer drinking water access at household and community level.</p>
                <p class="desc mb-2">Its lightweight sachet format allows:</p>
                <ul>
                  <li>rapid transportation</li>
                  <li>simplified storage</li>
                  <li>scalable deployment</li>
                  <li>emergency reserve stock</li>
                  <li>fast humanitarian distribution</li>
                </ul>
              </div>
              <div>
                <h3 class="sec-title h5">Strategic Water Preparedness</h3>
                <p class="desc">From a public health and emergency response perspective, maintaining reserve stock levels supports rapid deployment during water crises.</p>
                <p class="desc mb-2">Ubuntu Life Resources supports engagement with:</p>
                <ul>
                  <li>governments</li>
                  <li>NGOs</li>
                  <li>disaster response organisations</li>
                  <li>humanitarian programs</li>
                  <li>institutional buyers</li>
                  <li>distribution partners</li>
                </ul>
              </div>
            </div>
          </div>
        </section>""")

    parts.append("""        <section id="associations" class="ulr-amanzi-band ulr-amanzi-band--alt section-gap">
          <div class="ulr-amanzi-band__inner">
            <h2 class="sec-title ulr-amanzi-heading">Registered <span class="ulr-accent">Associations</span></h2>
            <div class="ulr-amanzi-badges">
              <div class="ulr-amanzi-badge"><strong>United Nations GM</strong>UNGM number 5618342</div>
              <div class="ulr-amanzi-badge"><strong>UNICEF</strong>Registered Vendor under UNGM5618343</div>
              <div class="ulr-amanzi-badge"><strong>IWA</strong>Corporate Membership number 16142154</div>
              <div class="ulr-amanzi-badge"><strong>WISA</strong>Corporate membership number 10242</div>
            </div>
          </div>
        </section>""")

    parts.append("""        <section id="contact" class="ulr-amanzi-band ulr-amanzi-cta section-gap">
          <div class="ulr-amanzi-band__inner">
            <div class="cta-area">
              <div class="cta-content">
                <h2 class="title">Partner With Ubuntu Life Resources</h2>
                <p class="desc">We support scalable clean water initiatives across Africa and developing regions through practical water purification solutions designed for real-world deployment.</p>
                <p class="desc mb-3"><strong>Contact us</strong><br>
                <a href="mailto:sanchia@ubuntuliferesources.co.za">sanchia@ubuntuliferesources.co.za</a><br>
                <a href="tel:+27796588189">079 658 8189</a><br>
                <a href="https://www.linkedin.com/in/sanchia-lynn-smit-935a44404" target="_blank" rel="noopener noreferrer">LinkedIn — Sanchia-Lynn Smit</a></p>
                <a class="tj-primary-btn" href="contact.html">
                  <span class="btn-text"><span>Get in touch</span></span>
                  <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                </a>
              </div>
            </div>
          </div>
        </section>""")

    return "\n".join(parts)


def splice_page(main_html: str) -> None:
    path = ROOT / "pillar-water-purification.html"
    text = path.read_text(encoding="utf-8")
    for marker in (
        '        <section class="ulr-amanzi-doc section-gap-x"',
        '        <section class="ulr-amanzi-scisan-hero section-gap-x"',
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

    for old, new in (
        ('body class="ulr-pillar-page ulr-amanzi-page ulr-amanzi-doc-flow"', 'body class="ulr-pillar-page ulr-amanzi-page ulr-amanzi-scisan"'),
        ('body class="ulr-pillar-page ulr-amanzi-page"', 'body class="ulr-pillar-page ulr-amanzi-page ulr-amanzi-scisan"'),
        ('body class="ulr-pillar-page"', 'body class="ulr-pillar-page ulr-amanzi-page ulr-amanzi-scisan"'),
    ):
        head = head.replace(old, new)

    if "ulr-amanzi-scisan.css" not in head:
        head = head.replace(
            '  <link rel="stylesheet" href="assets/css/ulr-amanzi-doc.css">',
            '  <link rel="stylesheet" href="assets/css/ulr-amanzi-scisan.css">',
        )
        if "ulr-amanzi-scisan.css" not in head:
            head = head.replace(
                '  <link rel="stylesheet" href="assets/css/ulr-amanzi-page.css">',
                '  <link rel="stylesheet" href="assets/css/ulr-amanzi-page.css">\n  <link rel="stylesheet" href="assets/css/ulr-amanzi-scisan.css">',
            )

    head = head.replace('  <link rel="stylesheet" href="assets/css/ulr-amanzi-doc.css">\n', "")
    tail = tail.replace('  <script src="assets/js/ulr-amanzi-doc.js" defer></script>\n', "")
    script = '  <script src="assets/js/ulr-amanzi-scisan.js" defer></script>'
    if "ulr-amanzi-scisan.js" not in tail:
        tail = tail.replace("</body>", f"{script}\n</body>", 1)

    path.write_text(head + main_html + "\n" + tail, encoding="utf-8")


def main() -> None:
    splice_page(build_main())
    print("Updated pillar-water-purification.html (scisan layout).")


if __name__ == "__main__":
    main()
