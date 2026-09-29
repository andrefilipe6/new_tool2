#!/usr/bin/env python3
"""Audit CSS (and the HTML/JS around it) for:
  1. Bootstrap: custom CSS overriding Bootstrap core selectors instead of using
     --bs-* variables / own classes, !important fights, load order.
  2. Custom-property (:root var) organisation: hard-coded repeated values,
     undefined / unused vars.
  3. JS doing things plain CSS can do (hover, sticky, smooth scroll, media
     queries, accordions, dark mode ...).

Usage: css_audit.py [--json] [--strict] PATH [PATH ...]
Exit 1 on error-level findings (or warnings with --strict).
"""
import argparse, json, os, re, sys
from collections import Counter

SEV = {"error": 0, "warn": 1, "info": 2}
BOOTSTRAP_CLASSES = ["btn", "navbar", "nav-link", "card", "container", "row", "col", "form-control",
                     "modal", "dropdown-menu", "alert", "badge", "table", "list-group", "breadcrumb",
                     "pagination", "accordion", "offcanvas", "carousel", "toast", "progress", "input-group"]
BS_RE = re.compile(r"(?<![\w-])\.(%s)(?![\w])(?!-(?:custom|my))" % "|".join(BOOTSTRAP_CLASSES) +
                   r"|(?<![\w-])\.(?:btn|col|text|bg|border|d|p|m)-(?:primary|secondary|success|danger|warning|info|light|dark|\d+|md-\d+|lg-\d+|sm-\d+)\b")

JS_HINTS = [
    (r"addEventListener\(\s*['\"](?:mouseover|mouseenter|mouseout|mouseleave)['\"]|\.on\(\s*['\"]hover|\.hover\(",
     "JS hover handling", "use :hover / :focus-visible / :focus-within"),
    (r"addEventListener\(\s*['\"]scroll['\"][\s\S]{0,300}(?:fixed|sticky|classList|offsetTop|scrollY|pageYOffset)|\$\(window\)\.scroll",
     "scroll listener toggling position/classes", "position: sticky, or animation-timeline: scroll()/view()"),
    (r"scrollTo\([^)]*smooth|scrollIntoView\([^)]*smooth|\.animate\(\{\s*scrollTop",
     "JS smooth scrolling", "html { scroll-behavior: smooth } (wrap in prefers-reduced-motion: no-preference)"),
    (r"matchMedia\(|window\.innerWidth\s*[<>]=?|addEventListener\(\s*['\"]resize['\"]",
     "JS viewport/breakpoint checks", "@media / @container queries"),
    (r"IntersectionObserver[\s\S]{0,400}classList\.(?:add|toggle)",
     "IntersectionObserver used to trigger animation classes", "animation-timeline: view() / animation-range"),
    (r"\.style\.(?:display|visibility)\s*=\s*['\"](?:none|block|hidden|visible)|\.toggle\(\)|\.slideToggle|\.fadeToggle|\.(?:show|hide)\(\)",
     "JS show/hide toggling", "<details>/<summary>, :target, :checked, [popover] or the dialog element"),
    (r"prefers-color-scheme|matchMedia\([^)]*dark|classList\.toggle\(['\"]dark",
     "JS dark-mode handling", "color-scheme + @media (prefers-color-scheme) with root vars (JS only for a saved user toggle)"),
    (r"\.style\.(?:height|minHeight)\s*=[^;]*(?:max|Math|offsetHeight|clientHeight)|equalHeight|matchHeight",
     "JS equalising heights", "CSS grid / flex (align-items: stretch), subgrid"),
    (r"\.style\.(?:width|height)\s*=[^;]*(?:\/|\*)\s*\d",
     "JS computing aspect ratio / sizes", "aspect-ratio, clamp(), min()/max()"),
    (r"\.style\.(?:opacity|transform|transition|color|backgroundColor|background)\s*=",
     "JS setting visual styles inline", "toggle a class (or CSS var via style.setProperty) and put the rules in CSS"),
    (r"data-tooltip|tooltip\(\s*\)|new\s+bootstrap\.Tooltip|\.tooltip\(",
     "JS tooltip", "CSS tooltip with :hover/:focus + ::after, or the popover attribute (anchor positioning where supported)"),
    (r"new\s+bootstrap\.(?:Collapse|Accordion)|data-bs-toggle=['\"]collapse",
     "Bootstrap JS collapse", "<details name=...> gives an accordion with no JS"),
    (r"maxlength|\.value\.length\s*[<>]|:invalid|checkValidity\(\)\s*\)\s*\{[\s\S]{0,80}classList",
     "JS form validation styling", ":user-invalid / :valid / :placeholder-shown, HTML validation attributes"),
    (r"parent\.classList|closest\([^)]*\)\.classList|previousElementSibling\.classList",
     "JS styling a parent/sibling", ":has() / sibling combinators"),
]


