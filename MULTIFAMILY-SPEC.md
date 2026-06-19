# BASE4 — Multifamily Page Audit & Redesign Spec
**Source audited:** https://www.base-4.com/multifamily/
**Audience:** Multifamily **developers, owners/operators, and general contractors** (market-rate, BTR, affordable, student)
**Goal:** Modernize look + UX while keeping every existing element in play. Nothing dropped — only upgraded, relocated, or added.
**Build target:** Single-file `index.html`, embedded TSV parsed at runtime, Cloudflare Pages — **identical engine to the hospitality rebuild** (`/base4 hospitality rebuild/index.html`). This page is a sibling, not a fork.

> **Carryover principle:** every improvement shipped on the hospitality rebuild applies here. This spec notes what's *the same* (reuse as-is) and what's *different* for multifamily (the buyer cares about unit yield and repeatability, not brand flags). New multifamily-only additions flagged in §5.

---

## 1. Audit Summary — What's Holding It Back

Same legacy template as hospitality, so the same core issues — plus two multifamily-specific gaps (#7, #8).

| # | Issue | Impact | Fix |
|---|-------|--------|-----|
| 1 | Legacy WordPress / Slider-Revolution-style build | Heavy, slow, dated, hard to maintain | Rebuild as static single-file HTML (reuse hospitality engine) |
| 2 | All project images are lazy-loaded `data:image/svg+xml` placeholders | Real renders don't paint on first load → looks broken | Eager-load hero + above-fold; lazy below fold (real CDN assets in §6) |
| 3 | Only conversion path is a `mailto:` link (`BlairH@base-4.com`) | High friction, no tracking, no lead capture | Inline consultation form + mailto fallback |
| 4 | Copy is generic ("efficiency, cost, speed") with **zero numbers** | MF developers underwrite on yield, unit count, cost/door | Add metrics: units designed, states, product types, stories |
| 5 | No process / "how we work" section | Developers + GCs need delivery clarity before trusting speed claims | Add 4-step delivery timeline |
| 6 | Dead "Featured Projects" filter — only `All / MF-showcase` | Filter UI exists, does nothing | Re-tab by **product type** (or region) |
| 7 | **No unit-yield / efficiency proof** — the #1 multifamily buyer metric | Reads like a brochure, not a yield partner | Lead value-prop + stat tiles with units/door-count framing |
| 8 | **No range-of-product signal** (garden, mid-rise, podium/wrap, townhome, BTR) | Developers can't tell if BASE4 fits their product | Add a "product types we deliver" band (replaces hospitality's brand-flag wall) |
| 9 | No differentiation vs. other A&E firms | Generic | Lead with **integrated A+E + industrialized construction + repeatable rollouts** |
| 10 | "STAY UPDATED" newsletter has no working form | Dead element | Wire it or fold into footer |
| 11 | No analytics events on CTAs | Can't measure funnel | GA4 events on every CTA (matches hospitality scope) |

---

## 2. Element Inventory — Every Existing Element, Mapped

> Rule: **nothing unused.** Each element is **Kept**, **Upgraded**, **Relocated**, or **Merged**. New additions in §5.

