#!/usr/bin/env python3
"""Deterministically assemble the offline HTML from ordered source fragments."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"index.html"
BOSS_MODULE=ROOT/"src"/"game"/"boss_encounters.js"
START="/* Boss pool and combat patterns."
END="\nfunction pause("
SHOT_OLD="}else if(s.kind==='imp'){"
SHOT_NEW="}else if(s.kind==='enemyHoming'){bossUpdateHomingProjectile(s,dt,p)}else if(s.kind==='imp'){"
def replace_range(text,start,end,fragment):
 if text.count(start)!=1:raise ValueError(f"START_ANCHOR_COUNT:{text.count(start)}")
 if text.count(end)!=1:raise ValueError(f"END_ANCHOR_COUNT:{text.count(end)}")
 a=text.index(start);b=text.index(end,a)
 if b<=a:raise ValueError("INVALID_RANGE")
 return text[:a]+fragment.rstrip("\n")+text[b:]
def replace_once(text,old,new):
 if text.count(old)!=1:raise ValueError(f"REPLACE_ANCHOR_COUNT:{text.count(old)}")
 return text.replace(old,new,1)
def build_html():
 text=INDEX.read_text(encoding="utf-8")
 text=replace_range(text,START,END,BOSS_MODULE.read_text(encoding="utf-8"))
 return replace_once(text,SHOT_OLD,SHOT_NEW)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--check",action="store_true");args=parser.parse_args()
 current=INDEX.read_text(encoding="utf-8");generated=build_html()
 if args.check:
  if current!=generated:print(json.dumps({"status":"FAIL","error":"INDEX_HTML_STALE"},ensure_ascii=False));return 1
  status="PASS_REPRODUCIBLE"
 else:INDEX.write_text(generated,encoding="utf-8",newline="");current=generated;status="BUILT"
 raw=current.encode("utf-8")
 print(json.dumps({"status":status,"artifact":"index.html","bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"source_fragments":["src/game/boss_encounters.js"],"offline_single_file":True},ensure_ascii=False,indent=2))
 return 0
if __name__=="__main__":sys.exit(main())
