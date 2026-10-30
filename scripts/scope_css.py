"""
Scopes a page's CSS to one container (default #b4-page) so it can't style the
WordPress theme's header/footer, and the theme's CSS can't leak into the page.

  :root, html, body        -> #b4-page
  body.x .y / html.x .y    -> body.x #b4-page .y
  html.is-embedded ...     -> dropped (iframe-only rules)
  .foo, h1, *::before ...  -> #b4-page .foo, #b4-page h1, #b4-page *::before
@media/@supports are scoped recursively; @keyframes/@font-face are left alone.
"""
import re
import tinycss2

SCOPE = "#b4-page"
ROOT_ONLY = re.compile(r"^(?::root|html|body)$")
ROOT_COMPOUND = re.compile(r"^((?:html|body)(?:[.#:\[][^\s>+~]*)?)(\s*[>+~]?\s*)(.*)$", re.S)


def split_selectors(prelude: str):
    parts, depth, cur = [], 0, ""
    for ch in prelude:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def scope_selector(sel: str, scope: str):
    if sel.startswith("html.is-embedded"):
        return None
    if ROOT_ONLY.match(sel):
        return scope
    m = ROOT_COMPOUND.match(sel)
    if m and re.match(r"^(html|body)\b", sel):
        compound, comb, rest = m.groups()
        if compound in ("html", "body"):
            return f"{scope} {rest}".strip() if rest else scope
        return f"{compound} {scope}" + (f" {rest}" if rest else "")
    return f"{scope} {sel}"


def scope_rules(rules, scope):
    out = []
    for r in rules:
        if r.type == "qualified-rule":
            sels = [scope_selector(s, scope) for s in split_selectors(tinycss2.serialize(r.prelude))]
            sels = [s for s in sels if s]
            if sels:
                out.append(", ".join(sels) + "{" + tinycss2.serialize(r.content) + "}")
        elif r.type == "at-rule":
            kw = r.lower_at_keyword
            head = "@" + r.at_keyword + tinycss2.serialize(r.prelude)
            if kw in ("media", "supports", "container", "layer") and r.content is not None:
                inner = tinycss2.parse_rule_list(r.content, skip_comments=True, skip_whitespace=True)
                out.append(head + "{" + scope_rules(inner, scope) + "}")
            elif r.content is not None:
                out.append(head + "{" + tinycss2.serialize(r.content) + "}")
            else:
                out.append(head + ";")
        # comments / whitespace / parse errors dropped
    return "\n".join(out)


# Neutralises theme/bootstrap rules that would otherwise reach page elements
# (SVG icons excluded so their drawing attributes keep working). Page rules all
# carry the #b4-page prefix too and come later, so they still win.
RESET = ("body{margin:0}\n"
         f"{SCOPE}{{display:block}}\n"
         f"{SCOPE} :where(*:not(svg):not(svg *)){{all:revert}}\n")


def scope_css(css: str, scope: str = SCOPE) -> str:
    rules = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
    return scope_rules(rules, scope)
