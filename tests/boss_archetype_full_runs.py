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
window.__contactSource=null;
window.__gnasherHits=[];
window.__gnasherLeapSamples=[];
window.__pilotDodgeStats={projectile:0,gnasher:0,gnasherBurrow:0,gnasherLeap:0,gnasherLeapSafeFrames:0,hazard:0,boundary:0,rift:0,criticalEscape:0};
window.__pilotHeading={x:0,y:0};
// The production RAF loop may render, but must neither advance simulation nor consume its RNG.
// drawWorld screen shake previously consumed the same rand() stream used by spawns and upgrades.
window.__simulationHarness={manualTicks:0,blockedFrameUpdates:0,renderRandomCalls:0};
window.__manualTick=false;
window.__renderPhase=false;
const __uncontrolledUpdate=update;
update=function(dt){
  if(window.__manualTick){window.__simulationHarness.manualTicks++;return __uncontrolledUpdate(dt);}
  window.__simulationHarness.blockedFrameUpdates++;
};
const __baseDamagePlayer=damagePlayer;
damagePlayer=function(n,source='enemy'){
  const p=game?.player,o=game?.objective;
  const nearGnashers=(game?.enemies||[]).filter(e=>!e.dead&&e.type==='gnasher')
    .map(e=>({e,d:p?Math.hypot(e.x-p.x,e.y-p.y):9999})).filter(x=>x.d<240).sort((a,b)=>a.d-b.d);
  const gnasher=nearGnashers[0];
  const nearestProjectile=(game?.shots||[]).filter(s=>s.kind==='enemy').map(s=>{
    const dx=(p?.x||0)-s.x,dy=(p?.y||0)-s.y,vx=s.vx||0,vy=s.vy||0,v2=vx*vx+vy*vy;
    const t=v2>1?(dx*vx+dy*vy)/v2:0;
    const miss=v2>1&&t>0?Math.hypot(dx-vx*t,dy-vy*t):Math.hypot(dx,dy);
    return {t:+t.toFixed(2),miss:+miss.toFixed(1),distance:+Math.hypot(dx,dy).toFixed(1),vx:+vx.toFixed(1),vy:+vy.toFixed(1),damage:s.dmg,sourceType:s.sourceType||null,sourceId:s.sourceId||null,sourceDamage:s.sourceDamage??null};
  }).sort((a,b)=>a.miss-b.miss)[0];
  window.__damageEvents.push({
    t:+(game?.time||0).toFixed(1),source,amount:+Number(n).toFixed(1),
    hpBefore:p?+p.hp.toFixed(1):null,x:p?+p.x.toFixed(1):null,y:p?+p.y.toFixed(1):null,
    objective:o?.type||null,objectiveProgress:o?.progress||0,
    playerMove:p?+p.move.toFixed(1):null,lastMove:p?+p.lastMove.toFixed(2):null,
    facing:p?+p.facing.toFixed(2):null,invuln:p?+p.invuln.toFixed(2):null,carriedCore:!!game?.carriedCore?.alive,moveSpeed:p?+p.move.toFixed(1):null,
    nearestGnasher:gnasher?{state:gnasher.e.state,stateT:+(gnasher.e.stateT||0).toFixed(2),distance:+gnasher.d.toFixed(1),x:+gnasher.e.x.toFixed(1),y:+gnasher.e.y.toFixed(1),leapX:Number.isFinite(gnasher.e.leapX)?+gnasher.e.leapX.toFixed(1):null,leapY:Number.isFinite(gnasher.e.leapY)?+gnasher.e.leapY.toFixed(1):null,dmg:+gnasher.e.dmg.toFixed(1)}:null,
    nearbyGnashers:nearGnashers.slice(0,6).map(x=>({state:x.e.state,stateT:+(x.e.stateT||0).toFixed(2),distance:+x.d.toFixed(1),x:+x.e.x.toFixed(1),y:+x.e.y.toFixed(1),leapX:Number.isFinite(x.e.leapX)?+x.e.leapX.toFixed(1):null,leapY:Number.isFinite(x.e.leapY)?+x.e.leapY.toFixed(1):null,dmg:+x.e.dmg.toFixed(1)})),
    nearestProjectile:nearestProjectile||null,contactSource:source==='contact'?window.__contactSource:null
  });
  if(source==='contact')window.__contactSource=null;
  return __baseDamagePlayer(n,source);
};
window.__setRunSeed=(seed)=>{
  window.__simulationHarness={manualTicks:0,blockedFrameUpdates:0,renderRandomCalls:0};window.__manualTick=false;window.__renderPhase=false;window.__pilotHeading={x:0,y:0};window.__contactSource=null;joy.x=0;joy.y=0;joy.active=true;
  let state=seed>>>0;
  Math.random=()=>{
    if(window.__renderPhase)window.__simulationHarness.renderRandomCalls++;
    state=(Math.imul(1664525,state)+1013904223)>>>0;
    return state/4294967296;
  };
};

