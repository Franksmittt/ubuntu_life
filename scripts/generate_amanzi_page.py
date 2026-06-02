# -*- coding: utf-8 -*-
"""Build pillar-water-purification.html from SANI AMANZI.Updated.docx content."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = "div"
TM = "&trade;"


def img(n: int) -> str:
    folder = ROOT / "assets/images/pillars/sani-amanzi/doc"
    for name in (f"image{n:03d}.png", f"image{n:03d}.jpg"):
        if (folder / name).exists():
            return f"assets/images/pillars/sani-amanzi/doc/{name}"
    raise FileNotFoundError(f"image{n:03d} missing in doc folder")


def fig(src: str, alt: str = "", flush: bool = False) -> str:
    extra = " ulr-amanzi-figure--flush" if flush else ""
    return (
        f'<figure class="ulr-brief-figure ulr-amanzi-figure m-0{extra}">'
        f'<img src="{src}" alt="{alt}" class="w-100" '
        f'loading="lazy" decoding="async"></figure>'
    )


def band(inner: str, mod: str = "", section_id: str = "") -> str:
    id_attr = f' id="{section_id}"' if section_id else ""
    return (
        f'        <section class="section-gap-x ulr-amanzi-band{mod}"{id_attr}>'
        f'<{T} class="ulr-amanzi-band__inner">{inner}</{T}></section>'
    )


def eyebrow(text: str) -> str:
    return f'<span class="ulr-amanzi-eyebrow"><i class="tji-worldwide" aria-hidden="true"></i>{text}</span>'


def heading(title: str, accent: str | None = None) -> str:
    if accent:
        return f'<h2 class="sec-title h3 ulr-amanzi-heading">{title} <span>{accent}</span></h2>'
    return f'<h2 class="sec-title h3 ulr-amanzi-heading">{title}</h2>'


def section_head(eyebrow_text: str, title: str, accent: str | None = None) -> str:
    eb = eyebrow(eyebrow_text) if eyebrow_text else ""
    return (
        f'<{T} class="ulr-amanzi-section-head">'
        f"{eb}{heading(title, accent)}</{T}>"
    )


def split_block(body: str, image_n: int, alt: str, flip: bool = False, title: str = "") -> str:
    flip_cls = " ulr-amanzi-split--flip" if flip else ""
    title_html = heading(title) if title else ""
    return (
        f'<{T} class="ulr-amanzi-split{flip_cls}">'
        f'<{T} class="ulr-amanzi-split__media">{fig(img(image_n), alt)}</{T}>'
        f'<{T} class="ulr-amanzi-prose">{title_html}{body}</{T}>'
        f"</{T}>"
    )


def jump_nav() -> str:
    links = [
        ("#crisis", "The crisis"),
        ("#quality", "Quality"),
        ("#product", "Product"),
        ("#impact", "Impact"),
        ("#science", "Science"),
        ("#how-to-use", "How to use"),
        ("#process", "Treatment"),
        ("#faq", "FAQ"),
        ("#contact", "Partner"),
    ]
    items = "".join(f'<a href="{href}">{label}</a>' for href, label in links)
    return f"""        <nav class="ulr-amanzi-jump section-gap-x" aria-label="On this page">
          <{T} class="ulr-amanzi-jump__inner">{items}</{T}>
        </nav>"""


def page_hero() -> str:
    return f"""        <section class="ulr-amanzi-hero section-gap-x" id="top">
          <{T} class="ulr-amanzi-band__inner">
            <{T} class="ulr-amanzi-hero__grid">
              <{T} class="ulr-amanzi-hero__glass ulr-hero-glass">
                <{T} class="ulr-hero-glass__env" aria-hidden="true">
                  <{T} class="ulr-hero-glass__gradient"></{T}>
                  <{T} class="ulr-hero-glass__grid-pattern"></{T}>
                  <span class="ulr-hero-glass__orb ulr-hero-glass__orb--blue"></span>
                  <span class="ulr-hero-glass__orb ulr-hero-glass__orb--green"></span>
                </{T}>
                <{T} class="ulr-hero-glass__panel">
                  <{T} class="ulr-amanzi-hero__logos">
                    <img src="{img(1)}" alt="SANI AMANZI" loading="eager" decoding="async">
                    <img src="{img(2)}" alt="" loading="eager" decoding="async">
                  </{T}>
                  {eyebrow("Water purification solutions")}
                  <h1 class="ulr-amanzi-hero__title">SANI AMANZI{TM} Water Sanitising &amp; Purification Solution</h1>
                  <p class="ulr-amanzi-hero__tagline">Caring for Life</p>
                  <{T} class="ulr-amanzi-hero__crumb tj-page-link">
                    <span><i class="tji-home"></i></span>
                    <span><a href="index.html">Home</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><a href="pillars.html">Core pillars</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span>Water Purification Solutions</span>
                  </{T}>
                  <{T} class="ulr-amanzi-hero__actions">
                    <a class="ulr-hero-glass__btn ulr-hero-glass__btn--primary" href="assets/downloads/sani-amanzi-brochure-2023.pdf" target="_blank" rel="noopener noreferrer"><span class="ulr-hero-glass__btn-label">Download brochure</span></a>
                    <a class="ulr-hero-glass__btn ulr-hero-glass__btn--secondary" href="contact.html">Contact us</a>
                  </{T}>
                </{T}>
              </{T}>
              <figure class="ulr-amanzi-hero__visual">
                <img src="{img(4)}" alt="SANI AMANZI point-of-use water purification." width="601" height="601" loading="eager" decoding="async">
              </figure>
            </{T}>
          </{T}>
        </section>"""


def cta_block() -> str:
    return f"""        <section class="tj-cta-section section-gap-x ulr-amanzi-cta" id="contact">
          <{T} class="container">
            <{T} class="row">
              <{T} class="col-12">
                <{T} class="cta-area">
                  <{T} class="cta-content">
                    <h2 class="title title-anim">Partner With Ubuntu Life Resources</h2>
                    <p class="desc">We support scalable clean water initiatives across Africa and developing regions through practical water purification solutions designed for real-world deployment.</p>
                    <{T} class="cta-btn mt-3 d-flex flex-wrap gap-2">
                      <a class="tj-primary-btn btn-dark" href="contact.html"><span class="btn-text"><span>Contact Us</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
                      <a class="tj-primary-btn btn-dark" href="tel:+27796588189"><span class="btn-text"><span>Call 079 658 8189</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
                      <a class="tj-primary-btn btn-dark" href="https://www.linkedin.com/in/sanchia-lynn-smit-935a44404" target="_blank" rel="noopener noreferrer"><span class="btn-text"><span>LinkedIn</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
                    </{T}>
                    <p class="desc mt-3 mb-0"><a href="mailto:sanchia@ubuntuliferesources.co.za">sanchia@ubuntuliferesources.co.za</a></p>
                  </{T}>
                  <{T} class="cta-img"><img src="assets/images/cta/ulr-cta-collaboration-wide.jpg" alt="Contact Ubuntu Life Resources." loading="lazy" decoding="async"></{T}>
                </{T}>
              </{T}>
            </{T}>
          </{T}>
        </section>"""


def build_main() -> str:
    parts: list[str] = [page_hero(), jump_nav()]

    intro = """<p class="desc">More than 2 billion people are currently trapped in water-stressed countries, while shockingly, a staggering 900 million individuals continue to endure the daily torment of lacking access to clean drinking water. This grim reality signifies that over 1 in every 8 people across the globe is living without this basic necessity.</p>
