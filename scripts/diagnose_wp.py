"""
Compares what we send to WordPress (content.raw) with what WordPress outputs
(content.rendered, after the theme/plugin content filters) for each page in
deploy_to_wp.PAGES, and reports what changed. Read-only: makes GET requests only.
"""
import base64, difflib, json, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from deploy_to_wp import PAGES, report

wp_url = os.environ["WP_URL"].strip().rstrip("/")
auth = base64.b64encode(f'{os.environ["WP_USER"].strip()}:{os.environ["WP_APP_PASSWORD"].replace(" ", "").strip()}'.encode()).decode()

def get(page_id):
    req = urllib.request.Request(f"{wp_url}/wp-json/wp/v2/pages/{page_id}?context=edit",
        headers={"Authorization": f"Basic {auth}", "User-Agent": "base4-github-deploy"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def scripts(html):
    return re.findall(r"(?s)<script\b[^>]*>(.*?)</script>", html)

for file_path, page_id in PAGES.items():
    if not page_id:
        continue
    d = get(page_id)
    raw, out = d["content"]["raw"], d["content"]["rendered"]
    rs, os_ = scripts(raw), scripts(out)
    notes = [f"template={d.get('template')!r}", f"raw={len(raw)} rendered={len(out)}",
             f"scripts raw={len(rs)} rendered={len(os_)}",
             f"tabs raw={raw.count(chr(9))} rendered={out.count(chr(9))}"]
    for i, (a, b) in enumerate(zip(rs, os_)):
        if a != b:
            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            ops = [op for op in sm.get_opcodes() if op[0] != "equal"][:4]
            ex = "; ".join(f"{t}: {a[i1:i2][:60]!r} -> {b[j1:j2][:60]!r}" for t, i1, i2, j1, j2 in ops)
            notes.append(f"script#{i} CHANGED ({len(a)}->{len(b)}) {ex}")
    for tag in ("<p>", "</p>", "<br />", "&#8217;", "&#8220;", "&#038;", "&#8211;"):
        added = out.count(tag) - raw.count(tag)
        if added > 0:
            notes.append(f"added {tag} x{added}")
    report("notice", f"{file_path} (page {page_id}): " + " | ".join(notes))
