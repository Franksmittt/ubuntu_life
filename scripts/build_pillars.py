# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = "div"  # HTML tag name for wrappers


def media(slug, n):
    folder = ROOT / "assets/images/pillars" / slug
    for ext in (".jpeg", ".jpg", ".png", ".webp"):
        p = folder / f"ulr-{slug}-{n:02d}{ext}"
        if p.exists():
            return f"assets/images/pillars/{slug}/ulr-{slug}-{n:02d}{ext}"
    return None


def ul(items):
    return '<ul class="desc mb-0">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def sec(title, body, image=None, alt="", flip=False, bg=False):
    cls = "section-gap ulr-brief-section" + (" bg-light" if bg else "")
    if not image:
        return (
            f'<section class="{cls}"><{T} class="container">'
            f'<{T} class="ulr-brief-copy mx-auto" style="max-width:52rem;">'
            f'<h2 class="sec-title h3 mb-3">{title}</h2>{body}</{T}></{T}></section>'
        )
    img_col = (
        f'<{T} class="col-lg-6"><figure class="ulr-brief-figure m-0">'
        f'<img src="{image}" alt="{alt}" class="w-100 rounded-3 shadow-sm" loading="lazy" decoding="async">'
        f"</figure></{T}>"
    )
    txt_col = (
        f'<{T} class="col-lg-6"><{T} class="ulr-brief-copy">'
        f'<h2 class="sec-title h3 mb-3">{title}</h2>{body}</{T}></{T}>'
    )
    row = (txt_col + img_col) if flip else (img_col + txt_col)
    return (
        f'<section class="{cls}"><{T} class="container">'
        f'<{T} class="row g-4 g-lg-5 align-items-center">{row}</{T}></{T}></section>'
    )


def page_header(h1, lead, crumb, bg):
    return f"""        <section class="tj-page-header section-gap-x" data-bg-image="{bg}">
          <{T} class="container position-relative" style="z-index:2;">
            <{T} class="row">
              <{T} class="col-lg-12">
                <{T} class="tj-page-header-content text-center">
                  <h1 class="tj-page-title">{h1}</h1>
                  <p class="pillar-header-lead">{lead}</p>
                  <{T} class="tj-page-link">
                    <span><i class="tji-home"></i></span>
                    <span><a href="index.html">Home</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><a href="pillars.html">Core pillars</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><span>{crumb}</span></span>
                  </{T}>
                </{T}>
              </{T}>
            </{T}>
          </{T}>
          <{T} class="page-header-overlay ulr-pheader-overlay" aria-hidden="true"></{T}>
        </section>"""


def cta(title, intro, bullets=None):
    bl = ul(bullets) if bullets else ""
    return f"""        <section class="tj-cta-section section-gap-x">
          <{T} class="container">
            <{T} class="row">
              <{T} class="col-12">
                <{T} class="cta-area">
                  <{T} class="cta-content">
                    <h2 class="title title-anim">{title}</h2>
                    <p class="desc">{intro}</p>
                    {bl}
                    <{T} class="cta-btn mt-3 d-flex flex-wrap gap-2">
                      <a class="tj-primary-btn btn-dark" href="contact.html"><span class="btn-text"><span>Contact Us</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
                      <a class="tj-primary-btn btn-dark" href="tel:+27796588189"><span class="btn-text"><span>WhatsApp 079 658 8189</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
                    </{T}>
                    <p class="desc mt-3 mb-0"><a href="mailto:sanchia@ubuntuliferesources.co.za">sanchia@ubuntuliferesources.co.za</a> &middot; <a href="https://www.ubuntuliferesources.co.za" target="_blank" rel="noopener noreferrer">www.ubuntuliferesources.co.za</a></p>
                  </{T}>
                  <{T} class="cta-img"><img src="assets/images/cta/ulr-cta-collaboration-wide.jpg" alt="Contact Ubuntu Life Resources." loading="lazy" decoding="async"></{T}>
                </{T}>
              </{T}>
            </{T}>
          </{T}>
        </section>"""