<p class="desc">The gravity of this crisis cannot be overstated. Access to safe drinking water is not a luxury but a fundamental human right, essential for our very survival and well-being.</p>
<p class="desc">What adds to the shock is the stark fact that contaminated water claims more lives than the combined toll of diseases like Malaria, COVID-19, and AIDS.</p>
<p class="desc">Contaminated water breeds and spreads deadly diseases like Cholera, Diarrhoea, Dysentery, Hepatitis A, Typhoid, and Polio, leaving a trail of suffering and death in its wake.</p>
<p class="desc">In line with the United Nations&rsquo; declaration that &ldquo;Everyone has the right to sufficient, continuous, safe, acceptable, physically accessible, and affordable water for personal and domestic use,&rdquo; this ongoing water crisis should serve as a resounding wake-up call. It highlights the urgent need for immediate and concerted action to address this dire global issue.</p>
<p class="desc">Introducing SANI AMANZI{tm}, a cutting-edge point-of-use solution that is not only affordable but also highly practical for all those exposed to contaminated water sources. This innovative product effectively eliminates waterborne pathogenic bacteria through a unique blend of safe active ingredients.</p>
<p class="desc">Developed by a team of experts deeply knowledgeable about the challenges posed by contaminated water, SANI AMANZI{tm} stands out as the ultimate solution to the clean water crisis.</p>
<p class="desc">Furthermore, SANI AMANZI{tm} demonstrates exceptional effectiveness against antibiotic-resistant bacteria and successfully eradicates a wide spectrum of pathogenic microbes. What sets this product apart is its ingenious design, incorporating an inorganic, natural, and non-polluting reagent.</p>
<p class="desc mb-0">SANI AMANZI{tm} is poised to revolutionise access to clean water and make a significant impact on global health.</p>""".format(
        tm=TM
    )
    parts.append(
        band(
            section_head("Global water crisis", "Safe water is a human right", "not a luxury")
            + f'<{T} class="ulr-amanzi-prose ulr-amanzi-prose--wide">{intro}</{T}>',
            mod=" ulr-amanzi-band--tint",
            section_id="crisis",
        )
    )

    parts.append(
        band(
            split_block(
                f"""<p class="desc">SANI AMANZI{TM} has been tested by accredited SANAS laboratories using the SANS 241-1:2015 Drinking Water Standards and the WRC Domestic Use Standard classification system (<em>see diagram</em>). After vigorous testing of SANI AMANZI{TM} it was determined that the samples collected and treated displayed physical, chemical and bacteriological qualities that were deemed as fit for use as potable water and for domestic use purposes. The WRC classified SANI AMANZI{TM} as being of &ldquo;Good Water Quality&rdquo; (class one); meaning treated water was suitable for life-time use, with rare instances of sub-clinical effects.</p>
<p class="desc mb-0">To gain more insight into the WRC Domestic Use Standard classification system please visit <a href="https://www.wrc.org.za" target="_blank" rel="noopener noreferrer">www.wrc.org.za</a>.</p>""",
                5,
                "WRC Domestic Use Standard classification.",
                flip=True,
                title="Water Quality Classification",
            ),
            mod=" ulr-amanzi-band--alt",
            section_id="quality",
        )
    )

    parts.append(
        band(
            f"""{section_head("Transparency", "Tested on real-world water", "99.99% pathogen reduction")}
<{T} class="ulr-amanzi-prose">
<p class="desc mb-2"><strong>The WRC Domestic Use Standard classification system</strong></p>
<p class="desc">Scientific Sanitation Solutions are always striving to achieve breakthrough discoveries in chemistry, to make effective clarification possible every time. Any Point-of-Use product claiming to be 100% successful in the clarification of water every time, irrespective of pH and other chemistry influences, are misleading and false.</p>
<p class="desc mb-0">We take great pride in providing our customers with full transparency, and have tested SANI-AMANZI{TM} on the most contaminated of water sources in South Africa to ensure we meet our efficacy standard goals of eliminating 99.99% of waterborne pathogenic bacteria and this remains our core goal to this very day.</p>
</{T}>"""
        )
    )

    parts.append(
        band(
            f"""{section_head("Sustainability", "Environmentally responsible", "plastic-free")}
