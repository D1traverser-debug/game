"""Bounded deterministic RNG integration for objective generation and world layout.

The diagnostic probe is injected into an in-memory browser document. No production
debug hooks are shipped and this test does not claim full-run deterministic replay.
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")
MARKER = "// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER) == 1

PROBE = r"""
window.__objectiveRngProbe = {
  async trace(seed, options={}) {
    const oldMuted=muted,oldCount=save.stats.objectives,oldHistory=save.objectiveHistory,oldTrial=save.trialSpellId;
    muted=options.muted===true;
    save.stats.objectives=50;
    save.objectiveHistory={fungi:1,statues:1,crab:1,rift:1,sludge:1,sacrifice:1,cores:1,brazier:1,beasts:1};
    save.trialSpellId=null;
    startRun(seed);
    game.player.x=0;game.player.y=0;game.seenObjectives=[];
    startObjective();
    const o=game.objective;
    const snapshot={
      seed:game.runSeed,rngVersion:game.rngVersion,
      worldLayoutSeed:game.worldLayoutSeed,worldLayoutVersion:game.worldLayoutVersion,
      type:o.type,variant:o.variant,target:o.target,x:o.x,y:o.y,
      objects:(o.objects||[]).map(v=>({x:v.x,y:v.y,index:v.index,hp:v.hp,alive:v.alive,activated:v.activated})),
      nodes:(o.nodes||[]).map(v=>({x:v.x,y:v.y,progress:v.progress})),
      crab:o.crab?{x:o.crab.x,y:o.crab.y,hp:o.crab.hp,r:o.crab.r,mother:o.crab.mother}:null,
      sequence:o.sequence||null,rngState:game.runRng.state.toString()
    };
    const worldSignature=options.includeWorldSignature?JSON.stringify(game.decor.map(v=>[v.x,v.y,v.type,v.s,v.rot,v.c])):null;
    const stateBefore=game.runRng.state.toString();
    game.shake=8;
    for(let i=0;i<(options.draws||0);i++)drawWorld();
    const stateAfterDraw=game.runRng.state.toString();
    for(let i=0;i<(options.audioCalls||0);i++){sound(440,.04,'sine');studioNoiseHit(.04,.0001,900,0)}
    const stateAfterAudio=game.runRng.state.toString();
    let stateDuringPause=stateAfterAudio;
    if(options.pauseResume){pause();await new Promise(resolve=>requestAnimationFrame(resolve));stateDuringPause=game.runRng.state.toString();resume()}
    const stateAfterResume=game.runRng.state.toString();
    muted=oldMuted;save.stats.objectives=oldCount;save.objectiveHistory=oldHistory;save.trialSpellId=oldTrial;
    return {snapshot,trace:JSON.stringify(snapshot),worldSignature,stateBefore,stateAfterDraw,stateAfterAudio,stateDuringPause,stateAfterResume};
  },
  newSeeds(count) {
    const oldMuted=muted;muted=true;const values=[];
    for(let i=0;i<count;i++){startRun();values.push(game.runSeed)}
    muted=oldMuted;return values;
  },
  finishSeed() {
    finish(false,true);
    return {text:$('resultStats').innerText,seed:game.runSeed,version:RUN_RNG_VERSION};
  }
};
"""
DOCUMENT = SOURCE.replace(MARKER, PROBE + "\n" + MARKER)

def objective_signature(row):
    snapshot=row["snapshot"]
    keys=("type","variant","target","x","y","objects","nodes","crab","sequence")
    return json.dumps({key:snapshot.get(key) for key in keys},ensure_ascii=False,sort_keys=True)

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
        baseline=await page.evaluate("(seed)=>window.__objectiveRngProbe.trace(seed,{muted:true,includeWorldSignature:true})",20261119)
        replay=await page.evaluate("(seed)=>window.__objectiveRngProbe.trace(seed,{muted:true})",20261119)
        isolated=await page.evaluate("(seed)=>window.__objectiveRngProbe.trace(seed,{muted:false,draws:24,audioCalls:8,pauseResume:true})",20261119)
        other_world=await page.evaluate("(seed)=>window.__objectiveRngProbe.trace(seed,{muted:true,includeWorldSignature:true})",20261120)
        samples=await page.evaluate("async()=>Promise.all(Array.from({length:32},(_,i)=>window.__objectiveRngProbe.trace(i+1,{muted:true})))")
        new_seeds=await page.evaluate("()=>window.__objectiveRngProbe.newSeeds(8)")
        display=await page.evaluate("()=>window.__objectiveRngProbe.finishSeed()")
        signatures={objective_signature(row) for row in samples}
        types={row["snapshot"]["type"] for row in samples}
        report["baseline"]=baseline["snapshot"]
        report["different_seed_sample"]={"count":len(samples),"unique_objective_traces":len(signatures),"objective_types":sorted(types)}
        report["new_run_seeds"]=new_seeds
        report["result_seed_display"]=display
        report["checks"]["same_seed_trace_repeats"]=baseline["trace"]==replay["trace"]
        report["checks"]["different_seeds_diverge"]=len(signatures)>=24 and len(types)>=4
        report["checks"]["world_layout_is_seed_independent"]=baseline["worldSignature"]==other_world["worldSignature"]
        report["checks"]["render_does_not_advance_run_rng"]=isolated["stateBefore"]==isolated["stateAfterDraw"]
        report["checks"]["audio_does_not_advance_run_rng"]=isolated["stateBefore"]==isolated["stateAfterAudio"]
        report["checks"]["pause_resume_does_not_advance_run_rng"]=isolated["stateBefore"]==isolated["stateDuringPause"]==isolated["stateAfterResume"]
        report["checks"]["render_audio_pause_do_not_change_objective_trace"]=baseline["trace"]==isolated["trace"]
        report["checks"]["ordinary_new_runs_get_fresh_seeds"]=len(set(new_seeds))==8
        report["checks"]["run_seed_and_algorithm_are_visible_on_result"]=str(display["seed"]) in display["text"] and display["version"] in display["text"]
        report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
        report["checks"]["offline_no_external_requests"]=not report["external_requests"]
        report["pass"]=all(report["checks"].values())
        print(json.dumps(report,ensure_ascii=False,indent=2))
        await browser.close()
    if not report["pass"]:
        raise SystemExit(1)

if __name__=="__main__":
    asyncio.run(main())
