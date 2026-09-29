#!/usr/bin/env python3
"""Scan .htaccess files and report misconfigurations, focusing on
extensionless (no .php) URL handling.

Usage: htaccess_scan.py [--json] [--strict] PATH [PATH ...]
Exit code: 1 if any error-level finding (or warning with --strict), else 0.
"""
import argparse
import json
import os
import re
import sys

SEV_ORDER = {"error": 0, "warn": 1, "info": 2}


class Finding:
    def __init__(self, sev, code, line, msg):
        self.sev, self.code, self.line, self.msg = sev, code, line, msg

    def as_dict(self, path):
        return {"file": path, "line": self.line, "severity": self.sev,
                "code": self.code, "message": self.msg}


def logical_lines(text):
    """Yield (lineno, stripped line) with backslash continuations joined and comments dropped."""
    buf, start = "", 0
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if not buf:
            start = i
        if line.endswith("\\"):
            buf += line[:-1] + " "
            continue
        buf += line
        s = buf.strip()
        buf = ""
        if s and not s.startswith("#"):
            yield start, s
    if buf.strip() and not buf.strip().startswith("#"):
        yield start, buf.strip()


def scan(text):
    F = []
    lines = list(logical_lines(text))
    engine_on_at = None
    php_rewrites = []      # lines of rules that append .php
    php_file_conds = []    # lines of %{REQUEST_FILENAME}.php -f style conds
    dir_guard = False
    multiviews = None
    direct_php_redirect = False
    has_indexes_off = False
    has_ifmodule_stack = []
    rules_before_engine = []

    for no, l in lines:
        low = l.lower()

        if re.match(r"<ifmodule\b", low):
            has_ifmodule_stack.append(no)
        elif re.match(r"</ifmodule>", low):
            if has_ifmodule_stack:
                has_ifmodule_stack.pop()
            else:
                F.append(Finding("error", "unbalanced-block", no, "</IfModule> without opening tag"))

        m = re.match(r"rewriteengine\s+(on|off)", low)
        if m:
            if m.group(1) == "on":
                engine_on_at = engine_on_at or no
            continue

        if re.match(r"(rewriterule|rewritecond)\b", low) and engine_on_at is None:
            rules_before_engine.append(no)

        # extensionless via MultiViews
        m = re.match(r"options\s+(.*)", low)
        if m:
            for tok in m.group(1).split():
                if tok in ("+multiviews", "multiviews"):
                    multiviews = no
                if tok == "-indexes":
                    has_indexes_off = True
                if tok in ("+indexes", "indexes"):
                    F.append(Finding("warn", "indexes-on", no,
                                     "Directory listing enabled (Options +Indexes); use -Indexes"))
                if tok in ("+execcgi", "execcgi"):
                    F.append(Finding("warn", "execcgi", no, "Options +ExecCGI enabled; confirm CGI execution is intended"))

        if low.startswith("rewritecond"):
            if re.search(r"%\{request_filename\}\.php\s+-f", low) or re.search(r"%\{document_root\}/?%\{request_uri\}\.php\s+-f", low):
                php_file_conds.append(no)
            if re.search(r"%\{request_filename\}\s+!-d", low):
                dir_guard = True
            # direct .php access redirected away
            if re.search(r"%\{the_request\}.*\.php", low):
                direct_php_redirect = True

        if low.startswith("rewriterule"):
            parts = l.split()
            if len(parts) >= 3:
                pat, sub = parts[1], parts[2]
                if re.search(r"\.php\b", sub) and not re.search(r"\.php\b", pat) and sub != "-":
                    # substitution appends .php to a captured/request path
                    if re.search(r"\$\d|%\{", sub):
                        php_rewrites.append(no)
                if re.search(r"\\?\.php", pat) and re.search(r"\[[^\]]*R=?\d*", l, re.I):
                    direct_php_redirect = True

        if low.startswith(("addhandler", "addtype", "sethandler")) and "php" in low:
            exts = re.findall(r"\.\w+", l)
            if any(e.lower() not in (".php", ".phtml", ".php5", ".php7", ".php8") for e in exts):
                F.append(Finding("warn", "odd-php-handler", no,
                                 "PHP handler mapped to non-standard extension(s): " + " ".join(exts)))
            if re.match(r"addhandler\b", low):
                F.append(Finding("info", "addhandler-php", no,
                                 "AddHandler matches double extensions (shell.php.jpg executes); prefer <FilesMatch \\.php$> SetHandler"))

        if low.startswith("forcetype") and "php" in low:
            F.append(Finding("info", "forcetype-php", no,
                             "ForceType PHP: serves matching files as PHP with no extension (ok only if scoped tightly)"))

        if re.match(r"php_(admin_)?flag\s+display_errors\s+(on|1)", low):
            F.append(Finding("warn", "display-errors", no, "display_errors On leaks paths/queries in production"))


    for n in has_ifmodule_stack:
        F.append(Finding("error", "unbalanced-block", n, "<IfModule> never closed"))

    for n in rules_before_engine[:1]:
        F.append(Finding("error", "no-rewrite-engine", n,
                         "Rewrite directive used without a preceding 'RewriteEngine On'; it is ignored"))

    # --- extensionless handling verdict ---
    ext_less = bool(php_rewrites) or multiviews is not None
    if multiviews is not None:
        F.append(Finding("warn", "multiviews", multiviews,
                         "Options +MultiViews serves /page as page.php via content negotiation. "
                         "Works, but is slow, can expose unintended files and conflicts with RewriteRules; "
                         "prefer explicit RewriteRule with -f check"))
    for n in php_rewrites:
        F.append(Finding("info", "extensionless-rule", n, "Rule maps extensionless URL to a .php file"))
    if php_rewrites and not php_file_conds:
        F.append(Finding("error", "missing-file-exists-check", php_rewrites[0],
                         "Appends .php without 'RewriteCond %{REQUEST_FILENAME}.php -f'. "
                         "Non-existent paths get rewritten to missing files (404s from PHP, loops/500s)"))
    if php_rewrites and not dir_guard:
        F.append(Finding("warn", "missing-dir-guard", php_rewrites[0],
                         "No 'RewriteCond %{REQUEST_FILENAME} !-d'; directories may be mis-rewritten"))
    if ext_less and not direct_php_redirect:
        F.append(Finding("warn", "duplicate-urls", php_rewrites[0] if php_rewrites else multiviews,
                         "Both /page and /page.php are reachable (duplicate content, inconsistent access rules). "
                         "Add a 301 from *.php to the extensionless URL (match on %{THE_REQUEST} to avoid loops)"))
    if not ext_less:
        F.append(Finding("info", "no-extensionless", None,
                         "Extensionless URLs are NOT enabled: /page will 404, only /page.php works"))
    if not has_indexes_off and not any(f.code == "indexes-on" for f in F):
        F.append(Finding("info", "indexes-unset", None,
                         "Directory listing not explicitly disabled; add 'Options -Indexes'"))

    body = "\n".join(l for _, l in lines).lower()
    if not re.search(r"(filesmatch|files)\b.*(\\\.env|\^\\\.|\.ht|\\\.git)", body) and "\\.env" not in body:
        F.append(Finding("info", "no-dotfile-protection", None,
                         "No rule blocking dotfiles (.env, .git, .htpasswd); add <FilesMatch \"^\\.\"> Require all denied"))
    return F


def find_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "vendor")]
                for f in files:
                    if f == ".htaccess" or f.endswith(".htaccess"):
                        yield os.path.join(root, f)
        elif os.path.isfile(p):
            yield p
        else:
            print(f"warning: {p} not found", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    a = ap.parse_args()

    results, failed, n = [], False, 0
    for path in find_files(a.paths):
        n += 1
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                fs = scan(fh.read())
        except OSError as e:
            print(f"error: {path}: {e}", file=sys.stderr)
            failed = True
            continue
        fs.sort(key=lambda f: (SEV_ORDER[f.sev], f.line or 0))
        results.append((path, fs))
        if any(f.sev == "error" or (a.strict and f.sev == "warn") for f in fs):
            failed = True

    if a.json:
        print(json.dumps([f.as_dict(p) for p, fs in results for f in fs], indent=2))
    else:
        for path, fs in results:
            print(f"\n{path}")
            if not fs:
                print("  OK")
            for f in fs:
                loc = f":{f.line}" if f.line else ""
                print(f"  [{f.sev.upper():5}] {f.code}{loc} - {f.msg}")
        print(f"\nScanned {n} file(s).")
    if n == 0:
        print("no .htaccess files found", file=sys.stderr)
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