<{T} class="ulr-amanzi-prose">
<p class="desc">In recognition of the climate crisis and our responsibility to do all we can to reduce the amount of plastic waste harming our environment, SANI AMANZI{TM} has been purposefully designed to reduce, and wherever possible, stop plastic bottle contamination.</p>
<p class="desc mb-0">With our &ldquo;plastic-free&rdquo; principle in mind, SANI AMANZI{TM} has been packaged via powder sachet as an alternative to liquid purifiers on the market. All you need is a sachet of SANI AMANZI{TM} and water to fill your bucket and you will have a powerful and environmentally friendly water purifier.</p>
</{T}>
<{T} class="ulr-amanzi-compare mt-4">
  <{T} class="ulr-amanzi-compare__col">{fig(img(6), "66 trucks for 2 million litres of bottled water.")}</{T}>
  <{T} class="ulr-amanzi-compare__vs" aria-hidden="true">VS</{T}>
  <{T} class="ulr-amanzi-compare__col">{fig(img(7), "1 truck for purifying 40 million litres with SANI AMANZI.")}</{T}>
</{T}>
<p class="desc mt-4 mb-0 ulr-amanzi-prose">We do not only believe in eradicating pathogens but also reducing our carbon footprint. By using a SANI AMANZI{TM} sachet as an alternative to bottled water or liquid water purifiers this means that less trucks are required for transportation, thus being more friendly on the environment.</p>"""
        )
    )

    features = "".join(
        f'<article class="ulr-amanzi-feature">{fig(img(n), alt)}</article>'
        for n, alt in [
            (8, "Triple foil high quality sachet."),
            (9, "1 sachet treats 20 litres."),
            (10, "Point-of-use purifier."),
            (11, "Precise dosage prevents overdose."),
            (12, "Affordable competitively priced."),
        ]
    )
    parts.append(
        band(
            f"""{section_head("Product highlights", "Key characteristics")}
<{T} class="ulr-amanzi-features">{features}</{T}>""",
            mod=" ulr-amanzi-band--alt",
            section_id="product",
        )
    )

    steps = "".join(
        f'<li class="ulr-amanzi-step">{fig(img(n), alt)}</li>'
        for n, alt in [
            (14, "Instructions step 1."),
            (15, "Instructions step 2."),
            (17, "Instructions step 3."),
            (16, "Instructions step 4."),
        ]
    )
    parts.append(
        band(
            f"""{section_head("How to use", "Instructions for use")}
<ul class="ulr-amanzi-steps">{steps}</ul>""",
            section_id="how-to-use",
        )
    )

    parts.append(
        band(
            f"""{section_head("", "World&rsquo;s Best Water Purifier?")}
<{T} class="d-flex justify-content-center">{fig(img(18), "World's best water purifier.", flush=True)}</{T}>""",
            mod=" ulr-amanzi-band--alt ulr-amanzi-band--tight",
        )
    )

    parts.append(
        band(
            f"""{section_head("Range", "Product range")}
{fig(img(19), "SANI AMANZI product range.")}
<{T} class="ulr-amanzi-actions">
  <a class="tj-primary-btn" href="assets/downloads/sani-amanzi-brochure-2023.pdf" target="_blank" rel="noopener noreferrer"><span class="btn-text"><span>Download brochure</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
  <a class="tj-primary-btn" href="contact.html"><span class="btn-text"><span>Contact us</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
  <a class="tj-primary-btn" href="tel:+27796588189"><span class="btn-text"><span>Call 079 658 8189</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
</{T}>"""
        )
    )

    parts.append(
        band(
            f'<{T} class="text-center">{fig(img(3), "SANI AMANZI branding.", flush=True)}</{T}>',
            mod=" ulr-amanzi-band--tight",
        )
    )

    parts.append(
        band(
            f"""{section_head("Why it matters", "Innovation for safe water", "every community")}
<{T} class="ulr-amanzi-prose ulr-amanzi-prose--wide">
<p class="desc">In a world where the availability of safe drinking water remains a paramount concern, SANI AMANZI{TM} rises as a beacon of innovation and hope. Against the backdrop of an alarming statistic, the imperative need for a transformative solution has become more pressing than ever. SANI AMANZI{TM} takes centre stage as a pioneering point-of-use water purifying solution, reshaping the landscape of clean water accessibility.</p>
</{T}>
<blockquote class="ulr-amanzi-stat">
  <p class="ulr-amanzi-stat__quote">&ldquo;1 in 3 people globally do not have access to safe drinking water&rdquo;</p>
  <p class="ulr-amanzi-stat__cite">UNICEF / World Health Organization Report</p>
</blockquote>
<p class="desc ulr-amanzi-prose">According to the World Health Organization (WHO) and UNICEF, approximately 2.2 billion people worldwide do not have access to safely managed drinking water services.</p>""",
            section_id="impact",
        )
    )

    parts.append(
        band(
            f"""{section_head("Our purpose", "Why we do, what we do")}
<ol class="ulr-amanzi-why-list">
<li>According to the World Health Organization (WHO) and UNICEF, approximately 2.2 billion people worldwide do not have access to safely managed drinking water services. This means that a significant portion of the global population lacks access to clean and safe water sources, putting them at risk of waterborne diseases and related health issues.</li>
<li>In many developing regions, particularly in sub-Saharan Africa, women and children spend hours each day collecting water from distant sources. On average, women and girls in sub-Saharan Africa collectively spend about 40 billion hours per year collecting water, which equates to approximately 16 million individuals spending an average of 2.5 hours each day fetching water.</li>
<li>Unsafe water, poor sanitation, and inadequate hygiene cause more deaths annually than all forms of violence, including wars. In 2019, the World Health Organization (WHO) estimated that around 1.5 million deaths were attributed to waterborne diseases, making it a significant global health concern.</li>
</ol>""",
            mod=" ulr-amanzi-band--alt",
        )
    )

    parts.append(
        band(
            f"""{section_head("Differentiation", "What sets sani amanzi apart", "from other purifiers")}
