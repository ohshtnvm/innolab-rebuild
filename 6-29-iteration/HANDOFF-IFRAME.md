# Hospitality Page — Developer Handoff (Route B: iframe embed)

**Deliverable:** embed the hosted page inside a WordPress page via `<iframe>`. Fastest path —
live in minutes, fully isolated from theme CSS/JS. Trade-offs are real; read §4 before choosing
this over Route A.

**Hosted URL** (pick one; both serve the file and neither blocks framing):
- `https://innolab-rebuild.pages.dev/6-29-iteration/index.html` (Cloudflare Pages — faster CDN)
- `https://ohshtnvm.github.io/innolab-rebuild/6-29-iteration/index.html` (GitHub Pages)

The page already reports its height to the parent when embedded, so an auto-height iframe just
works. No library needed.

---

## Option 1 — Auto-height iframe (seamless scroll, recommended for a showcase)

Paste into a **Custom HTML** block (or a full-width template). The iframe grows to fit the
content; no inner scrollbar.

```html
<div style="width:100%">
  <iframe
    id="base4-hospitality"
    src="https://innolab-rebuild.pages.dev/6-29-iteration/index.html"
    title="BASE4 Hospitality — Architecture, Engineering & Interiors"
    loading="lazy"
    scrolling="no"
    allow="fullscreen"
    style="width:100%;border:0;display:block;height:6000px"></iframe>
</div>
<script>
(function(){
  var iframe  = document.getElementById('base4-hospitality');
  var ORIGIN  = 'https://innolab-rebuild.pages.dev'; // MUST match the iframe src origin exactly
  window.addEventListener('message', function(e){
    if(e.origin !== ORIGIN) return;                  // ignore anything not from our page
    var d = e.data || {};
    if(d.type === 'base4-embed-height' && d.height){
      iframe.style.height = d.height + 'px';
    }
  });
})();
</script>
```

- The `height:6000px` inline value is just a pre-resize fallback; the script overwrites it with
  the real height on load and on any content change.
- If you use the GitHub Pages URL instead, set `ORIGIN` to `https://ohshtnvm.github.io`.
- The `ORIGIN` check is a security best practice — it rejects height messages from any other frame.

---

## Option 2 — Fixed-height iframe (correct modals + sticky header)

```html
<iframe
  src="https://innolab-rebuild.pages.dev/6-29-iteration/index.html"
  title="BASE4 Hospitality"
  loading="lazy"
  allow="fullscreen"
  style="width:100%;height:100vh;border:0;display:block"></iframe>
```

No script needed. The page scrolls **inside** the iframe. Because the iframe viewport is a normal
screen-sized box, the page's sticky header, image lightbox, and consultation modal all position
correctly. The cost is a nested scroll region (a scrollbar inside the page).

---

## Which option for THIS page?

This page has a **sticky header, an image lightbox, and a consultation-form modal**, all using
`position:fixed`. That drives the choice:

- **If the consultation CTA / lightbox matter (they do for lead-gen): use Option 2 (fixed height).**
  In an auto-height iframe those fixed overlays center within the *full tall iframe*, not the
  visitor's screen — so a clicked lightbox or the "Schedule a Consultation" modal can open
  off-screen. Option 2 avoids this.
- **If it's mainly a scroll-through showcase and modals are secondary:** Option 1 looks more
  native (no inner scrollbar).

Recommendation for a live lead-gen page: **Option 2**, or better, **Route A** (see `HANDOFF.md`).

---

## 4. Route B trade-offs (know these before shipping)

- **SEO:** iframe content is **not** indexed as part of the WordPress page. If organic ranking
  for `/hospitality/` matters, use Route A instead.
- **No shared chrome:** the embed shows the page's own header/nav/footer, independent of the WP
  site's global nav. Fine for a standalone landing page; inconsistent if you want the site's real
  header around it.
- **Analytics:** GA4 fires *inside* the iframe as its own pageview, separate from the WP page's
  analytics, and referrer is the iframe origin. Coordinate with whoever owns GA so it isn't
  double-counted or mis-attributed.
- **Form + mailto:** the consultation form still falls back to `mailto:BlairH@base-4.com` until
  `FORM_ENDPOINT` is set (same as Route A). Works from inside the iframe.
- **Deep links / anchors:** the parent can't drive scrolling to internal sections of the iframe.

---

## 5. Framing / security notes

- Confirmed: neither host sends `X-Frame-Options` or a blocking `Content-Security-Policy`, so the
  page can be framed by base-4.com.
- The height-reporter posts only a number (`{type:'base4-embed-height', height}`) with
  `targetOrigin '*'`. The parent snippet validates `e.origin` before acting, so no other frame can
  spoof a resize. No user data crosses the frame boundary.
- Assets still load from `ASSET_BASE` (see `HANDOFF.md` §3); the embed depends on that host and the
  page host staying published.

---

## 6. Quick test before publishing

1. Drop Option 1 into a draft WP page and preview.
2. The iframe should resize to fit with no inner scrollbar and no big empty gap at the bottom.
3. Resize the browser / rotate a phone — height should re-fit (the page re-posts on resize).
4. If a clicked project image or the consultation modal opens off-screen, switch to Option 2.
