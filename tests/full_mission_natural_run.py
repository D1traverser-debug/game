"""Accelerated but non-cheating full mission acceptance attempt.

The test runs the production simulation update loop for up to 25 in-game minutes.
It only supplies movement, interacts with nearby real objects, and chooses actual
upgrade cards offered by the game. It NEVER sets mission time, player HP, enemy
HP, boss HP, XP, objective progress, or victory state.
This is an automated pilot, not a human fun/UX sign-off.
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
window.__fullRun = async (maxSeconds) => {
  const dt=0.1;
  let elapsed=0,ticks=0,upgrades=0,interactions=0;
  const nearest=(items,p)=>items.filter(x=>x&&x.alive!==false)
    .map(o=>({o,d:Math.hypot(o.x-p.x,o.y-p.y)}))
    .sort((a,b)=>a.d-b.d)[0];
  while(elapsed<maxSeconds && !game.ended &&
        (screen==='playing'||screen==='upgrade')) {
    if(screen==='upgrade'){
      const opts=game.pending?.opts||[];
      if(!opts.length)break;
      // The pilot may only select an option the real UI has offered.
      const chosen=opts.find(o=>o.kind==='stat'&&['armor','regen','damage','crit'].includes(o.k))
        ||opts.find(o=>['spellAugment','spellLevel','spellLevelBonus','newSpell'].includes(o.kind))
        ||opts[0];
      applyUpgrade(chosen);upgrades++;continue;
    }
    const p=game.player;
    let target=null;
    const b=game.boss&&!game.boss.dead?game.boss:null;
    if(b){
      const d=Math.hypot(b.x-p.x,b.y-p.y)||1;
      if(d>300)target={x:b.x,y:b.y};
      else {
        // Circle-strafe the real boss; attacks remain automatic and unmodified.
        target={x:p.x+(p.y-b.y)/d*180,y:p.y-(p.x-b.x)/d*180};
      }
    } else if(game.objective&&!game.objective.done){
      const o=game.objective;
      if(o.type==='crab'&&o.crab?.alive)target=o.crab;
      else if(o.objects?.length){
        const found=nearest(o.objects,p);if(found)target=found.o;
      }
      if(!target&&Number.isFinite(o.x)&&Number.isFinite(o.y))target=o;
    }
    if(!target){
      const orb=nearest(game.orbs.filter(o=>o.type==='xp'),p);
      if(orb&&orb.d<700)target=orb.o;
    }
    let dx=0,dy=0;
    if(target){
      const d=Math.hypot(target.x-p.x,target.y-p.y)||1;
      if(d>28){dx=(target.x-p.x)/d;dy=(target.y-p.y)/d;}
    } else {
      const a=Math.floor(elapsed/8)*Math.PI/2;dx=Math.cos(a);dy=Math.sin(a);
    }
    keys={KeyD:dx>.25,KeyA:dx<-.25,KeyS:dy>.25,KeyW:dy<-.25};
    const chest=game.chests.find(c=>!c.open&&Math.hypot(c.x-p.x,c.y-p.y)<74);
    const objectiveItem=game.objective?.type==='brazier'&&game.objective.objects?.some(x=>x.alive&&Math.hypot(x.x-p.x,x.y-p.y)<78);
    if(chest||objectiveItem){interact();interactions++;}
    update(dt);elapsed+=dt;ticks++;
    if(ticks%100===0)await new Promise(r=>setTimeout(r,0));
  }
  keys={};
  const b=game.boss;
  return {
    screen,ended:game.ended,elapsed,gameTime:game.time,kills:game.player.kills,
    level:game.player.level,hp:game.player.hp,maxHp:game.player.maxHp,
    objectives:game.player.objectives,upgrades,interactions,
    bossSpawned:!!b,bossId:b?.bossId||null,bossHp:b?.hp??null,bossMax:b?.max??null,
    bossDead:!!b?.dead,wins:save.wins||0,losses:save.runs-(save.wins||0),
    errors:game.player.hp<0||!Number.isFinite(game.player.hp)||!Number.isFinite(game.time)
  };
};
"""
DOCUMENT=SOURCE.replace(MARKER,PROBE+"\n"+MARKER)

async def main():
    report={"checks":{},"page_errors":[],"console_errors":[],"external_requests":[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
        page=await browser.new_page(viewport={"width":1280,"height":800})
        page.on("pageerror",lambda e:report["page_errors"].append(str(e)))
        page.on("console",lambda m:report["console_errors"].append(m.text) if m.type=="error" else None)
        page.on("request",lambda r:report["external_requests"].append(r.url) if r.url.startswith(("http://","https://")) else None)
        await page.set_default_timeout(180000)
        await page.set_content(DOCUMENT,wait_until="load")
        await page.locator("#start").click()
        state=await page.evaluate("window.__fullRun(1500)",timeout=180000)
        report["state"]=state
        report["checks"]["reached_nineteen_minute_boss_window"]=state["gameTime"]>=1140 or state["bossSpawned"]
        report["checks"]["boss_naturally_spawned"]=state["bossSpawned"]
        report["checks"]["boss_naturally_defeated"]=state["bossDead"] and state["ended"] and state["screen"]=="result"
        report["checks"]["natural_win_recorded"]=state["wins"]>=1
        report["checks"]["no_invalid_player_or_clock_state"]=not state["errors"]
        report["checks"]["no_runtime_or_console_errors"]=not report["page_errors"] and not report["console_errors"]
        report["checks"]["offline_no_external_requests"]=not report["external_requests"]
        report["pass"]=all(report["checks"].values())
        print(json.dumps(report,ensure_ascii=False,indent=2))
        await browser.close()
    if not report["pass"]:
        raise SystemExit(1)

if __name__=="__main__":
    asyncio.run(main())