def build_agri():
    s = "agri-biosecurity"
    parts = [
        page_header(
            "Agricultural Biosecurity Starts Here",
            "Advanced Veterinary Grade Disinfection Solutions For Modern Agriculture. Ubuntu Life Resources delivers scalable agricultural biosecurity solutions through <strong>SANI-99&trade; for AGRI</strong> &mdash; helping farms, poultry operations, abattoirs, dairies, hatcheries and food processing environments reduce pathogen risks and improve hygiene standards.",
            "Agricultural Biosecurity",
            media(s, 1),
        ),
        f"""        <section class="section-gap pt-0 pb-4">
          <{T} class="container text-center">
            <p class="desc mb-3">Agricultural Biosecurity &middot; Water Purification Solutions &middot; Food Security</p>
            <{T} class="d-flex flex-wrap gap-2 justify-content-center">
              <a class="tj-primary-btn" href="product-sani-99-agri.html"><span class="btn-text"><span>SANI-99&trade; Product Page</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
              <a class="tj-primary-btn" href="contact.html"><span class="btn-text"><span>Contact Us</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
            </{T}>
          </{T}>
        </section>""",
        sec(
            "What Is SANI-99&trade; for AGRI?",
            """<p class="desc">SANI-99&trade; for AGRI is a veterinary and food grade agricultural disinfectant designed to support biosecurity across multiple agricultural sectors.</p>
<p class="desc">The solution has been developed to assist farms and agricultural facilities in reducing pathogen exposure while supporting hygiene, operational safety and disease prevention protocols.</p>
<p class="desc mb-2"><strong>SANI-99&trade; for AGRI provides:</strong></p>"""
            + ul(
                [
                    "Broad-spectrum disinfection",
                    "360&deg; biosecurity support",
                    "High efficacy pathogen control",
                    "Long-lasting residual activity",
                    "Food and veterinary grade applications",
                    "Agricultural equipment sanitation",
                    "Facility and livestock area disinfection",
                ]
            )
            + '<p class="desc mt-3 mb-0">Designed for modern agriculture, SANI-99&trade; for AGRI supports operations ranging from poultry and livestock farming to abattoirs, dairies, aquaculture and food processing facilities.</p>',
            media(s, 2),
            "SANI-99 for AGRI disinfectant.",
        ),
        sec(
            "Key Features",
            ul(
                [
                    "<strong>360&deg; Agricultural Biosecurity</strong> &mdash; comprehensive disinfection across livestock facilities, poultry housing, food processing environments, equipment sanitation and operational hygiene protocols.",
                    "<strong>Alcohol &amp; Chlorine Free</strong> &mdash; reduces harsh chemical exposure while maintaining strong disinfection performance.",
                    "<strong>Safe Around Livestock</strong> &mdash; designed for agricultural environments where animal welfare remains essential.",
                    "<strong>Food &amp; Veterinary Grade</strong> &mdash; suitable for multiple agricultural and food-related applications.",
                    "<strong>Halal Certified</strong> &mdash; supports diverse agricultural and food production requirements.",
                ]
            ),
            media(s, 3),
            "SANI-99 key features.",
            flip=True,
        ),
        sec(
            "Industries &amp; Applications",
            "<p class=\"desc mb-2\">SANI-99&trade; for AGRI supports a wide range of agricultural industries and operational environments including:</p>"
            + ul(
                [
                    "Poultry Farming",
                    "Livestock Facilities",
                    "Dairy Operations",
                    "Hatcheries",
                    "Abattoirs",
                    "Cold Storage Facilities",
                    "Food Processing Areas",
                    "Aquaculture",
                    "Crop Production",
                    "Horticulture",
                    "Agricultural Machinery",
                    "Water Systems &amp; Foot Baths",
                ]
            )
            + "<p class=\"desc mt-3 mb-0\">The solution can be integrated into both preventative hygiene protocols and active biosecurity management systems.</p>",
            media(s, 4),
            "Industries and applications.",
        ),
        sec(
            "Eliminating Pathogens, Viruses &amp; Diseases",
            "<p class=\"desc\">SANI-99&trade; for AGRI has been formulated to assist in controlling and reducing exposure to a broad spectrum of pathogens affecting agricultural environments.</p><p class=\"desc mb-2\">This includes support against:</p>"
            + ul(
                [
                    "E.coli",
                    "Salmonella",
                    "Listeria monocytogenes",
                    "Newcastle Disease",
                    "Avian Influenza",
                    "Swine Flu",
                    "Foot &amp; Mouth Disease",
                    "Poxviridae",
                    "Staphylococcus aureus",
                    "Enterococcus hirae",
                    "Pseudomonas aeruginosa",
                ]
            )
            + "<p class=\"desc mt-3 mb-0\">Its broad-spectrum disinfection capabilities support improved operational hygiene across agricultural sectors.</p>",
            media(s, 5),
            "Pathogen control.",
            flip=True,
        ),
        sec(
            "Advanced Poultry Biosecurity",
            "<p class=\"desc\">The poultry industry faces increasing pressure from airborne disease transmission, Avian Influenza outbreaks and operational hygiene risks.</p><p class=\"desc mb-2\">SANI-99&trade; for AGRI supports poultry biosecurity protocols through:</p>"
            + ul(
                [
                    "Poultry housing disinfection",
                    "Fogging applications",
                    "Airborne pathogen reduction support",
                    "Surface sanitation",
                    "Dust suppression support",
                    "Foot bath applications",
                    "Equipment sanitation",
                ]
            )
            + "<p class=\"desc mt-3 mb-0\">The fogging application process assists in improving coverage throughout poultry facilities while supporting operational hygiene standards.</p>",
            media(s, 6),
            "Poultry biosecurity.",
        ),
        sec(
            "Abattoirs &amp; Food Processing",
            "<p class=\"desc mb-2\">SANI-99&trade; for AGRI supports hygiene management within:</p>"
            + ul(
                [
                    "Abattoirs",
                    "Meat processing facilities",
                    "Carcass washing systems",
                    "Equipment sanitation",
                    "Biosecurity control areas",
                    "Food processing environments",
                ]
            )
            + "<p class=\"desc mt-3 mb-2\">Applications include:</p>"
            + ul(
                [
                    "Equipment disinfection",
                    "Surface sanitation",
                    "Carcass dipping",
                    "Processing area disinfection",
                    "Worker hygiene support",
                    "Facility sanitation",
                ]
            ),
            media(s, 7),
            "Abattoir and food processing.",
            flip=True,
        ),
        sec(
            "Certifications &amp; Approvals",
            "<p class=\"desc mb-2\">SANI-99&trade; for AGRI aligns with multiple international and agricultural disinfection standards and approvals including:</p>"
            + ul(
                [
                    "DEFRA Approval",
                    "ECHA Approval",
                    "BEIC Approval",
                    "EN1276",
                    "EN13697",
                    "EN14476",
                    "EN1040",
                    "EN13727",
                    "SANS 51276",
                    "SANS 53697",
                ]
            )
            + "<p class=\"desc mt-3 mb-0\">These certifications support its use across veterinary hygiene, agricultural biosecurity and food-related operational environments.</p>",
            media(s, 8),
            "Certifications.",
        ),
        sec(
            "Flexible Application Methods",
            "<p class=\"desc mb-2\">SANI-99&trade; for AGRI supports multiple agricultural application methods including:</p>"
            + ul(
                [
                    "Fogging",
                    "Pressure Washers",
                    "Sprayers",
                    "Foot Baths",
                    "Dip Tanks",
                    "Handheld Sprayers",
                    "Soaking Tubs",
                    "Surface Wipes",
                    "Agricultural Machinery Sanitation",
                ]
            )
            + "<p class=\"desc mt-3 mb-0\">This flexibility allows integration into both small-scale and industrial agricultural operations.</p>",
            media(s, 9),
            "Application methods.",
            flip=True,
        ),
        sec(
            "Available Product Formats",
            f"""<{T} class="row g-3">
              <{T} class="col-md-6"><{T} class="p-4 border rounded-3 h-100 bg-light"><h4 class="h5">96g Sachets</h4><p class="desc small mb-0">Ideal for backpack sprayers, fogging systems, foot baths, small-scale sanitation and portable applications.</p></{T}></{T}>
              <{T} class="col-md-6"><{T} class="p-4 border rounded-3 h-100 bg-light"><h4 class="h5">1kg &ndash; 25kg Tubs</h4><p class="desc small mb-0">Ideal for pressure washers, large agricultural operations, IBC systems, industrial sanitation and commercial agricultural deployment.</p></{T}></{T}>
            </{T}>""",
            media(s, 10),
            "Product formats.",
        ),
        sec(
            "Smarter Transport. Lower Environmental Impact.",
            """<p class="desc">At Ubuntu Life Resources, sustainability and operational efficiency form part of our long-term agricultural biosecurity vision.</p>
<p class="desc">SANI-99&trade; for AGRI is supplied in concentrated powder form, significantly reducing transport weight, storage requirements and plastic container usage compared to traditional pre-mixed disinfectants.</p>
<p class="desc mb-2"><strong>Example:</strong></p>
<div class="ulr-brief-compare">
  <motion class="ulr-brief-compare-card"><strong>66</strong><span class="small d-block">trucks for 2 million litres of pre-mixed disinfectant</span></div>
  <div class="ulr-brief-compare-card"><strong>1</strong><span class="small d-block">truck for equivalent SANI-99&trade; for AGRI volume</span></div>
</motion>
<p class="desc mb-0">This dramatically improves logistics efficiency, deployment scalability, storage management, distribution capability and carbon footprint reduction. Designed for commercial farms, poultry operations, abattoirs, distributors, government biosecurity programmes and emergency outbreak response.</p>""".replace(
                "<motion", f"<{T}"
            ).replace("</motion>", f"</{T}>"),
            media(s, 11),
            "Transport efficiency.",
            flip=True,
        ),
        f"""        <section class="section-gap bg-light ulr-brief-section">
          <{T} class="container">
            <{T} class="sec-heading text-center mb-5">
              <h2 class="sec-title">Tailored Agricultural <span>Biosecurity Solutions</span></h2>
              <p class="desc mx-auto" style="max-width:40rem;">Different agricultural environments face different pathogen risks and operational challenges.</p>
            </{T}>
            <{T} class="row g-4">
              <{T} class="col-lg-4"><{T} class="p-4 bg-white border rounded-3 h-100 shadow-sm"><h3 class="h5">Poultry Operations</h3><p class="desc small mb-0">Fogging solutions for poultry house disinfection, airborne pathogen reduction support, dust suppression, surface sanitation and improved hygiene management.</p></{T}></{T}>
              <{T} class="col-lg-4"><{T} class="p-4 bg-white border rounded-3 h-100 shadow-sm"><h3 class="h5">Abattoirs &amp; Food Processing</h3><p class="desc small mb-0">Carcass washing protocols, equipment sanitation, surface disinfection, worker hygiene support, processing area sanitation and biosecurity compliance measures.</p></{T}></{T}>
              <{T} class="col-lg-4"><{T} class="p-4 bg-white border rounded-3 h-100 shadow-sm"><h3 class="h5">Piggeries &amp; Livestock</h3><p class="desc small mb-0">Facility sanitation, livestock area disinfection, equipment hygiene, disease prevention support and operational biosecurity.</p></{T}></{T}>
            </{T}>
            <figure class="ulr-brief-figure mt-5 mb-0"><img src="{media(s,12)}" alt="Tailored biosecurity." class="w-100 rounded-3 shadow-sm" loading="lazy" decoding="async"></figure>
          </{T}>
        </section>""",
        sec(
            "Simple To Deploy",
            "<p class=\"desc mb-2\"><strong>Standard Sachet Mixing Example:</strong> 96g Sachet + 16 Litres Water</p><p class=\"desc mb-2\">Coverage guidelines:</p>"
            + ul(
                [
                    "High contamination: up to 160m&sup2;",
                    "Medium contamination: up to 400m&sup2;",
                    "Low contamination: up to 800m&sup2;",
                ]
            )
            + "<p class=\"desc mt-3 mb-0\">The concentrated formula allows scalable deployment while simplifying transport and storage requirements.</p>",
            media(s, 13),
            "Deployment guide.",
        ),
        sec(
            "Why Ubuntu Life Resources",
            "<p class=\"desc mb-2\">Ubuntu Life Resources focuses on supporting:</p>"
            + ul(["Agricultural Biosecurity", "Water Purification Solutions", "Food Security Initiatives"])
            + "<p class=\"desc mt-3 mb-0\">We work alongside agricultural networks, institutional stakeholders and operational partners to help strengthen hygiene and biosecurity standards across Africa and international markets.</p>",
            media(s, 14),
            "Ubuntu Life Resources.",
            flip=True,
        ),
        cta(
            "Ready to Discuss Agricultural Biosecurity Solutions?",
            "We welcome engagement from farms, poultry operations, dairies, abattoirs, food processing facilities, agricultural groups, government departments, distributors and biosecurity stakeholders.",
            [
                "Farms",
                "Poultry Operations",
                "Dairies",
                "Abattoirs",
                "Food Processing Facilities",
                "Agricultural Groups",
                "Government Departments",
                "Distributors",
                "Biosecurity Stakeholders",
            ],
        ),
    ]
    return "\n".join(parts)


