import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
t = p.read_text(encoding="utf-8")

t = re.sub(
    r'\s*<div class="banner-scroll[^"]*"[^>]*>.*?</div>\s*',
    "\n",
    t,
    count=1,
    flags=re.S,
)

new_hero = """          <div class="hero-visual-strip wow fadeIn" data-wow-delay=".25s">
            <div class="hero-split-banner" role="group" aria-label="Featured photography: farmer spraying, Water Purification Solutions hands, Tonno Bonno warehouse, hygiene and sanitation">
              <article class="ulr-hero-tile">
                <div class="ulr-hero-tile__image">
                  <img src="bio.jpeg" alt="Farmer spraying, agricultural biosecurity." width="640" height="480" decoding="async" fetchpriority="high">
                  <span class="ulr-hero-tile__label">Agricultural Biosecurity</span>
                </div>
              </article>
              <article class="ulr-hero-tile">
                <div class="ulr-hero-tile__image">
                  <img src="water.jpeg" alt="Hands with water, water purification solutions." width="640" height="480" decoding="async" fetchpriority="high">
                  <span class="ulr-hero-tile__label">Water Purification Solutions</span>
                </div>
              </article>
              <article class="ulr-hero-tile">
                <div class="ulr-hero-tile__image">
                  <img src="food.jpeg" alt="Tonno Bonno warehouse, shelf-stable food supply." width="640" height="480" decoding="async" fetchpriority="high">
                  <span class="ulr-hero-tile__label">Food Security</span>
                </div>
              </article>
              <article class="ulr-hero-tile ulr-hero-tile--hygiene">
                <div class="ulr-hero-tile__image">
                  <div class="ulr-hero-tile__image-placeholder" role="img" aria-label="Hygiene and sanitation image placeholder">
                    <i class="tji-image" aria-hidden="true"></i>
                    <span class="ulr-hero-tile__image-placeholder-label">Coming soon</span>
                  </div>
                  <span class="ulr-hero-tile__label">Hygiene &amp; Sanitation</span>
                </div>
              </article>
            </div>
          </div>
        </section>"""

m = re.search(r'<div class="hero-visual-strip.*?</section>', t, re.S)
if not m:
    raise SystemExit("hero block not found")
t = t[: m.start()] + new_hero + t[m.end() :]
p.write_text(t, encoding="utf-8", newline="\n")
print("patched", p)