class R:
    def __init__(s): s.f = []
    def add(s, sev, code, file, line, msg): s.f.append(dict(severity=sev, code=code, file=file, line=line, message=msg))


def strip_comments(t):
    return re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group()), t, flags=re.S)


def line_of(text, idx): return text.count("\n", 0, idx) + 1


def read(p):
    with open(p, encoding="utf-8", errors="replace") as fh: return fh.read()


def walk(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "vendor", "dist", "build")]
                for f in files: yield os.path.join(root, f)
        elif os.path.isfile(p): yield p
        else: print(f"warning: {p} not found", file=sys.stderr)


def is_vendor(path):
    b = os.path.basename(path).lower()
    return b.endswith(".min.css") or re.match(r"(bootstrap|bootstrap-\w+)(\.\w+)?\.css$", b) or "/vendor/" in path or "/node_modules/" in path


def audit_css(path, css, uses_bs, r):
    text = strip_comments(css)
    rules = [(m.group(1).strip(), m.group(2), m.start()) for m in re.finditer(r"([^{}@][^{}]*)\{([^{}]*)\}", text)]

    # --- root vars ---
    defined = {}
    for sel, body, pos in rules:
        if re.search(r":root|^html$|\[data-bs-theme", sel):
            for m in re.finditer(r"(--[\w-]+)\s*:", body): defined.setdefault(m.group(1), line_of(text, pos))
    for m in re.finditer(r"(?:^|[;{\s])(--[\w-]+)\s*:", text): defined.setdefault(m.group(1), line_of(text, m.start()))
    used = Counter(re.findall(r"var\(\s*(--[\w-]+)", text))
    root_defined = bool(re.search(r":root\s*\{[^}]*--", text))
    if not root_defined and len(rules) > 5:
        r.add("warn", "no-root-vars", path, None, "No custom properties in :root; centralise colours, spacing, fonts and radii as vars")
    for v, n in used.items():
        if v not in defined and not v.startswith("--bs-"):
            r.add("warn", "undefined-var", path, None, f"var({v}) used but never defined in scanned CSS")
    for v, ln in defined.items():
        if v not in used and not v.startswith("--bs-") and not re.search(re.escape(v) + r"\s*\)", text):
            r.add("info", "unused-var", path, ln, f"{v} defined but never used in this file")

    colours = Counter(m.lower() for m in re.findall(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b|rgba?\([^)]*\)|hsla?\([^)]*\)",
                      "\n".join(b for s, b, _ in rules if not re.search(r":root", s))))
    for c, n in colours.most_common():
        if n >= 3: r.add("warn", "repeated-colour", path, None, f"{c} hard-coded {n}x; make it a var (--color-...)")
    fonts = Counter(re.findall(r"font-family\s*:\s*([^;}]+)", text))
    for f, n in fonts.items():
        if n >= 2 and "var(" not in f: r.add("info", "repeated-font", path, None, f"font-family '{f.strip()[:40]}' repeated {n}x; use --font-*")
    sp = Counter(re.findall(r"(?:margin|padding|gap)[\w-]*\s*:\s*(\d+px)\b", text))
    for v, n in sp.items():
        if n >= 5: r.add("info", "repeated-spacing", path, None, f"{v} used for spacing {n}x; consider a spacing scale (--space-*)")

    # --- Bootstrap ---
    if uses_bs and not is_vendor(path):
        for sel, body, pos in rules:
            if re.search(r":root|\[data-bs-theme|--bs-", sel) and not re.search(r"\.btn|\.card|\.navbar", sel): continue
            hits = [s for s in sel.split(",") if BS_RE.search(s)]
            if not hits: continue
            ln = line_of(text, pos)
            if "!important" in body:
                r.add("warn", "bs-important-override", path, ln, f"'{sel[:50]}' overrides Bootstrap with !important; raise specificity or set the component's --bs-* var instead")
            elif re.fullmatch(r"\s*(?:\.[\w-]+)\s*", hits[0]) and not re.search(r"--bs-|--", body):
                r.add("warn", "bs-core-override", path, ln, f"'{hits[0].strip()}' redefines a Bootstrap class globally. Prefer setting --bs-* vars (e.g. --bs-btn-bg), your own modifier class (.btn-brand), or Sass variables")
        if not re.search(r"--bs-", text) and any(BS_RE.search(s) for s, _, _ in rules):
            r.add("info", "bs-no-vars", path, None, "Overrides Bootstrap but uses no --bs-* variables (Bootstrap 5.2+ components expose them)")
    if uses_bs and re.match(r"bootstrap(\.css)$", os.path.basename(path).lower()) and re.search(r"\bcustom\b|\bTODO\b|\bmy-", css):
        r.add("error", "bs-core-edited", path, None, "bootstrap.css appears edited; keep vendor untouched and override in a separate stylesheet loaded after it")

    # --- modern CSS hygiene ---
    if re.search(r"@keyframes|animation\s*:|transition\s*:", text) and "prefers-reduced-motion" not in text:
        r.add("warn", "no-reduced-motion", path, None, "Animations/transitions with no prefers-reduced-motion handling")
    for m in re.finditer(r"transition\s*:\s*all\b", text):
        r.add("info", "transition-all", path, line_of(text, m.start()), "transition: all animates everything; list properties")
    for m in re.finditer(r"outline\s*:\s*(?:none|0)\b", text):
        seg = text[max(0, m.start() - 200):m.end() + 200]
        if "focus-visible" not in seg and "box-shadow" not in seg:
            r.add("warn", "outline-removed", path, line_of(text, m.start()), "outline removed without a visible focus replacement (:focus-visible)")
    if not r_has(r, path, "important") and len(re.findall(r"!important", text)) > 5 and not is_vendor(path):
        r.add("info", "many-important", path, None, f"{len(re.findall('!important', text))} uses of !important")
    return text


