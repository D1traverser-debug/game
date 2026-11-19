#!/usr/bin/env python3
"""Deterministically assemble the offline HTML from ordered source fragments."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"index.html"
BOSS_MODULE=ROOT/"src"/"game"/"boss_encounters.js"
RNG_MODULE=ROOT/"web"/"src"/"core"/"seeded-rng.mjs"
WIZARD_ATLAS_B64=ROOT/"assets"/"wizard_4x4_pack.avif.b64"
RNG_START="/* Shared deterministic gameplay RNG. */"
RNG_END="\nlet coreClock=null;"
START="/* Shared, data-driven boss attack lifecycle."
END="\nfunction pause("
SHOT_OLD="}else if(s.kind==='imp'){"
SHOT_NEW="}else if(s.kind==='enemyHoming'){bossUpdateHomingProjectile(s,dt,p)}else if(s.kind==='imp'){"
SHOT_2D_OLD="else if(s.kind==='enemy'){v2ellipse(0,0,s.r+1,s.r+1,'#db8abd')"
SHOT_2D_NEW="else if(s.kind==='enemy'||s.kind==='enemyHoming'){v2ellipse(0,0,s.r+1,s.r+1,'#db8abd')"
SHOT_3D_OLD="let c=s.kind==='enemy'?[.81,.46,.74,1]:"
SHOT_3D_NEW="let c=s.kind==='enemy'||s.kind==='enemyHoming'?[.81,.46,.74,1]:"
def replace_range(text,start,end,fragment):
 if text.count(start)!=1:raise ValueError(f"START_ANCHOR_COUNT:{text.count(start)}")
 if text.count(end)!=1:raise ValueError(f"END_ANCHOR_COUNT:{text.count(end)}")
 a=text.index(start);b=text.index(end,a)
 if b<=a:raise ValueError("INVALID_RANGE")
 return text[:a]+fragment.rstrip("\n")+text[b:]
def replace_once(text,old,new):
 if text.count(old)!=1:raise ValueError(f"REPLACE_ANCHOR_COUNT:{text.count(old)}")
 return text.replace(old,new,1)
def replace_idempotent(text,old,new,label):
 if new in text:
  if text.count(new)!=1:raise ValueError("DUPLICATE_"+label)
  return text
 return replace_once(text,old,new)
def build_html():
 text=INDEX.read_text(encoding="utf-8")
 rng=replace_once(RNG_MODULE.read_text(encoding="utf-8"),"export class SeededRng","class SeededRng")
 text=replace_range(text,RNG_START,RNG_END,RNG_START+"\n"+rng)
 text=replace_range(text,START,END,BOSS_MODULE.read_text(encoding="utf-8"))
 text=replace_idempotent(text,SHOT_OLD,SHOT_NEW,"HOMING_UPDATE")
 text=replace_idempotent(text,SHOT_2D_OLD,SHOT_2D_NEW,"HOMING_2D_STYLE")
 text=replace_idempotent(text,SHOT_3D_OLD,SHOT_3D_NEW,"HOMING_3D_STYLE")
 encoded=WIZARD_ATLAS_B64.read_text(encoding="ascii").strip()
 alphabet=set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
 if not encoded or any(char not in alphabet for char in encoded):raise ValueError("WIZARD_ATLAS_BASE64_INVALID")
 marker=f"V2_WIZARD_PACK.src='data:image/avif;base64,{encoded}';"
 if marker in text:
  if text.count(marker)!=1:raise ValueError("DUPLICATE_WIZARD_ATLAS_EMBED")
 else:
  text=replace_once(text,"V2_WIZARD_PACK.src='__WIZARD_ATLAS_DATA_URI__';",marker)
 return text
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--check",action="store_true");args=parser.parse_args()
 current=INDEX.read_text(encoding="utf-8");generated=build_html()
 if args.check:
  if current!=generated:print(json.dumps({"status":"FAIL","error":"INDEX_HTML_STALE"},ensure_ascii=False));return 1
  status="PASS_REPRODUCIBLE"
 else:INDEX.write_text(generated,encoding="utf-8",newline="");current=generated;status="BUILT"
 raw=current.encode("utf-8")
 print(json.dumps({"status":status,"artifact":"index.html","bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"source_fragments":["web/src/core/seeded-rng.mjs","src/game/boss_encounters.js","assets/wizard_4x4_pack.avif.b64"],"offline_single_file":True},ensure_ascii=False,indent=2))
 return 0
if __name__=="__main__":sys.exit(main())
