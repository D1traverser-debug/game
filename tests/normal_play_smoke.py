"""Normal-play 90-second combat smoke.

Unlike component probes, this test does not inject game-state values, damage
enemies, skip mission time, grant XP, or force a result. It only supplies player
movement and selects offered upgrades through the production upgrade handler.
The simulation clock is advanced in 100 ms steps to keep CI deterministic.
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
let __pendingNormalRunSeed=null;
const __normalOriginalStartRun=startRun;
startRun=(seed=null)=>{const effectiveSeed=seed===null?__pendingNormalRunSeed:seed;__pendingNormalRunSeed=null;return __normalOriginalStartRun(effectiveSeed)};
window.__setRunSeed=(seed)=>{
  __pendingNormalRunSeed=seed>>>0;
  let state=seed>>>0;
  Math.random=()=>{
    state=(Math.imul(1664525,state)+1013904223)>>>0;
    return state/4294967296;
  };
};
window.__normalDamageEvents=[];
const __normalBaseDamage=damagePlayer;
damagePlayer=(n,source)=>{
  const p=game?.player;
  window.__normalDamageEvents.push({
    t:+(game?.time||0).toFixed(1),source,amount:+Number(n).toFixed(1),
    hp:p?+p.hp.toFixed(1):null,x:p?+p.x.toFixed(1):null,y:p?+p.y.toFixed(1):null
  });
  return __normalBaseDamage(n,source);
};
window.__normalPlay = async (seconds,seed) => {
  const dt = 0.1;
  let elapsed=0,ticks=0,upgrades=0,interactions=0;
  const nearest=(items,p)=>items.map(o=>({o,d:Math.hypot(o.x-p.x,o.y-p.y)})).sort((a,b)=>a.d-b.d)[0];
  const chooseUpgrade=(opts,p)=>{
    const priority={maxHp:0,regen:1,armor:2,dodge:3};
    const defense=opts.filter(x=>x.kind==='stat'&&Object.prototype.hasOwnProperty.call(priority,x.k))
      .sort((a,b)=>priority[a.k]-priority[b.k])[0];
    const sustain=new Set(['健康成长','壁垒','厚皮','闪避疗愈','致命回响','魔力虹吸','魔力汲取','目标馈赠']);
    const scroll=opts.find(x=>x.kind==='scroll'&&sustain.has(x.name));
    if(p.hp/Math.max(1,p.maxHp)<.8&&scroll)return scroll;
    if(defense)return defense;
    if(scroll)return scroll;
    return opts.find(x=>x.kind==='newSpell')||opts.find(x=>x.kind==='spellAugment')||opts[0];
  };
  while(elapsed<seconds&&(screen==='playing'||screen==='upgrade')&&!game.ended){
    if(screen==='upgrade'){
      const opts=game.pending?.opts||[];
      if(!opts.length)break;
      applyUpgrade(chooseUpgrade(opts,game.player));
      upgrades++;
      continue;
    }
    const p=game.player,hpRatio=p.hp/Math.max(1,p.maxHp);
    const health=nearest(game.orbs.filter(o=>o.type==='health'),p);
    const xp=nearest(game.orbs.filter(o=>o.type==='xp'),p);
    const target=hpRatio<.76&&health&&health.d<900?health:(xp&&xp.d<650?xp:null);
    let gx=target&&target.d>24?(target.o.x-p.x)/target.d:Math.cos(Math.floor(elapsed/7)%4*Math.PI/2);
    let gy=target&&target.d>24?(target.o.y-p.y)/target.d:Math.sin(Math.floor(elapsed/7)%4*Math.PI/2);
    let rx=0,ry=0;
    for(const e of game.enemies){
      if(e.dead||e.state==='burrow')continue;
      const dx=p.x-e.x,dy=p.y-e.y,d=Math.hypot(dx,dy)||1;
      const range=e.type==='gnasher'?420:e.type==='ranged'?300:220;
      if(d<range){const w=(range-d)/range*2.2;rx+=dx/d*w;ry+=dy/d*w;}
    }
    for(const shot of game.shots){
      if(shot.kind!=='enemy')continue;
      const dx=p.x-shot.x,dy=p.y-shot.y,d=Math.hypot(dx,dy)||1;
      if(d<190){const w=(190-d)/190*1.8;rx+=dx/d*w;ry+=dy/d*w;}
      const vx=shot.vx||0,vy=shot.vy||0,v2=vx*vx+vy*vy;
      if(v2>1){
        const tm=(dx*vx+dy*vy)/v2;
        if(tm>.05&&tm<1.8){
          const cx=dx-vx*tm,cy=dy-vy*tm,miss=Math.hypot(cx,cy);
          if(miss<110){
            const speed=Math.sqrt(v2),px=-vy/speed,py=vx/speed;
            const danger=(x,y)=>game.enemies.reduce((sum,e)=>{
              if(e.dead||e.type==='boss')return sum;
              const q=Math.hypot(e.x-x,e.y-y);
              return sum+(q<230?(230-q)/230:0);
            },0);
            const side=danger(p.x+px*90,p.y+py*90)<=danger(p.x-px*90,p.y-py*90)?1:-1;
            const w=(110-miss)/110*2.8;
            rx+=px*side*w;ry+=py*side*w;
          }
        }
      }
    }
    for(const h of game.hazards){
      if(h.hit||!Number.isFinite(h.timer))continue;
      const dx=p.x-h.x,dy=p.y-h.y,d=Math.hypot(dx,dy)||1,range=(h.r||0)+p.r+110;
      if(d<range&&h.timer<1.2){const w=(range-d)/range*2;rx+=dx/d*w;ry+=dy/d*w;}
    }
    if(hpRatio<.30){rx*=1.55;ry*=1.55;}
    let mx=gx+rx*1.45,my=gy+ry*1.45;
    if(p.x>1150)mx-=1.5;if(p.x< -1150)mx+=1.5;
    if(p.y>850)my-=1.5;if(p.y< -850)my+=1.5;
    const mag=Math.hypot(mx,my)||1;mx/=mag;my/=mag;
    keys={KeyD:mx>.22,KeyA:mx<-.22,KeyS:my>.22,KeyW:my<-.22};
    const chest=game.chests.find(c=>!c.open&&Math.hypot(c.x-p.x,c.y-p.y)<70);
    if(chest){interact();interactions++;}
    update(dt);
    elapsed+=dt;ticks++;
    if(ticks%100===0)await new Promise(r=>setTimeout(r,0));
  }
  keys={};
  return {
    seed,screen,ended:game.ended,time:game.time,kills:game.player.kills,level:game.player.level,
    hp:game.player.hp,maxHp:game.player.maxHp,xp:game.player.xp,nextXp:game.player.nextXp,upgrades,
    objectives:game.player.objectives,enemyCount:game.enemies.filter(e=>!e.dead).length,
    dodgeStats:{projectiles:game.shots.length,damageEvents:window.__normalDamageEvents.length},
    damageEvents:window.__normalDamageEvents.slice(-25)
  };
};
"""
DOCUMENT = SOURCE.replace(MARKER, PROBE + "\n" + MARKER)

