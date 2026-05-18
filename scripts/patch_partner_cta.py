from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
text = p.read_text(encoding="utf-8")
start = text.find('<section id="partner"')
end = text.find("<!-- end: Partner CTA -->")
if start == -1 or end == -1:
    raise SystemExit(f"markers not found: {start}, {end}")

new_block = """        <section id="partner" class="section-gap section-gap-x ulr-partner-section">
          <div class="container">
            <motion class="ulr-partner-card wow fadeInUp" data-wow-delay=".08s">
              <div class="row g-4 g-lg-5 align-items-start">
                <div class="col-lg-8">
                  <span class="ulr-partner-eyebrow"><i class="tji-team"></i> Partner with us</span>
                  <h2 class="ulr-partner-title title-anim">Expand your products and solutions into African markets</h2>
                  <p class="ulr-partner-lead">Ubuntu Life Resources welcomes collaboration with manufacturers, suppliers, distributors, investors, institutions, NGOs, agricultural groups, and strategic partners seeking structured market access and commercial growth across Southern Africa and selected Sub-Saharan African regions.</p>
                  <p class="ulr-partner-tagline">Let&rsquo;s build scalable, impact-driven solutions together.</p>
                  <a class="tj-primary-btn" href="contact.html">
                    <span class="btn-text"><span>Contact us today</span></span>
                    <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
                  </a>
                </div>
                <motion class="col-lg-4">
                  <aside class="ulr-partner-aside">
                    <p class="ulr-partner-aside-label">Leadership</p>
                    <p class="ulr-partner-aside-name mb-0">Sanchia-Lynn Smit</p>
                    <p class="ulr-partner-aside-role">CEO / Founder<br>Ubuntu Life Resources</p>
                    <p class="mb-0"><a href="mailto:sanchia@ubuntuliferesources.co.za">sanchia@ubuntuliferesources.co.za</a></p>
                    <p class="ulr-partner-aside-loc mb-0">South Africa</p>
                  </aside>
                </div>
              </div>
            </div>
          </div>
        </section>
        """
new_block = new_block.replace("motion", "div")

text = text[:start] + new_block + text[end:]
p.write_text(text, encoding="utf-8")
print("Patched partner CTA")
