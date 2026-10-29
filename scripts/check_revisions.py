"""Read-only: show where the pre-rebuild versions of the live pages are stored."""
import base64, json, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from deploy_to_wp import PAGES, report

wp_url = os.environ["WP_URL"].strip().rstrip("/")
auth = base64.b64encode(f'{os.environ["WP_USER"].strip()}:{os.environ["WP_APP_PASSWORD"].replace(" ", "").strip()}'.encode()).decode()

def get(path):
    req = urllib.request.Request(f"{wp_url}/wp-json/wp/v2/{path}", headers={"Authorization": f"Basic {auth}", "User-Agent": "base4-github-deploy"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def summarize(html):
    html = html or ""
    iframes = re.findall(r'<iframe[^>]*src="([^"]+)"', html)
    built = "Built from" in html
    return f"{len(html)} chars, iframes={iframes[:2]}, rebuild={'yes' if built else 'no'}, starts={html[:90]!r}"

for file_path, page_id in PAGES.items():
    if not page_id:
        continue
    page = get(f"pages/{page_id}?context=edit")
    meta_keys = sorted((page.get("meta") or {}).keys()) if isinstance(page.get("meta"), dict) else page.get("meta")
    report("notice", f"page {page_id} current: template={page.get('template')!r} meta_keys={meta_keys} modified={page.get('modified')}")
    for r in get(f"pages/{page_id}/revisions?per_page=100&context=edit"):
        report("notice", f"page {page_id} revision {r['id']} ({r['date']}): {summarize(r['content']['raw'])}")
    try:
        ar = get(f"pages/{page_id}/autosaves?context=edit")
        for a in ar:
            report("notice", f"page {page_id} autosave {a['id']} ({a['date']}): {summarize(a['content']['raw'])}")
    except Exception as e:
        report("notice", f"page {page_id} autosaves: {e}")
