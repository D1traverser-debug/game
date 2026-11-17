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
  let elapsed=0,ticks=0,upgrades=0,interactions=0,lastTrace=0;
  const trace=[];
  const nearest=(items,p)=>items.filter(x=>x&&x.alive!==false)
    .map(o=>({o,d:Math.hypot(o.x-p.x,o.y-p.y)}))
    .sort((a,b)=>a.d-b.d)[0];
  const objectiveTarget=(o,p)=>{
    if(!o||o.done)return null;
    if(o.type==='crab'&&o.crab?.alive)return o.crab;
    if(o.type==='rift'&&o.nodes?.length){
      const n=nearest(o.nodes.filter(x=>x.progress<100),p);return n?.o||o;
    }
    if(o.type==='cores'&&o.variant==='heavy'){
      if(game.carriedCore)return o;
      return nearest(o.objects||[],p)?.o||o;
    }
    if(o.type==='brazier'){
      const wanted=o.variant==='sequence'?o.sequence?.[o.sequenceIndex]:null;
      const arr=(o.objects||[]).filter(x=>x.alive&&(wanted===null||wanted===undefined||x.index===wanted));
      return nearest(arr,p)?.o||o;
    }
    if(o.type==='beasts'){
      if(o.variant==='devoted')return o;
      const beast=nearest(o.objects||[],p)?.o;if(!beast)return o;
      const dx=beast.x-o.x,dy=beast.y-o.y,d=Math.hypot(dx,dy)||1;
      return {x:beast.x+dx/d*125,y:beast.y+dy/d*125};
    }
    if(o.objects?.length)return nearest(o.objects,p)?.o||o;
    return o;
  };
  const choose=(opts)=>{
    const scrollPriority=['growth','thick','bulwark','evasion','fight','blood','go','mana','vital','elixir','hard','attune','siphon'];
    const scroll=opts.filter(x=>x.kind==='scroll').sort((a,b)=>scrollPriority.indexOf(a.name)-scrollPriority.indexOf(b.name))[0];
    if(scroll)return scroll;
    const newSpell=opts.find(x=>x.kind==='newSpell');
    if(newSpell)return newSpell;
    // A competent solo build secures sustain first, then layers spell damage.
    const statPriority=['regen','armor','dodge','maxHp','speed','damage','cast','crit','critDmg','spellSize','manaPull','manaGain','luck'];
    const stat=opts.filter(x=>x.kind==='stat').sort((a,b)=>statPriority.indexOf(a.k)-statPriority.indexOf(b.k))[0];
    if(stat)return stat;
    const augPriority=['healingSprout','quakeBurst','diceTwin','diceEcho','sawTwin','sawReturn','orbSplit','orbBurst','quakeAfter','quakePull','sawMagnet','seeking','surge','tempo','reach'];
    const aug=opts.filter(x=>x.kind==='spellAugment').sort((a,b)=>augPriority.indexOf(a.aug)-augPriority.indexOf(b.aug))[0];
    if(aug)return aug;
    const bonus=opts.find(x=>x.kind==='spellLevelBonus'&&x.mode==='damage')||opts.find(x=>x.kind==='spellLevelBonus');
    if(bonus)return bonus;
    const infusion=opts.find(x=>x.kind==='infuse');
    if(infusion)return infusion;
    const level=opts.filter(x=>x.kind==='spellLevel').sort((a,b)=>a.spell.level-b.spell.level)[0];
    return level||opts[0];
  };
  while(elapsed<maxSeconds&&!game.ended&&(screen==='playing'||screen==='upgrade')){
    if(screen==='upgrade'){
      const opts=game.pending?.opts||[];
      if(!opts.length)break;
      // Only choose from real cards currently offered by the production game.
      applyUpgrade(choose(opts));upgrades++;continue;
    }
    const p=game.player;
    let target=null,goalX=0,goalY=0;
    const b=game.boss&&!game.boss.dead?game.boss:null;
    if(b){
      // Mul'gath's healing servants are a priority target: official patch notes
      // state they heal Mul'gath and can be corrupted to damage him on collision.
      const healer=b.bossId==='mul'?nearest(game.enemies.filter(e=>e.bossHealer),p):null;
      if(healer){
        const dx=healer.o.x-p.x,dy=healer.o.y-p.y,d=Math.hypot(dx,dy)||1;
        if(d>92){goalX=dx/d;goalY=dy/d;}
        else{goalX=-dy/d;goalY=dx/d;}
      }else{
        const dx=b.x-p.x,dy=b.y-p.y,d=Math.hypot(dx,dy)||1;
        if(d>315){goalX=dx/d;goalY=dy/d;}
        else if(d<225){goalX=-dx/d;goalY=-dy/d;}
        else{goalX=-dy/d;goalY=dx/d;}
      }
    }else{
      const o=game.objective&&!game.objective.done?game.objective:null;
      if(o)target=objectiveTarget(o,p);
      if(!target){
        const chest=nearest(game.chests.filter(c=>!c.open),p);
        if(chest&&chest.d<780)target=chest.o;
      }
      // Health pickups are real drops and must be considered by the pilot.
      const health=nearest(game.orbs.filter(x=>x.type==='health'),p);
      if(health&&p.hp<p.maxHp-5&&health.d<(p.hp<45?700:p.hp<75?420:0))target=health.o;
      if(!target){
        const magnet=nearest(game.orbs.filter(x=>x.type==='magnet'),p);
        if(magnet&&magnet.d<260)target=magnet.o;
      }
      if(!target){
        const orb=nearest(game.orbs.filter(x=>x.type==='xp'),p);
        if(orb&&orb.d<850)target=orb.o;
      }
      if(target){
        const dx=target.x-p.x,dy=target.y-p.y,d=Math.hypot(dx,dy)||1;
        if(d>28){goalX=dx/d;goalY=dy/d;}
      }else{
        const a=Math.floor(elapsed/8)*Math.PI/2;
        goalX=Math.cos(a);goalY=Math.sin(a);
      }
    }
    // Avoid nearby enemies and incoming enemy projectiles instead of blindly
    // walking through the crowd to an XP orb. This changes input only.
    let rx=0,ry=0,minThreat=9999;
    for(const e of game.enemies){
      if(e.dead||e.type==='boss'||(e.bossHealer&&game.boss?.bossId==='mul'))continue;
      const dx=e.x-p.x,dy=e.y-p.y,d=Math.hypot(dx,dy)||1;
      minThreat=Math.min(minThreat,d);
      if(d<255){
        const w=((255-d)/255)**1.35*(e.type==='ranged'?1.25:1);
        rx-=dx/d*w;ry-=dy/d*w;
      }
    }
    for(const shot of game.shots){
      if(shot.kind!=='enemy')continue;
      const dx=p.x-shot.x,dy=p.y-shot.y,d=Math.hypot(dx,dy)||1;
      if(d<190){const w=(190-d)/190*1.7;rx+=dx/d*w;ry+=dy/d*w;}
      // Predict the closest approach of a live projectile and sidestep its path.
      const vx=shot.vx||0,vy=shot.vy||0,v2=vx*vx+vy*vy;
      if(v2>1){
        const t=-(dx*vx+dy*vy)/v2;
        if(t>0&&t<1.35){
          const cx=dx-vx*t,cy=dy-vy*t,cd=Math.hypot(cx,cy);
          if(cd<92){
            const speed=Math.sqrt(v2),px=-vy/speed,py=vx/speed;
            const danger=(x,y)=>game.enemies.reduce((sum,e)=>{
              if(e.dead||e.type==='boss')return sum;
              const q=Math.hypot(e.x-x,e.y-y);
              return sum+(q<230?(230-q)/230:0);
            },0);
            const side=danger(p.x+px*90,p.y+py*90)<=danger(p.x-px*90,p.y-py*90)?1:-1;
            const w=(92-cd)/92*2.5;
            rx+=px*side*w;ry+=py*side*w;
          }
        }
      }
    }
    for(const h of game.hazards){
      if(h.hit||!['warning','runestone','krogLeap','krogAcid'].includes(h.kind))continue;
      const dx=p.x-h.x,dy=p.y-h.y,d=Math.hypot(dx,dy)||1,range=(h.r||0)+95;
      if(d<range){const w=(range-d)/range*2;rx+=dx/d*w;ry+=dy/d*w;}
    }
    const evade=Math.max(0,Math.min(2.4,(255-minThreat)/110));
    goalX+=rx*evade;goalY+=ry*evade;
    // Do not let the pilot pin itself against the map boundary.
    if(p.x>1010)goalX-=1.2;if(p.x< -1010)goalX+=1.2;
    if(p.y>735)goalY-=1.2;if(p.y< -735)goalY+=1.2;
    const mag=Math.hypot(goalX,goalY)||1;goalX/=mag;goalY/=mag;
    keys={KeyD:goalX>.22,KeyA:goalX<-.22,KeyS:goalY>.22,KeyW:goalY<-.22};
    const chestNear=game.chests.some(c=>!c.open&&Math.hypot(c.x-p.x,c.y-p.y)<74);
    const o=game.objective&&!game.objective.done?game.objective:null;
    let itemNear=false;
    if(o?.type==='cores'&&o.variant==='heavy'&&!game.carriedCore)
      itemNear=(o.objects||[]).some(x=>x.alive&&Math.hypot(x.x-p.x,x.y-p.y)<72);
    if(o?.type==='brazier'){
      const wanted=o.variant==='sequence'?o.sequence?.[o.sequenceIndex]:null;
      itemNear=(o.objects||[]).some(x=>x.alive&&(wanted===null||wanted===undefined||x.index===wanted)&&Math.hypot(x.x-p.x,x.y-p.y)<80);
    }
    if(chestNear||itemNear){interact();interactions++;}
    update(dt);elapsed+=dt;ticks++;
    if(game.time-lastTrace>=30){
      const q=game.player,near=nearest(game.enemies.filter(e=>!e.dead),q);
      trace.push({t:+game.time.toFixed(1),hp:+q.hp.toFixed(1),maxHp:q.maxHp,level:q.level,
        kills:q.kills,damageTaken:+q.damageTaken.toFixed(1),armor:+q.armor.toFixed(1),
        regen:+q.regen.toFixed(1),damage:+q.damage.toFixed(2),cast:+q.cast.toFixed(2),crit:+q.crit.toFixed(2),
        spellCount:q.spells.length,enemyCount:game.enemies.filter(e=>!e.dead).length,
        nearestEnemy:near?+near.d.toFixed(1):null,healthOrbs:game.orbs.filter(x=>x.type==='health').length,magnetOrbs:game.orbs.filter(x=>x.type==='magnet').length,objective:game.objective?.type||null,
        objectiveProgress:game.objective?.progress||0,spells:q.spells.map(x=>({id:x.id,level:x.level,augments:x.augments.slice(),infusions:x.infusions.slice()}))});
      lastTrace=game.time;
    }
    if(ticks%100===0)await new Promise(r=>setTimeout(r,0));
  }
  keys={};
  const p=game.player,b=game.boss;
  return {
    screen,ended:game.ended,elapsed,gameTime:game.time,kills:p.kills,level:p.level,
    hp:p.hp,maxHp:p.maxHp,damageTaken:p.damageTaken,armor:p.armor,regen:p.regen,
    objectives:p.objectives,upgrades,interactions,
    spells:p.spells.map(x=>({id:x.id,level:x.level,augments:x.augments.slice(),infusions:x.infusions.slice()})),
    objective:game.objective?.type||null,
    bossSpawned:!!b,bossId:b?.bossId||null,bossHp:b?.hp??null,bossMax:b?.max??null,
    bossDead:!!b?.dead,wins:save.wins||0,losses:save.runs-(save.wins||0),
    enemyCount:game.enemies.filter(e=>!e.dead).length,trace,
    errors:p.hp<0||!Number.isFinite(p.hp)||!Number.isFinite(game.time)
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
        page.set_default_timeout(180000)
        await page.set_content(DOCUMENT,wait_until="load")
        await page.locator("#start").click()
        state=await asyncio.wait_for(page.evaluate("window.__fullRun(1500)"),timeout=180)
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
