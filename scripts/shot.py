#!/usr/bin/env -S uv run --with playwright --script
"""Screenshot rendered pages so layout can be reviewed rather than guessed at.

Usage:
    ./scripts/shot.py OUTDIR [width] [page.html ...]

Defaults to the home page at desktop width. Pages are paths relative to
_site/. Requires "uvx --from playwright playwright install chromium" once.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent.parent
site = root / "_site"

outdir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "_shots"
width = int(sys.argv[2]) if len(sys.argv) > 2 else 1440
pages = sys.argv[3:] or ["index.html"]

outdir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": width, "height": 1000})
    for rel in pages:
        target = site / rel
        if not target.exists():
            print(f"missing {target}")
            continue
        page.goto(target.as_uri())
        page.wait_for_timeout(400)
        name = rel.replace("/", "-").replace(".html", "")
        out = outdir / f"{name}-{width}.png"
        page.screenshot(path=str(out), full_page=True)
        print(out)
    browser.close()
