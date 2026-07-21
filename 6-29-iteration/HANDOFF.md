# Hospitality Page — Developer Handoff (Route A: WordPress-native template)

**Deliverable:** `6-29-iteration/index.html` — a single, self-contained rebuild of the
`base-4.com/hospitality/` page. All markup, CSS, JavaScript, and page copy are inside this one
file. No build step, no framework, no database.

**Goal of Route A:** port this into the WordPress theme as a real, full-width page at
`/hospitality/` (or a staging slug) so it is a native, indexable WP page — not an iframe.

---

## 1. How the page is built (read this first)

The page renders itself **at runtime from an embedded data block**. There is no static
per-section HTML to copy out — the JS builds the DOM on load:

1. `<script id="content-tsv" type="text/tab-separated-values">` holds all content as
   `# SHEET:`-delimited, **tab-separated** tables (Hero, Stats, Differentiators, Projects,
   RenderReality, Nav, Testimonials, etc.).
2. The app `<script>` parses that TSV and injects the sections into these container elements:
   - `#header` → nav (`#mainNav`) + socials (`#headerSocials`)
   - `#app` → hero, brand marquee, "Why BASE4" (USP cards), portfolio gallery (`#projects`),
     Render→Reality carousel (`#render-reality`), testimonials, closing CTA (`#consult`)
   - `#footer` → footer columns + socials
   - `#lightbox`, `#consultModal` → gallery lightbox and the consultation form modal
3. Behavior wired on load: sticky/condensing header, scroll-reveal, brand marquee + R→R
   auto-carousel, gallery filter + lightbox, consultation modal, mailto form fallback, GA events.

**Implication:** keep the file as one unit. Do not split it into page-builder blocks — that
breaks the render model and the shared stylesheet.

---

## 2. Recommended integration — custom page template

Work in a **child theme** so updates to the parent theme don't overwrite this.

1. Create a template file, e.g. `template-hospitality.php`, in the child theme.
2. Decide the site chrome (pick one):
   - **Standalone / blank canvas (highest fidelity):** the page already ships its own header,
     nav, and footer. Use a canvas template that does **not** call `get_header()` /
     `get_footer()`, so it renders exactly like the standalone file. Simplest, zero theme-CSS
     conflicts.
   - **Wrapped in the global site chrome:** call `get_header()` / `get_footer()` and **remove
     this file's own `<header>` and `<footer>`** to avoid duplicates. Better for consistency
     with the rest of base-4.com, but you'll reconcile the theme's header CSS with the page.
3. Move the file's parts into the template:
   - The `<style>` block → enqueue as a stylesheet (`wp_enqueue_style`) or inline in the template.
   - The `<body>` inner markup (the `#header`/`#app`/`#footer`/`#lightbox`/`#consultModal`
     containers) → the template body.
   - Both `<script>` blocks — **including** the `type="text/tab-separated-values"` TSV block —
     before `</body>`. The TSV block must be present or the page renders empty.
   - The `<head>` extras (Google Fonts `<link>`, canonical, OG/Twitter meta) → enqueue/`wp_head`.
4. In WP admin: create a Page, assign the template, set the slug, publish.

Do **not** paste the full `<!DOCTYPE html>…</html>` document into a normal WP page/Custom-HTML
block — you can't nest a whole document inside the theme's `<body>`.

### Gotchas
- **Vanilla JS, no jQuery.** Runs on `DOMContentLoaded`. It targets fixed IDs
  (`#app`, `#footer`, `#content-tsv`, `#lightbox`, `#consultModal`, …) — make sure nothing else
  on the page reuses those IDs.
- **Theme CSS bleed.** If you wrap it in site chrome, the theme's global `img{}`, `a{}`,
  container `max-width`, or `box-sizing` rules can interfere. The blank-canvas template avoids
  this entirely.
- **Full-width.** The layout expects the viewport width (max content width is 1200px, handled
  internally). Don't constrain it inside a narrow theme container.

---

## 3. Assets & the `ASSET_BASE` switch

Images, the hero video, and logos are **not** embedded — they load from an absolute base URL set
by one constant near the top of the app script:

```js
const ASSET_BASE = 'https://ohshtnvm.github.io/innolab-rebuild/6-29-iteration/';
```

Everything local (logos, `usp/`, `rvr/`, `base4-hero.mp4` + poster) resolves against this;
anything already absolute (e.g. `base-4.com` photos) passes through untouched.

**For a self-contained WP install (recommended for production):** upload the asset folders
(`logos/`, `usp/`, `rvr/`, and `base4-hero.mp4` + `base4-hero-poster.jpg`) to the **WP Media
Library** (or theme `/assets/`), then repoint `ASSET_BASE` to that path. One line. Until then it
depends on the GitHub Pages repo staying published.

---

## 4. Editing content later

All copy lives in the `# SHEET:` TSV block. Fields are separated by **real tab characters** —
keep tabs, not spaces, or parsing breaks. Editing content means editing this block in the
template file (not the WP block editor). If in-admin editing by non-devs is a requirement, that's
a larger rebuild into native blocks/ACF — out of scope for this drop-in.

---

## 5. Pre-launch checklist

- [ ] **GA4:** replace the placeholder `G-XXXXXXXXXX` with the real Measurement ID — **or**
      remove the GA snippet if analytics is already handled globally (GTM/site-wide tag), to
      avoid double-counting.
- [ ] **Lead form:** `FORM_ENDPOINT` is empty, so the consultation form currently falls back to
      `mailto:BlairH@base-4.com`. Point it at a real endpoint or a WP form plugin.
- [ ] **Assets:** decide GitHub Pages vs. WP Media Library and set `ASSET_BASE` accordingly (§3).
- [ ] **Fonts:** Inter + Inter Tight load from Google Fonts — keep, or self-host if required.
- [ ] **Canonical / OG:** already set to `https://www.base-4.com/hospitality/`; confirm the final
      slug matches.
- [ ] **Social links, nav links:** verified current, but confirm before go-live.

---

## 6. External dependencies (what the page calls out to)

- `fonts.googleapis.com`, `fonts.gstatic.com` — fonts
- `ohshtnvm.github.io` (or your chosen `ASSET_BASE`) — images, logos, hero video
- `www.base-4.com` — a few portfolio/USP photos + outbound links
- `www.googletagmanager.com` — GA4 (placeholder)
- linkedin / instagram / youtube / facebook / x — social profile links

---

## 7. Design tokens (for reference / matching)

- Accent green `#8dc63f` · Deep green `#1C3A2E` · Ink `#0E1A14`
- Surfaces: white `#FFFFFF`, alt `#F5F7F4`; hairline `#E3E8E1`
- Type: **Inter Tight** (headings) + **Inter** (body)
- Max content width 1200px; section rhythm ~88px vertical

---

*Questions on intent or content, contact the marketing owner. Questions on the file's structure
are answerable from this doc + inline comments in `index.html`.*
