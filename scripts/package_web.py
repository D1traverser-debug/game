#!/usr/bin/env python3
"""Validate and package the self-contained browser prototype for preview hosting."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.html"
OUTPUT = ROOT / "dist"

def validate(raw: bytes) -> dict:
    try:
        html = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"HTML_NOT_UTF8:{exc}") from exc
    lower = html.lower()
    required = {"doctype":"<!doctype html","title":"<title>","inline_style":"<style>","inline_script":"<script>", "world_canvas":'<canvas id="world"'}
    missing = [name for name, marker in required.items() if marker not in lower]
    if missing:
        raise ValueError("MISSING_WEB_RUNTIME_MARKERS:" + ",".join(missing))
    if "window.__qa" in lower:
        raise ValueError("PRODUCTION_DEBUG_MUTATION_SURFACE")
    forbidden = [
        (r"<script\b[^>]*\bsrc\s*=", "EXTERNAL_SCRIPT"),
        (r"<link\b[^>]*\brel\s*=\s*['\"]stylesheet['\"][^>]*\bhref\s*=", "EXTERNAL_STYLESHEET"),
        (r"<iframe\b[^>]*\bsrc\s*=", "EXTERNAL_IFRAME"),
    ]
    for pattern, label in forbidden:
        if re.search(pattern, html, re.IGNORECASE):
            raise ValueError(label)
    return {"artifact":"index.html","bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
            "delivery":"static-browser-preview","external_runtime_dependencies":0,"product_status":"NOT_READY"}

def package() -> dict:
    raw = SOURCE.read_bytes()
    manifest = validate(raw)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "index.html").write_bytes(raw)
    (OUTPUT / "build-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest

def verify_output() -> dict:
    raw = SOURCE.read_bytes()
    expected = validate(raw)
    target, manifest_path = OUTPUT/"index.html", OUTPUT/"build-manifest.json"
    if not target.is_file() or target.read_bytes() != raw:
        raise ValueError("PACKAGED_HTML_MISSING_OR_MISMATCHED")
    if not manifest_path.is_file():
        raise ValueError("BUILD_MANIFEST_MISSING")
    if json.loads(manifest_path.read_text(encoding="utf-8")) != expected:
        raise ValueError("BUILD_MANIFEST_MISMATCH")
    return expected

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true",help="validate source without packaging")
    parser.add_argument("--verify-output",action="store_true",help="verify byte-identical package")
    args=parser.parse_args()
    try:
        result=validate(SOURCE.read_bytes()) if args.check else verify_output() if args.verify_output else package()
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"FAIL","error":str(exc)},ensure_ascii=False)); return 1
    print(json.dumps({"status":"PASS_WEB_PACKAGE",**result},ensure_ascii=False,indent=2)); return 0

if __name__=="__main__":
    sys.exit(main())