<{T} class="ulr-amanzi-prose ulr-amanzi-prose--wide">
<p class="desc">SANI AMANZI{TM} isn&rsquo;t just another entry in the realm of water purifiers &ndash; it&rsquo;s a revolutionary leap forward. While many products claim to offer clean water solutions, SANI AMANZI{TM} sets itself apart through a combination of cutting-edge technology, affordability, and practicality that speaks directly to the needs of individuals and communities exposed to contaminated water sources.</p>
<p class="desc">Behind the creation of SANI AMANZI{TM} lies a culmination of expertise from a team deeply entrenched in understanding the intricacies of contaminated water challenges. This amalgamation of scientific knowledge and practical experience has resulted in a solution that doesn&rsquo;t merely purify water, but addresses the complex web of issues surrounding waterborne pathogens and contaminants.</p>
<p class="desc mb-0">What once was considered solely a concern for rural areas has transcended boundaries, becoming an urgent urban crisis as well. SANI-AMANZI{TM}, however, remains steadfast in the face of evolving challenges. Its efficacy extends beyond conventional bacteria to encompass antibiotic-resistant strains &ndash; a testament to its remarkable capability in tackling a broad spectrum of pathogens.</p>
</{T}>"""
        )
    )

    parts.append(
        band(
            split_block(
                f"""<p class="desc">Central to SANI AMANZI{TM}&rsquo;s potency is its innovative reagent, an inorganic composition derived from natural, non-polluting substances. The use of inorganic raw materials underscores a commitment to both efficacy and environmental responsibility. Moreover, SANI-AMANZI{TM} not only purifies but nourishes. With a formula that supports diverse gut microbiota, it contributes to overall health while acting as a detoxifier, thus enhancing the body&rsquo;s pH balance.</p>
<p class="desc">SANI-AMANZI{TM} also prioritises the well-being of its users. Every facet of its design is meticulously crafted to ensure that once diluted, the product is not only effective but also safe for human consumption. Moreover, SANI-AMANZI{TM} stands out from liquid alternatives in the market by incorporating a precise dosage mechanism (6g per sachet). This innovative feature eradicates the possibility of overdosing, setting a new benchmark in safety and accuracy that redefines the landscape of water purification solutions.</p>
<p class="desc mb-0">In a market flooded with choices, SANI AMANZI{TM} stands out as an embodiment of innovation, efficacy, and a steadfast commitment to delivering clean, safe water to every corner of the globe.</p>""",
                23,
                "SANI AMANZI innovative reagent.",
            ),
            mod=" ulr-amanzi-band--alt",
            section_id="science",
        )
    )

    parts.append(
        band(
            f'<{T} class="text-center">{fig(img(24), "Key advantages of SANI AMANZI.", flush=True)}</{T}>',
            mod=" ulr-amanzi-band--tight",
        )
    )

    advantages = [
        f"<strong>Innovative Packaging:</strong> Encased within compact 6g sachet, each sachet effectively purifies up to 20 litres of contaminated water, making it a practical solution even in resource-constrained environments.",
        f"<strong>Convenient Powder Formulation:</strong> Its powdered formulation not only facilitates easy transport but also ensures effortless utilisation, regardless of the location.",
        f"<strong>Robust Pathogen Eradication:</strong> SANI-AMANZI{TM}&rsquo;s efficacy extends to formidable pathogens such as Salmonella, Shigella, and Cholera, ensuring comprehensive and reliable water purification.",
        "<strong>Exceptional Effectiveness:</strong> Demonstrating an exceptional sanitising efficacy rate of 0 (ZERO) E.coli per 100ml, it sets an unprecedented benchmark in water purification performance.",
        f"<strong>Accurate Dosage:</strong> In contrast to liquid alternatives, SANI-AMANZI{TM} eliminates the risk of overdose by delivering precise and consistent dosages within each sachet.",
        f"<strong>Chemical-Free Approach:</strong> Committed to user health and safety, SANI-AMANZI{TM} avoids the use of chlorine or other harmful chemicals, prioritising the well-being of its consumers.",
        f"<strong>Premium Packaging:</strong> Triple foil sachets guarantee that SANI-AMANZI{TM} arrives in optimal condition, preserving its potency and reliability for maximum effectiveness.",
        f"<strong>Sustainability Focus:</strong> SANI-AMANZI{TM} contributes to a reduced carbon footprint through its innovative packaging, making it an eco-friendly water purification solution.",
    ]
    parts.append(
        band(
            section_head("Benefits", "Key advantages of using Sani Amanzi")
            + f'<ul class="ulr-amanzi-advantages">{"".join(f"<li>{a}</li>" for a in advantages)}</ul>'
        )
    )

    parts.append(
        band(
            split_block(
                f"""<p class="desc">Designed to protect against a spectrum of waterborne threats, SANI-AMANZI{TM} guarantees the purity and quality of the water you consume. Its remarkable efficacy stems from its ability to destroy 99.99% of bacteria, viruses, and protozoa present in the water, shielding consumers from potential health hazards.</p>
<p class="desc">One of SANI-AMANZI{TM}&rsquo;s distinct advantages lies in its capacity to neutralise key threats, including the notorious Salmonella, Shigella, and E. coli. These pathogens are known culprits of severe gastrointestinal illnesses, and SANI-AMANZI{TM} ensures they are effectively eradicated. Moreover, it tackles cryptosporidium and oocysts, which are often responsible for waterborne infections and digestive discomfort.</p>
<p class="desc mb-0">A standout feature of SANI-AMANZI{TM} is its remarkable sanitising efficacy. It achieves a sanitising efficacy of 0 (ZERO) E.coli per 100ml, a testament to its rigorous purification process and commitment to water safety.</p>""",
                22,
                "Shield against deadly pathogens.",
                flip=True,
                title="A shield against deadly pathogens",
            ),
            mod=" ulr-amanzi-band--alt",
        )
    )

    parts.append(
        band(
            f'<{T} class="text-center">{fig(img(25), "Waterborne pathogen protection.", flush=True)}</{T}>',
            mod=" ulr-amanzi-band--tight",
        )
    )

    contaminants = [
        (26, "Arsenic", """<p class="desc">Arsenic is a natural element that can contaminate water sources through geological processes and human activities. In its inorganic form, it poses health risks when consumed.</p>
