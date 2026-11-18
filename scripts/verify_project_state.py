#!/usr/bin/env python3
"""Mechanical browser-product checkpoint guard; this is not a game-quality test."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

OWNER_SCOPE={
 "product":"Original-IP browser-first 3D co-op roguelite inspired by observable spell-survivor gameplay",
 "modes":["solo","online_coop_1_to_4"],"players":"1-4","multiplayer":True,
 "target_platform":"Modern desktop browsers first; mobile browser compatibility",
 "input":["keyboard_mouse","controller","touch"],
 "engine":"WebGL2 3D world + DOM UI; raw WebGL2 vs bundled Three.js decision pending measured vertical-slice comparison",
 "final_delivery":"Deployable static browser frontend plus separate authoritative WebSocket room service",
 "original_ip_required":True,"browser_first":True,
}
def verify(root:Path)->dict:
 state_path,source_path,handoff=root/"docs"/"PROJECT_STATE.json",root/"index.html",root/"HANDOFF.md"
 errors=[]
 try: state=json.loads(state_path.read_text(encoding="utf-8"))
 except (OSError,ValueError) as exc: return {"status":"FAIL","errors":[f"STATE_MISSING_OR_INVALID:{exc}"]}
 if state.get("repository")!="D1traverser-debug/game": errors.append("WRONG_REPOSITORY")
 if state.get("active_production_branch")!="full-game" or state.get("branch")!="full-game": errors.append("ACTIVE_BRANCH_DRIFT")
 if state.get("legacy_prototype_branch")!="development": errors.append("LEGACY_BRANCH_DRIFT")
 for key,value in OWNER_SCOPE.items():
  if state.get("scope",{}).get(key)!=value: errors.append(f"SCOPE_DRIFT:{key}")
 if "read-only" not in state.get("caos_boundary","").lower(): errors.append("CAOS_BOUNDARY_MISSING")
 if state.get("status")=="READY" and not state.get("owner_acceptance"): errors.append("UNSUPPORTED_READY_STATUS")
 artifact=state.get("web_game_artifact",{})
 try: raw=source_path.read_bytes()
 except OSError as exc: return {"status":"FAIL","errors":[f"HTML_MISSING:{exc}"]+errors}
 if artifact.get("path")!="index.html": errors.append("WEB_ARTIFACT_PATH_DRIFT")
 if artifact.get("bytes")!=len(raw): errors.append("WEB_ARTIFACT_SIZE_MISMATCH")
 text=raw.decode("utf-8","replace")
 if '<canvas id="world"' not in text or "<script>" not in text or "<style>" not in text: errors.append("WEB_RUNTIME_MARKERS_MISSING")
 if "window.__QA" in text: errors.append("PRODUCTION_DEBUG_MUTATION_SURFACE")
 if re.search(r"<script\b[^>]*\bsrc\s*=",text,re.I): errors.append("EXTERNAL_RUNTIME_SCRIPT")
 if not handoff.is_file(): errors.append("HANDOFF_MISSING")
 return {"status":"PASS_MECHANICAL_ONLY" if not errors else "FAIL","branch":state.get("active_production_branch"),
         "checkpoint":state.get("checkpoint"),"product_status":state.get("status"),"bytes":len(raw),"errors":errors,
         "warning":"This checks scope metadata and static HTML integrity only. It does not prove full gameplay, co-op, production art/audio, browser compatibility, performance, hosting or player acceptance."}
def main()->int:
 p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]); a=p.parse_args()
 result=verify(a.root); print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result["status"]=="PASS_MECHANICAL_ONLY" else 1
if __name__=="__main__": sys.exit(main())
