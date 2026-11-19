"""Bounded enemy-director RNG and entity identity regression.

The browser probe is injected into an in-memory document only. Production HTML
contains no diagnostic hooks and this test does not claim full-run replay.
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
MARKER="// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER)==1
SPAWN_BLOCK=SOURCE.split("function spawnEnemy",1)[1].split("\nfunction enemyType",1)[0]
assert "Math.random" not in SPAWN_BLOCK
assert "enemyRand(" in SPAWN_BLOCK and "enemyRandom(" in SPAWN_BLOCK
assert "id:Math.random()" not in SOURCE

PROBE=r"""
window.__enemyDirectorProbe={
 async trace(seed,options={}) {
  const oldMuted=muted;muted=options.muted===true;
  startRun(seed);
  const enemyStateBefore=game.enemyRng.state.toString();
  const objectiveStateBefore=game.runRng.state.toString();
  if(options.draws){game.shake=8;for(let i=0;i<options.draws;i++)drawWorld()}
  for(let i=0;i<(options.audioCalls||0);i++){sound(440,.04,'sine');studioNoiseHit(.04,.0001,900,0)}
  let stateDuringPause=game.enemyRng.state.toString();
  if(options.pauseResume){pause();await new Promise(resolve=>requestAnimationFrame(resolve));stateDuringPause=game.enemyRng.state.toString();resume()}
  const enemyStateAfterPresentation=game.enemyRng.state.toString();
  game.time=650;
  for(let i=0;i<24;i++)spawnEnemy(false);
  const rows=game.enemies.map(e=>({
   id:e.id,type:e.type,x:e.x,y:e.y,r:e.r,hp:e.hp,max:e.max,speed:e.speed,
   dmg:e.dmg,attack:e.attack,heal:e.heal,elite:e.elite,visualPhase:e.visualPhase
  }));
  const enemyStateAfterSpawn=game.enemyRng.state.toString();
  const objectiveStateAfterSpawn=game.runRng.state.toString();
  muted=oldMuted;
  return {
   rows,trace:JSON.stringify(rows),enemyStateBefore,enemyStateAfterPresentation,
   enemyStateAfterSpawn,objectiveStateBefore,objectiveStateAfterSpawn,stateDuringPause,
   nextEnemyId:game.nextEnemyId,enemyRngVersion:game.enemyRngVersion,
   enemyRngSequence:game.enemyRngSequence
  };
 },
 director(seed) {
  startRun(seed);game.time=300;game.nextObj=4;game.nextChest=99999;game.spawn=0;
  const before=game.enemies.filter(e=>!e.dead).length;
  updateEnemyDirector(1/30);
  const afterFirst=game.enemies.filter(e=>!e.dead).length;
  const firstRows=game.enemies.slice(before).map(e=>({id:e.id,type:e.type,x:e.x,y:e.y}));
  game.spawn=0;updateEnemyDirector(1/30);
  const afterSecond=game.enemies.filter(e=>!e.dead).length;
  return {before,afterFirst,afterSecond,firstRows,secondRows:game.enemies.slice(afterFirst).map(e=>({id:e.id,type:e.type,x:e.x,y:e.y})),target:Math.min(64,18+Math.floor(game.time/40))};
 },
 allocator(seed) {
  startRun(seed);const before=game.enemyRng.state.toString();
  const ids=[allocateEnemyId(),allocateEnemyId()];
  return {ids,before,after:game.enemyRng.state.toString(),nextEnemyId:game.nextEnemyId};
 },
 cap(seed) {
  startRun(seed);
  for(let i=0;i<100;i++)spawnEnemy(false,'crawler');
  const count=game.enemies.filter(e=>!e.dead).length,next=game.nextEnemyId,state=game.enemyRng.state.toString();
  spawnEnemy(false,'crawler');
  return {count,next,nextAfter:game.nextEnemyId,state,stateAfter:game.enemyRng.state.toString(),ids:game.enemies.map(e=>e.id)};
 },
 objectiveIsolation(seed) {
  startRun(seed);const before=game.enemyRng.state.toString();
  game.player.x=0;game.player.y=0;game.seenObjectives=[];
  startObjective();
  return {before,after:game.enemyRng.state.toString()};
 }
};
"""
DOCUMENT=SOURCE.replace(MARKER,PROBE+"\n"+MARKER)

def signature(row):
    return json.dumps(row["rows"],ensure_ascii=False,sort_keys=True)

async def main():
 report={"checks":{},"page_errors":[],"console_errors":[],"external_requests":[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  page=await browser.new_page(viewport={"width":1280,"height":800})
  page.on("pageerror",lambda e:report["page_errors"].append(str(e)))
  page.on("console",lambda m:report["console_errors"].append(m.text) if m.type=="error" else None)
  page.on("request",lambda r:report["external_requests"].append(r.url) if r.url.startswith(("http://","https://")) else None)
  await page.set_content(DOCUMENT,wait_until="load")
  await page.locator("#start").click()
  baseline=await page.evaluate("(seed)=>window.__enemyDirectorProbe.trace(seed,{muted:true})",20261119)
  replay=await page.evaluate("(seed)=>window.__enemyDirectorProbe.trace(seed,{muted:true})",20261119)
  isolated=await page.evaluate("(seed)=>window.__enemyDirectorProbe.trace(seed,{muted:false,draws:24,audioCalls:8,pauseResume:true})",20261119)
  samples=await page.evaluate("async()=>Promise.all(Array.from({length:32},(_,i)=>window.__enemyDirectorProbe.trace(i+1,{muted:true})))")
  director=await page.evaluate("(seed)=>window.__enemyDirectorProbe.director(seed)",20261119)
  directorReplay=await page.evaluate("(seed)=>window.__enemyDirectorProbe.director(seed)",20261119)
  allocator=await page.evaluate("(seed)=>window.__enemyDirectorProbe.allocator(seed)",20261119)
  cap=await page.evaluate("(seed)=>window.__enemyDirectorProbe.cap(seed)",20261119)
  objectiveIsolation=await page.evaluate("(seed)=>window.__enemyDirectorProbe.objectiveIsolation(seed)",20261119)
  unique={signature(row) for row in samples}
  types={enemy["type"] for row in samples for enemy in row["rows"]}
  ids=baseline["rows"] and [row["id"] for row in baseline["rows"]]
  report["sample"]={"count":len(samples),"unique_spawn_traces":len(unique),"enemy_types":sorted(types),"baseline_enemy_count":len(baseline["rows"])}
  report["director"]=director
  report["allocator"]=allocator
  report["cap"]={"active_count":cap["count"],"next_id":cap["next"],"unique_ids":len(set(cap["ids"]))}
  report["checks"]["same_seed_spawn_trace_repeats"]=signature(baseline)==signature(replay)
  report["checks"]["different_seeds_diverge"]=len(unique)>=24 and len(types)==7
  report["checks"]["enemy_ids_are_monotonic_unique"]=ids==list(range(1,len(ids)+1)) and len(set(ids))==len(ids)
  report["checks"]["enemy_visual_phase_is_deterministic"]=all(0<=e["visualPhase"]<6.283185307179586 for e in baseline["rows"])
  report["checks"]["render_audio_pause_do_not_advance_enemy_rng"]=baseline["enemyStateBefore"]==isolated["enemyStateBefore"]==isolated["enemyStateAfterPresentation"]==isolated["stateDuringPause"]
  report["checks"]["enemy_spawns_do_not_advance_objective_rng"]=baseline["objectiveStateBefore"]==baseline["objectiveStateAfterSpawn"]
  report["checks"]["objective_generation_does_not_advance_enemy_rng"]=objectiveIsolation["before"]==objectiveIsolation["after"]
  report["checks"]["id_allocator_does_not_consume_rng"]=allocator["ids"]==[13,14] and allocator["before"]==allocator["after"]
  report["checks"]["enemy_population_director_is_repeatable"]=director==directorReplay
  report["checks"]["enemy_population_director_respects_target"]=director["before"]==12 and director["afterFirst"]==14 and director["afterSecond"]==15 and director["target"]==25
  report["checks"]["enemy_population_cap_and_id_allocator_hold"]=cap["count"]==64 and cap["next"]==65 and cap["nextAfter"]==65 and cap["state"]==cap["stateAfter"] and len(set(cap["ids"]))==64
  report["checks"]["enemy_rng_metadata_is_versioned"]=baseline["enemyRngVersion"]=="pcg-xsh-rr32-v1" and baseline["enemyRngSequence"]==0xE11E
  report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
  report["checks"]["offline_no_external_requests"]=not report["external_requests"]
  report["pass"]=all(report["checks"].values())
  print(json.dumps(report,ensure_ascii=False,indent=2))
  await browser.close()
 if not report["pass"]:raise SystemExit(1)

if __name__=="__main__":asyncio.run(main())
