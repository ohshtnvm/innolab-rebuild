# BASE4 — Innovation Lab / Markets Page Rebuilds

Static, single-file rebuilds of BASE4 market & Innovation Lab pages. Each page is a self-contained
`*.html` file with content embedded as a `# SHEET:`-delimited TSV block parsed at runtime — no build
step, no database. Designed to drop onto any static host (Cloudflare Pages, GitHub Pages).

## Pages

| File | Rebuild of | Notes |
|------|------------|-------|
| [`index.html`](index.html) | `/hospitality/` | Hospitality A+E+I — primary rebuild |
| [`multifamily.html`](multifamily.html) | `/multifamily/` | Re-tabbed by product type; units-based metrics |
| [`industrialized-construction.html`](industrialized-construction.html) | `/industrialized-construction-systems/` | Innovation Lab; cross-links to the market pages |
| [`c.html`](c.html) | `/hospitality/` | Alternate hospitality design variant |
| [`g.html`](g.html) | `/hospitality/` | Alternate hospitality design variant (Tailwind) |

Each page is reachable at its own path, e.g. `/multifamily.html`, `/industrialized-construction.html`.

## Shared design system

`index.html`, `multifamily.html`, and `industrialized-construction.html` share one design system:
BASE4 green `#8dc63f`, deep green `#1C3A2E`, Inter Tight + Inter, 1200px max width, sticky condensing
header, scroll-reveal, GA4 event scaffold, and an inline consultation form that falls back to
`mailto:BlairH@base-4.com`.

## Before going live (per-page TODOs, marked in source)

- Replace the GA4 placeholder `G-XXXXXXXXXX` with the real Measurement ID.
- Set the `FORM_ENDPOINT` constant to a real lead-capture endpoint (otherwise forms fall back to mailto).
- Confirm the data-driven figures (keys/units/states) and product-type assignments with BASE4.
- Supply client testimonials to replace the interim proof walls.

## Editing content

Open the page and edit the TSV inside `<script id="content-tsv" type="text/tab-separated-values">`.
Fields are **tab-separated** — keep real tabs, not spaces.