| Existing element | Disposition | Where it lands |
|---|---|---|
| Logo "BASE4" | Kept | Sticky header, left |
| Social icons (FB, X, LinkedIn, IG, YouTube) | Kept | Header + footer |
| Main nav (Projects, Data Centers ▸ Data Center Insights, Markets ▸ Hospitality/Multifamily, Innovation Lab ▸ Destination/Industrialized Construction, Blog ▸ Infographics, About ▸ Our Clients, Contact ▸ Careers) | Kept | Sticky header dropdowns |
| Hero headline "Multifamily Design & Engineering" | Upgraded | New hero §4.1, sharper headline |
| Hero subhead ("balance efficiency, cost, and speed to market") | Upgraded | Hero subhead, tightened |
| CTA "View Our Multifamily Portfolio" | Kept | Hero secondary CTA |
| "Designed for Scale and Efficiency" block | Upgraded | Becomes the **value-prop strip** §4.2 |
| Home-strip images: Fuze520 – Maricopa AZ, Flatz308 – Casa Grande AZ | Relocated + Upgraded | Feed the **product-type band** §5 / gallery (see §6.3 — Fuze520 is a 7th project) |
| "What Drives Multifamily Projects" (4 bullets) | Upgraded | Becomes **"What Developers Are Actually Buying"** §4.3 |
| "Featured Multifamily Projects" grid (6 projects) | Upgraded | New **project gallery** with product-type filter §4.5 |
| Project filter tabs (All / MF-showcase) | Upgraded | Re-tab by product type / region |
| 6 projects (Flatz308; Multifamily Townhomes; Community Apartments Edgewater FL; Riverbend North Phase 2 Otsego MN; Yellowstone Landing Belgrade MT; Fuze512 San Marcos TX) | Kept | Project data table §6 |
| "SEE ALL PROJECTS" button → /projects/ | Kept | End of gallery |
| "Why BASE4" (4 bullets) | Upgraded | Becomes **differentiators** §4.4 with icons |
| (No testimonials on page) | Added | New **proof band** §4.6 — logo/metric wall as interim |
| CTA "Schedule a Project Consultation" (mailto:BlairH@base-4.com) | Kept + Upgraded | Primary CTA → inline form; mailto fallback |
| Newsletter "STAY UPDATED" + email field | Merged | Folded into footer, wired or removed |
| "Florida Registered Architectural Firm - AA26003324" | Kept | Footer credibility line |
| "© 2026 BASE4 \| All rights reserved." | Kept | Footer |
| Footer nav + social repeat | Kept | Footer |
| Newsletter / back-to-top | Kept | Floating back-to-top |
| Brand green `#8dc63f` | Kept | Primary accent §3 |

---

## 3. Design System

**Identical to the hospitality rebuild** — reuse the same tokens so the two market pages are visually a set.

- **Accent:** `#8dc63f` · **Ink:** `#0E1A14` · **Deep:** `#1C3A2E` · **Surface:** `#FFFFFF` / `#F5F7F4` · **Hairline:** `#E3E8E1`
- **Type:** Inter Tight (display) + Inter (body); tabular figures for all metrics. H1 `clamp(2.5rem,5vw,4rem)`, H2 ~2rem, body 1.0625rem, lh 1.6.
- **Layout/motion:** max 1200px, 8px grid, sticky condensing header, restrained scroll-reveal (200–300ms), floating back-to-top, mobile-first.
- **Imagery:** project gallery uses the **real BASE4 CDN photos in §6.2** — no placeholders. Hero + section-break slots use **Unsplash** (apartment/residential exteriors). Above-fold eager, below-fold `loading="lazy"`.

---

## 4. Section-by-Section Redesign

### 4.1 — Hero
- **Eyebrow:** `MULTIFAMILY ARCHITECTURE · ENGINEERING · DELIVERY`
- **H1:** *Multifamily designed for unit yield, built for speed to market.*
- **Subhead:** BASE4 partners with multifamily developers, owners, and general contractors to deliver projects that maximize unit yield and constructability — integrated architecture and engineering, repeatable across your pipeline.
- **Primary CTA:** `Schedule a Project Consultation` → inline form
- **Secondary CTA:** `View Multifamily Portfolio` (kept)
- **Trust micro-row:** `Florida Registered Architectural Firm AA26003324 · High-volume residential experience · Integrated A + E`
- **Visual:** full-bleed mid-rise/garden apartment exterior at dusk, dark-green gradient overlay.

### 4.2 — Value-Prop Strip (from "Designed for Scale and Efficiency")
> **Designed for scale and efficiency.**
> Multifamily projects live and die on unit yield, cost control, and repeatability. BASE4 keeps architecture and engineering under one roof — maximizing doors per acre while holding quality and constructability, project after project.

