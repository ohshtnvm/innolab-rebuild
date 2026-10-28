"""
Builds WordPress-ready versions of the Home and About pages.

The source pages render their content from the embedded TSV with JavaScript,
so the raw HTML is nearly empty ("Loading..."). For SEO, this script opens each
page in headless Chromium, lets it render, and saves the rendered markup, so the
full text is in the HTML that WordPress serves. The original scripts are kept,
so menus, modal, forms and animations still work on the live page.

Output (body content only, ready for a Custom HTML block):
  wp-pages/home.html
  wp-pages/about.html

Usage:  python scripts/build_wp_pages.py
Needs:  pip install playwright && python -m playwright install chromium
"""

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent

# source page in this repo -> built file for WordPress
SOURCES = {
    "home/v3/index.html": "wp-pages/home.html",
    "about-us/v1/index.html": "wp-pages/about.html",
}

# Removes runtime state so the saved markup is clean, then returns body markup without scripts.
SNAPSHOT_JS = """
() => {
  const body = document.body.cloneNode(true);
  body.querySelectorAll('script').forEach(s => s.remove());
  body.querySelectorAll('[style]').forEach(el => {
    el.style.removeProperty('opacity');
    el.style.removeProperty('transform');
    el.style.removeProperty('transition');
    if (!el.getAttribute('style').trim()) el.removeAttribute('style');
  });
  body.querySelectorAll('.scrolled, .open, .is-open, .active-modal').forEach(el => {
    el.classList.remove('scrolled', 'open', 'is-open', 'active-modal');
  });
  return body.innerHTML.trim();
}
"""


def build(src: Path, out: Path, browser) -> None:
    raw = src.read_text(encoding="utf-8")
    head = re.search(r"(?s)<head[^>]*>(.*?)</head>", raw).group(1)
    body = re.search(r"(?s)<body[^>]*>(.*)</body>", raw).group(1)

    # Fonts and page styles from <head>. Title/meta/canonical/OG go in Yoast, and the
    # placeholder GA4 tag is dropped because the site already has analytics.
    font_links = [
        l for l in re.findall(r"<link[^>]+>", head)
        if "fonts.googleapis.com/css" in l
    ]
    styles = re.findall(r"(?s)<style[^>]*>.*?</style>", head)
    scripts = re.findall(r"(?s)<script[^>]*>.*?</script>", body)

    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(src.as_uri(), wait_until="networkidle")
    page.wait_for_function(
        "() => !document.querySelector('#app')?.textContent.includes('Loading...')",
        timeout=20000,
    )
    page.wait_for_timeout(1500)
    rendered = page.evaluate(SNAPSHOT_JS)
    page.close()
    if errors:
        raise RuntimeError(f"{src}: page errors while rendering: {errors}")
    if "Loading..." in rendered:
        raise RuntimeError(f"{src}: page did not finish rendering")

    parts = [
        f"<!-- Built from {src.relative_to(ROOT).as_posix()} by scripts/build_wp_pages.py. "
        "Edit the source page, not this file or the WordPress page. -->",
        *font_links,
        *styles,
        rendered,
        *scripts,
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")

    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", rendered)))
    print(f"OK   {src.relative_to(ROOT)} -> {out.relative_to(ROOT)} "
          f"({len(text):,} chars of indexable text, {rendered.count('<h1')} h1)")


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for src, out in SOURCES.items():
                build(ROOT / src, ROOT / out, browser)
        finally:
            browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
