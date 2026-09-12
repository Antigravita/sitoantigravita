"""Adds a footer link block to every page.

The pages under /percorsi/ had one inbound link each and were not in the menu,
which is enough on a small site for Google to leave them out of the index. A
sitewide footer block gives every page a stable internal link without adding a
seventh item to a menu that already wraps on mobile.

Idempotent: running it twice does not duplicate the block.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = 'class="footer-links"'

GROUPS = [
    (
        "Percorsi",
        [
            ("/percorsi/schiena", "Schiena e lombalgia"),
            ("/percorsi/postura", "Postura"),
            ("/percorsi/stress", "Stress e sonno"),
        ],
    ),
    (
        "Massaggi",
        [
            ("/massaggi/decontratturante-trieste", "Decontratturante"),
            ("/massaggi/olistico-trieste", "Olistico"),
            ("/massaggi/pietre-calde-trieste", "Pietre calde"),
            ("/massaggi/fly-massage-trieste", "Fly Massage"),
        ],
    ),
    (
        "Yoga",
        [
            ("/fly-yoga-trieste", "Fly Yoga"),
            ("/yoga-mal-di-schiena-trieste", "Yoga mal di schiena"),
            ("/yoga-cervicale-trieste", "Yoga cervicale"),
            ("/massaggio-cervicale-trieste", "Massaggio cervicale"),
        ],
    ),
]


def canonical_path(file: Path) -> str:
    rel = file.relative_to(ROOT).as_posix().removesuffix(".html")
    if rel == "index":
        return "/"
    if rel.endswith("/index"):
        return "/" + rel.removesuffix("/index") + "/"
    return "/" + rel


def build_block(current: str) -> str:
    cols = []
    for title, links in GROUPS:
        items = "".join(
            # The page never links to itself: a self-link passes nothing on and
            # reads as a dead control to anyone using the footer to navigate.
            f'<li><span aria-current="page">{label}</span></li>'
            if href == current
            else f'<li><a href="{href}">{label}</a></li>'
            for href, label in links
        )
        cols.append(f'<div class="footer-links-col"><h4>{title}</h4><ul>{items}</ul></div>')
    return (
        '\n                <nav class="footer-links" aria-label="Altre pagine">\n'
        "                    " + "".join(cols) + "\n"
        "                </nav>\n"
    )


def main() -> int:
    files = sorted(
        p
        for p in ROOT.rglob("*.html")
        if ".git" not in p.parts and "tools" not in p.parts
    )
    anchor = re.compile(r'(?=\s*</div>\s*<div class="footer-map">)')
    changed = skipped = 0

    for file in files:
        html = file.read_text(encoding="utf-8")
        if MARKER in html:
            skipped += 1
            continue
        if not anchor.search(html):
            print(f"  no footer anchor: {file.relative_to(ROOT)}")
            skipped += 1
            continue
        block = build_block(canonical_path(file))
        file.write_text(anchor.sub(block, html, count=1), encoding="utf-8")
        changed += 1

    print(f"footer links added: {changed}, skipped: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
