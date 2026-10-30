"""
Pushes each HTML file in wp-pages/ (built by scripts/build_wp_pages.py) into its WordPress page as a single
Custom HTML block, so the content lives in WordPress itself and Google
indexes it as part of base-4.com.

Setup:
  1. Fill in PAGES below with the WordPress page ID for each file.
     The ID is the number in the page's edit URL: .../post.php?post=123&action=edit
  2. Add the repo secrets WP_URL, WP_USER, WP_APP_PASSWORD
     (Settings -> Secrets and variables -> Actions).

Title, meta description, canonical and OG tags are set in Yoast on each WordPress page.
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Page template that hides the theme header/footer/sidebar.
# Comes from the "BASE4 Blank" snippet in Code Snippets; set to "" to leave the template alone.
TEMPLATE = "base4-themed"   # "base4-blank" = no site header; "base4-themed" = site header + page

# file in repo -> WordPress page ID
PAGES = {
    # TEST pages (password-protected drafts) - preview changes here first
    "wp-pages/home.html": 16061,         # Test Home Rebuild
    "wp-pages/about.html": 16060,        # Test About Us Rebuild
    "wp-pages/hospitality.html": 16070,  # Test Hospitality Rebuild
    "wp-pages/multifamily.html": 16068,  # Test Multifamily Rebuild

    # LIVE pages - swap these in (and comment out the test lines) to go live
    # "wp-pages/home.html": 11485,       # Home
    # "wp-pages/about.html": 13200,      # About Us
    # "wp-pages/hospitality.html": 15573,  # Hospitality
    # "wp-pages/multifamily.html": 15816,  # Multifamily
}


def report(level: str, msg: str) -> None:
    """Print, and also surface as a GitHub Actions annotation so it shows on the run page."""
    print(msg)
    if os.environ.get("GITHUB_ACTIONS"):
        safe = msg.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::{level}::{safe}")


def update_page(wp_url: str, auth: str, page_id: int, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{wp_url}/wp-json/wp/v2/pages/{page_id}",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "User-Agent": "base4-github-deploy",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def main() -> int:
    missing = [k for k in ("WP_URL", "WP_USER", "WP_APP_PASSWORD") if not os.environ.get(k, "").strip()]
    if missing:
        report("error", f"Missing repo secrets: {', '.join(missing)}")
        return 1
    wp_url = os.environ["WP_URL"].strip().rstrip("/")
    user = os.environ["WP_USER"].strip()
    app_password = os.environ["WP_APP_PASSWORD"].replace(" ", "").strip()
    auth = base64.b64encode(f"{user}:{app_password}".encode()).decode()

    failed = False
    for file_path, page_id in PAGES.items():
        if not page_id:
            report("warning", f"SKIP {file_path}: no page ID set")
            continue

        html = Path(file_path).read_text(encoding="utf-8").strip()
        if re.search(r"<(html|head|body)[\s>]", html, re.IGNORECASE):
            report("error", f"FAIL {file_path}: remove <html>/<head>/<body> tags (body content only)")
            failed = True
            continue

        # Wrap as a Custom HTML block so the editor doesn't reformat the markup
        content = f"<!-- wp:html -->\n{html}\n<!-- /wp:html -->"

        payload = {"content": content}
        if TEMPLATE:
            payload["template"] = TEMPLATE
        try:
            try:
                result = update_page(wp_url, auth, page_id, payload)
            except urllib.error.HTTPError as e:
                # Template not registered yet (snippet inactive): publish content anyway.
                if e.code == 400 and "template" in payload:
                    report("warning", f"{file_path}: template '{TEMPLATE}' not available; "
                                      "activate the BASE4 Blank snippet in Code Snippets. Publishing content only.")
                    payload.pop("template")
                    result = update_page(wp_url, auth, page_id, payload)
                else:
                    raise
            report("notice", f"OK {file_path} -> page {page_id} ({result.get('status')}, template: "
                             f"{result.get('template') or 'default'}) {result.get('link', '')}")
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")[:400]
            report("error", f"FAIL {file_path} -> page {page_id}: HTTP {e.code} {body}")
            failed = True
        except urllib.error.URLError as e:
            report("error", f"FAIL {file_path} -> page {page_id}: could not reach {wp_url} ({e.reason})")
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