async def main():
    report={"checks":{},"trials":[],"page_errors":[],"console_errors":[],"external_requests":[]}
    candidates=[20261117,20261118,20261119,20261120,20261121,20261122]
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
        winner=None
        for seed in candidates:
            page=await browser.new_page(viewport={"width":1280,"height":800})
            errors=[];console=[];requests=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            page.on("console",lambda m:console.append(m.text) if m.type=="error" else None)
            page.on("request",lambda r:requests.append(r.url) if r.url.startswith(("http://","https://")) else None)
            await page.set_content(DOCUMENT,wait_until="load")
            await page.evaluate("(seed)=>window.__setRunSeed(seed)",seed)
            await page.locator("#start").click()
            state=await page.evaluate("([seconds,seed])=>window.__normalPlay(seconds,seed)",[90,seed])
            trial={"seed":seed,"state":state,"pageErrors":errors,"consoleErrors":console,"externalRequests":requests}
            report["trials"].append(trial)
            report["page_errors"].extend(errors)
            report["console_errors"].extend(console)
            report["external_requests"].extend(requests)
            if state["upgrades"]>0 and state["level"]>1 and state["screen"]=="playing" and not state["ended"]:
                winner=trial
                await page.close()
                break
            await page.close()
        await browser.close()
    report["seed"]=winner["seed"] if winner else None
    report["state"]=winner["state"] if winner else (report["trials"][-1]["state"] if report["trials"] else {})
    checks=[t["state"] for t in report["trials"]]
    report["checks"]["natural_time_advanced"]=bool(checks) and all(x["time"]>=89 for x in checks)
    report["checks"]["normal_combat_kills"]=bool(checks) and all(x["kills"]>0 for x in checks)
    report["checks"]["player_survived_smoke"]=bool(checks) and all(x["hp"]>0 and x["hp"]<=x["maxHp"] for x in checks)
    report["checks"]["real_upgrade_flow_used"]=winner is not None
    report["checks"]["no_ended_or_failed_screen"]=winner is not None and winner["state"]["screen"]=="playing" and not winner["state"]["ended"]
    report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
    report["checks"]["offline_no_external_requests"]=not report["external_requests"]
    report["pass"]=all(report["checks"].values())
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report["pass"]:raise SystemExit(1)

if __name__=="__main__":
    asyncio.run(main())
