"""Deterministic browser regressions for boss phases, attacks and counterplay."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
MARKER="// Keep the single-player game running without external assets or libraries."
assert SOURCE.count(MARKER)==1
PROBE=r"""
window.__BOSS_QA={
 spawn:(id)=>{
  game.boss=null;game.enemies=game.enemies.filter(e=>e.type!=='boss');
  const index=BOSS_ARCHETYPES.findIndex(x=>x.id===id);if(index<0)throw Error('unknown boss '+id);
  const old=Math.random;Math.random=()=>Math.min(.999,(index+.25)/BOSS_ARCHETYPES.length);
  game.bossPending={x:game.player.x+420,y:game.player.y-260};
  try{spawnBoss()}finally{Math.random=old}
  game.boss.attackCooldown=999;game.boss.phaseTransitionTimer=0;return game.boss;
 },
 phase:(id,ratio)=>{const b=window.__BOSS_QA.spawn(id);b.hp=b.max*ratio;bossSyncPhase(b);return{phaseIndex:b.phaseIndex,phaseCount:b.phaseCount,fieldActive:b.fieldActive,headCount:b.headCount}},
 attackDefs:()=>Object.fromEntries(Object.entries(BOSS_ATTACK_DEFS).map(([id,defs])=>[id,defs.map(d=>({id:d.id,shape:d.shape,effect:d.effect,telegraph:d.telegraph,active:d.active,recovery:d.recovery,cooldown:d.cooldown}))])),
 geometry:(id,attackId)=>{const b=window.__BOSS_QA.spawn(id),def=BOSS_ATTACK_DEFS[id].find(x=>x.id===attackId);const a=bossBeginAttack(b,def),before=JSON.stringify(a.geometry);game.player.x+=37;game.player.y-=19;return{stage:a.stage,geometry:a.geometry,unchanged:before===JSON.stringify(a.geometry)}},
 lifecycle:(id,attackId)=>{
  const b=window.__BOSS_QA.spawn(id),p=game.player,def=BOSS_ATTACK_DEFS[id].find(x=>x.id===attackId);p.hp=p.maxHp=100000;p.dodge=0;p.invuln=0;
  const a=bossBeginAttack(b,def),hp0=p.hp;updateBossEncounter(.05);const telegraphStage=a.stage,hpDuringTelegraph=p.hp;
  updateBossEncounter(def.telegraph);const activeStage=a.stage,hpAtActive=p.hp;
  updateBossEncounter(def.active+.02);const recoveryStage=a.stage;updateBossEncounter(def.recovery+.02);
  return{telegraphStage,hpDuringTelegraph,hp0,activeStage,hpAtActive,recoveryStage,cleared:!b.attackInstance,cooldown:b.attackCooldown};
 },
 field:()=>{const b=window.__BOSS_QA.spawn('krog');b.hp=b.max*.6;bossSyncPhase(b);const p=game.player,c=b.fieldCenter;p.x=c.x+b.fieldRadius+100;p.y=c.y;const before=Math.hypot(p.x-c.x,p.y-c.y);bossApplyMagneticField(b,.1);return{active:b.fieldActive,before,after:Math.hypot(p.x-c.x,p.y-c.y),radius:b.fieldRadius}},
 minions:()=>{
  const b=window.__BOSS_QA.spawn('mul');b.hp=b.max*.7;const healer=spawnBossHealer(b);healer.x=b.x+220;healer.y=b.y;
  const before=Math.hypot(healer.x-b.x,healer.y-b.y),hpBefore=b.hp;bossUpdateMulMinions(b,.25);
  const moved=Math.hypot(healer.x-b.x,healer.y-b.y)<before,healed=b.hp>hpBefore;
  const corrupted=spawnBossHealer(b);corrupted.state='corrupt';corrupted.corruptT=5;corrupted.x=b.x+40;corrupted.y=b.y;
  const beforeCorrupt=b.hp;bossUpdateMulMinions(b,.05);
  return{moved,healed,corruptedDead:corrupted.dead,bossDamaged:b.hp<beforeCorrupt};
 },
 collision:()=>{const p={x:20,y:0,r:5};return{circle:bossAttackContainsPlayer({kind:'circle',x:0,y:0,r:20},p),outside:!bossAttackContainsPlayer({kind:'circle',x:0,y:0,r:10},p),line:bossAttackContainsPlayer({kind:'line',x:0,y:0,tx:100,ty:0,width:20},{x:55,y:8,r:5}),grid:bossAttackContainsPlayer({kind:'grid',points:[{x:0,y:0,r:12}]},{x:15,y:0,r:5})}},
 homing:()=>{const p={x:1000,y:1000,r:16},s={x:0,y:0,vx:180,vy:0,speed:190,turnRate:3,life:3,dmg:1,r:7,kind:'enemyHoming'};bossUpdateHomingProjectile(s,.12,p);return{vy:s.vy,turnsTowardTarget:s.vy>0}},
 warning:(id,attackId)=>{const b=window.__BOSS_QA.spawn(id),def=BOSS_ATTACK_DEFS[id].find(x=>x.id===attackId),a=bossBeginAttack(b,def),h=game.hazards.find(x=>x.bossAttackToken===a.token);return{token:a.token,count:game.hazards.filter(x=>x.bossAttackToken===a.token).length,shape:h?.bossShape,geometryMatches:JSON.stringify(h?.bossGeometry)===JSON.stringify(a.geometry)}},
 freezeCancel:()=>{const b=window.__BOSS_QA.spawn('sol'),a=bossBeginAttack(b,BOSS_ATTACK_DEFS.sol[0]);b.freeze=1.5;for(let i=0;i<15;i++){updateBossEncounter(.1);for(const h of game.hazards){h.timer-=.1;h.life-=.1}game.hazards=game.hazards.filter(h=>h.life>0)}return{oldAttackCancelled:b.attackInstance!==a,oldWarnings:game.hazards.filter(h=>h.bossAttackToken===a.token).length,remainingFreeze:b.freeze}},
 phaseCancel:()=>{const b=window.__BOSS_QA.spawn('krog'),a=bossBeginAttack(b,BOSS_ATTACK_DEFS.krog[1]);b.hp=b.max*.6;bossSyncPhase(b);return{oldAttackCancelled:b.attackInstance!==a,oldWarnings:game.hazards.filter(h=>h.bossAttackToken===a.token).length,phase:b.phaseIndex}},
 staggerCancel:()=>{const b=window.__BOSS_QA.spawn('sol'),a=bossBeginAttack(b,BOSS_ATTACK_DEFS.sol[0]);b.stagger=100;updateBossEncounter(.05);return{oldAttackCancelled:b.attackInstance!==a,oldWarnings:game.hazards.filter(h=>h.bossAttackToken===a.token).length,vulnerable:b.vulnerable}},
 pullSnapshot:()=>{const b=window.__BOSS_QA.spawn('krog'),a=bossBeginAttack(b,BOSS_ATTACK_DEFS.krog[0]),g=a.geometry,p=game.player;p.x=g.x-100;p.y=g.y;const before=p.x;b.x=g.x-300;bossApplyPull(b,a,.1);return{movedTowardSnapshot:p.x>before,after:p.x,snapshot:g.x,currentBoss:b.x}},
 radialOrigin:()=>{const b=window.__BOSS_QA.spawn('sol'),a=bossBeginAttack(b,BOSS_ATTACK_DEFS.sol[1]),g=a.geometry;game.shots=[];b.x+=300;bossFireProjectiles(b,a);return{actual:game.shots[0]?.x,expected:g.x+b.r+8,match:Math.abs(game.shots[0]?.x-(g.x+b.r+8))<.001}},
 homingOrigin:()=>{const b=window.__BOSS_QA.spawn('sol'),startX=b.x,a=bossBeginAttack(b,BOSS_ATTACK_DEFS.sol[2]);game.shots=[];b.x+=300;bossFireProjectiles(b,a);return{actual:game.shots[0]?.x,expected:startX+b.r+8,match:Math.abs(game.shots[0]?.x-(startX+b.r+8))<.001}},
 commitment:()=>{const b=window.__BOSS_QA.spawn('krog');bossBeginAttack(b,BOSS_ATTACK_DEFS.krog[1]);const before={x:b.x,y:b.y};game.player.x=b.x+800;game.player.y=b.y;updateBossEncounter(.1);return{stationary:Math.abs(b.x-before.x)<.001&&Math.abs(b.y-before.y)<.001,before,after:{x:b.x,y:b.y}}},
 pauseClock:()=>{const b=window.__BOSS_QA.spawn('sol'),a=bossBeginAttack(b,BOSS_ATTACK_DEFS.sol[0]),life=game.hazards.find(h=>h.bossAttackToken===a.token)?.life,time=game.time,timer=a.timer;pause();update(.2);const result={timeUnchanged:game.time===time,attackTimerUnchanged:a.timer===timer,warningLifeUnchanged:game.hazards.find(h=>h.bossAttackToken===a.token)?.life===life};resume();return result},
 invulnerability:()=>{const p=game.player;p.hp=100;p.maxHp=100;p.invuln=1;p.dodge=0;const a={def:{effect:'impact',damage:50},geometry:{kind:'circle',x:p.x,y:p.y,r:100},resolved:false};bossResolveAttack(null,a,.1);const afterFirst=p.hp;p.invuln=0;bossResolveAttack(null,a,.1);return{blocked:afterFirst===100,notReplayed:p.hp===100,resolved:a.resolved}}
};
"""
TEST_HTML=SOURCE.replace(MARKER,PROBE+"\n"+MARKER)
async def main():
 outcome={"checks":{},"page_errors":[],"requests":[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage","--enable-webgl","--ignore-gpu-blocklist","--use-gl=angle","--use-angle=swiftshader-webgl","--enable-unsafe-swiftshader"])
  page=await browser.new_page(viewport={"width":1280,"height":720})
  page.on("pageerror",lambda e:outcome["page_errors"].append(str(e)));page.on("request",lambda r:outcome["requests"].append(r.url))
  await page.set_content(TEST_HTML,wait_until="domcontentloaded");await page.locator("#start").click();c=outcome["checks"]
  defs=await page.evaluate("__BOSS_QA.attackDefs()")
  c["three_attack_cards_per_boss"]=all(len(defs[k])>=3 for k in ("sol","krog","mul"))
  c["attack_lifecycle_contracts"]=all(d["telegraph"]>0 and d["active"]>0 and d["recovery"]>0 and d["cooldown"]>0 and d["shape"] in ("circle","radial","target","pull","line","grid") for group in defs.values() for d in group)
  krog=await page.evaluate("__BOSS_QA.phase('krog',0.66)");c["krog_first_segment_activates_field"]=krog["phaseIndex"]==1 and krog["fieldActive"]
  mul2=await page.evaluate("__BOSS_QA.phase('mul',0.66)");mul3=await page.evaluate("__BOSS_QA.phase('mul',0.32)")
  c["mul_heads_follow_three_segments"]=mul2["phaseIndex"]==1 and mul2["headCount"]==2 and mul3["phaseIndex"]==2 and mul3["headCount"]==3
  geo=await page.evaluate("__BOSS_QA.geometry('krog','tongueSmash')");c["telegraph_geometry_is_snapshotted"]=geo["stage"]=="telegraph" and geo["unchanged"] and geo["geometry"]["kind"]=="line"
  life=await page.evaluate("__BOSS_QA.lifecycle('sol','obelisk')")
  c["telegraph_precedes_damage"]=life["telegraphStage"]=="telegraph" and life["hpDuringTelegraph"]==life["hp0"]
  c["attack_advances_active_recovery_cooldown"]=life["activeStage"]=="active" and life["recoveryStage"]=="recovery" and life["cleared"] and life["cooldown"]>0
  c["active_obelisk_resolves_hit"]=life["hpAtActive"]<life["hp0"]
  field=await page.evaluate("__BOSS_QA.field()");c["krog_field_constrains_arena"]=field["active"] and field["after"]<field["before"]
  minions=await page.evaluate("__BOSS_QA.minions()");c["mul_minions_seek_and_heal_boss"]=minions["moved"] and minions["healed"];c["corrupted_minion_damages_boss"]=minions["corruptedDead"] and minions["bossDamaged"]
  collision=await page.evaluate("__BOSS_QA.collision()");c["circle_line_grid_collision_contracts"]=all(collision.values())
  homing=await page.evaluate("__BOSS_QA.homing()");c["homing_projectile_turns_toward_player"]=homing["turnsTowardTarget"]
  warning=await page.evaluate("__BOSS_QA.warning('mul','spikeGrid')");c["telegraph_payload_preserves_geometry"]=warning["count"]==1 and warning["shape"]=="grid" and warning["geometryMatches"]
  frozen=await page.evaluate("__BOSS_QA.freezeCancel()");c["freeze_cancels_attack_and_its_warning"]=frozen["oldAttackCancelled"] and frozen["oldWarnings"]==0
  phase_cancel=await page.evaluate("__BOSS_QA.phaseCancel()");c["phase_transition_cancels_attack_and_warning"]=phase_cancel["oldAttackCancelled"] and phase_cancel["oldWarnings"]==0 and phase_cancel["phase"]==1
  stagger=await page.evaluate("__BOSS_QA.staggerCancel()");c["stagger_cancels_attack_and_warning"]=stagger["oldAttackCancelled"] and stagger["oldWarnings"]==0 and stagger["vulnerable"]>0
  pull=await page.evaluate("__BOSS_QA.pullSnapshot()");c["pull_uses_snapshotted_origin"]=pull["movedTowardSnapshot"]
  radial=await page.evaluate("__BOSS_QA.radialOrigin()");c["radial_projectiles_use_snapshotted_origin"]=radial["match"]
  homing_origin=await page.evaluate("__BOSS_QA.homingOrigin()");c["homing_projectiles_use_snapshotted_origin"]=homing_origin["match"]
  commitment=await page.evaluate("__BOSS_QA.commitment()");c["boss_commits_position_during_telegraph"]=commitment["stationary"]
  paused=await page.evaluate("__BOSS_QA.pauseClock()");c["pause_freezes_attack_and_warning_clocks"]=paused["timeUnchanged"] and paused["attackTimerUnchanged"] and paused["warningLifeUnchanged"]
  invuln=await page.evaluate("__BOSS_QA.invulnerability()");c["invulnerability_blocks_attack_once"]=invuln["blocked"] and invuln["notReplayed"] and invuln["resolved"]
  c["no_runtime_exceptions"]=not outcome["page_errors"];c["no_external_requests"]=not outcome["requests"]
  await browser.close()
 outcome["pass"]=all(outcome["checks"].values());outcome["count"]=len(outcome["checks"]);outcome["limitations"]=["Deterministic component probes only; not a human full-run or final-balance acceptance."]
 print(json.dumps(outcome,ensure_ascii=False,indent=2))
 if not outcome["pass"]:raise SystemExit(1)
if __name__=="__main__":asyncio.run(main())