- 3 stat tiles (derived from §6.1 — use as a floor; confirm portfolio-wide with BASE4):
  - `708+ units designed` (204 + 24 + 168 + 312 across the 4 featured projects with disclosed counts)
  - `5 states` (AZ, FL, MN, MT, TX)
  - `Garden → mid-rise` (product range, 3–4 stories across featured work)
- **UX:** quantified yield credibility immediately after hero. Numbers persuade.

### 4.3 — "What Developers Are Actually Buying" (from "What Drives Multifamily Projects")
Reframe the 4 existing bullets as buyer priorities tied to delivery.

| Priority (existing bullet) | The BASE4 answer |
|---|---|
| Unit efficiency & layout optimization | Plans optimized for doors-per-acre and rentable-area efficiency without sacrificing livability |
| Cost control & constructability | Engineered for buildable, value-stable details — fewer field surprises, tighter budgets |
| Speed through entitlement & delivery | Coordinated documents that clear entitlement faster and keep delivery on schedule |
| Repetition & scalability across projects | Repeatable prototypes + industrialized construction so a winning building travels across your pipeline |

- **Format:** 4 cards, icon + priority + answer.

### 4.4 — Differentiators (from "Why BASE4")
- **Integrated A + E** — architecture and engineering under one contract; one team accountable end to end.
- **Proven at residential volume** — experience delivering high-volume multifamily for active developers.
- **Engineered for yield + cost** — layouts and systems tuned for unit yield and constructability.
- **Built for repeatable rollouts** — prototype + industrialized construction systems for multi-site pipelines.
- **Format:** 2×2 grid. Link out to **Innovation Lab → Industrialized Construction Systems** here.

### 4.5 — Project Gallery (from "Featured Multifamily Projects")
- **Filter tabs (re-tabbed):** `All · Garden · Mid-Rise · Townhome · Mixed-Use` — *recommended; confirm type assignment with BASE4.* **Fallback (fully derivable from data): re-tab by region** `All · AZ · FL · MN · MT · TX`.
- **Grid:** responsive cards, hover lift, type/region tag, location, unit count, stories.
- 6 existing projects (+ room for Fuze520 as 7th, §6.3). Click → lightbox of all project photos (§6.2).
- **CTA:** `See All Projects` → /projects/ (kept).

### 4.6 — Proof / Trust Band
- No testimonials exist on the live page. Per the hospitality convention: **interim = metric/region proof wall**; swap to real quotes when BASE4 supplies developer/GC voices.
- `Read More Client Stories` → existing `/our-clients/`.