window.__fullRun = async (maxSeconds, stopAtBossSpawn=false) => {
  const dt=1/30,stepsPerDecision=1;
  const manualStart=window.__simulationHarness.manualTicks,blockedStart=window.__simulationHarness.blockedFrameUpdates;
  let elapsed=0,ticks=0,upgrades=0,interactions=0,lastTrace=0,lastYield=0,upgradeLog=[];
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
    const hpRatio=p.hp/Math.max(1,p.maxHp);
    // Preserve the level-13/20 spell-slot milestones, but do not build a glass cannon.
    // Defense targets are modest and are selected only while the corresponding stat is deficient.
    const defensivePriority={maxHp:0,armor:1,regen:2,dodge:3,speed:4};
    const defensive=opts.filter(x=>x.kind==='stat'&&Object.prototype.hasOwnProperty.call(defensivePriority,x.k))
      .sort((a,b)=>defensivePriority[a.k]-defensivePriority[b.k]);
    const defensiveNeed=defensive.filter(x=>
      (x.k==='maxHp'&&p.maxHp<300)||
      (x.k==='armor'&&p.armor<36)||
      (x.k==='regen'&&p.regen<2)||
      (x.k==='dodge'&&p.dodge<.12)||
      (x.k==='speed'&&p.move<205));
    const sustainNames=new Set(['健康成长','壁垒','厚皮','闪避疗愈','致命回响','魔力虹吸','魔力汲取','目标馈赠']);
    const scrollPriority={
      '健康成长':0,'壁垒':1,'厚皮':2,'闪避疗愈':3,'致命回响':4,
      '魔力虹吸':5,'魔力汲取':6,'目标馈赠':7,'炼金过载':8,
      '战或逃':9,'血速':10,'严酷教训':11,'延迟命运':12,
      '静心调谐':13,'灵药恒存':14
    };
    const scrolls=opts.filter(x=>x.kind==='scroll')
      .sort((a,b)=>(scrollPriority[a.name]??99)-(scrollPriority[b.name]??99));
    const sustainScroll=scrolls.find(x=>sustainNames.has(x.name));
    if(hpRatio<.45&&defensive.length)return defensive[0];
    const newSpell=opts.find(x=>x.kind==='newSpell');
    if(newSpell)return newSpell;
    if(hpRatio<.82&&sustainScroll)return sustainScroll;
    if(hpRatio<.62&&defensive.length)return defensive[0];
    if(defensiveNeed.length)return defensiveNeed[0];
    if(scrolls.length)return scrolls[0];
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
    const statPriority={damage:0,cast:1,crit:2,critDmg:3,spellSize:4,speed:5,manaGain:6,manaPull:7,luck:8};
    const stat=opts.filter(x=>x.kind==='stat')
      .sort((a,b)=>(statPriority[a.k]??99)-(statPriority[b.k]??99))[0];
    if(stat)return stat;
    if(defensive.length)return defensive[0];
    return opts[0];
  };
  while(elapsed<maxSeconds&&!game.ended&&(screen==='playing'||screen==='upgrade')&&!(stopAtBossSpawn&&game.boss&&!game.boss.dead)){
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
      upgradeLog.push({t:+game.time.toFixed(1),hpRatio:+(game.player.hp/Math.max(1,game.player.maxHp)).toFixed(3),rerollsBefore,offered:opts.map(x=>({kind:x.kind,k:x.k,name:x.name,aug:x.aug,spell:x.spell?.id,title:x.title,rarity:x.rarity})),selected:{kind:choice.kind,k:choice.k,name:choice.name,aug:choice.aug,spell:choice.spell?.id},rerollsAfter:game.player.rerolls||0});
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
      if(health&&p.hp<p.maxHp-5&&health.d<(p.hp<45?900:p.hp<75?650:p.hp<p.maxHp*.9?420:0))target=health.o;
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
    let rx=0,ry=0,projectileRx=0,projectileRy=0,hazardRx=0,hazardRy=0,minThreat=9999;
    for(const e of game.enemies){
      if(e.dead||e.type==='boss'||(e.bossHealer&&game.boss?.bossId==='mul'))continue;
      const dx=e.x-p.x,dy=e.y-p.y,d=Math.hypot(dx,dy)||1;
      minThreat=Math.min(minThreat,d);
      if(d<255){
        const w=((255-d)/255)**1.35*(e.type==='ranged'?1.25:1);
        rx-=dx/d*w;ry-=dy/d*w;
      }
    }
    // Score a fresh heading each frame against all active leap landing points.
    // A locked heading can become unusable when the player reaches a world edge.
    let gnasherThreat=false,gnasherEscapeX=0,gnasherEscapeY=0,gnasherMode=null,gnasherStateT=null;
    const activeGnashers=game.enemies.filter(e=>!e.dead&&e.type==='gnasher'&&(e.state==='burrow'||e.state==='leap'))
      .map(e=>({e,d:Math.hypot(e.x-p.x,e.y-p.y),landingD:e.state==='leap'?Math.hypot(p.x-(e.leapX??e.x),p.y-(e.leapY??e.y)):Infinity}))
      .sort((a,b)=>(a.e.state==='leap'?0:1)-(b.e.state==='leap'?0:1)||(a.e.stateT||0)-(b.e.stateT||0)||Math.min(a.d,a.landingD)-Math.min(b.d,b.landingD));
    const leapThreats=activeGnashers.filter(x=>x.e.state==='leap'&&Math.min(x.d,x.landingD)<500);
    const burrowThreats=activeGnashers.filter(x=>x.e.state==='burrow'&&x.d<600);
    const activeGnasher=leapThreats[0]||burrowThreats[0];
    if(activeGnasher){
      const e=activeGnasher.e,leaping=e.state==='leap';
      const tx=leaping?(e.leapX??e.x):p.x,ty=leaping?(e.leapY??e.y):p.y;
      const pathX=leaping?tx-e.x:p.x-e.x,pathY=leaping?ty-e.y:p.y-e.y,pathD=Math.hypot(pathX,pathY)||1;
      const lateralX=-pathY/pathD,lateralY=pathX/pathD;
      const awayD=Math.hypot(p.x-tx,p.y-ty)||1;
      const awayX=leaping?(p.x-tx)/awayD:lateralX,awayY=leaping?(p.y-ty)/awayD:lateralY;
      const enemyD=Math.hypot(p.x-e.x,p.y-e.y)||1;
      // During burrow the Gnasher tracks the wizard; create radial separation instead of orbiting it.
      const burrowAwayX=(p.x-e.x)/enemyD,burrowAwayY=(p.y-e.y)/enemyD;
      const preferredX=leaping?awayX*.78+lateralX*.22:burrowAwayX;
      const preferredY=leaping?awayY*.78+lateralY*.22:burrowAwayY;
      const moveSpeed=(p.move||220)*(game.carriedCore&&game.carriedCore.alive?.58:1)*
        (p.lowSpeed?1+(1-p.hp/Math.max(1,p.maxHp))*.21:1)*(p.fightT>0?1.3:1);
      const criticalHealth=p.hp/Math.max(1,p.maxHp)<.55;
      const hitTime=leaping?Math.max(.05,Math.min(.55,e.stateT||.55)):.55;
      const step=Math.max(20,moveSpeed*hitTime);
      let bestScore=-Infinity;
      for(let k=0;k<24;k++){
        const a=k*Math.PI/12,dx=Math.cos(a),dy=Math.sin(a);
        const nx=clamp(p.x+dx*step,-1200,1200),ny=clamp(p.y+dy*step,-900,900);
        const travel=Math.hypot(nx-p.x,ny-p.y);
        const landingDistance=leaping&&leapThreats.length
          ?Math.min(...leapThreats.map(x=>Math.hypot(nx-(x.e.leapX??x.e.x),ny-(x.e.leapY??x.e.y)))):0;
        let nearestEnemy=420;
        for(const other of game.enemies){
          if(other===e||other.dead||other.type==='boss')continue;
          nearestEnemy=Math.min(nearestEnemy,Math.hypot(other.x-nx,other.y-ny));
        }
        let hazardPenalty=0;
        for(const h of game.hazards){
          if(h.hit||!Number.isFinite(h.timer)||h.timer>1.4)continue;
          const hd=Math.hypot(nx-h.x,ny-h.y),hr=(h.r||0)+p.r+35;
          if(hd<hr)hazardPenalty+=(hr-hd)*.75;
        }
        let projectilePenalty=0;
        for(const shot of game.shots){
          if(shot.kind!=='enemy')continue;
          const sx=shot.x+(shot.vx||0)*.55,sy=shot.y+(shot.vy||0)*.55;
          const sd=Math.hypot(nx-sx,ny-sy),sr=(shot.r||6)+p.r+28;
          if(sd<sr)projectilePenalty+=(sr-sd)*.9;
        }
        const edgeClearance=Math.min(1200-Math.abs(nx),900-Math.abs(ny));
        const lateral=dx*preferredX+dy*preferredY;
        const score=(leaping?landingDistance*2.0:0)+travel*1.8+
          Math.min(nearestEnemy,420)*(criticalHealth?.38:.16)+Math.min(edgeClearance,350)*(criticalHealth?.42:.24)+
          lateral*(leaping?4:16)-hazardPenalty-projectilePenalty;
        if(score>bestScore){bestScore=score;gnasherEscapeX=dx;gnasherEscapeY=dy;}
      }
      gnasherThreat=true;gnasherMode=leaping?'leap':'burrow';gnasherStateT=+(e.stateT||0).toFixed(2);
      window.__pilotDodgeStats.gnasher++;
      if(leaping){
        window.__pilotDodgeStats.gnasherLeap++;
        if(activeGnasher.landingD>60)window.__pilotDodgeStats.gnasherLeapSafeFrames++;
        window.__gnasherLeapSamples.push({t:+game.time.toFixed(1),id:e.id,stateT:+(e.stateT||0).toFixed(2),
          playerX:+p.x.toFixed(1),playerY:+p.y.toFixed(1),targetX:+tx.toFixed(1),targetY:+ty.toFixed(1),
          distance:+activeGnasher.landingD.toFixed(1),escapeX:+gnasherEscapeX.toFixed(2),escapeY:+gnasherEscapeY.toFixed(2),
          edge:Math.min(1200-Math.abs(p.x),900-Math.abs(p.y))});
        if(window.__gnasherLeapSamples.length>400)window.__gnasherLeapSamples.shift();
      }else window.__pilotDodgeStats.gnasherBurrow++;
      target=null;
    }
    let imminentProjectile=false,imminentHazard=false;
    for(const shot of game.shots){
      if(shot.kind!=='enemy')continue;
      const dx=p.x-shot.x,dy=p.y-shot.y,d=Math.hypot(dx,dy)||1;
      if(d<190){const w=(190-d)/190*1.7;rx+=dx/d*w;ry+=dy/d*w;projectileRx+=dx/d*w;projectileRy+=dy/d*w;}
      // Predict the closest approach of a live projectile and sidestep its path.
      const vx=shot.vx||0,vy=shot.vy||0,v2=vx*vx+vy*vy;
      if(v2>1){
        // r = player - projectile; r(t) = r - velocity*t.
        // Positive dot(r, velocity) means the projectile is approaching.
        const t=(dx*vx+dy*vy)/v2;
        if(t>0&&t<2.4){
          const cx=dx-vx*t,cy=dy-vy*t,cd=Math.hypot(cx,cy);
          if(t>.05&&t<2.4&&cd<130)imminentProjectile=true;
          if(cd<130){
            const speed=Math.sqrt(v2),px=-vy/speed,py=vx/speed;
            const danger=(x,y)=>game.enemies.reduce((sum,e)=>{
              if(e.dead||e.type==='boss')return sum;
              const q=Math.hypot(e.x-x,e.y-y);
              return sum+(q<230?(230-q)/230:0);
            },0);
            const side=danger(p.x+px*90,p.y+py*90)<=danger(p.x-px*90,p.y-py*90)?1:-1;
            const w=(130-cd)/130*3.2;
            rx+=px*side*w;ry+=py*side*w;
            projectileRx+=px*side*w;projectileRy+=py*side*w;
            window.__pilotDodgeStats.projectile++;
          }
        }
      }
    }
    for(const h of game.hazards){
      if(h.hit||!['warning','runestone','krogLeap','krogAcid','meteor','bell','bomb','slam','dice','explosiveSprout','explosiveMushroom'].includes(h.kind))continue;
      const dx=p.x-h.x,dy=p.y-h.y,d=Math.hypot(dx,dy)||1,range=(h.r||0)+95;
      if(d<range){const w=(range-d)/range*2;rx+=dx/d*w;ry+=dy/d*w;hazardRx+=dx/d*w;hazardRy+=dy/d*w;window.__pilotDodgeStats.hazard++;}
      if(Number.isFinite(h.timer)&&h.timer<.9&&d<range+85)imminentHazard=true;
    }
    const riftDist=target?Math.hypot(p.x-target.x,p.y-target.y):Infinity;
    const riftRadius=activeObjective?.variant==='multi'?55:92;
    const riftHold=activeObjective?.type==='rift'&&target&&riftDist<riftRadius;
    if(riftHold&&riftDist>1&&!imminentProjectile&&!imminentHazard&&!gnasherThreat){
      // Preserve capture position only when no imminent lethal tell exists.
      const nx=(p.x-target.x)/riftDist,ny=(p.y-target.y)/riftDist;
      const outward=rx*nx+ry*ny;
      if(outward>0){rx-=nx*outward;ry-=ny*outward;}
      window.__pilotDodgeStats.rift++;
    }
    const hpRatio=p.hp/Math.max(1,p.maxHp);
    if(gnasherThreat){
      // Keep the escape intent clean; the planner below resolves simultaneous threats.
      goalX=gnasherEscapeX;goalY=gnasherEscapeY;
    }else{
      let evade=Math.max(0,Math.min(2.4,(255-minThreat)/110))*(riftHold?.72:1);
      if(imminentProjectile)evade=Math.max(evade,2.0);
      if(imminentHazard)evade=Math.max(evade,1.35);
      if(hpRatio<.55&&minThreat<320){
        const threat=nearest(game.enemies.filter(e=>!e.dead&&e.type!=='boss'),p);
        if(threat){goalX=(p.x-threat.o.x)/(threat.d||1);goalY=(p.y-threat.o.y)/(threat.d||1);}
        evade=Math.max(evade,2.6);window.__pilotDodgeStats.criticalEscape++;
      }
      goalX+=rx*evade;goalY+=ry*evade;
    }
    // Unified short-horizon planner: score candidate headings against projectiles,
    // every active Gnasher, hazards, enemy contact, objectives and map boundaries.
    // This avoids vector cancellation and corner traps from independently blended forces.
    const edgeNow=Math.min(1200-Math.abs(p.x),900-Math.abs(p.y));
    const emergency=gnasherThreat||imminentProjectile||imminentHazard||minThreat<190||edgeNow<180;
    if(emergency){
      const moveSpeed=(p.move||220)*(game.carriedCore&&game.carriedCore.alive?.58:1)*
        (p.lowSpeed?1+(1-p.hp/Math.max(1,p.maxHp))*.21:1)*(p.fightT>0?1.3:1);
      const horizon=1.5;
      const desiredD=Math.hypot(goalX,goalY)||1;
      const desiredX=goalX/desiredD,desiredY=goalY/desiredD;
      const previous=window.__pilotHeading||{x:desiredX,y:desiredY};
      let bestScore=-Infinity,bestX=desiredX,bestY=desiredY;
      for(let k=0;k<24;k++){
        const a=k*Math.PI/12,dx=Math.cos(a),dy=Math.sin(a);
        const nx=clamp(p.x+dx*moveSpeed*horizon,-1200,1200);
        const ny=clamp(p.y+dy*moveSpeed*horizon,-900,900);
        let score=(dx*desiredX+dy*desiredY)*28+
          (dx*(previous.x||0)+dy*(previous.y||0))*11;
        if(target){
          const beforeDistance=Math.hypot(target.x-p.x,target.y-p.y);
          const afterDistance=Math.hypot(target.x-nx,target.y-ny);
          score+=Math.max(-120,Math.min(120,beforeDistance-afterDistance))*.28;
        }
        // Gnasher leap landing points are fixed during the tell. Evaluate all
        // simultaneous leaps at their actual remaining impact times.
        for(const threat of leapThreats){
          const e=threat.e,t=Math.max(0,Math.min(horizon,e.stateT||0));
          const fx=clamp(p.x+dx*moveSpeed*t,-1200,1200);
          const fy=clamp(p.y+dy*moveSpeed*t,-900,900);
          const landingD=Math.hypot(fx-(e.leapX??e.x),fy-(e.leapY??e.y));
          const safe=92;
          if(landingD<safe)score-=(safe-landingD)*4.8;
          else score+=Math.min(landingD-safe,100)*.025;
        }
        // During burrow the Gnasher tracks the wizard. Prefer headings that
        // maintain separation from every burrowing Gnasher, not just the nearest.
        for(const threat of burrowThreats){
          const e=threat.e,d=Math.max(1,threat.d);
          const awayX=(p.x-e.x)/d,awayY=(p.y-e.y)/d;
          const weight=Math.max(0,1-d/650);
          score+=(dx*awayX+dy*awayY)*24*weight;
          const chaseTime=Math.min(horizon,Math.max(.03,e.stateT||.03));
          const closing=Math.max(0,(e.speed*3-moveSpeed)*chaseTime);
          const predictedGap=Math.max(0,d-closing);
          if(predictedGap<115)score-=(115-predictedGap)*.42;
        }
        // Predict relative motion, not a perpendicular force. This handles
        // crossing shots and multiple projectiles without their vectors cancelling.
        for(const shot of game.shots){
          if(shot.kind!=='enemy')continue;
          const rx0=p.x-shot.x,ry0=p.y-shot.y;
          const rvx=dx*moveSpeed-(shot.vx||0),rvy=dy*moveSpeed-(shot.vy||0);
          const rv2=rvx*rvx+rvy*rvy;
          if(rv2<1)continue;
          const t=Math.max(0,Math.min(horizon,-(rx0*rvx+ry0*rvy)/rv2));
          const miss=Math.hypot(rx0+rvx*t,ry0+rvy*t);
          const armorValue=p.armor+(p.thick?(1-p.hp/Math.max(1,p.maxHp))*90:0);
          const expected=(shot.dmg||0)*100/(100+armorValue)*(1-(p.dodge||0));
          const risk=expected/Math.max(1,p.hp);
          const safe=(shot.r||6)+p.r+28+Math.min(110,risk*70);
          if(miss<safe+24)score-=(safe+24-miss)*(4.4+Math.min(3,risk*1.5));
          else score+=Math.min(miss-safe,120)*.018;
        }
        // Timed hazards are evaluated at their trigger time.
        for(const h of game.hazards){
          if(h.hit||!Number.isFinite(h.timer)||h.timer>horizon+.2||
            !['warning','runestone','krogLeap','krogAcid','meteor','bell','bomb','slam','dice','explosiveSprout','explosiveMushroom'].includes(h.kind))continue;
          const ht=Math.max(0,Math.min(horizon,h.timer));
          const hx=clamp(p.x+dx*moveSpeed*ht,-1200,1200);
          const hy=clamp(p.y+dy*moveSpeed*ht,-900,900);
          const hd=Math.hypot(hx-h.x,hy-h.y),safe=(h.r||0)+p.r+42;
          if(hd<safe)score-=(safe-hd)*2.8;
        }
        // Predict enemy approach over the same horizon.
        const armorValue=p.armor+(p.thick?(1-p.hp/Math.max(1,p.maxHp))*90:0);
        for(const e of game.enemies){
          if(e.dead||e.type==='boss'||e.state==='burrow'||e.state==='leap')continue;
          const ex0=p.x-e.x,ey0=p.y-e.y,ed=Math.hypot(ex0,ey0)||1;
          const es=(e.speed||0)*Math.max(0,1-(e.slow||0));
          const ex=e.x+ex0/ed*es*horizon,ey=e.y+ey0/ed*es*horizon;
          const contactD=Math.hypot(nx-ex,ny-ey);
          const expected=(e.dmg||0)*.14*(e.weakness>0?.65:1)*100/(100+armorValue)*(1-(p.dodge||0));
          const risk=expected/Math.max(1,p.hp);
          const safe=e.r+p.r+28+Math.min(130,risk*95);
          if(contactD<safe)score-=(safe-contactD)*(2.0+Math.min(3,risk*2.2));
          else if(contactD<safe+55)score-=(safe+55-contactD)*.12;
        }
        // Reward moving inward; do not hard-steer toward an edge while dodging.
        const edgeAfter=Math.min(1200-Math.abs(nx),900-Math.abs(ny));
        score+=(edgeAfter-edgeNow)*1.35;
        if(edgeAfter<28)score-=(28-edgeAfter)*3.5;
        if(score>bestScore){bestScore=score;bestX=dx;bestY=dy;}
      }
      goalX=bestX;goalY=bestY;
      window.__pilotHeading={x:goalX,y:goalY};
    }else{
      // Outside emergencies, softly turn inward before reaching the hard clamp.
      if(p.x>1120){goalX=Math.min(goalX,-.65);window.__pilotDodgeStats.boundary++;}
      if(p.x< -1120){goalX=Math.max(goalX,.65);window.__pilotDodgeStats.boundary++;}
      if(p.y>820){goalY=Math.min(goalY,-.65);window.__pilotDodgeStats.boundary++;}
      if(p.y< -820){goalY=Math.max(goalY,.65);window.__pilotDodgeStats.boundary++;}
      const desiredD=Math.hypot(goalX,goalY)||1;
      goalX/=desiredD;goalY/=desiredD;
      window.__pilotHeading={x:goalX,y:goalY};
    }
    const mag=Math.hypot(goalX,goalY)||1;goalX/=mag;goalY/=mag;
    keys={};joy.x=goalX;joy.y=goalY;joy.active=true;
    const chestNear=game.chests.some(c=>!c.open&&Math.hypot(c.x-p.x,c.y-p.y)<74);
    const o=game.objective&&!game.objective.done?game.objective:null;
    let itemNear=false;
    if(o?.type==='cores'&&o.variant==='heavy'&&!game.carriedCore)
      itemNear=(o.objects||[]).some(x=>x.alive&&Math.hypot(x.x-p.x,x.y-p.y)<72);
    if(o?.type==='brazier'){
      const wanted=o.variant==='sequence'?o.sequence?.[o.sequenceIndex]:null;
      itemNear=(o.objects||[]).some(x=>x.alive&&(wanted===null||wanted===undefined||x.index===wanted)&&Math.hypot(x.x-p.x,x.y-p.y)<80);
    }
    if(!gnasherThreat&&(chestNear||itemNear)){interact();interactions++;}
    window.__manualTick=true;
    try{
      for(let step=0;step<stepsPerDecision&&screen==='playing'&&!game.ended;step++){
        update(dt);elapsed+=dt;ticks++;
      }
    }finally{window.__manualTick=false;}
    if(game.time-lastTrace>=15){
      const q=game.player,near=nearest(game.enemies.filter(e=>!e.dead),q);
      trace.push({t:+game.time.toFixed(1),hp:+q.hp.toFixed(1),maxHp:q.maxHp,level:q.level,
        kills:q.kills,damageTaken:+q.damageTaken.toFixed(1),armor:+q.armor.toFixed(1),
        regen:+q.regen.toFixed(1),damage:+q.damage.toFixed(2),cast:+q.cast.toFixed(2),crit:+q.crit.toFixed(2),
        spellCount:q.spells.length,enemyCount:game.enemies.filter(e=>!e.dead).length,
        nearestEnemy:near?+near.d.toFixed(1):null,
        position:{x:+q.x.toFixed(1),y:+q.y.toFixed(1)},carriedCore:!!game.carriedCore?.alive,moveSpeed:+q.move.toFixed(1),
        target:target?{kind:target.type||target.kind||'objective',x:+target.x.toFixed(1),y:+target.y.toFixed(1)}:null,
        edgeDistance:Math.min(1200-Math.abs(q.x),900-Math.abs(q.y)),
        imminentProjectile,imminentHazard,gnasherThreat,gnasherMode,gnasherStateT,
        gnasherEscape:{x:+gnasherEscapeX.toFixed(2),y:+gnasherEscapeY.toFixed(2)},
        projectileAvoidance:{x:+projectileRx.toFixed(2),y:+projectileRy.toFixed(2)},
        hazardAvoidance:{x:+hazardRx.toFixed(2),y:+hazardRy.toFixed(2)},
        activeGnasher:activeGnasher?{state:activeGnasher.e.state,stateT:+(activeGnasher.e.stateT||0).toFixed(2),distance:+activeGnasher.d.toFixed(1),landingX:Number.isFinite(activeGnasher.e.leapX)?+activeGnasher.e.leapX.toFixed(1):null,landingY:Number.isFinite(activeGnasher.e.leapY)?+activeGnasher.e.leapY.toFixed(1):null}:null,
        healthOrbs:game.orbs.filter(x=>x.type==='health').length,magnetOrbs:game.orbs.filter(x=>x.type==='magnet').length,objective:game.objective?.type||null,
        objectiveProgress:game.objective?.progress||0,objectiveTarget:game.objective?.target||0,
        objectiveDone:!!game.objective?.done,objectiveVariant:game.objective?.variant||null,
        objectiveTime:game.objective?+game.objective.time.toFixed(1):null,
        rerolls:q.rerolls,scrolls:q.scrolls.slice(),invuln:+q.invuln.toFixed(2),
        spells:q.spells.map(x=>({id:x.id,level:x.level,augments:x.augments.slice(),infusions:x.infusions.slice()}))});
      lastTrace=game.time;
    }
    if(ticks-lastYield>=300){lastYield=ticks;await new Promise(r=>setTimeout(r,0));}
  }
  keys={};
  const p=game.player,b=game.boss;
  return {
    screen,ended:game.ended,elapsed,gameTime:game.time,tickCount:ticks,
    simulationHarness:{manualTicks:window.__simulationHarness.manualTicks-manualStart,blockedFrameUpdates:window.__simulationHarness.blockedFrameUpdates-blockedStart,renderRandomCalls:window.__simulationHarness.renderRandomCalls},
    renderRandomCalls:window.__simulationHarness.renderRandomCalls,simulationStepSeconds:dt,
    kills:p.kills,level:p.level,
    hp:p.hp,maxHp:p.maxHp,damageTaken:p.damageTaken,armor:p.armor,regen:p.regen,
    objectives:p.objectives,upgrades,interactions,upgradeLog,
    spells:p.spells.map(x=>({id:x.id,level:x.level,augments:x.augments.slice(),infusions:x.infusions.slice()})),
    scrolls:p.scrolls.slice(),rerolls:p.rerolls,
    position:{x:+p.x.toFixed(1),y:+p.y.toFixed(1)},
    damageEvents:window.__damageEvents.slice(-80),
    pilotDodgeStats:{...window.__pilotDodgeStats},
    gnasherHits:window.__gnasherHits.slice(-80),
    gnasherLeapSamples:window.__gnasherLeapSamples.slice(-120),
    trialSpellId:save.trialSpellId||null,
    objective:game.objective?.type||null,carriedCore:!!game.carriedCore?.alive,
    bossSpawned:!!b,bossId:b?.bossId||null,bossHp:b?.hp??null,bossMax:b?.max??null,
    bossDead:!!b?.dead,wins:save.wins||0,losses:save.runs-(save.wins||0),
    enemyCount:game.enemies.filter(e=>!e.dead).length,trace,
    newSpellChoiceViolations:upgradeLog.filter(x=>x.offered.some(o=>o.kind==='newSpell')&&x.hpRatio>=.80&&x.selected.kind!=='newSpell').length,
    errors:p.hp<0||!Number.isFinite(p.hp)||!Number.isFinite(game.time)
  };
};
"""
GNASHER_HIT="if(Math.hypot(p.x-e.x,p.y-e.y)<60)damagePlayer(gnasherLeapDamage(e),'gnasher');"
GNASHER_INSTRUMENTED="if(Math.hypot(p.x-e.x,p.y-e.y)<60){window.__gnasherHits.push({t:+g.time.toFixed(1),id:e.id,state:e.state,stateT:+e.stateT.toFixed(2),x:+e.x.toFixed(1),y:+e.y.toFixed(1),leapX:+e.leapX.toFixed(1),leapY:+e.leapY.toFixed(1),playerX:+p.x.toFixed(1),playerY:+p.y.toFixed(1),distance:+Math.hypot(p.x-e.x,p.y-e.y).toFixed(1),dmg:+gnasherLeapDamage(e).toFixed(1)});damagePlayer(gnasherLeapDamage(e),'gnasher');}"
assert SOURCE.count(GNASHER_HIT)==1,"Gnasher hit instrumentation anchor must occur exactly once"
CONTACT_HIT="if(d<e.r+p.r+3&&e.state!=='corrupt'){e.touch=(e.touch||0)-dt;if(e.touch<=0){damagePlayer(enemyContactDamage(e),'contact');e.touch=.65}}"
CONTACT_INSTRUMENTED="if(d<e.r+p.r+3&&e.state!=='corrupt'){e.touch=(e.touch||0)-dt;if(e.touch<=0){window.__contactSource={type:e.type,state:e.state,id:e.id,hp:+e.hp.toFixed(1),dmg:+e.dmg.toFixed(1),distance:+d.toFixed(1),damage:+enemyContactDamage(e).toFixed(1)};damagePlayer(enemyContactDamage(e),'contact');e.touch=.65}}"
RANGED_SHOT="g.shots.push({x:e.x,y:e.y,vx:Math.cos(a)*190,vy:Math.sin(a)*190,life:3,dmg:e.dmg*.52,r:6,kind:'enemy',color:'#d28fcb'})"
TAGGED_RANGED_SHOT="g.shots.push({x:e.x,y:e.y,vx:Math.cos(a)*190,vy:Math.sin(a)*190,life:3,dmg:e.dmg*.52,r:6,kind:'enemy',sourceType:e.type,sourceId:e.id,sourceDamage:e.dmg,color:'#d28fcb'})"
assert SOURCE.count(CONTACT_HIT)==1,"Contact source instrumentation anchor must occur exactly once"
assert SOURCE.count(RANGED_SHOT)==1,"Ranged projectile source instrumentation anchor must occur exactly once"
DRAW_SHAKE="let sx=g?.shake?rand(-g.shake,g.shake):0,sy=g?.shake?rand(-g.shake,g.shake):0;"
DRAW_SHAKE_25D="ctx.translate(-cx+(g?.shake?rand(-g.shake,g.shake):0),-cy+(g?.shake?rand(-g.shake,g.shake):0));"
FRAME_RENDER="if(save.renderMode==='3d'&&window.Game3D?.available){window.Game3D.render(game,game?.time||t/1000);drawOverlay3D();}\n else drawWorld();"
assert SOURCE.count(DRAW_SHAKE)==1,"2D screen-shake RNG anchor must occur exactly once"
assert SOURCE.count(DRAW_SHAKE_25D)==1,"atlas-backed 2.5D screen-shake RNG anchor must occur exactly once"
assert SOURCE.count(FRAME_RENDER)==1,"render path anchor must occur exactly once"
DETERMINISTIC_SHAKE="let sx=g?.shake?Math.sin(g.time*37)*g.shake:0,sy=g?.shake?Math.cos(g.time*41)*g.shake:0;"
DETERMINISTIC_SHAKE_25D="ctx.translate(-cx+(g?.shake?Math.sin(g.time*37)*g.shake:0),-cy+(g?.shake?Math.cos(g.time*41)*g.shake:0));"
TRACKED_RENDER="window.__renderPhase=true;try{if(save.renderMode==='3d'&&window.Game3D?.available){window.Game3D.render(game,game?.time||t/1000);drawOverlay3D();}else drawWorld();}finally{window.__renderPhase=false;}"
DOCUMENT=(SOURCE.replace(MARKER,PROBE+"\n"+MARKER)
  .replace(GNASHER_HIT,GNASHER_INSTRUMENTED)
  .replace(CONTACT_HIT,CONTACT_INSTRUMENTED)
  .replace(RANGED_SHOT,TAGGED_RANGED_SHOT)
  .replace(DRAW_SHAKE,DETERMINISTIC_SHAKE)
  .replace(DRAW_SHAKE_25D,DETERMINISTIC_SHAKE_25D)
  .replace(FRAME_RENDER,TRACKED_RENDER))
assert "rand(-g.shake,g.shake)" not in DOCUMENT,"render RNG source remains in test document"

async def main():
  seeds=[int(x) for x in sys.argv[1:]] or list(range(1,25))
  required_baseline={1,2,3}
  valid_bosses={"sol","krog","mul"}
  report={"runs":[],"checks":{},"required_baseline_seeds":sorted(required_baseline),"seed_budget":seeds}
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
      await page.locator("#start").click()
      if seed in required_baseline:
        state=await asyncio.wait_for(page.evaluate("window.__fullRun(1500,false)"),timeout=180)
        phase="baseline_full_natural_run"
      else:
        # Scouting stops at the naturally selected boss. It never selects or mutates
        # the boss. Only a missing archetype is fought to completion.
        scout=await asyncio.wait_for(page.evaluate("window.__fullRun(1500,true)"),timeout=180)
        covered={x["boss"] for x in report["runs"] if x["natural_win"]}
        if scout["bossId"] in valid_bosses and scout["bossId"] not in covered:
          state=await asyncio.wait_for(page.evaluate("window.__fullRun(1500,false)"),timeout=180)
          phase="candidate_full_natural_win"
        else:
          state=scout
          phase="candidate_boss_scout_only"
      natural_win=bool(state["bossDead"] and state["ended"] and state["screen"]=="result" and state["wins"]>=1)
      compact_state={
        "screen":state["screen"],"ended":state["ended"],"elapsed":round(state["elapsed"],1),
        "gameTime":round(state["gameTime"],1),"tickCount":state["tickCount"],
        "simulationHarness":state["simulationHarness"],"renderRandomCalls":state["renderRandomCalls"],"simulationStepSeconds":state["simulationStepSeconds"],"kills":state["kills"],"level":state["level"],
        "hp":round(state["hp"],1),"maxHp":state["maxHp"],"damageTaken":round(state["damageTaken"],1),
        "armor":state["armor"],"regen":state["regen"],"objectives":state["objectives"],
        "upgrades":state["upgrades"],"interactions":state["interactions"],"position":state["position"],"rerolls":state["rerolls"],"pilotDodgeStats":state["pilotDodgeStats"],"newSpellChoiceViolations":state["newSpellChoiceViolations"],"spells":state["spells"],
        "scrolls":state["scrolls"],"rerolls":state["rerolls"],"position":state["position"],"carriedCore":state["carriedCore"],
        "bossSpawned":state["bossSpawned"],"bossId":state["bossId"],"bossHp":state["bossHp"],
        "bossMax":state["bossMax"],"bossDead":state["bossDead"],"wins":state["wins"],
        "losses":state["losses"],"enemyCount":state["enemyCount"],"errors":state["errors"],
        "pilotDodgeStats":state["pilotDodgeStats"],"newSpellChoiceViolations":state["newSpellChoiceViolations"],
        "recentDamageEvents":state["damageEvents"][-10:],"recentGnasherHits":state["gnasherHits"][-10:],
        "recentGnasherLeapSamples":state["gnasherLeapSamples"][-30:],
        "recentTrace":state["trace"][-10:],"recentUpgrades":state["upgradeLog"][-10:]
      }
      item={"seed":seed,"phase":phase,"boss":state["bossId"],"natural_win":natural_win,"state":compact_state,
            "page_errors":errors,"console_errors":console,"external_requests":requests}
      report["runs"].append(item)
      await context.close()
      baseline_runs=[x for x in report["runs"] if x["seed"] in required_baseline]
      baseline_ok=len(baseline_runs)==len(required_baseline) and {x["seed"] for x in baseline_runs}==required_baseline and all(x["natural_win"] for x in baseline_runs)
      winning_bosses={x["boss"] for x in report["runs"] if x["natural_win"]}
      if baseline_ok and winning_bosses==valid_bosses:
        break
    # Repeat seed 1 in a fresh context. A seeded result must not depend on RAF scheduling.
    replay_context=await browser.new_context(viewport={"width":1280,"height":800})
    replay_page=await replay_context.new_page()
    replay_errors=[];replay_console=[];replay_requests=[]
    replay_page.on("pageerror",lambda e:replay_errors.append(str(e)))
    replay_page.on("console",lambda m:replay_console.append(m.text) if m.type=="error" else None)
    replay_page.on("request",lambda r:replay_requests.append(r.url) if r.url.startswith(("http://","https://")) else None)
    await replay_page.set_content(DOCUMENT,wait_until="load")
    await replay_page.evaluate("(seed)=>window.__setRunSeed(seed)",1)
    await replay_page.locator("#start").click()
    replay_state=await asyncio.wait_for(replay_page.evaluate("window.__fullRun(1500,false)"),timeout=180)
    replay_fields=["screen","ended","elapsed","gameTime","tickCount","kills","level","hp","maxHp","damageTaken","armor","regen","objectives","bossId","bossDead","wins","enemyCount","spells","scrolls","upgrades","interactions","position","rerolls","pilotDodgeStats","newSpellChoiceViolations","renderRandomCalls","simulationStepSeconds"]
    first_seed_one=next(x["state"] for x in report["runs"] if x["seed"]==1)
    replay_signature={k:replay_state[k] for k in replay_fields}
    for k in ("elapsed","gameTime","hp","damageTaken"):
      replay_signature[k]=round(replay_signature[k],1)
    first_signature={k:first_seed_one[k] for k in replay_fields}
    report["same_seed_replay"]={
      "seed":1,"matches":first_signature==replay_signature,
      "first":first_signature,"repeat":replay_signature,
      "simulationHarness":replay_state["simulationHarness"],"tickCount":replay_state["tickCount"],
      "page_errors":replay_errors,"console_errors":replay_console,"external_requests":replay_requests
    }
    await replay_context.close()
    await browser.close()
  baseline_runs=[x for x in report["runs"] if x["seed"] in required_baseline]
  baseline_ok=len(baseline_runs)==len(required_baseline) and {x["seed"] for x in baseline_runs}==required_baseline and all(x["natural_win"] for x in baseline_runs)
  winning_runs=[x for x in report["runs"] if x["natural_win"]]
  winning_bosses={x["boss"] for x in winning_runs}
  all_boss_ids=[x["boss"] for x in report["runs"] if x["boss"] is not None]
  report["checks"]={
    "baseline_seeds_1_2_3_natural_wins":baseline_ok,
    "at_least_three_natural_wins":len(winning_runs)>=3,
    "boss_ids_recorded_and_valid":all(x in valid_bosses for x in all_boss_ids),
    "all_three_boss_archetypes_naturally_defeated":winning_bosses==valid_bosses,
    "manual_simulation_is_single_clock":all(x["state"]["simulationHarness"]["manualTicks"]==x["state"]["tickCount"] and x["state"]["simulationHarness"]["blockedFrameUpdates"]>0 for x in report["runs"]) and report["same_seed_replay"]["simulationHarness"]["manualTicks"]==report["same_seed_replay"]["tickCount"] and report["same_seed_replay"]["simulationHarness"]["blockedFrameUpdates"]>0,
    "render_path_does_not_consume_seeded_rng":all(x["state"]["renderRandomCalls"]==0 for x in report["runs"]) and report["same_seed_replay"]["repeat"]["renderRandomCalls"]==0,
    "production_fixed_step_is_used":all(abs(x["state"]["simulationStepSeconds"]-(1/30))<1e-12 for x in report["runs"]) and abs(report["same_seed_replay"]["repeat"]["simulationStepSeconds"]-(1/30))<1e-12,
    "same_seed_replay_is_identical":report["same_seed_replay"]["matches"],
    "healthy_new_spell_offers_are_taken":all(x["state"]["newSpellChoiceViolations"]==0 for x in report["runs"]),
    "replay_has_no_browser_errors_or_external_requests":not report["same_seed_replay"]["page_errors"] and not report["same_seed_replay"]["console_errors"] and not report["same_seed_replay"]["external_requests"],
    "all_attempted_runs_no_browser_errors":all(not x["page_errors"] and not x["console_errors"] for x in report["runs"]),
    "offline_no_external_requests":all(not x["external_requests"] for x in report["runs"])
  }
  report["boss_ids"]=sorted(set(all_boss_ids))
  report["natural_winning_boss_ids"]=sorted(winning_bosses)
  report["coverage_winning_seeds"]={boss:[x["seed"] for x in winning_runs if x["boss"]==boss] for boss in sorted(valid_bosses)}
  report["scout_only_runs"]=[x["seed"] for x in report["runs"] if x["phase"]=="candidate_boss_scout_only"]
  report["natural_wins"]=len(winning_runs)
  report["pass"]=all(report["checks"].values())
  print(json.dumps(report,ensure_ascii=False,indent=2))
  if not report["pass"]:raise SystemExit(1)

if __name__=="__main__":
  asyncio.run(main())
