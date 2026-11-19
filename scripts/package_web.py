#!/usr/bin/env python3
"""Build a reproducible, offline static browser preview and its runtime modules."""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.html"
OUTPUT = ROOT / "dist"
CORE_FILES = (
    "fixed-step-clock.mjs", "seeded-rng.mjs", "combatant.mjs", "damage-pipeline.mjs",
    "event-buffer.mjs", "input-validator.mjs", "projectile-system.mjs", "spell-system.mjs",
)
LAUNCHER_FILES = ("PLAY.bat", "PLAY.sh", "scripts/serve_web.py")

def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def runtime_manifest() -> list[dict]:
    result=[]
    for name in CORE_FILES:
        path=ROOT/"web"/"src"/"core"/name
        if not path.is_file():
            raise ValueError(f"CORE_RUNTIME_MODULE_MISSING:{name}")
        raw=path.read_bytes()
        try: raw.decode("utf-8")
        except UnicodeDecodeError as exc: raise ValueError(f"CORE_MODULE_NOT_UTF8:{name}") from exc
        result.append({"path":f"web/src/core/{name}","bytes":len(raw),"sha256":sha256(raw)})
    return result

def validate(raw: bytes) -> dict:
    try: html=raw.decode("utf-8")
    except UnicodeDecodeError as exc: raise ValueError(f"HTML_NOT_UTF8:{exc}") from exc
    lower=html.lower()
    if re.search(r"<script\b[^>]*\bsrc\s*=",html,re.IGNORECASE): raise ValueError("EXTERNAL_SCRIPT")
    required={"doctype":"<!doctype html>","title":"<title>","inline_style":"<style>","inline_script":"<script>","world_canvas":'<canvas id="world"'}
    missing=[name for name,marker in required.items() if marker not in lower]
    if missing: raise ValueError("MISSING_WEB_RUNTIME_MARKERS:"+",".join(missing))
    if "window.__qa" in lower: raise ValueError("PRODUCTION_DEBUG_MUTATION_SURFACE")
    forbidden=[
      (r"<link\b[^>]*\brel\s*=\s*['\"]stylesheet['\"][^>]*\bhref\s*=","EXTERNAL_STYLESHEET"),
      (r"<iframe\b[^>]*\bsrc\s*=","EXTERNAL_IFRAME"),
    ]
    for pattern,label in forbidden:
        if re.search(pattern,html,re.IGNORECASE): raise ValueError(label)
    if "import('./web/src/core/fixed-step-clock.mjs')" not in html:
        raise ValueError("FIXED_STEP_RUNTIME_IMPORT_MISSING")
    modules=runtime_manifest()
    for relative in LAUNCHER_FILES:
        launcher_path=ROOT/relative
        if not launcher_path.is_file():
            raise ValueError(f"LAUNCHER_FILE_MISSING:{relative}")
        try: launcher_path.read_bytes().decode("utf-8")
        except UnicodeDecodeError as exc: raise ValueError(f"LAUNCHER_FILE_NOT_UTF8:{relative}") from exc
    launcher={"windows":"PLAY.bat","unix":"PLAY.sh","server":"scripts/serve_web.py",
              "default_host":"127.0.0.1","default_port":8000,"offline":True}
    return {"artifact":"index.html","bytes":len(raw),"sha256":sha256(raw),
            "delivery":"static-browser-preview","external_runtime_dependencies":0,
            "runtime_modules":modules,"launcher":launcher,"product_status":"NOT_READY"}

def package() -> dict:
    raw=SOURCE.read_bytes()
    manifest=validate(raw)
    OUTPUT.mkdir(parents=True,exist_ok=True)
    (OUTPUT/"index.html").write_bytes(raw)
    if (OUTPUT/"web").exists(): shutil.rmtree(OUTPUT/"web")
    for module in manifest["runtime_modules"]:
        source=ROOT/module["path"]
        target=OUTPUT/module["path"]
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
    readme=ROOT/"web"/"README.md"
    if readme.is_file(): shutil.copyfile(readme,OUTPUT/"web"/"README.md")
    for relative in LAUNCHER_FILES:
        source=ROOT/relative
        target=OUTPUT/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
    (OUTPUT/"build-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest

def verify_output() -> dict:
    raw=SOURCE.read_bytes()
    expected=validate(raw)
    target,manifest_path=OUTPUT/"index.html",OUTPUT/"build-manifest.json"
    if not target.is_file() or target.read_bytes()!=raw: raise ValueError("PACKAGED_HTML_MISSING_OR_MISMATCHED")
    if not manifest_path.is_file(): raise ValueError("BUILD_MANIFEST_MISSING")
    if json.loads(manifest_path.read_text(encoding="utf-8"))!=expected: raise ValueError("BUILD_MANIFEST_MISMATCH")
    for module in expected["runtime_modules"]:
        packaged=OUTPUT/module["path"]
        if not packaged.is_file(): raise ValueError(f"PACKAGED_RUNTIME_MODULE_MISSING:{module['path']}")
        raw_module=packaged.read_bytes()
        if len(raw_module)!=module["bytes"] or sha256(raw_module)!=module["sha256"]:
            raise ValueError(f"PACKAGED_RUNTIME_MODULE_MISMATCH:{module['path']}")
    for relative in LAUNCHER_FILES:
        source=ROOT/relative
        packaged=OUTPUT/relative
        if not packaged.is_file() or packaged.read_bytes()!=source.read_bytes():
            raise ValueError(f"PACKAGED_LAUNCHER_MISSING_OR_MISMATCHED:{relative}")
    return expected

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true",help="validate source without packaging")
    parser.add_argument("--verify-output",action="store_true",help="verify byte-identical package and runtime modules")
    args=parser.parse_args()
    try: result=validate(SOURCE.read_bytes()) if args.check else verify_output() if args.verify_output else package()
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"FAIL","error":str(exc)},ensure_ascii=False)); return 1
    print(json.dumps({"status":"PASS_WEB_PACKAGE",**result},ensure_ascii=False,indent=2)); return 0

if __name__=="__main__": sys.exit(main())