<p class="desc mb-0">Long-term exposure, often through drinking water, has been linked to cancer, skin issues, cardiovascular problems, neurological effects, and more.</p>"""),
        (27, "Fluorides", """<p class="desc">Fluorides are naturally occurring compounds that can be found in soil, rocks, and water sources. In water, fluoride ions are derived from the dissolution of minerals like fluorite.</p>
<p class="desc mb-0">While fluoride is often associated with dental health due to its role in preventing tooth decay, excessive levels of fluoride in drinking water can pose health risks.</p>"""),
        (28, "Nitrates", """<p class="desc">Nitrates, composed of nitrogen and oxygen, are natural components found in soil, water, and fertilisers. While they themselves are generally safe, elevated nitrate levels in drinking water, often from agricultural runoff, can lead to health risks.</p>
<p class="desc mb-0">Within the body, nitrates can undergo conversion to nitrites, which can impact the blood&rsquo;s ability to transport oxygen.</p>"""),
        (29, "Pesticides", """<p class="desc">Pesticides are chemicals used to control pests in agriculture, but improper use can lead to their presence in water sources.</p>
<p class="desc">They enter water through runoff, irrigation, and accidents, impacting aquatic life and potentially human health.</p>
<p class="desc mb-0">Pesticide contamination varies in effects, from neurological issues to increased cancer risk, depending on type and concentration.</p>"""),
        (30, "Iron", """<p class="desc">Excessive iron in drinking water, while a natural element, can lead to discolouration and taste issues. Soluble iron can transform into insoluble rust, causing water to appear reddish or brownish.</p>
<p class="desc">This discolouration not only affects aesthetics but can also alter taste.</p>
<p class="desc mb-0">Additionally, high iron intake can result in stomach discomfort, particularly for those with certain medical conditions.</p>"""),
    ]
    contaminant_cards = "".join(
        f"""<article class="ulr-amanzi-contaminant">
  {fig(img(n), f"{title} contaminant.")}
  <{T}>
    <h3 class="ulr-amanzi-contaminant__title">{title}</h3>
    {body}
  </{T}>
</article>"""
        for n, title, body in contaminants
    )
    parts.append(
        band(
            section_head("Contaminants", "What contaminants can sani amanzi remove from water?")
            + f'<{T} class="ulr-amanzi-contaminants">{contaminant_cards}</{T}>'
        )
    )

    parts.append(
        band(
            split_block(
            f"""<p class="desc">Antibiotic-resistant bacteria are strains of microorganisms that have developed the ability to withstand the effects of commonly used antibiotics. This phenomenon poses a significant challenge, especially in developing regions, where access to advanced medical care is limited. These resilient bacteria can thrive in water sources, magnifying the existing health risks in communities already facing limited healthcare resources.</p>
<p class="desc">In areas where clean water is scarce and sanitation infrastructure is inadequate, the presence of antibiotic-resistant bacteria in water sources compounds the health dangers. Consuming or using contaminated water can lead to the spread of infections that are not easily treatable, resulting in prolonged illnesses and heightened healthcare expenses. The rise of antibiotic-resistant bacteria amplifies the urgency for effective water purification solutions tailored to the needs of these regions.</p>
<p class="desc mb-0">Against this backdrop, SANI AMANZI{TM} emerges as a beacon of hope. Its innovative water purification approach not only ensures water safety but also addresses the challenges posed by antibiotic-resistant bacteria. By effectively neutralising even the most resilient microorganisms, including antibiotic-resistant strains, SANI AMANZI{TM} contributes to the health and well-being of communities in developing regions.</p>""",
            31,
            "Antibiotic-resistant bacteria in water.",
                title="Addressing anti-biotic resistant bacteria in water",
            ),
            mod=" ulr-amanzi-band--alt",
        )
    )

    parts.append(
        band(
            split_block(
                f"""<p class="desc">SANI AMANZI{TM} stands as a remarkable solution in the realm of water purification, distinguished by its chlorine-free approach. Unlike traditional methods that often rely on chlorine for disinfection, SANI AMANZI{TM} offers a significant advantage by steering clear of this chemical element. While chlorine can effectively eliminate contaminants, it often leaves an undesirable footprint, introducing taste and odour complexities to the treated water. In contrast, SANI AMANZI{TM}&rsquo;s innovative chlorine-free process ensures that purified water remains free from these unpleasant aftereffects, preserving its natural and revitalising taste.</p>
<p class="desc mb-0">Beyond the matter of taste, the absence of chlorine brings an additional layer of safety. Chlorine-based purification methods have the potential to form harmful disinfection byproducts when they react with organic matter present in water. By adopting a chlorine-free approach, SANI AMANZI{TM} averts the creation of these potentially detrimental compounds. In doing so, it not only guarantees the safety of the purified water but also enhances the overall drinking experience by providing water that is not only pure but also genuinely satisfying to the palate.</p>""",
                32,
                "Chlorine-free water purification.",
                flip=True,
                title="No chlorine, no problem!",
            )
        )
    )

    parts.append(
        band(
            f"""{section_head("Standards", "The classification of drinking water")}