### 4.7 — Final Conversion Band
- **Headline:** *Planning a multifamily project? Get an integrated A+E team focused on unit yield and speed to market.*
- **Primary CTA:** `Schedule a Project Consultation` → inline form (name, company, email, project location, product type, # units, message).
- **Fallback:** `mailto:BlairH@base-4.com` preserved (subject pre-fill `| Multifamily | BASE4`).
- Dark-green band, single action, GA4 conversion on submit.

---

## 5. New Components to Add

1. **Product-type band** *(multifamily replacement for hospitality's brand-flag wall)* — Garden, Mid-Rise, Podium/Wrap, Townhome, Build-to-Rent. Signals range so a developer instantly sees fit. Use the existing Fuze520 / Flatz308 strip imagery here.
2. **4-step delivery timeline** — *Concept & Programming → Entitlements → Construction Documents → Construction Support.*
3. **Inline consultation form** — replaces mailto-only friction; captures product type + unit count to qualify the lead. Mailto fallback retained.
4. **Stat tiles** — units / states / product range (confirm portfolio-wide numbers with BASE4).
5. **Sticky condensing header + floating back-to-top** — same components as hospitality.

---

## 6. Project Data (TSV-Ready) + Photo Manifest

All specs + image URLs scraped live from each portfolio page. Every URL is a real `base-4.com` CDN asset.

### 6.1 — Project specs (drop-in TSV)
```tsv
name	type	location	units	stories	year	services	url	primary_image
Flatz308 – Casa Grande, AZ	Garden	Casa Grande, AZ	204	3	2023	Architectural; Structural; MEP; Exterior Renderings	https://www.base-4.com/portfolio/flatz308-casa-grande-az/	https://www.base-4.com/wp-content/uploads/2025/02/Flatz308-–-Casa-Grande-AZ-01.jpg
Multifamily Townhomes	Townhome	—	24	3	—	Exterior Renderings; Site Plan Design; Conceptual Design; Initial Programming	https://www.base-4.com/portfolio/multifamily-townhomes/	https://www.base-4.com/wp-content/uploads/2025/07/Multifamily-Townhomes-01.jpg
Community Apartments – Edgewater, FL	Garden	Edgewater, FL	—	—	2023	Exterior Renderings; Site Plan Design; Conceptual Design; Initial Programming	https://www.base-4.com/portfolio/community-apartments-edgewater-fl/	https://www.base-4.com/wp-content/uploads/2023/01/Community-Apartments-–-Edgewater-FL-01.jpg
Riverbend North Phase 2 – Otsego, MN	Mid-Rise	Otsego, MN	—	—	2022	Concept Design; Architectural; Structural; MEP; Exterior Renderings; Interior Design	https://www.base-4.com/portfolio/riverbend-north-phase-2-otsego-mn/	https://www.base-4.com/wp-content/uploads/2022/11/Riverbend-North-Phase-2-Otsego-MN-01.jpg
Yellowstone Landing – Belgrade, MT	Mid-Rise	Belgrade, MT	168	4	2020	Architectural; Structural; MEP; Exterior Renderings; Construction Administration; Interior Design	https://www.base-4.com/portfolio/yellowstone-landing-belgrade-mt/	https://www.base-4.com/wp-content/uploads/2024/12/Yellowstone-Landing-Belgrade-MT-001.jpg
Fuze512 Development – San Marcos, TX	Mixed-Use	San Marcos, TX	312	—	2020	Exterior Renderings; Site Plan Design; Architectural; MEP; Structural; Construction Administration	https://www.base-4.com/portfolio/fuze512-development-san-marcos-tx/	https://www.base-4.com/wp-content/uploads/2020/11/Fuze512-Development-San-Marcos-TX-001.jpg
```
> **Confirm with BASE4:** unit counts for Community Apartments + Riverbend (not published); stories for Community Apartments / Riverbend / Fuze512; and the `type` assignments above (inferred from stories/scale — verify Garden/Mid-Rise/Mixed-Use/Townhome).

### 6.2 — Full image manifest (every scraped photo URL)

**Logo:** `https://www.base-4.com/wp-content/uploads/2018/09/cropped-Base4_Logo-270x270.jpg`

**Flatz308 – Casa Grande, AZ** (14)
- `…/2025/02/Flatz308-–-Casa-Grande-AZ-01.jpg`
- `…/2025/07/Flatz308-Casa-Grande-AZ-02.jpg`
- `…/2025/07/Flatz308-Casa-Grande-AZ-03.jpg`
- `…/2025/02/Flatz308-Casa-Grande-AZ-04.jpg` → through `-14.jpg` (04–14 all under `/2025/02/`)

**Multifamily Townhomes** (4)
- `…/2025/07/Multifamily-Townhomes-01.jpg` → `-04.jpg`

**Community Apartments – Edgewater, FL** (5)
- `…/2023/01/Community-Apartments-–-Edgewater-FL-01.jpg` → `-05.jpg`

**Riverbend North Phase 2 – Otsego, MN** (1)
- `…/2022/11/Riverbend-North-Phase-2-Otsego-MN-01.jpg`

**Yellowstone Landing – Belgrade, MT** (~26 — most photographed project)
- `…/2024/12/Yellowstone-Landing-Belgrade-MT-001.jpg`
- `…/2025/03/Yellowstone-Landing-Belgrade-MT-19.jpg` … `-26.jpg`
- `…/2022/08/Yellowstone-Landing-Belgrade-MT-001.jpg`, `-07-1.jpg`, `-10-1.jpg`, `-25.jpg`, `-26.jpg`
- `…/2024/06/Yellowstone-Landing-–-Belgrade-MT-001.jpg`, `-003.jpg`, `-006.jpg`
- `…/2024/10/Yellowstone-Landing-–-Belgrade-MT-11.jpg`, `-12.jpg`, `-14.jpg`, `-15.jpg`
- `…/2024/12/Yellowstone-Landing-–-Belgrade-MT-17.jpg`, `-18.jpg`
- `…/2022/11/Yellowstone-Landing-–-Belgrade-MT-02.jpg`, `-04.jpg`, `-05.jpg`
- *(Note: filenames mix en-dash and hyphen and span multiple upload dates — use exactly as scraped; some are re-renders of the same view. Pick the cleanest 6–8 for the lightbox.)*

**Fuze512 Development – San Marcos, TX** (9)
- `…/2020/11/Fuze512-Development-San-Marcos-TX-001.jpg`
- `…/2021/12/Fuze512-Development-San-Marcos-TX-007.jpg`, `-8.jpg`, `-9.jpg`, `-10.jpg`, `-11.jpg`
- `…/2024/06/Fuze512-Development-San-Marcos-TX-16.jpg`, `-17.jpg`, `-001.jpg`

**Total: ~59 project photos + 1 logo.**

### 6.3 — Could NOT be fully resolved (need raw HTML / direct upload)
- The home-strip images in "Designed for Scale" lazy-load without resolvable URLs: **Fuze520 – Maricopa, AZ** and **Flatz308**. Recover via `data-lazy-src` in raw HTML or direct upload.
- **Fuze520 – Maricopa, AZ is a *7th* multifamily project** not in the featured grid — worth adding as a 7th gallery card once assets are supplied.

---

## 7. Conversion & Analytics

- GA4 events on: hero primary CTA, hero secondary CTA, each project card click, "See All Projects," consultation form submit, mailto fallback click, newsletter signup, product-type filter.
- Primary conversion = **form submit** (`generate_lead`); mailto click = secondary.
- Keep `BlairH@base-4.com` routing (preserve the `| Multifamily | BASE4` subject pre-fill).
- Newsletter: wire to a real list or retire — no dead field.

---

## 8. Build Notes

- **Reuse the hospitality engine verbatim** — same single-file `index.html`, embedded `# SHEET:`-delimited TSV parsed at runtime, same CSS tokens, same JS (header condense, reveal, lightbox, filter, GA4, mailto form). Only the TSV content and a few labels (`keys`→`units`, brand filter→type filter, brand wall→product-type band) change.
- Hero + first project row eager-loaded; everything else `loading="lazy"`.
- No build step, no DB. Carry over SEO meta/OG/Twitter; preserve FL registration + `© 2026 BASE4`.
- `FORM_ENDPOINT` constant left empty → mailto fallback until a real capture endpoint is wired.

---

### Open items to confirm with BASE4 before build
1. Real portfolio-wide numbers (units / states / project count).
2. Unit counts + stories missing for Community Apartments, Riverbend, Fuze512.
3. Product-type assignments (Garden / Mid-Rise / Mixed-Use / Townhome) for the filter.
4. Testimonials/quotes availability (else metric wall only).
5. Fuze520 – Maricopa AZ + Flatz308 strip images — recover from raw HTML or direct upload (§6.3); add Fuze520 as 7th project.
6. Whether the newsletter list is live.
