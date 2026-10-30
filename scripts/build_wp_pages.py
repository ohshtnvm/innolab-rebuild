"""
Builds WordPress-ready versions of the Home and About pages.

The source pages render their content from the embedded TSV with JavaScript,
so the raw HTML is nearly empty ("Loading..."). For SEO, this script opens each
page in headless Chromium, lets it render, and saves the rendered markup, so the
full text is in the HTML that WordPress serves. The original scripts are kept,
so menus, modal, forms and animations still work on the live page.

Output (body content only, ready for a Custom HTML block): see SOURCES below.

Usage:  python scripts/build_wp_pages.py
Needs:  pip install playwright && python -m playwright install chromium
"""

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scope_css import RESET, SCOPE, scope_css  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# source page in this repo -> built file for WordPress
SOURCES = {
    "home/v3/index.html": "wp-pages/home.html",
    "about-us/v1/index.html": "wp-pages/about.html",
    "6-29-iteration/index.html": "wp-pages/hospitality.html",
    "7-22-mf/index.html": "wp-pages/multifamily.html",
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


# Font stacks used when a page names only the web font. Without a fallback, the
# browser drops to its default serif whenever the web font is slow or blocked.
FONT_FALLBACKS = {
    "Inter Tight": "'Inter Tight','Inter',system-ui,-apple-system,'Segoe UI',Arial,sans-serif",
    "Inter": "'Inter',system-ui,-apple-system,'Segoe UI',Arial,sans-serif",
}


def add_font_fallbacks(css: str) -> str:
    def fix(m: re.Match) -> str:
        family = m.group(2)
        return f"{m.group(1)}{FONT_FALLBACKS[family]}" if family in FONT_FALLBACKS else m.group(0)
    # font-family:'X' with nothing after it (no existing fallback list)
    return re.sub(r"(font-family:\s*)['\"]([^'\",;}]+)['\"]\s*(?=[;}!])", fix, css)


# The WordPress theme also uses id="header"/"footer", so the page's own get renamed.
ID_RENAMES = {"header": "b4-header", "footer": "b4-footer"}


def rename_ids(html: str) -> str:
    for old, new in ID_RENAMES.items():
        html = re.sub(rf'\bid=(["\']){old}\1', f'id="{new}"', html)
        html = re.sub(rf"getElementById\((['\"]){old}\1\)", f"getElementById('{new}')", html)
        html = re.sub(rf"#{old}(?![\w-])", f"#{new}", html)
    return html


def rem_to_px(html: str) -> str:
    """The theme sets the root font size (Bootstrap: 10px), so rem would shrink the page. Pin 1rem = 16px."""
    def px(m: re.Match) -> str:
        v = float(m.group(1)) * 16
        return f"{v:.2f}".rstrip("0").rstrip(".") + "px"
    return re.sub(r"(?<![\w.])(\d*\.?\d+)rem\b", px, html)


def build(src: Path, out: Path, browser) -> None:
    raw = rem_to_px(rename_ids(src.read_text(encoding="utf-8")))
    head = re.search(r"(?s)<head[^>]*>(.*?)</head>", raw).group(1)
    body = re.search(r"(?s)<body[^>]*>(.*)</body>", raw).group(1)

    # Fonts and page styles from <head>. Title/meta/canonical/OG go in Yoast, and the
    # placeholder GA4 tag is dropped because the site already has analytics.
    font_links = [
        l for l in re.findall(r"<link[^>]+>", head)
        if "fonts.googleapis.com/css" in l
    ]
    css = "\n".join(re.findall(r"(?s)<style[^>]*>(.*?)</style>", head))
    styles = ["<style>\n" + RESET + scope_css(add_font_fallbacks(css)) + "\n</style>"]
    scripts = re.findall(r"(?s)<script[^>]*>.*?</script>", body)

    # Render a renamed copy next to the source so relative asset paths still work.
    tmp = src.with_name(f".wpbuild-{src.name}")
    tmp.write_text(raw, encoding="utf-8")
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        page.goto(tmp.as_uri(), wait_until="networkidle")
    finally:
        tmp.unlink(missing_ok=True)
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
        f'<div id="{SCOPE[1:]}">',
        rendered,
        "</div>",
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
