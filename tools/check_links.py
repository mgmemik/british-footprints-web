#!/usr/bin/env python3
"""Checks the built pages: every local href/src/srcset target exists, tags are balanced,
images have alt text, and lists the external links. Usage: python3 tools/check_links.py"""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "privacy/index.html", "support/index.html"]
VOID = {"meta", "link", "img", "br", "input", "source", "hr"}


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.stack, self.errors, self.ids = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        for k in ("href", "src"):
            if a.get(k):
                self.refs.append(a[k])
        if a.get("srcset"):
            self.refs += [p.strip().split()[0] for p in a["srcset"].split(",")]
        if tag == "img" and "alt" not in a:
            self.errors.append(f"img without alt: {a.get('src')}")
        if a.get("id"):
            self.ids.append(a["id"])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unbalanced </{tag}> (open: {self.stack[-3:]})")
        else:
            self.stack.pop()


def main():
    bad, external = [], set()
    for page in PAGES:
        path = ROOT / page
        p = P()
        p.feed(path.read_text("utf-8"))
        bad += [f"{page}: {e}" for e in p.errors]
        if p.stack:
            bad.append(f"{page}: unclosed {p.stack}")
        if len(p.ids) != len(set(p.ids)):
            bad.append(f"{page}: duplicate ids")
        for ref in p.refs:
            if ref.startswith(("http://", "https://")):
                external.add(ref)
                continue
            if ref.startswith(("mailto:", "#")):
                continue
            target = (path.parent / unquote(urlsplit(ref).path))
            if ref.endswith("/") or target.is_dir():
                target = target / "index.html"
            if not target.exists():
                bad.append(f"{page}: missing {ref}")
    print("external links:")
    for e in sorted(external):
        print("  ", e)
    for b in bad:
        print("PROBLEM:", b)
    print("ok" if not bad else f"{len(bad)} problems")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
