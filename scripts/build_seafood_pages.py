# Generates Tonno Bonno SKU pages (shell from product-sani-99-agri.html)
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = (ROOT / "product-sani-99-agri.html").read_text(encoding="utf-8")
pre, rest = BASE.split('<main id="primary" class="site-main">', 1)
inner, post = rest.split("      </main>", 1)
assert inner.startswith("\n        <div class=\"space-for-header\"></div>")

IMG = "assets/images/service/ulr-service-shelf-stable-seafood-retail.jpg"

COMMON_AGENT = (
    "<p class=\"mb-0\">Ubuntu Life Resources is the <strong>strategic agent</strong> for Tonno Bonno International in Southern Africa. "
    "We coordinate pallet-ready supply, VC 8014-aligned documentation expectations, and programme volumes without anonymous marketplace sourcing.</p>"
)

COMMON_REG = (
    "<p class=\"small text-muted mb-0\">Canned fish for the South African trade is regulated under NRCS VC 8014 (thermal process, "
    "hermetic seals, heavy-metal limits). Always retain supplier COAs and import permits your channel requires.</p>"
)


def sku_page(
    filename: str,
    h1: str,
    meta: str,
    header_lead: str,
    intro: str,
    para2: str,
    uses: list[str],
    nutrition_block: str,
    table_rows: str,
    related_html: str,
) -> str:
    h1e = h1.replace("&", "&amp;")
    uses_li = "".join(f'<li class="ulr-sku-info-list-item">{u}</li>' for u in uses)
    return f"""
        <div class="space-for-header"></div>
        <section class="tj-page-header section-gap-x" data-bg-image="{IMG}">
          <div class="container position-relative" style="z-index:2;">
            <div class="row">
              <div class="col-lg-12">
                <div class="tj-page-header-content text-center">
                  <h1 class="tj-page-title">{h1e}</h1>
                  <p class="pillar-header-lead">{header_lead}</p>
                  <div class="tj-page-link">
                    <span><i class="tji-home"></i></span>
                    <span><a href="index.html">Home</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><a href="products.html">Products</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><a href="product-tonno-bonno.html">Tonno Bonno</a></span>
                    <span><i class="tji-arrow-right"></i></span>
                    <span><span>{h1e}</span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="page-header-overlay ulr-pheader-overlay" aria-hidden="true"></div>
        </section>

        <section class="tj-about-section section-gap">
          <div class="container">
            <div class="row align-items-center g-4 g-lg-5">
              <div class="col-lg-6 order-2 order-lg-1">
                <div class="about-img overflow-hidden rounded-3 shadow">
                  <img class="w-100" src="{IMG}" alt="{h1e}.">
                </div>
              </div>
              <div class="col-lg-6 order-1 order-lg-2">
                <div class="sec-heading">
                  <span class="sub-title"><i class="tji-add-cart"></i> Food security</span>
                  <h2 class="sec-title">Shelf-stable <span>marine protein</span></h2>
                  <p class="desc">{intro}</p>
                </div>
                <p class="mb-3">{para2}</p>
                {COMMON_AGENT}
              </div>
            </div>
          </div>
        </section>

        <section class="section-gap bg-light ulr-sku-panels-section">
          <div class="container">
            <div class="row g-4 align-items-lg-stretch">
              <div class="col-lg-6">
                <article class="ulr-sku-info-card h-100">
                  <header class="ulr-sku-info-card-head">
                    <span class="sub-title"><i class="tji-organize"></i> Ideal placements</span>
                    <h3 class="ulr-sku-info-card-title sec-title h4 mb-0">Where this SKU <span>wins</span></h3>
                  </header>
                  <ul class="ulr-sku-info-list mb-0">{uses_li}</ul>
                </article>
              </div>
              <div class="col-lg-6">
                <article class="ulr-sku-info-card h-100">
                  <header class="ulr-sku-info-card-head">
                    <span class="sub-title"><i class="tji-excellence"></i> Nutrition &amp; menu logic</span>
                    <h3 class="ulr-sku-info-card-title sec-title h4 mb-0">Why buyers stock <span>this cut</span></h3>
                  </header>
                  <div class="ulr-sku-info-card-body">
                    {nutrition_block}
                  </div>
                </article>
              </div>
            </div>
          </div>
        </section>

        <section class="section-gap">
          <div class="container">
            <div class="row justify-content-center mb-4">
              <div class="col-lg-10 text-center">
                <span class="sub-title"><i class="tji-box"></i> Case configuration</span>
                <h2 class="sec-title">Standard <span>pack metrics</span></h2>
                <p class="mb-0">Use this table for pallet math and GS1 planning. Confirm MOQ and factory rotation with Sanchia when you tender.</p>
              </div>
            </div>
            <div class="row justify-content-center">
              <div class="col-lg-10">
                <div class="table-responsive border rounded-3 shadow-sm bg-white">
                  <table class="table table-striped mb-0 align-middle">
                    <thead class="table-light">
                      <tr>
                        <th scope="col">Product</th>
                        <th scope="col">Packing medium</th>
                        <th scope="col">Case count</th>
                        <th scope="col">Unit size</th>
                      </tr>
                    </thead>
                    <tbody>
                      {table_rows}
                    </tbody>
                  </table>
                </div>
                {COMMON_REG}
              </div>
            </div>
          </div>
        </section>

        <section class="section-gap bg-light ulr-related-products-section">
          <div class="container">
            <div class="sec-heading text-center mb-4">
              <span class="sub-title"><i class="tji-list"></i> Range navigation</span>
              <h2 class="sec-title">Related <span>products</span></h2>
            </div>
            <div class="row g-3 justify-content-center">
              {related_html}
            </div>
            <div class="row g-4 mt-2">
              <div class="col-md-4">
                <div class="ulr-utility-tile h-100 bg-white border rounded-3 shadow-sm overflow-hidden d-flex flex-column">
                  <div class="ulr-card-img-placeholder" aria-hidden="true"><i class="tji-list"></i></div>
                  <div class="p-4 flex-grow-1">
                    <h5 class="mb-2">Full catalogue</h5>
                    <p class="small mb-0"><a href="product-tonno-bonno.html">Tonno Bonno overview</a> lists every tuna, pilchard, and sardine page.</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="ulr-utility-tile h-100 bg-white border rounded-3 shadow-sm overflow-hidden d-flex flex-column">
                  <div class="ulr-card-img-placeholder" aria-hidden="true"><i class="tji-growth"></i></div>
                  <div class="p-4 flex-grow-1">
                    <h5 class="mb-2">Sector context</h5>
                    <p class="small mb-0"><a href="pillar-shelf-stable-nutrition.html">Shelf-stable nutrition pillar</a> explains how Ubuntu supports programmes.</p>
                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="ulr-utility-tile h-100 bg-white border rounded-3 shadow-sm overflow-hidden d-flex flex-column">
                  <div class="ulr-card-img-placeholder" aria-hidden="true"><i class="tji-organize"></i></div>
                  <div class="p-4 flex-grow-1">
                    <h5 class="mb-2">Logistics</h5>
                    <p class="small mb-0">Ambient container loads, long dated stock, and consolidated mixed-SKU pallets for retail DCs.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section class="section-gap">
          <div class="container">
            <div class="row justify-content-center">
              <div class="col-lg-10">
                <div class="p-4 p-md-5 border rounded-3 bg-light">
                  <h4 class="mb-3">Enquire on {h1e}</h4>
                  <p class="mb-1"><strong>Sanchia-Lynn Smit</strong>, CEO / Founder</p>
                  <p class="mb-1"><a href="tel:+27796588189">+27 79 658 8189</a></p>
                  <p class="mb-4"><a href="mailto:sanchia@ubuntuliferesources.co.za">sanchia@ubuntuliferesources.co.za</a></p>
                  <div class="d-flex flex-wrap gap-3">
                    <a class="tj-primary-btn" href="contact.html">
                      <span class="btn-text"><span>Contact form</span></span>
                      <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                    </a>
                    <a class="tj-primary-btn" href="products.html">
                      <span class="btn-text"><span>Product catalogue</span></span>
                      <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section class="tj-cta-section">
          <div class="container">
            <div class="row">
              <div class="col-12">
                <div class="cta-area">
                  <div class="cta-content">
                    <h2 class="title title-anim">Need pallets, mixed containers, or programme pricing?</h2>
                    <div class="cta-btn wow fadeInUp" data-wow-delay=".2s">
                      <a class="tj-primary-btn btn-dark" href="contact.html">
                        <span class="btn-text"><span>Get in touch</span></span>
                        <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                      </a>
                    </div>
                  </div>
                  <div class="cta-img">
                    <img src="assets/images/cta/ulr-cta-collaboration-wide.jpg" alt="Collaboration and next steps.">
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
""".rstrip()


