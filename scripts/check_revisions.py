"""Read-only: list recent revisions of the live pages and whether an earlier one still holds the old iframe version."""
import base64, json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from deploy_to_wp import PAGES, report

wp_url = os.environ["WP_URL"].strip().rstrip("/")
auth = base64.b64encode(f'{os.environ["WP_USER"].strip()}:{os.environ["WP_APP_PASSWORD"].replace(" ", "").strip()}'.encode()).decode()

def get(path):
    req = urllib.request.Request(f"{wp_url}/wp-json/wp/v2/{path}", headers={"Authorization": f"Basic {auth}", "User-Agent": "base4-github-deploy"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

for file_path, page_id in PAGES.items():
    if not page_id:
        continue
    revs = get(f"pages/{page_id}/revisions?per_page=100&context=edit&_fields=id,date,content")
    old = [r for r in revs if "<iframe" in r["content"]["raw"] and "base4-blank" not in r["content"]["raw"]]
    newest_old = old[0] if old else None
    report("notice", f"page {page_id} ({file_path}): {len(revs)} revisions; "
           + (f"last pre-rebuild version = revision {newest_old['id']} from {newest_old['date']} "
              f"({len(newest_old['content']['raw'])} chars, has iframe)" if newest_old else "NO revision with the old iframe version found"))
