# Infographics / Resource Library — Developer Handoff

**Deliverable:** `infographics/v2/index.html` — a single, self-contained page: a **filterable, searchable
library of infographic resources**, each gated behind a **lead-capture download form**. It rebuilds
`base-4.com/infographics/`. No build step, no framework, no database.

**This is a lead-generation funnel, not a static gallery.** Every "Download" opens a form that captures
name + email (+ company/phone/newsletter opt-in) before the resource opens. Read §3 and §4 before launch —
the funnel is not wired to capture leads yet, and the "downloads" don't point at real files yet.

---

## 1. How the page is built

Single file: inline `<style>`, inline `<script>`, hardcoded HTML. Unlike the market-page rebuilds
(hospitality / multifamily), **this page has no TSV data block** — the resource cards are authored directly
as HTML.

- **Header / nav / footer** — hardcoded HTML (not generated).
- **Resource grid** — 10 `<article class="card">` elements inside `#grid`. Each card carries
  `data-category` (hvac / modular / systems / plumbing) and `data-title`, plus a thumbnail `<img>`, an
  `<h3>`, and a description.
- **Filter + search** — the filter buttons (`data-filter`) and the search box filter cards live in JS
  (`update()`), matching on category + title/description text. An empty-state block shows when nothing
  matches.
- **Download flow** — JS appends a "Download" button to each card; clicking the button *or the thumbnail*
  opens the **download modal** (`#downloadModal`), a lead form. On submit it posts the lead (or falls back
  to mailto), then opens the resource URL in a new tab.
- **Consultation flow** — a second modal (`#consultModal`); also reachable from the "Prefer to talk…" link
  inside the download modal, and from the page's CTA.
- **Newsletter** — footer form; submits via mailto.
- **Social icons** — injected by JS from the `SOCIALS` array (current BASE4 AEC handles).

### To add / edit a resource
Copy an existing `<article class="card">` block in `#grid` and edit its `data-category`, `data-title`,
thumbnail `src`/`alt`, heading, and description. To give it a custom download-modal subtitle, add an entry
to the `DOWNLOAD_SUBTEXTS` map in the script (keyed by the exact `data-title`). New categories also need a
matching `<button class="filter" data-filter="…">`.

---

## 2. WordPress integration

Same two routes as the market-page handoffs:

- **Route A — native page template (recommended):** port the `<body>` markup + `<style>` + `<script>` into
  a full-width child-theme template; publish at the `/infographics/` slug. Best for SEO and consistency.
- **Route B — iframe embed:** fastest, fully isolated. **Note:** unlike the market pages, this file has
  **no embed height-reporter**, so an auto-height iframe won't self-size — use a fixed-height iframe
  (`height:100vh`), or add the reporter. Also, the download/consult modals are `position:fixed`, so in a
  tall iframe they'd mis-center (same caveat as the market pages' Route B).

---

## 3. Pre-launch checklist — MUST fix (the funnel is inert without these)

- [ ] **`FORM_ENDPOINT` is empty** (top of the script). Until it's set, **every lead form — download,
      consultation, and newsletter — falls back to `mailto:BlairH@base-4.com`**. That means no lead is
      captured in a CRM; it just opens the visitor's email client. Point it at the production lead-capture
      endpoint to actually collect leads.
- [ ] **The "downloads" don't point at real files.** The download opens `img.src` — i.e. the card's
      **thumbnail/header JPG**, not a downloadable PDF. Example: the "HVAC for Multifamily" download opens
      `…/HVAC-for-Multifamily-Header-Website.jpg`. Supply the real resource URL (PDF or full infographic)
      for each of the 10 cards and wire it — e.g. add a `data-download="…"` attribute per card and have
      `openDownload()` use it instead of the thumbnail `src`.
- [ ] **The gate is bypassable.** Because the resource opens only after the form and uses the thumbnail
      URL, a visitor can also just open the image directly. Once real gated files exist, confirm whether
      they should be truly access-controlled (signed URLs / endpoint-issued links) or if open URLs are
      acceptable.

## 4. Pre-launch checklist — should fix

- [ ] **Consultation modal is hotel-only.** Its copy says "brand, site, key count," and the fields are
      **Brand / flag** (Hyatt / Marriott / …) and **# of keys**. This page serves hotel *and* multifamily
      *and* data-center audiences — generalize the fields (project type, units/keys, etc.) or make them
      market-neutral.
- [ ] **Privacy Policy link is commented out** in the download form's legal text, with a note to "Replace #
      with the confirmed BASE4 Privacy Policy URL before launch." Since the form collects PII and offers a
      marketing opt-in, add the real Privacy Policy link before go-live.
- [ ] **No analytics.** This page has **no GA4 / gtag** at all (the market pages do). For a lead-gen page,
      add conversion tracking on download-form submit, consult submit, filter clicks, and search — or wire
      it through the site's global tag manager.
- [ ] **Hero background is a Google Drive image**
      (`lh3.googleusercontent.com/d/1rZOSXenpgYtVtTb9ff75YkOWYjtdE4dC`). Drive-hosted images are unreliable
      for production (rate limits, can stop serving). Move it to the WP Media Library or the repo.
- [ ] **Featured-guide section is dead code.** A "Featured Guide" block is commented out (its JS is guarded
      with `?.`, so it's harmless). Decide whether to ship it or delete the block + its script.
- [ ] **Verify footer links.** `/markets/` and `/about/` are hardcoded in the footer — confirm those slugs
      exist on base-4.com (the market rebuilds used different paths).

---

## 5. External dependencies

- `fonts.googleapis.com`, `fonts.gstatic.com` — Inter / Inter Tight
- `ohshtnvm.github.io/innolab-rebuild/6-29-iteration/logos/base4-logo.png` — the BASE4 logo (header +
  footer). Depends on that repo staying published; move to WP media if you want no external dependency.
- `lh3.googleusercontent.com` — hero background (see §4; replace)
- `www.base-4.com` — all card thumbnails, and the current (placeholder) download targets
- `mailto:BlairH@base-4.com` — the fallback for all three forms until `FORM_ENDPOINT` is set

## 6. Content inventory (10 resources)

HVAC (3): HVAC for Multifamily · HVAC Systems for Hotel Projects · Hotel HVAC Options
Modular (5): Modular Construction Logistics · How Bathroom Pods Equal Savings · Modular FAQ Part 1 ·
Modular FAQ Part 2 · Bathroom Pods: Faster, Cheaper, Smarter
Plumbing (1): Tankless Water Heater Systems
Building Systems (1): Trusses vs. I-Joists

## 7. Design tokens (shared with the market rebuilds)

Accent green `#8dc63f` · Deep green `#1c3a2e` · Ink `#0e1a14` · Surface `#fff` / alt `#f4f7f2` ·
hairline `#e2e8df` · Inter Tight (display) + Inter (body) · max width 1200px.

---

*Current state: page renders and runs with no console errors; filters, search, both modals, and the mailto
fallback all work. The blockers above are integration/content gaps, not bugs.*