def r_has(r, path, code): return any(f["file"] == path and code in f["code"] for f in r.f)


def audit_js_html(path, txt, r, css_seen):
    for pat, what, fix in JS_HINTS:
        for m in re.finditer(pat, txt, re.I):
            r.add("warn" if "inline" not in what else "info", "css-instead-of-js", path, line_of(txt, m.start()), f"{what} -> {fix}")
            break
    if path.endswith((".html", ".htm", ".php")):
        links = [(m.start(), m.group(1)) for m in re.finditer(r"<link[^>]+href=[\"']([^\"']+\.css[^\"']*)[\"']", txt, re.I)]
        bs = [i for i, (_, h) in enumerate(links) if "bootstrap" in h.lower()]
        cu = [i for i, (_, h) in enumerate(links) if "bootstrap" not in h.lower()]
        if bs and cu and min(cu) < max(bs):
            r.add("error", "bs-load-order", path, line_of(txt, links[min(cu)][0]),
                  "Custom stylesheet is linked BEFORE Bootstrap, so Bootstrap wins the cascade; load yours after")
        if len(re.findall(r"\sstyle=[\"']", txt)) > 5:
            r.add("info", "inline-styles", path, None, "Many inline style= attributes; move to classes using root vars")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+"); ap.add_argument("--json", action="store_true"); ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    files = list(walk(a.paths))
    css = [f for f in files if f.endswith((".css", ".scss", ".sass", ".less"))]
    other = [f for f in files if f.endswith((".html", ".htm", ".php", ".js", ".mjs", ".jsx", ".vue", ".ts", ".tsx"))]
    blob = "\n".join(read(f) for f in other + css if not is_vendor(f))[:5_000_000]
    pkgs = "".join(read(f) for f in files if os.path.basename(f) == "package.json")
    uses_bs = bool(re.search(r"bootstrap", pkgs + blob, re.I)) or any("bootstrap" in os.path.basename(f).lower() for f in files)
    r = R()
    if not css and not other:
        print("no css/html/js files found", file=sys.stderr); return 2
    for f in css:
        if not is_vendor(f) or os.path.basename(f).lower().startswith("bootstrap.css"): audit_css(f, read(f), uses_bs, r)
    for f in other:
        if not is_vendor(f): audit_js_html(f, read(f), r, css)
    r.f.sort(key=lambda x: (x["file"], SEV[x["severity"]], x["line"] or 0))
    if a.json: print(json.dumps(r.f, indent=2))
    else:
        print(f"Bootstrap detected: {'yes' if uses_bs else 'no'}  |  {len(css)} stylesheet(s), {len(other)} html/js file(s)")
        cur = None
        for x in r.f:
            if x["file"] != cur: cur = x["file"]; print(f"\n{cur}")
            loc = f":{x['line']}" if x["line"] else ""
            print(f"  [{x['severity'].upper():5}] {x['code']}{loc} - {x['message']}")
        if not r.f: print("\nNo findings.")
    bad = any(x["severity"] == "error" or (a.strict and x["severity"] == "warn") for x in r.f)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