<{T} class="ulr-amanzi-prose ulr-amanzi-prose--wide">
<p class="desc">Water classification systems play a pivotal role in assessing the quality and suitability of water for various purposes. These systems are designed to categorise water based on specific parameters, ensuring that its characteristics align with the standards set for safe consumption, domestic use, and other applications. Two prominent classification systems, the SANS 241-1:2015 Drinking Water Standards and the Quality of Domestic Water Supplies Classification System by the WRC (Water Research Commission), are widely employed to evaluate water quality.</p>
<p class="desc">The SANS 241-1:2015 Drinking Water Standards, developed by the South African Bureau for Standards (SABS), establish guidelines for the microbiological, physical, aesthetic, and chemical attributes of drinking water. This comprehensive framework outlines permissible limits for various constituents, such as pH, electrical conductivity, total dissolved solids, chlorides, sulphates, nitrates, nitrites, ammonia, and more. Water samples are assessed against these standards to determine compliance with the prescribed criteria.</p>
<p class="desc mb-0">Additionally, the Quality of Domestic Water Supplies classification system by the WRC is another essential tool in evaluating water quality. This system categorises water based on its characteristics, offering insights into its potential impact on human health and overall usability. The classification system comprises several classes, each representing a different level of water quality. Ranging from &ldquo;Ideal&rdquo; (Class 0) to &ldquo;Unacceptable&rdquo; (Class 4), these classifications consider factors such as taste, appearance, health risks, and suitability for lifetime use.</p>
</{T}>
<{T} class="ulr-amanzi-class-grid">
  {fig(img(33), "Water classification diagram 1.")}
  {fig(img(34), "Water classification diagram 2.")}
  {fig(img(35), "Water classification diagram 3.")}
</{T}>
<{T} class="ulr-amanzi-prose">
  <p class="desc mb-2">According to the WRC Domestic Use Standard, water quality can be classified as:</p>
  <p class="desc">When assessing water quality, various variables are considered, including pH levels, electrical conductivity, total dissolved solids, turbidity, presence of pathogens like E.coli and coliform bacteria, as well as the concentrations of specific elements and compounds like fluoride, iron, and more. By comparing these variables to established standards, experts can ascertain whether water meets the required quality benchmarks.</p>
  <p class="desc mb-0">The process of water classification involves rigorous analysis and comparison of the collected data against established limits. The aim is to ensure that water is safe for human consumption, devoid of harmful contaminants, and suitable for its intended uses. The application of these classification systems ensures that communities have access to water that meets health and safety standards, safeguarding public health and well-being.</p>
</{T}>""",
            mod=" ulr-amanzi-band--alt",
        )
    )

    parts.append(
        band(
            f'<{T} class="text-center mb-4">{fig(img(36), "SANI AMANZI testing standards.", flush=True)}</{T}>'
            + f"""{section_head("Lab results", "Does sani amanzi meet testing standards?")}
<{T} class="ulr-amanzi-prose ulr-amanzi-prose--wide">
<p class="desc">SANI AMANZI{TM} has demonstrated its efficacy in meeting the SANS 241-1:2015 Drinking Water Standards and the Quality of Domestic Water Supplies Classification System set by the Water Research Commission (WRC) through rigorous testing and analysis. <em>Please refer to independent test reports.</em></p>
<p class="desc"><strong>SANS 241-1:2015 Drinking Water Standards:</strong> SANI AMANZI{TM} has been tested in accordance with the parameters outlined in the SANS 241-1:2015 standard. This includes testing for various physical, chemical, and microbiological parameters such as pH, total dissolved solids (TDS), turbidity, and the absence of harmful microorganisms like E. coli and Coliforms. The results of these tests have demonstrated that water treated with SANI AMANZI{TM} meets the specified standards for safe drinking water quality. The absence of contaminants such as E. coli and Coliforms in treated water samples indicates its effectiveness in complying with microbiological standards.</p>
<p class="desc mb-0"><strong>Quality of Domestic Water Supplies Classification System by WRC:</strong> The WRC&rsquo;s Quality of Domestic Water Supplies Classification System evaluates the suitability of water for different uses based on its quality. Water treated with SANI AMANZI{TM} has consistently shown improvements in its quality, moving from potentially contaminated states to classifications indicating better suitability for domestic use. This indicates that the treatment process employed by SANI AMANZI{TM} is effective in reducing microbial and other contaminant levels, aligning with the WRC&rsquo;s classification system for improved water quality.</p>
</{T}>"""
        )
    )

    parts.append(
        band(
            section_head("Performance", "How did sani amanzi perform?")
            + fig(img(37), "SANI AMANZI performance results."),
            mod=" ulr-amanzi-band--alt",
        )
    )

    parts.append(
        band(
            f"""{section_head("Water chemistry", "Understanding TDS and the impact on water quality")}