def build_food():
    s = "food-supply"
    hero = media(s, 1) or "assets/images/tonno-bonno/ulr-utility-sector-nutrition.jpg"
    parts = [
        page_header(
            "Reliable Supply. Nutritious Choice.",
            "Premium canned seafood solutions for wholesalers, distributors, retailers, institutions and government food programs across Africa and selected international markets. Ubuntu Life Resources supports structured food supply partnerships through <strong>Tonno Bonno</strong>.",
            "Strategic Food Supply",
            hero,
        ),
        f"""        <section class="section-gap pt-0 pb-4">
          <{T} class="container text-center">
            <a class="tj-primary-btn" href="product-tonno-bonno.html"><span class="btn-text"><span>View Tonno Bonno Catalogue</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
          </{T}>
        </section>""",
        sec(
            "Who We Supply",
            ul(
                [
                    "Food Importers",
                    "National Distributors",
                    "Supermarket Chains",
                    "Wholesale Food Suppliers",
                    "Government Feeding Programs",
                    "NGOs &amp; Humanitarian Organizations",
                    "Military Supply Programs",
                    "Hospitality &amp; Catering Groups",
                    "Schools, Hospitals &amp; Institutions",
                ]
            ),
            "assets/images/tonno-bonno/ulr-utility-logistics.jpg",
            "Tonno Bonno supply chain.",
        ),
        sec(
            "Pilchards",
            "<p class=\"desc\"><strong>Pilchards In Tomato Sauce</strong> &mdash; 155g, 400g. Rich in Omega-3 and packed in quality tomato sauce.</p><p class=\"desc\"><strong>Pilchards In Chilli Sauce</strong> &mdash; 155g, 400g. A flavorful option for markets preferring bold and spicy seafood products.</p><p class=\"desc mb-0\"><strong>Pilchards In Vegetable Oil</strong> &mdash; 155g, 400g. Premium pilchards packed in vegetable oil for versatile consumption and broad market appeal.</p>",
            "assets/images/tonno-bonno/ulr-related-pilchard-thumb.jpg",
            "Pilchards range.",
            flip=True,
        ),
        sec(
            "Sardines",
            "<p class=\"desc\"><strong>Sardines In Tomato Sauce</strong> &mdash; 155g, 400g.</p><p class=\"desc\"><strong>Sardines In Chilli Sauce</strong> &mdash; 155g, 400g.</p><p class=\"desc mb-0\"><strong>Sardines In Vegetable Oil</strong> &mdash; 155g, 400g. High-quality sardines preserved in vegetable oil for everyday consumption and commercial supply.</p>",
            "assets/images/tonno-bonno/ulr-related-sardine-thumb.jpg",
            "Sardines range.",
        ),
        sec(
            "Tuna",
            "<p class=\"desc\"><strong>Light Meat Tuna Chunks In Brine</strong> &mdash; 170g. Premium tuna chunks in brine, high in protein.</p><p class=\"desc mb-0\"><strong>Light Meat Shredded Tuna In Brine</strong> &mdash; 170g. Light shredded tuna offering convenience, quality nutrition and broad consumer appeal.</p>",
            "assets/images/tonno-bonno/ulr-related-tuna-thumb.jpg",
            "Tuna range.",
            flip=True,
        ),
        sec(
            "Why Tonno Bonno",
            ul(
                [
                    "<strong>Premium Quality</strong> &mdash; produced according to international food quality and safety standards.",
                    "<strong>Reliable Supply</strong> &mdash; structured supply capability supporting regional and international demand.",
                    "<strong>Nutritious Protein Source</strong> &mdash; rich in Omega-3 and high-quality protein.",
                    "<strong>Commercial Packaging</strong> &mdash; suitable for retail, wholesale and institutional supply channels.",
                    "<strong>Trusted Market Positioning</strong> &mdash; supporting sustainable food supply solutions across Africa and selected global markets.",
                ]
            ),
            "assets/images/tonno-bonno/ulr-utility-full-catalogue.jpg",
            "Tonno Bonno catalogue.",
        ),
        sec(
            "Expanding Across Africa &amp; The Middle East",
            "<p class=\"desc mb-2\">Ubuntu Life Resources is actively supporting food distribution and market expansion across:</p>"
            + ul(["Southern Africa", "East Africa", "West Africa", "Selected Middle Eastern Markets"])
            + "<p class=\"desc mt-3 mb-0\">We continue building strategic partnerships with distributors, importers, wholesalers and institutional buyers throughout these regions.</p>",
            hero,
            "Regional expansion.",
            flip=True,
            bg=True,
        ),
        f"""        <section class="section-gap ulr-brief-section">
          <{T} class="container">
            <h2 class="sec-title h3 mb-3">Bulk Supply &amp; Packaging</h2>
            <table class="ulr-product-table">
              <thead><tr><th>Product</th><th>Sizes</th><th>Packaging</th></tr></thead>
              <tbody>
                <tr><td>Pilchards</td><td>155g / 400g</td><td>24 cans / 12 cans</td></tr>
                <tr><td>Sardines</td><td>155g / 400g</td><td>24 cans / 12 cans</td></tr>
                <tr><td>Tuna</td><td>170g</td><td>48 cans</td></tr>
              </tbody>
            </table>
          </{T}>
        </section>""",
        cta(
            "Ready to Discuss Supply Opportunities?",
            "Ubuntu Life Resources supports structured food supply partnerships across wholesale, retail, government and institutional sectors. Wholesale enquiries, distribution opportunities and bulk supply requests welcome.",
            ["Importers", "Distributors", "Retailers", "Government Procurement Departments", "NGOs &amp; Humanitarian Organizations", "Institutional Buyers"],
        ),
    ]
    return "\n".join(parts)


def build_amanzi():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "generate_amanzi_scisan_page",
        ROOT / "scripts" / "generate_amanzi_scisan_page.py",
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build_main()


def splice_page(filename, main_html, leadership_marker='        <section class="section-gap ulr-pillar-leadership-section">'):
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    start = text.index('        <section class="tj-page-header section-gap-x"')
    end = text.index(leadership_marker)
    head, tail = text[:start], text[end:]
    if "ulr-pillar-brief.css" not in head:
        head = head.replace(
            '<link rel="stylesheet" href="assets/css/main.css">',
            '<link rel="stylesheet" href="assets/css/main.css">\n  <link rel="stylesheet" href="assets/css/ulr-pillar-brief.css">',
        )
    # update meta/title per page handled separately
    path.write_text(head + main_html + "\n" + tail, encoding="utf-8")


def main():
    splice_page("pillar-agri-biosecurity.html", build_agri())
    splice_page("pillar-shelf-stable-nutrition.html", build_food())
    splice_page("pillar-water-purification.html", build_amanzi())
    print("Updated 3 pillar pages.")


if __name__ == "__main__":
    main()