def rel_card(href: str, title: str, sub: str) -> str:
    return f"""
              <div class="col-12 col-sm-6 col-lg-4">
                <a class="ulr-related-product-card text-decoration-none text-reset d-block h-100" href="{href}">
                  <div class="ulr-related-product-card-surface border rounded-3 bg-white shadow-sm h-100 overflow-hidden d-flex flex-column">
                    <div class="ulr-card-img-placeholder" aria-hidden="true"><i class="tji-box"></i></div>
                    <div class="p-3 p-lg-4 flex-grow-1">
                      <span class="d-block fw-semibold">{title}</span>
                      <span class="small text-muted">{sub}</span>
                    </div>
                  </div>
                </a>
              </div>"""


SKU_DATA = [
    {
        "filename": "product-tuna-chunks-in-brine.html",
        "h1": "Tuna chunks in brine",
        "meta": "Tonno Bonno tuna chunks in brine: 48x170g cases, lean protein for retail and institutions. Ubuntu Life Resources, Southern Africa.",
        "header_lead": "<strong>48 &times; 170&nbsp;g</strong> cases &middot; Defined muscle chunks &middot; Low-fat brine pack",
        "intro": "<strong>Tuna chunks</strong> are intact loin pieces that survive retorting with toothsome texture. Packing in brine keeps calories modest and foregrounds clean tuna flavour for salad bars, deli pots, and health-positioned retail bays.",
        "para2": "Brine (controlled saltwater) is the default choice when buyers want to avoid added oil calories but still need a shelf-stable complete protein that needs no cold chain from port to township spaza.",
        "uses": [
            "School feeding sandwiches and high-protein lunchbox programmes.",
            "QSR and canteen salad lines where oil separation is undesirable.",
            "Export repack kitchens that marinade in-house oils downstream.",
            "Disaster kits that prioritise lean protein diversity next to starch staples.",
        ],
        "nutrition_block": "<p class=\"mb-2\">High biological value protein with minimal added fat; pairs with lemon, herbs, or beans without competing lipid layers.</p><p class=\"mb-0\">Chunks hold shape in pasta bakes and hotpots better than flaked formats, reducing customer complaints about mushy texture.</p>",
        "table_rows": "<tr><td>Tuna chunks</td><td>Brine</td><td>48</td><td>170&nbsp;g</td></tr>",
        "related": [
            ("product-tuna-chunks-in-vegetable-oil.html", "Tuna chunks in vegetable oil", "Higher energy density"),
            ("product-tuna-shredded-light-brine.html", "Shredded tuna in brine", "Sandwich spread format"),
            ("product-tuna-shredded-light-olive-oil.html", "Shredded in olive oil", "Premium oil pack"),
        ],
    },
    {
        "filename": "product-tuna-chunks-in-vegetable-oil.html",
        "h1": "Tuna chunks in vegetable oil",
        "meta": "Tonno Bonno tuna chunks in vegetable oil, 48x170g. Energy-dense shelf protein via Ubuntu Life Resources.",
        "header_lead": "<strong>48 &times; 170&nbsp;g</strong> &middot; Anaerobic oil barrier &middot; Calorie uplift for vulnerable households",
        "intro": "Vegetable oil surrounds each chunk, displacing oxygen inside the can and carrying fat-soluble flavour compounds. For food-security buyers, that extra lipid load is a feature: it raises energy per gram when households lack cooking oil.",
        "para2": "Still a chunk geometry, so kitchens retain plate presence while benefiting from oil-assisted mouthfeel compared with brine-only packs.",
        "uses": [
            "Households stretching one can across multiple starch-based meals.",
            "Camp and field kitchens that need ready lipid calories without separate oil tins.",
            "Retail multipacks targeting bulk shoppers in cash-sensitive corridors.",
            "Institutional menus where dietitians sign off higher energy baskets.",
        ],
        "nutrition_block": "<p class=\"mb-2\">Delivers complete protein plus plant oil energy; useful when dietary counselling emphasises total kcal recovery, not only protein grams.</p><p class=\"mb-0\">Label-conscious retailers can still merchandise beside brine SKUs to cover both wellness and value segments.</p>",
        "table_rows": "<tr><td>Tuna chunks</td><td>Vegetable oil</td><td>48</td><td>170&nbsp;g</td></tr>",
        "related": [
            ("product-tuna-chunks-in-brine.html", "Tuna chunks in brine", "Lower fat variant"),
            ("product-tuna-shredded-light-vegetable-oil.html", "Shredded in vegetable oil", "Spreadable texture"),
            ("product-tuna-shredded-light-olive-oil.html", "Shredded in olive oil", "Premium fat profile"),
        ],
    },
    {
        "filename": "product-tuna-shredded-light-brine.html",
        "h1": "Light meat shredded tuna in brine",
        "meta": "Tonno Bonno light meat shredded tuna in brine, 48x170g cases. Sandwich and institutional protein via Ubuntu.",
        "header_lead": "<strong>48 &times; 170&nbsp;g</strong> &middot; Fine flake &middot; Rapid flavour pickup",
        "intro": "Shredded / flaked light-meat tuna increases surface area so dressings and spices penetrate quickly. Brine packing keeps the profile lean for calorie-capped programmes while still delivering full tuna umami.",
        "para2": "Food technologists like the format for emulsified spreads, fish cakes, and volume sandwich fillings where chunk geometry would shred unevenly during mixing.",
        "uses": [
            "Large-scale sandwich manufacturing and airline catering trays.",
            "Blended protein dips with mayonnaise or yoghurt bases.",
            "Communal kitchens that batch-cook fillings for hundreds of portions.",
            "Nutrition NGOs fortifying composite meals with fish flavour kids accept.",
        ],
        "nutrition_block": "<p class=\"mb-2\">Higher surface-area-to-weight ratio speeds sodium and acid equilibration, so recipe developers hit flavour targets faster than with whole chunks.</p><p class=\"mb-0\">Still retorted shelf-stable, so cold-chain gaps do not interrupt feeding cycles.</p>",
        "table_rows": "<tr><td>Light meat shredded</td><td>Brine</td><td>48</td><td>170&nbsp;g</td></tr>",
        "related": [
            ("product-tuna-shredded-light-vegetable-oil.html", "Shredded in vegetable oil", "Oil-based flake"),
            ("product-tuna-chunks-in-brine.html", "Chunks in brine", "Plated texture"),
            ("product-tuna-shredded-light-olive-oil.html", "Shredded in olive oil", "Premium oil"),
        ],
    },
    {
        "filename": "product-tuna-shredded-light-vegetable-oil.html",
        "h1": "Light meat shredded tuna in vegetable oil",
        "meta": "Tonno Bonno shredded tuna in vegetable oil, 48x170g. Spreadable shelf protein via Ubuntu Life Resources.",
        "header_lead": "<strong>48 &times; 170&nbsp;g</strong> &middot; Flake + oil &middot; Sandwich and sauce workhorse",
        "intro": "Combining flake geometry with vegetable oil yields a forgiving, scoopable texture straight from the can. Oil lubricates portioning equipment in industrial kitchens and stops flakes clumping in steam tables.",
        "para2": "Buyers who need tuna flavour distribution across starch bases (pap, rice, flatbread) often prefer this SKU to chunks because it folds through heat without breaking customer expectations on bite size.",
        "uses": [
            "Bulk sandwich lines and meal-kit assembly.",
            "Saucy casseroles where oil becomes part of the sauce body.",
            "Field kitchens needing spoonable protein for rapid service.",
            "Retail delis selling flavoured tuna salads in oil.",
        ],
        "nutrition_block": "<p class=\"mb-2\">Delivers combined protein and fat calories for households under energy stress while staying fish-forward for micronutrient diversity.</p><p class=\"mb-0\">Pairs with chilli, herbs, or tomato sofos without extra fry oil in the pan.</p>",
        "table_rows": "<tr><td>Light meat shredded</td><td>Vegetable oil</td><td>48</td><td>170&nbsp;g</td></tr>",
        "related": [
            ("product-tuna-shredded-light-brine.html", "Shredded in brine", "Lean flake"),
            ("product-tuna-chunks-in-vegetable-oil.html", "Chunks in vegetable oil", "Chunk oil pack"),
            ("product-tuna-shredded-light-olive-oil.html", "Shredded in olive oil", "Olive oil premium"),
        ],
    },
    {
        "filename": "product-tuna-shredded-light-olive-oil.html",
        "h1": "Light meat shredded tuna in olive oil",
        "meta": "Tonno Bonno shredded tuna in olive oil, 48x170g. Premium monounsaturated fat profile via Ubuntu.",
        "header_lead": "<strong>48 &times; 170&nbsp;g</strong> &middot; Olive oil &middot; Premium aisle positioning",
        "intro": "Olive oil carries polyphenol complexity and a softer mouthfeel than standard vegetable oil, signalling premium placement in supermarkets and hospitality grab-and-go sets.",
        "para2": "Still the shredded geometry for fast marination, but with a heart-health story that resonates with Discovery-type healthy-food catalogue positioning referenced for the broader Tonno Bonno range.",
        "uses": [
            "Upsell bays next to speciality crackers and antipasti.",
            "Hotel breakfast buffets and airline premium cabins.",
            "Corporate wellness gifting and high-end disaster comfort packs.",
            "Deli counters merchandising Mediterranean flavour cues.",
        ],
        "nutrition_block": "<p class=\"mb-2\">Monounsaturated fat emphasis supports cardiovascular messaging when paired with responsible portion guidance.</p><p class=\"mb-0\">Oil colour and aroma differentiate the can on shelf versus generic vegetable oil competitors.</p>",
        "table_rows": "<tr><td>Light meat shredded</td><td>Olive oil</td><td>48</td><td>170&nbsp;g</td></tr>",
        "related": [
            ("product-tuna-shredded-light-vegetable-oil.html", "Shredded in vegetable oil", "Value oil flake"),
            ("product-tuna-chunks-in-vegetable-oil.html", "Chunks in vegetable oil", "Chunk format"),
            ("product-tuna-chunks-in-brine.html", "Chunks in brine", "Brine baseline"),
        ],
    },
    {
        "filename": "product-pilchards-tomato-sauce.html",
        "h1": "Pilchards in tomato sauce",
        "meta": "Tonno Bonno pilchards in tomato sauce: 24x155g or 12x400g. Calcium-rich shelf fish via Ubuntu Life Resources.",
        "header_lead": "<strong>Tomato sauce</strong> &middot; 24 &times; 155&nbsp;g or 12 &times; 400&nbsp;g &middot; Staple carbohydrate pairing",
        "intro": "Pilchards are larger sardine-family fish; retorting softens vertebrae into an edible calcium source. Tomato sauce adds lycopene-rich acidity that balances oil-forward fish and clings to pap, ugali, or rice without extra stew ingredients.",
        "para2": "The 400&nbsp;g line suits multi-person households and community pots; the 155&nbsp;g line fits single-heat servings in tuck shops and school feeding lines.",
        "uses": [
            "National school nutrition programmes needing one-can-one-pot simplicity.",
            "Wholesale cash-and-carry pallet builds for township independent retailers.",
            "NGO buckets paired with maize meal in drought corridors.",
            "Military and mine site mess halls rotating canned protein menus.",
        ],
        "nutrition_block": "<p class=\"mb-2\">Combines heme iron, long-chain Omega-3, and vegetable-sauce antioxidants in one shelf-stable unit.</p><p class=\"mb-0\">Sauce viscosity is tuned so heat-up time stays short on paraffin or induction plates.</p>",
        "table_rows": "<tr><td>Pilchards</td><td>Tomato sauce</td><td>24</td><td>155&nbsp;g</td></tr>"
        "<tr><td>Pilchards</td><td>Tomato sauce</td><td>12</td><td>400&nbsp;g</td></tr>",
        "related": [
            ("product-pilchards-chilli-sauce.html", "Pilchards in chilli sauce", "Heat-forward variant"),
            ("product-pilchards-vegetable-oil.html", "Pilchards in vegetable oil", "Oil-only pack"),
            ("product-sardines-tomato-sauce.html", "Sardines in tomato sauce", "Smaller fish format"),
        ],
    },
    {
        "filename": "product-pilchards-chilli-sauce.html",
        "h1": "Pilchards in chilli sauce",
        "meta": "Tonno Bonno pilchards in chilli sauce, 24x155g or 12x400g. Spiced shelf protein via Ubuntu.",
        "header_lead": "<strong>Chilli sauce</strong> &middot; Regional palate heat &middot; Dual case sizes",
        "intro": "Capsicum-forward sauce lifts metabolic zest and masks residual fish notes for consumers who prefer assertive seasoning. Same dual case ladder as tomato for logistics continuity.",
        "para2": "Heat level is formulated for broad Southern African preference profiles, not novelty-scoville extremes, so institutions can serve large cohorts safely.",
        "uses": [
            "Street-food vendors topping vetkoek or roasted mealies.",
            "University and factory canteens with spice-forward daily menus.",
            "Retail multipacks in peri-urban corridors where chilli variants outsell plain tomato.",
            "Export markets with diaspora demand for heat-balanced sauces.",
        ],
        "nutrition_block": "<p class=\"mb-2\">Capsaicin can modestly increase satiety signals, helpful when portion sizes are budget-capped.</p><p class=\"mb-0\">Still delivers pilchard calcium and Omega-3 benefits underneath the sauce matrix.</p>",
        "table_rows": "<tr><td>Pilchards</td><td>Chilli sauce</td><td>24</td><td>155&nbsp;g</td></tr>"
        "<tr><td>Pilchards</td><td>Chilli sauce</td><td>12</td><td>400&nbsp;g</td></tr>",
        "related": [
            ("product-pilchards-tomato-sauce.html", "Pilchards in tomato sauce", "Tomato baseline"),
            ("product-pilchards-vegetable-oil.html", "Pilchards in vegetable oil", "Oil pack"),
            ("product-sardines-chilli-sauce.html", "Sardines in chilli sauce", "Smaller fish chilli"),
        ],
    },
    {
        "filename": "product-pilchards-vegetable-oil.html",
        "h1": "Pilchards in vegetable oil",
        "meta": "Tonno Bonno pilchards in vegetable oil, 24x155g or 12x400g. Energy-dense canned fish via Ubuntu.",
        "header_lead": "<strong>Vegetable oil</strong> &middot; Highest lipid calories in pilchard line &middot; Dual sizes",
        "intro": "Oil-packed pilchards trade sauce viscosity for pure lipid energy, ideal when households already have tomato or onion sofrito at home and mainly need fish plus cooking medium in one can.",
        "para2": "Chefs can drain oil for frying aromatics, then flake fish into the same pan, reducing total oil spend in ultra price-sensitive kitchens.",
        "uses": [
            "Bulk humanitarian crates where recipients request oil-inclusive rations.",
            "Traditional Sunday cooks who finish pilchards in self-made tomato gravy.",
            "Small restaurants controlling sauce salt independently.",
            "Cross-dock mixes with tomato SKUs for balanced pallet merchandising.",
        ],
        "nutrition_block": "<p class=\"mb-2\">Delivers maximum kcal per shelf cm versus brine or light sauce packs, important when stunting risk tracks total energy availability.</p><p class=\"mb-0\">Oil clarity signals quality control at receiving docks.</p>",
        "table_rows": "<tr><td>Pilchards</td><td>Vegetable oil</td><td>24</td><td>155&nbsp;g</td></tr>"
        "<tr><td>Pilchards</td><td>Vegetable oil</td><td>12</td><td>400&nbsp;g</td></tr>",
        "related": [
            ("product-pilchards-tomato-sauce.html", "Pilchards in tomato sauce", "Sauced variant"),
            ("product-pilchards-chilli-sauce.html", "Pilchards in chilli sauce", "Spiced sauced"),
            ("product-sardines-vegetable-oil.html", "Sardines in vegetable oil", "Smaller fish oil"),
        ],
    },
    {
        "filename": "product-sardines-tomato-sauce.html",
        "h1": "Sardines in tomato sauce",
        "meta": "Tonno Bonno sardines in tomato sauce, 24x155g or 12x400g. Fine-texture Omega-3 fish via Ubuntu.",
        "header_lead": "<strong>Tomato sauce</strong> &middot; EPA/DHA rich smaller fish &middot; Dual case sizes",
        "intro": "Sardines deliver finer muscle texture than pilchards but share the same sauced convenience. Tomato base supports iron absorption synergies when served with fortified starches in nutrition programmes.",
        "para2": "Smaller fish cook quicker in the can, yielding tender bite through the lateral line while bones soften for calcium uptake in children and elders.",
        "uses": [
            "Primary school feeding where bite size must be child friendly.",
            "Retail twin-packs for single-adult households.",
            "Community nutrition drives pairing one can with bulk starch bags.",
            "Coastal informal traders needing fast stock rotation SKUs.",
        ],
        "nutrition_block": "<p class=\"mb-2\">EPA/DHA density per gram remains high because sardines are oily forage fish; tomato adds vitamin C partner nutrients.</p><p class=\"mb-0\">Sauce colour aids visual appetite appeal in photography for social grant communications.</p>",
        "table_rows": "<tr><td>Sardines</td><td>Tomato sauce</td><td>24</td><td>155&nbsp;g</td></tr>"
        "<tr><td>Sardines</td><td>Tomato sauce</td><td>12</td><td>400&nbsp;g</td></tr>",
        "related": [
            ("product-sardines-vegetable-oil.html", "Sardines in vegetable oil", "Oil variant"),
            ("product-sardines-chilli-sauce.html", "Sardines in chilli sauce", "Chilli variant"),
            ("product-pilchards-tomato-sauce.html", "Pilchards in tomato sauce", "Larger fish tomato"),
        ],
    },
    {
        "filename": "product-sardines-vegetable-oil.html",
        "h1": "Sardines in vegetable oil",
        "meta": "Tonno Bonno sardines in vegetable oil, 24x155g or 12x400g. Shelf-stable Omega-3 via Ubuntu Life Resources.",
        "header_lead": "<strong>Vegetable oil</strong> &middot; Fine texture &middot; Dual case sizes",
        "intro": "Oil-packed sardines shine when buyers want to drain and pan-fry quickly, crisping skin while keeping interior moist. The oil doubles as sauté medium for onions before returning fish to the pan.",
        "para2": "Matches pilchard oil logistics for mixed pallets while offering a lower price point per can for budget aisles.",
        "uses": [
            "Households batch-preparing fish cakes with minimal extra fat.",
            "Backpacking and trail ration packs needing spill-resistant protein.",
            "Hospitality breakfast buffets with Mediterranean mezze spreads.",
            "Wholesale split cases to spaza shops with high oil preference.",
        ],
        "nutrition_block": "<p class=\"mb-2\">Preserves long-chain Omega-3 alongside lipid energy; helpful when total dietary fat targets are still below WHO minima.</p><p class=\"mb-0\">Clear oil appearance aids QC spot checks for rancidity before acceptance.</p>",
        "table_rows": "<tr><td>Sardines</td><td>Vegetable oil</td><td>24</td><td>155&nbsp;g</td></tr>"
        "<tr><td>Sardines</td><td>Vegetable oil</td><td>12</td><td>400&nbsp;g</td></tr>",
        "related": [
            ("product-sardines-tomato-sauce.html", "Sardines in tomato sauce", "Tomato sauced"),
            ("product-sardines-chilli-sauce.html", "Sardines in chilli sauce", "Chilli sauced"),
            ("product-pilchards-vegetable-oil.html", "Pilchards in vegetable oil", "Larger fish oil"),
        ],
    },
    {
        "filename": "product-sardines-chilli-sauce.html",
        "h1": "Sardines in chilli sauce",
        "meta": "Tonno Bonno sardines in chilli sauce, 24x155g or 12x400g. Spiced fine-texture fish via Ubuntu.",
        "header_lead": "<strong>Chilli sauce</strong> &middot; Smaller fish &middot; Dual case sizes",
        "intro": "Combines sardine tenderness with a spiced sauce matrix that carries chilli heat without overwhelming calcium-rich bone softness.",
        "para2": "Ideal rotation SKU next to tomato sardines so retailers capture variety seekers without doubling cold-chain risk because both are ambient.",
        "uses": [
            "Student res dining halls with diverse spice preferences.",
            "Convenience stores near taxi ranks selling heat-and-eat combos.",
            "Food parcel diversity rotations in extended disaster seasons.",
            "Cross-border traders needing HS-code-friendly shelf-stable protein.",
        ],
        "nutrition_block": "<p class=\"mb-2\">Heat increases sensory satisfaction on lower per-meal meat grams, supporting compliance in rationed programmes.</p><p class=\"mb-0\">Maintains Omega-3 payload underneath sauce solids.</p>",
        "table_rows": "<tr><td>Sardines</td><td>Chilli sauce</td><td>24</td><td>155&nbsp;g</td></tr>"
        "<tr><td>Sardines</td><td>Chilli sauce</td><td>12</td><td>400&nbsp;g</td></tr>",
        "related": [
            ("product-sardines-tomato-sauce.html", "Sardines in tomato sauce", "Mild sauced"),
            ("product-sardines-vegetable-oil.html", "Sardines in vegetable oil", "Oil only"),
            ("product-pilchards-chilli-sauce.html", "Pilchards in chilli sauce", "Larger fish chilli"),
        ],
    },
]


def main():
    for d in SKU_DATA:
        related_html = "".join(rel_card(h, t, s) for h, t, s in d["related"])
        main = sku_page(
            d["filename"],
            d["h1"],
            d["meta"],
            d["header_lead"],
            d["intro"],
            d["para2"],
            d["uses"],
            d["nutrition_block"],
            d["table_rows"],
            related_html,
        )
        if not main.startswith("\n        "):
            main = "\n" + main
        out = pre + '<main id="primary" class="site-main">' + main + "\n      " + "</main>" + post
        title = f"{d['h1']} | Ubuntu Life Resources"
        out = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", out, count=1, flags=re.DOTALL)
        out = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{d["meta"]}">',
            out,
            count=1,
        )
        (ROOT / d["filename"]).write_text(out, encoding="utf-8")
        print("wrote", d["filename"])
    print("done")


if __name__ == "__main__":
    main()
