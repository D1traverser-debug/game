import test from "node:test";
import assert from "node:assert/strict";
import { FixedStepClock } from "../src/core/fixed-step-clock.mjs";
import { SeededRng } from "../src/core/seeded-rng.mjs";
import { CombatantState } from "../src/core/combatant.mjs";
import { DamagePipeline, DamageOutcome, DamagePolicy } from "../src/core/damage-pipeline.mjs";
import { SimulationEventBuffer } from "../src/core/event-buffer.mjs";
import { PlayerCommandValidator, PlayerButtons, CommandValidationOutcome } from "../src/core/input-validator.mjs";
import { ProjectileState, ProjectileSystem } from "../src/core/projectile-system.mjs";
import { SpellDefinition, SpellRuntimeState, SpellSystem, SpellTargetingMode, ProjectilePattern, SpellCastOutcome } from "../src/core/spell-system.mjs";

test("fixed clock advances exact ticks and discards paused wall time",()=>{
 const c=new FixedStepClock({stepSeconds:.1,maxStepsPerAdvance:8}),seen=[];
 assert.equal(c.advance(.25,{simulateTick:(tick,dt)=>seen.push([tick,dt])}),2);
 assert.deepEqual(seen.map(x=>x[0]),[0,1]); assert.equal(c.tick,2);
 assert.equal(c.advance(5,{paused:true,simulateTick:()=>assert.fail()}),0);
 assert.equal(c.advance(.05,{simulateTick:(tick)=>seen.push([tick])}),1);
 assert.equal(c.tick,3);
});
test("fixed clock preserves backlog when the per-frame step cap is reached",()=>{
 const c=new FixedStepClock({stepSeconds:.1,maxStepsPerAdvance:2});
 assert.equal(c.advance(.55,{simulateTick:()=>{}}),2); assert.ok(Math.abs(c.pendingSeconds-.35)<1e-9);
 assert.equal(c.advance(0,{simulateTick:()=>{}}),2); assert.ok(Math.abs(c.pendingSeconds-.15)<1e-9);
});
test("fixed clock rejects invalid time and missing callback",()=>{
 const c=new FixedStepClock(); assert.throws(()=>c.advance(-1,{simulateTick:()=>{}}),RangeError);
 assert.throws(()=>c.advance(1),TypeError);
});
test("seeded RNG repeats an identical stream",()=>{
 const a=new SeededRng(12345),b=new SeededRng(12345);
 assert.deepEqual(Array.from({length:50},()=>a.nextUint32()),Array.from({length:50},()=>b.nextUint32()));
});
test("seeded RNG returns bounded integers and unit floats",()=>{
 const r=new SeededRng(99);
 for(let i=0;i<1000;i++){const n=r.nextInt(-3,7),f=r.nextFloat01();assert.ok(n>=-3&&n<7);assert.ok(f>=0&&f<1);}
 assert.throws(()=>r.nextInt(1,1),RangeError);
});
test("damage pipeline applies damage and reports lethal transition",()=>{
 const a=new CombatantState({id:1,teamId:1,health:100}),b=new CombatantState({id:2,teamId:2,health:25});
 const hit=DamagePipeline.apply(a,b,{sourceId:1,targetId:2,rawDamage:40});
 assert.equal(hit.outcome,DamageOutcome.KILLED);assert.equal(hit.damageApplied,25);assert.equal(b.health,0);
});
test("damage policy blocks friendly fire and self damage independently",()=>{
 const a=new CombatantState({id:1,teamId:1,health:100}),ally=new CombatantState({id:2,teamId:1,health:100});
 assert.equal(DamagePipeline.apply(a,ally,{sourceId:1,targetId:2,rawDamage:10},new DamagePolicy({friendlyFireEnabled:false})).outcome,DamageOutcome.BLOCKED_FRIENDLY_FIRE);
 assert.equal(DamagePipeline.apply(a,a,{sourceId:1,targetId:1,rawDamage:10},new DamagePolicy({selfDamageEnabled:false})).outcome,DamageOutcome.BLOCKED_SELF_DAMAGE);
});
test("damage pipeline respects invulnerability and dead sources",()=>{
 const a=new CombatantState({id:1,teamId:1,health:100}),b=new CombatantState({id:2,teamId:2,health:100,invulnerabilityTicks:2});
 assert.equal(DamagePipeline.apply(a,b,{sourceId:1,targetId:2,rawDamage:5}).outcome,DamageOutcome.BLOCKED_INVULNERABILITY);
 a.applyDamage(100);
 assert.equal(DamagePipeline.apply(a,b,{sourceId:1,targetId:2,rawDamage:5}).outcome,DamageOutcome.SOURCE_UNAVAILABLE);
});
test("damage pipeline rejects malformed requests",()=>{
 const a=new CombatantState({id:1,health:10}),b=new CombatantState({id:2,health:10});
 assert.equal(DamagePipeline.apply(a,b,{sourceId:1,targetId:2,rawDamage:NaN}).outcome,DamageOutcome.INVALID_REQUEST);
});
test("event buffer sequences events and drains without resetting sequence",()=>{
 const e=new SimulationEventBuffer();e.publish(2,"cast",{sourceId:1});e.publish(2,"hit",{targetId:4});
 assert.deepEqual(e.drain().map(x=>x.sequence),[0,1]);assert.equal(e.count,0);
 assert.equal(e.publish(3,"death").sequence,2);
});
test("event buffer rejects backward ticks and non-finite payloads",()=>{
 const e=new SimulationEventBuffer();e.publish(4,"cast");
 assert.throws(()=>e.publish(3,"hit"),RangeError);assert.throws(()=>e.publish(4,"hit",{value:Infinity}),RangeError);
});
test("input validator accepts a bounded command and rejects replay",()=>{
 const v=new PlayerCommandValidator(),active=new Set([7]),cmd={playerId:7,sequence:1,clientTick:10,moveX:.5,moveY:.5,buttons:PlayerButtons.DODGE};
 assert.equal(v.validate(cmd,active,10),CommandValidationOutcome.ACCEPTED);
 assert.equal(v.validate(cmd,active,10),CommandValidationOutcome.OUT_OF_ORDER);
});
test("input validator rejects unknown player, invalid tick, movement and buttons",()=>{
 const v=new PlayerCommandValidator(),active=new Set([7]),base={playerId:7,sequence:1,clientTick:10,moveX:0,moveY:0,buttons:0};
 assert.equal(v.validate({...base,playerId:8},active,10),CommandValidationOutcome.UNKNOWN_PLAYER);
 assert.equal(v.validate({...base,clientTick:1000},active,10),CommandValidationOutcome.TICK_OUTSIDE_WINDOW);
 assert.equal(v.validate({...base,moveX:2},active,10),CommandValidationOutcome.INVALID_MOVEMENT);
 assert.equal(v.validate({...base,buttons:128},active,10),CommandValidationOutcome.INVALID_BUTTONS);
});
test("projectile swept collision prevents fast projectile tunneling",()=>{
 const source=new CombatantState({id:1,teamId:1,health:100}),target=new CombatantState({id:2,teamId:2,health:100});
 const p=new ProjectileState({id:9,spawn:{sourceId:1,x:0,y:0,velocityX:100,velocityY:0,damage:30},radius:1,lifetimeTicks:5});
 const result=ProjectileSystem.step([p],[{combatant:target,x:50,y:0,radius:2}],new Map([[1,source],[2,target]]),1);
 assert.equal(result.hits.length,1);assert.equal(target.health,70);assert.equal(p.isAlive,false);
});
test("piercing projectile resolves impacts by time then stable target id",()=>{
 const source=new CombatantState({id:1,teamId:1,health:100}),a=new CombatantState({id:3,teamId:2,health:100}),b=new CombatantState({id:2,teamId:2,health:100});
 const p=new ProjectileState({id:10,spawn:{sourceId:1,x:0,y:0,velocityX:100,velocityY:0,damage:10,pierceCount:1},radius:1,lifetimeTicks:4});
 const result=ProjectileSystem.step([p],[{combatant:a,x:40,y:0,radius:2},{combatant:b,x:40,y:0,radius:2}],new Map([[1,source],[2,b],[3,a]]),1);
 assert.deepEqual(result.hits.map(x=>x.targetId),[2,3]);assert.equal(result.hits.length,2);assert.equal(p.isAlive,false);
});
test("projectile does not hit same target twice and expires by tick",()=>{
 const source=new CombatantState({id:1,teamId:1,health:100}),target=new CombatantState({id:2,teamId:2,health:100});
 const p=new ProjectileState({id:11,spawn:{sourceId:1,x:0,y:0,velocityX:1,velocityY:0,damage:5,pierceCount:2},radius:.2,lifetimeTicks:1});
 const map=new Map([[1,source],[2,target]]),t=[{combatant:target,x:1,y:0,radius:1}];
 ProjectileSystem.step([p],t,map,.1);assert.equal(target.health,95);
 const again=ProjectileSystem.step([p],t,map,.1);assert.equal(again.hits.length,0);
});
test("spell selects nearest eligible target and starts cooldown",()=>{
 const def=new SpellDefinition({id:"arcane_bolt",cooldownTicks:3,range:20,damage:12,projectileSpeed:8});
 const runtime=new SpellRuntimeState(),caster={id:1,teamId:1,x:0,y:0};
 const result=SpellSystem.tryCast(def,runtime,caster,[{id:4,teamId:2,x:10,y:0,health:100,maxHealth:100},{id:2,teamId:2,x:3,y:0,health:100,maxHealth:100}]);
 assert.equal(result.outcome,SpellCastOutcome.CAST);assert.equal(result.targetId,2);assert.equal(runtime.cooldownRemainingTicks,3);
 assert.equal(SpellSystem.tryCast(def,runtime,caster,[]).outcome,SpellCastOutcome.ON_COOLDOWN);
});
test("spell does not consume cooldown when no target exists",()=>{
 const def=new SpellDefinition({id:"bolt",cooldownTicks:4,range:5,damage:10,projectileSpeed:5});
 const runtime=new SpellRuntimeState(),result=SpellSystem.tryCast(def,runtime,{id:1,teamId:1,x:0,y:0},[]);
 assert.equal(result.outcome,SpellCastOutcome.NO_TARGET);assert.equal(runtime.cooldownRemainingTicks,0);
});
test("spread spell emits symmetric projectiles",()=>{
 const def=new SpellDefinition({id:"fan",cooldownTicks:2,range:20,damage:8,projectileSpeed:6,projectileCount:3,spreadRadians:Math.PI/3,pattern:ProjectilePattern.SPREAD});
 const result=SpellSystem.tryCast(def,new SpellRuntimeState(),{id:1,teamId:1,x:0,y:0},[{id:2,teamId:2,x:10,y:0,health:20,maxHealth:20}]);
 assert.equal(result.projectiles.length,3);assert.ok(Math.abs(result.projectiles[0].velocityY+result.projectiles[2].velocityY)<1e-9);
});
test("radial spell uses deterministic evenly spaced directions",()=>{
 const def=new SpellDefinition({id:"nova",cooldownTicks:5,range:1,damage:7,projectileSpeed:4,projectileCount:4,targetingMode:SpellTargetingMode.NONE,pattern:ProjectilePattern.RADIAL});
 const result=SpellSystem.tryCast(def,new SpellRuntimeState(),{id:1,teamId:1,x:2,y:3},[]);
 assert.equal(result.projectiles.length,4);assert.ok(Math.abs(result.projectiles[0].velocityX-4)<1e-9);assert.ok(Math.abs(result.projectiles[1].velocityY-4)<1e-9);
});
test("random targeting is seeded and repeatable",()=>{
 const def=new SpellDefinition({id:"chaos",cooldownTicks:1,range:20,damage:3,projectileSpeed:5,targetingMode:SpellTargetingMode.RANDOM});
 const caster={id:1,teamId:1,x:0,y:0},targets=[1,2,3,4].map(id=>({id,teamId:2,x:id,y:0,health:10,maxHealth:10}));
 const a=SpellSystem.tryCast(def,new SpellRuntimeState(),caster,targets,new SeededRng(55));
 const b=SpellSystem.tryCast(def,new SpellRuntimeState(),caster,targets,new SeededRng(55));
 assert.equal(a.targetId,b.targetId);
});
