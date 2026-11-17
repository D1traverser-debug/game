#!/usr/bin/env python3
"""Deterministically assemble the self-contained HTML from ordered source fragments.

The root index.html remains the deliverable and the stable HTML shell. The boss
encounter block is maintained in src/game/boss_encounters.js and inserted into
its fixed in-IIFE location. This is an ordered source fragment, not an ES module:
it intentionally shares the runtime closure and is bundled into one offline file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
BOSS_MODULE = ROOT / "src" / "game" / "boss_encounters.js"
START_ANCHOR = "/* Boss pool and combat patterns."
END_ANCHOR = "\nfunction pause("


def render(html_text: str, module_text: str) -> str:
    if html_text.count(START_ANCHOR) != 1:
        raise ValueError("BOSS_SOURCE_START_ANCHOR_MUST_OCCUR_ONCE")
    start = html_text.index(START_ANCHOR)
    if html_text.count(END_ANCHOR) != 1:
        raise ValueError("BOSS_SOURCE_END_ANCHOR_MUST_OCCUR_ONCE")
    end = html_text.index(END_ANCHOR, start)
    if end <= start:
        raise ValueError("BOSS_SOURCE_RANGE_INVALID")
    return html_text[:start] + module_text.rstrip("\n") + html_text[end:]


def build_html() -> str:
    html_text = INDEX.read_text(encoding="utf-8")
    module_text = BOSS_MODULE.read_text(encoding="utf-8")
    return render(html_text, module_text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if index.html is not reproducible")
    args = parser.parse_args()
    current = INDEX.read_text(encoding="utf-8")
    generated = build_html()
    if args.check:
        if current != generated:
            print(json.dumps({"status": "FAIL", "error": "INDEX_HTML_STALE"}, ensure_ascii=False))
            return 1
        status = "PASS_REPRODUCIBLE"
    else:
        INDEX.write_text(generated, encoding="utf-8", newline="")
        current = generated
        status = "BUILT"
    raw = current.encode("utf-8")
    print(json.dumps({
        "status": status,
        "artifact": "index.html",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "source_fragments": ["src/game/boss_encounters.js"],
        "offline_single_file": True
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
