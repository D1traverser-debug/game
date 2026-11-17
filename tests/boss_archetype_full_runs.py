"""Seeded, non-cheating full mission wins for each natural boss archetype.

Each run uses a fresh browser context and deterministic Math.random seed.
The test does not select a boss directly or mutate game state. It supplies only
normal movement, ordinary interaction, and choices from actual upgrade offers.
"""
import asyncio
import json
import sys
from playwright.async_api import async_playwright
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
MARKER="// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER)==1

PROBE=r"""
// Diagnostic instrumentation exists only in this temporary browser document.
// It records incoming damage without changing the production damage pipeline.
window.__damageEvents=[];
window.__pilotDodgeStats={projectile:0,gnasher:0,hazard:0,boundary:0,rift:0};
const __baseDamagePlayer=damagePlayer;
damagePlayer=function(n,source='enemy'){
  const p=game?.player,o=game?.objective;
  const gnasher=(game?.enemies||[]).filter(e=>!e.dead&&e.type==='gnasher')
    .map(e=>({e,d:p?Math.hypot(e.x-p.x,e.y-p.y):9999})).sort((a,b)=>a.d-b.d)[0];
  window.__damageEvents.push({
    t:+(game?.time||0).toFixed(1),source,amount:+Number(n).toFixed(1),
    hpBefore:p?+p.hp.toFixed(1):null,x:p?+p.x.toFixed(1):null,y:p?+p.y.toFixed(1):null,
    objective:o?.type||null,objectiveProgress:o?.progress||0,
    nearestGnasher:gnasher?{state:gnasher.e.state,distance:+gnasher.d.toFixed(1),x:+gnasher.e.x.toFixed(1),y:+gnasher.e.y.toFixed(1)}:null
  });
  return __baseDamagePlayer(n,source);
};
window.__setRunSeed=(seed)=>{
  let state=seed>>>0;
  Math.random=()=>{
    state=(Math.imul(1664525,state)+1013904223)>>>0;
    return state/4294967296;
  };
};

window.__fullRun = async (maxSeconds) => {
  const dt=0.1;
  let elapsed=0,ticks=0,upgrades=0,interactions=0,lastTrace=0,upgradeLog=[];
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
  const choose=(opts,p)=>{
    const newSpell=opts.find(x=>x.kind==='newSpell');
    if(newSpell)return newSpell;
    // Scroll options expose Chinese display names, not the internal IDs.
    // Rank the actual displayed cards so a mislabeled comparison cannot silently
    // turn every scroll into an arbitrary first-card choice.
    const scrollPriority={
      '健康成长':0,'壁垒':1,'厚皮':2,'闪避疗愈':3,'致命回响':4,
      '魔力虹吸':5,'魔力汲取':6,'目标馈赠':7,'炼金过载':8,
      '战或逃':9,'血速':10,'严酷教训':11,'延迟命运':12,
      '静心调谐':13,'灵药恒存':14
    };
    const scroll=opts.filter(x=>x.kind==='scroll')
      .sort((a,b)=>(scrollPriority[a.name]??99)-(scrollPriority[b.name]??99))[0];
    if(scroll)return scroll;
    const defensivePriority={maxHp:0,regen:1,armor:2,dodge:3};
    const defensive=opts.filter(x=>x.kind==='stat'&&Object.prototype.hasOwnProperty.call(defensivePriority,x.k))
      .sort((a,b)=>defensivePriority[a.k]-defensivePriority[b.k]);
    const hpRatio=p.hp/Math.max(1,p.maxHp);
    // Defense is selected whenever offered; spell upgrades are next priority.
    if(defensive.length)return defensive[0];
    const augPriority=['healingSprout','quakeBurst','diceTwin','diceEcho','sawTwin','sawReturn','orbSplit','orbBurst','quakeAfter','quakePull','sawMagnet','seeking','surge','tempo','reach'];
    const aug=opts.filter(x=>x.kind==='spellAugment')
      .sort((a,b)=>{const ai=augPriority.indexOf(a.aug),bi=augPriority.indexOf(b.aug);return (ai<0?999:ai)-(bi<0?999:bi)})[0];
    if(aug)return aug;
    const bonus=opts.find(x=>x.kind==='spellLevelBonus'&&x.mode==='damage')||opts.find(x=>x.kind==='spellLevelBonus');
    if(bonus)return bonus;
    const infusion=opts.find(x=>x.kind==='infuse');
    if(infusion)return infusion;
    const level=opts.filter(x=>x.kind==='spellLevel').sort((a,b)=>a.spell.level-b.spell.level)[0];
    if(level)return level;
    if(defensive.length)return defensive[0];
    // Spell levels and augmentations outrank marginal economy/mobility stats.
    const statPriority={damage:0,cast:1,crit:2,critDmg:3,spellSize:4,speed:5,manaGain:6,manaPull:7,luck:8};
    const stat=opts.filter(x=>x.kind==='stat')
      .sort((a,b)=>(statPriority[a.k]??99)-(statPriority[b.k]??99))[0];
    if(stat)return stat;
    return opts[0];
  };
  while(elapsed<maxSeconds&&!game.ended&&(screen==='playing'||screen==='upgrade')){
    if(screen==='upgrade'){
      const opts=game.pending?.opts||[];
      if(!opts.length)break;
      // Spend only a real free reroll when health is critical and the current
      // offers contain neither sustain nor a meaningful spell upgrade. Never pay HP.
      const hpRatio=game.player.hp/Math.max(1,game.player.maxHp);
      const hasDefensive=opts.some(x=>x.kind==='stat'&&['regen','armor','dodge','maxHp'].includes(x.k));
      const hasStrongUpgrade=opts.some(x=>['newSpell','spellAugment','spellLevelBonus','spellLevel','infuse'].includes(x.kind));
      const hasSustainScroll=opts.some(x=>x.kind==='scroll'&&['健康成长','壁垒','厚皮','闪避疗愈','致命回响','魔力虹吸','魔力汲取','目标馈赠'].includes(x.name));
      if(hpRatio<.62&&!hasDefensive&&!hasStrongUpgrade&&!hasSustainScroll&&game.player.rerolls>0){$('reroll').click();continue;}
      // Only choose from real cards currently offered by the production game.
      const rerollsBefore=game.player.rerolls||0;
      const choice=choose(opts,game.player);
      upgradeLog.push({t:+game.time.toFixed(1),rerollsBefore,offered:opts.map(x=>({kind:x.kind,k:x.k,name:x.name,aug:x.aug,spell:x.spell?.id,title:x.title,rarity:x.rarity})),selected:{kind:choice.kind,k:choice.k,name:choice.name,aug:choice.aug,spell:choice.spell?.id},rerollsAfter:game.player.rerolls||0});
      applyUpgrade(choice);upgrades++;continue;
    }
    const p=game.player;
    let target=null,goalX=0,goalY=0,activeObjective=null;
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
      activeObjective=o;
      if(o)target=objectiveTarget(o,p);
      if(!target){
        const chest=nearest(game.chests.filter(c=>!c.open),p);
        if(chest&&chest.d<780)target=chest.o;
      }
      // Health pickups are real drops and must be considered by the pilot.
      const health=nearest(game.orbs.filter(x=>x.type==='health'&&Math.abs(x.x)<1120&&Math.abs(x.y)<820),p);
      if(health&&p.hp<p.maxHp-5&&health.d<(p.hp<45?700:p.hp<75?420:0))target=health.o;
      if(!target){
        const magnet=nearest(game.orbs.filter(x=>x.type==='magnet'&&Math.abs(x.x)<1120&&Math.abs(x.y)<820),p);
        if(magnet&&magnet.d<260)target=magnet.o;
      }
      if(!target){
        const orb=nearest(game.orbs.filter(x=>x.type==='xp'&&Math.abs(x.x)<1120&&Math.abs(x.y)<820),p);
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
    // Gnasher's burrow is faster than the player: combine retreat with a
    // lateral sidestep. During leap, use the visible enemy position and keep
    // moving sideways; do not rely on its hidden target coordinate.
    for(const e of game.enemies){
      if(e.dead||e.type!=='gnasher')continue;
      const side=(Number(e.id||0)%2===0)?1:-1;
      if(e.state==='burrow'){
        const dx=p.x-e.x,dy=p.y-e.y,d=Math.hypot(dx,dy)||1;
        if(d<390){
          const nx=dx/d,ny=dy/d,w=(390-d)/390*3.8;
          rx+=nx*w*.65-ny*side*w*1.9;ry+=ny*w*.65+nx*side*w*1.9;
          window.__pilotDodgeStats.gnasher++;
        }
      }else if(e.state==='leap'){
        let dx=p.x-e.x,dy=p.y-e.y,d=Math.hypot(dx,dy);
        if(d<1){const a=side*Math.PI/2;dx=Math.cos(a);dy=Math.sin(a);d=1;}
        if(d<230){
          const nx=dx/d,ny=dy/d,w=(230-d)/230*4.4;
          rx+=nx*w*.55-ny*side*w*2.1;ry+=ny*w*.55+nx*side*w*2.1;
          window.__pilotDodgeStats.gnasher++;
        }
      }
    }
    for(const shot of game.shots){
      if(shot.kind!=='enemy')continue;
      const dx=p.x-shot.x,dy=p.y-shot.y,d=Math.hypot(dx,dy)||1;
      if(d<190){const w=(190-d)/190*1.7;rx+=dx/d*w;ry+=dy/d*w;}
      // Predict the closest approach of a live projectile and sidestep its path.
      const vx=shot.vx||0,vy=shot.vy||0,v2=vx*vx+vy*vy;
      if(v2>1){
        // r = player - projectile; r(t) = r - velocity*t.
        // Positive dot(r, velocity) means the projectile is approaching.
        const t=(dx*vx+dy*vy)/v2;
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
            rx+=px*side*w;ry+=py*side*w;window.__pilotDodgeStats.projectile++;
          }
        }
      }
    }
    for(const h of game.hazards){
      if(h.hit||!['warning','runestone','krogLeap','krogAcid','meteor','bell','bomb','slam','dice','explosiveSprout','explosiveMushroom'].includes(h.kind))continue;
      const dx=p.x-h.x,dy=p.y-h.y,d=Math.hypot(dx,dy)||1,range=(h.r||0)+95;
      if(d<range){const w=(range-d)/range*2;rx+=dx/d*w;ry+=dy/d*w;window.__pilotDodgeStats.hazard++;}
    }
    const riftDist=target?Math.hypot(p.x-target.x,p.y-target.y):Infinity;
    const riftRadius=activeObjective?.variant==='multi'?55:92;
    const riftHold=activeObjective?.type==='rift'&&target&&riftDist<riftRadius;
    if(riftHold&&riftDist>1){
      // Keep the capture position while allowing tangential dodges; remove
      // only the outward radial component that would reset Rift progress.
      const nx=(p.x-target.x)/riftDist,ny=(p.y-target.y)/riftDist;
      const outward=rx*nx+ry*ny;
      if(outward>0){rx-=nx*outward;ry-=ny*outward;}
      window.__pilotDodgeStats.rift++;
    }
    let evade=Math.max(0,Math.min(2.4,(255-minThreat)/110))*(riftHold?.32:1);
    if(p.hp/Math.max(1,p.maxHp)<.30&&minThreat<200){
      const threat=nearest(game.enemies.filter(e=>!e.dead&&e.type!=='boss'),p);
      if(threat){goalX=(p.x-threat.o.x)/(threat.d||1);goalY=(p.y-threat.o.y)/(threat.d||1);}
      evade=Math.max(evade,1.8);
    }
    goalX+=rx*evade;goalY+=ry*evade;
    // Hard inward steering prevents a target or a summed avoidance vector
    // from pinning the pilot against the clamped world boundary.
    if(p.x>980){goalX=Math.min(goalX,-.9);window.__pilotDodgeStats.boundary++;}
    if(p.x< -980){goalX=Math.max(goalX,.9);window.__pilotDodgeStats.boundary++;}
    if(p.y>720){goalY=Math.min(goalY,-.9);window.__pilotDodgeStats.boundary++;}
    if(p.y< -720){goalY=Math.max(goalY,.9);window.__pilotDodgeStats.boundary++;}
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
    if(game.time-lastTrace>=15){
      const q=game.player,near=nearest(game.enemies.filter(e=>!e.dead),q);
      trace.push({t:+game.time.toFixed(1),hp:+q.hp.toFixed(1),maxHp:q.maxHp,level:q.level,
        kills:q.kills,damageTaken:+q.damageTaken.toFixed(1),armor:+q.armor.toFixed(1),
        regen:+q.regen.toFixed(1),damage:+q.damage.toFixed(2),cast:+q.cast.toFixed(2),crit:+q.crit.toFixed(2),
        spellCount:q.spells.length,enemyCount:game.enemies.filter(e=>!e.dead).length,
        nearestEnemy:near?+near.d.toFixed(1):null,
        position:{x:+q.x.toFixed(1),y:+q.y.toFixed(1)},
        target:target?{kind:target.type||target.kind||'objective',x:+target.x.toFixed(1),y:+target.y.toFixed(1)}:null,
        edgeDistance:Math.min(1200-Math.abs(q.x),900-Math.abs(q.y)),
        healthOrbs:game.orbs.filter(x=>x.type==='health').length,magnetOrbs:game.orbs.filter(x=>x.type==='magnet').length,objective:game.objective?.type||null,
        objectiveProgress:game.objective?.progress||0,objectiveTarget:game.objective?.target||0,
        objectiveDone:!!game.objective?.done,objectiveVariant:game.objective?.variant||null,
        objectiveTime:game.objective?+game.objective.time.toFixed(1):null,
        rerolls:q.rerolls,scrolls:q.scrolls.slice(),invuln:+q.invuln.toFixed(2),
        spells:q.spells.map(x=>({id:x.id,level:x.level,augments:x.augments.slice(),infusions:x.infusions.slice()}))});
      lastTrace=game.time;
    }
    if(ticks%100===0)await new Promise(r=>setTimeout(r,0));
  }
  keys={};
  const p=game.player,b=game.boss;
  return {
    screen,ended:game.ended,elapsed,gameTime:game.time,kills:p.kills,level:p.level,
    hp:p.hp,maxHp:p.maxHp,damageTaken:p.damageTaken,armor:p.armor,regen:p.regen,
    objectives:p.objectives,upgrades,interactions,upgradeLog,
    spells:p.spells.map(x=>({id:x.id,level:x.level,augments:x.augments.slice(),infusions:x.infusions.slice()})),
    scrolls:p.scrolls.slice(),rerolls:p.rerolls,
    position:{x:+p.x.toFixed(1),y:+p.y.toFixed(1)},
    damageEvents:window.__damageEvents.slice(-80),
    pilotDodgeStats:{...window.__pilotDodgeStats},
    trialSpellId:save.trialSpellId||null,
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
  seeds=[int(x) for x in sys.argv[1:]] or [1,2,3]
  report={"runs":[],"checks":{}}
  async with async_playwright() as p:
    browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for seed in seeds:
      context=await browser.new_context(viewport={"width":1280,"height":800})
      page=await context.new_page()
      errors=[];console=[];requests=[]
      page.on("pageerror",lambda e:errors.append(str(e)))
      page.on("console",lambda m:console.append(m.text) if m.type=="error" else None)
      page.on("request",lambda r:requests.append(r.url) if r.url.startswith(("http://","https://")) else None)
      page.set_default_timeout(180000)
      await page.set_content(DOCUMENT,wait_until="load")
      await page.evaluate("(seed)=>window.__setRunSeed(seed)",seed)
# Baseline natural mission: use the default Reginald loadout, without a temporary trial.
      await page.locator("#start").click()
      state=await asyncio.wait_for(page.evaluate("window.__fullRun(1500)"),timeout=180)
      item={"seed":seed,"boss":state["bossId"],"natural_win":bool(state["bossDead"] and state["ended"] and state["screen"]=="result" and state["wins"]>=1),"state":state,"page_errors":errors,"console_errors":console,"external_requests":requests}
      report["runs"].append(item)
      await context.close()
    await browser.close()
  bosses=[x["boss"] for x in report["runs"]]
  report["checks"]={
    "all_seeded_runs_natural_wins":bool(report["runs"]) and all(x["natural_win"] for x in report["runs"]),
    "boss_ids_recorded":bool(bosses) and all(x in {"sol","krog","mul"} for x in bosses),
    "seed_count_at_least_three":len(seeds)>=3,
    "all_three_boss_archetypes_covered":len(seeds)>=3 and set(bosses)=={"sol","krog","mul"},
    "no_browser_errors":all(not x["page_errors"] and not x["console_errors"] for x in report["runs"]),
    "offline_no_external_requests":all(not x["external_requests"] for x in report["runs"])
  }
  report["boss_ids"]=sorted(set(x for x in bosses if x))
  report["pass"]=all(report["checks"].values())
  print(json.dumps(report,ensure_ascii=False,indent=2))
  if not report["pass"]:raise SystemExit(1)

if __name__=="__main__":
  asyncio.run(main())