<{T} class="ulr-amanzi-prose ulr-amanzi-prose--wide">
<p class="desc">Total Dissolved Solids (TDS) encompass minerals, salts, and organic compounds dissolved within water. While a certain level of TDS is natural and even beneficial for water&rsquo;s taste and mineral content, elevated TDS levels can trigger a range of issues, particularly in regions facing water quality challenges. Some of the challenges of elevated TDS levels include:</p>
<ul class="desc">
<li><strong>Unpleasant Taste:</strong> Water laden with high TDS often carries a salty or bitter taste, rendering it unappetising and less likely to be consumed by communities already struggling with water scarcity.</li>
<li><strong>Cloudy Appearance:</strong> Elevated TDS can lead to cloudy or murky water, adding another layer of concern for regions where access to clean and clear water is a rarity.</li>
<li><strong>Mineral Deposits:</strong> High TDS water leaves behind mineral deposits on items like glasses, faucets, and equipment. For communities without ready access to cleaning supplies, these deposits pose not only a visual issue but also a significant hygiene challenge.</li>
<li><strong>Reduced Cleaning Power:</strong> Excessive TDS interferes with the efficacy of soaps and detergents, leaving individuals with compromised cleaning agents. This is especially problematic where maintaining cleanliness is essential for health and well-being.</li>
<li><strong>Infrastructure Strain:</strong> In regions where infrastructure is already under strain, the accumulation of mineral deposits in appliances, pipes, and plumbing fixtures exacerbates efficiency concerns. This results in increased energy usage, potential damage, and further strain on limited resources.</li>
</ul>
<p class="desc"><strong>Significant TDS reduction with our flocculant</strong></p>
<p class="desc">Our product&rsquo;s flocculant has showcased remarkable effectiveness in significantly reducing Total Dissolved Solids (TDS). This achievement stems from meticulous adherence to recommended protocols, encompassing the careful timing for the flocculant&rsquo;s action and the subsequent filtration of water through a dense cloth. The primary aim of this TDS reduction is to address aesthetic considerations, enhancing the overall visual and sensory qualities of the treated water.</p>
<p class="desc">In rural African contexts, TDS doesn&rsquo;t take precedence due to its limited immediate harm. Instead, the focus revolves around combating waterborne pathogens, which present substantial health risks. It&rsquo;s noteworthy that TDS standards set by WHO and EPA are geared towards controlled waterworks systems, differing from the dynamic realities of rural point-of-use scenarios. For instance, while WHO suggests a TDS level of 300 ppm, the Bureau of Indian Standards (BIS) permits up to 500 ppm &ndash; a significant variance even within controlled systems.</p>
<p class="desc">This divergence underscores how regions like India and Africa interpret water quality standards distinctively compared to more developed nations. Although TDS levels themselves don&rsquo;t directly indicate health risks, they can offer early signals of potential inorganic influences that might escalate if left unmonitored.</p>
<p class="desc mb-0">Conductivity and total dissolved solids share a complex relationship. Total dissolved solids encompass inorganic salts, including calcium, magnesium, potassium, sodium, bicarbonates, chlorides, sulfates, and trace amounts of organic matter, all dissolved in water. While TDS tests quantify dissolved ions, they don&rsquo;t provide a nuanced understanding of their specific impact. By diligently adhering to proper protocols, SANI-AMANZI{TM} effectively accomplishes a substantial reduction in TDS and can aid in mitigating hard water issues. This speaks to the comprehensive capabilities of SANI-AMANZI{TM} as a versatile water treatment solution.</p>
</{T}>
<{T} class="ulr-amanzi-split mt-4">
  <{T}>{fig(img(38), "TDS and water quality.")}</{T}>
  <{T}>{fig(img(39), "Water treatment illustration.")}</{T}>
</{T}>""",
            mod=" ulr-amanzi-band--alt",
        )
    )

    parts.append(
        band(
            f"""{section_head("Treatment steps", "Simple water treatment process")}
<ul class="ulr-amanzi-process-steps">
  <li><strong>Step 1</strong> Add 1 sachet to 20 litres of contaminated water.</li>
  <li><strong>Step 2</strong> Stir thoroughly to create strong agitation.</li>
  <li><strong>Step 3</strong> Allow water to stand for a minimum of 30 minutes.</li>
  <li><strong>Step 4</strong> Filter treated water through a dense cloth before use.</li>
</ul>
<p class="desc"><strong>Important note</strong> &mdash; optimal treatment performance depends on correct dosage, proper agitation, full settling time, and correct filtration protocol.</p>
{fig(img(40), "Simple water treatment process diagram.")}""",
            section_id="process",
        )
    )

    parts.append(
        band(
            f"""{section_head("Dosage", "Scalable water treatment")}
<{T} class="ulr-table-scroll ulr-product-table-wrap"><table class="ulr-product-table">
  <thead><tr><th>Water Volume</th><th>Recommended Dosage</th></tr></thead>
  <tbody>
    <tr><td>20 Litres</td><td>6g</td></tr>
    <tr><td>1,000 Litres</td><td>300g</td></tr>
    <tr><td>5,000 Litres</td><td>1.5kg</td></tr>
  </tbody>
</table></{T}>
<p class="desc mt-3 ulr-amanzi-prose">SANI AMANZI{TM} supports scalable treatment applications across varying water volumes and operational environments.</p>
<p class="desc ulr-amanzi-prose">Remember that the chemistry of each water source can vary, influencing factors such as pH, particle size, particle density, liquid density, surface charge, and water chemistry. These factors can impact the efficiency of the treatment process, so following the recommended instructions and safety guidelines is crucial to achieve optimal results. It&rsquo;s also important to keep in mind the following safety guidelines when using SANI AMANZI{TM}:</p>
<{T} class="ulr-amanzi-safety-grid">
  {fig(img(41), "No mixing with other disinfectants.")}
  {fig(img(42), "Avoid contact with eyes.")}
  {fig(img(43), "Do not ingest anhydrous powder.")}
  {fig(img(44), "No consumption of coagulants or precipitate.")}
</{T}>
<{T} class="ulr-amanzi-safety-note">
  <p><strong>No Mixing with Other Disinfectants</strong> &mdash; Do not use SANI AMANZI{TM} alongside other disinfectants, sanitisers, acids, or ammonia.</p>
  <p><strong>Avoid Contact with Eyes</strong></p>
  <p><strong>Do Not Ingest Anhydrous Powder</strong></p>
  <p><strong>No Consumption of Coagulants/ Precipitate</strong> &mdash; can lead to unpredictable reactions and compromise the effectiveness of water treatment.</p>
</{T}>""",
            mod=" ulr-amanzi-band--alt",
        )
    )

    parts.append(
        band(
            split_block(
                f"""<p class="desc">SANI AMANZI{TM} embodies more than just effective water purification; it carries a deep commitment to environmental responsibility. When you choose SANI AMANZI{TM}, you&rsquo;re not only enhancing water quality but also actively contributing to a more sustainable future. The utilisation of innovative powder sachets, over liquid alternatives, significantly reduces transportation requirements, resulting in a decreased carbon footprint and a healthier planet for current and future generations.</p>
<p class="desc">Dedicated to reducing plastic waste and environmental impact, SANI AMANZI{TM} is meticulously designed to minimise, and whenever feasible, eliminate the use of plastic bottles. The groundbreaking powder sachets replace conventional liquid purifiers, offering a straightforward and eco-friendly solution. With just a sachet of SANI AMANZI{TM} and a container of water, you can harness the power of sustainable water purification.</p>
<p class="desc">Beyond being another water purifying product, SANI AMANZI{TM} symbolises a commitment to fostering healthier communities, free from the threats of waterborne diseases. As the urgency of the climate crisis grows, we acknowledge our responsibility to combat plastic pollution.</p>
<p class="desc mb-0">SANI AMANZI{TM} takes pride in championing a &ldquo;plastic-free&rdquo; ethos, providing pragmatic solutions that not only enhance well-being but also contribute to a cleaner environment.</p>""",
                45,
                "Sustainable water purification.",
                title="Sustainable water purification",
            )
        )
    )

    faq_items = [
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
    faq_html = "".join(
        f'<article class="ulr-amanzi-faq__item"><strong>{q}</strong><p>{a}</p></article>'
        for q, a in faq_items
    )
    parts.append(
        band(
            section_head("Support", "Frequently asked questions") + f'<{T} class="ulr-amanzi-faq">{faq_html}</{T}>',
            mod=" ulr-amanzi-band--alt",
            section_id="faq",
        )
    )

    parts.append(
        band(
            section_head("Credentials", "Registered associations")
            + """<{T} class="ulr-amanzi-badges">
  <article class="ulr-amanzi-badge"><strong>United Nations GM</strong> UNGM number 5618342</article>
  <article class="ulr-amanzi-badge"><strong>UNICEF</strong> Registered Vendor under UNGM5618343</article>
  <article class="ulr-amanzi-badge"><strong>IWA</strong> Corporate Membership number 16142154</article>
  <article class="ulr-amanzi-badge"><strong>WISA</strong> Corporate membership number 10242</article>
</{T}>"""
        )
    )

    parts.append(
        band(
            f"""{section_head("Emergency readiness", "Disaster response &amp; government readiness")}
<{T} class="ulr-amanzi-readiness__grid">
  <{T}>
    <p class="desc mb-2">In situations such as:</p>
    <ul class="desc">
      <li>flooding</li>
      <li>infrastructure failure</li>
      <li>drought</li>
      <li>contamination events</li>
      <li>humanitarian emergencies</li>
      <li>municipal water interruptions</li>
    </ul>
    <p class="desc">SANI AMANZI{TM} provides an immediate portable solution to support safer drinking water access at household and community level.</p>
  </{T}>
  <{T}>
    <p class="desc mb-2">Its lightweight sachet format allows:</p>
    <ul class="desc">
      <li>rapid transportation</li>
      <li>simplified storage</li>
      <li>scalable deployment</li>
      <li>emergency reserve stock</li>
      <li>fast humanitarian distribution</li>
    </ul>
  </{T}>
</{T}>
<h3 class="h5 mt-4 mb-2">Strategic Water Preparedness</h3>
<p class="desc">From a public health and emergency response perspective, maintaining reserve stock levels supports rapid deployment during water crises.</p>
<p class="desc">Given Nigeria&rsquo;s population of over 215 million people, scalable preparedness frameworks may involve maintaining millions of sachets monthly across regional emergency stock programs to support community-level water access during crisis situations.</p>
<p class="desc mb-2">Ubuntu Life Resources supports engagement with:</p>
<ul class="desc mb-0">
  <li>governments</li>
  <li>NGOs</li>
  <li>disaster response organisations</li>
  <li>humanitarian programs</li>
  <li>institutional buyers</li>
  <li>distribution partners</li>
</ul>""",
            mod=" ulr-amanzi-band--deep",
        )
    )

    parts.append(cta_block())
    return "\n".join(parts)


def splice_page(main_html: str) -> None:
    path = ROOT / "pillar-water-purification.html"
    text = path.read_text(encoding="utf-8")
    for marker in (
        '        <section class="ulr-amanzi-hero section-gap-x"',
        '        <section class="tj-page-header section-gap-x"',
    ):
        if marker in text:
            start = text.index(marker)
            break
    else:
        raise ValueError("Could not find water page hero section marker")
    end = text.index('        <section class="section-gap ulr-pillar-leadership-section">')
    head, tail = text[:start], text[end:]
    head = head.replace('body class="ulr-pillar-page"', 'body class="ulr-pillar-page ulr-amanzi-page"')
    if "ulr-pillar-brief.css" not in head:
        head = head.replace(
            '<link rel="stylesheet" href="assets/css/main.css">',
            '<link rel="stylesheet" href="assets/css/main.css">\n  <link rel="stylesheet" href="assets/css/ulr-pillar-brief.css">',
        )
    if "ulr-hero-glass.css" not in head:
        head = head.replace(
            '<link rel="stylesheet" href="assets/css/ulr-pillar-brief.css">',
            '<link rel="stylesheet" href="assets/css/ulr-pillar-brief.css">\n  <link rel="stylesheet" href="assets/css/ulr-hero-glass.css">',
        )
    if "ulr-amanzi-page.css" not in head:
        head = head.replace(
            '<link rel="stylesheet" href="assets/css/ulr-hero-glass.css">',
            '<link rel="stylesheet" href="assets/css/ulr-hero-glass.css">\n  <link rel="stylesheet" href="assets/css/ulr-amanzi-page.css">',
        )
    new_desc = (
        "SANI AMANZI™ water sanitising and purification — point-of-use safe drinking water "
        "for communities, governments, NGOs and emergency response."
    )
    head = head.replace(
        'content="SANI AMANZI Water Purification Solutions — portable water purification for communities, governments, NGOs and emergency response across Africa."',
        f'content="{new_desc}"',
    )
    head = head.replace(
        "<title>Water Purification Solutions | SANI AMANZI | Ubuntu Life Resources</title>",
        "<title>SANI AMANZI™ Water Sanitising &amp; Purification | Ubuntu Life Resources</title>",
    )
    path.write_text(head + main_html + "\n" + tail, encoding="utf-8")


def main() -> None:
    splice_page(build_main())
    print("Updated pillar-water-purification.html from document.")


if __name__ == "__main__":
    main()
