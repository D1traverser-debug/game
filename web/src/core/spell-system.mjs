import { SeededRng } from "./seeded-rng.mjs";

export const SpellTargetingMode=Object.freeze({NEAREST:"nearest",LOWEST_HEALTH:"lowest_health",RANDOM:"random",NONE:"none"});
export const ProjectilePattern=Object.freeze({SINGLE:"single",SPREAD:"spread",RADIAL:"radial"});
export const SpellCastOutcome=Object.freeze({CAST:"cast",ON_COOLDOWN:"on_cooldown",NO_TARGET:"no_target",INVALID_STATE:"invalid_state"});
export class SpellDefinition {
  constructor({id,cooldownTicks,range,damage,projectileSpeed,projectileCount=1,spreadRadians=0,pierceCount=0,targetingMode=SpellTargetingMode.NEAREST,pattern=ProjectilePattern.SINGLE}) {
    if (typeof id!=="string"||!id.trim()) throw new TypeError("stable spell id required");
    if (!Number.isInteger(cooldownTicks)||cooldownTicks<0) throw new RangeError("cooldownTicks must be non-negative");
    if (![range,damage,projectileSpeed].every(Number.isFinite)||range<=0||damage<=0||projectileSpeed<=0) throw new RangeError("range, damage and speed must be positive");
    if (!Number.isInteger(projectileCount)||projectileCount<=0||!Number.isFinite(spreadRadians)||spreadRadians<0||spreadRadians>Math.PI*2||!Number.isInteger(pierceCount)||pierceCount<0) throw new RangeError("invalid projectile configuration");
    if (targetingMode===SpellTargetingMode.NONE && pattern!==ProjectilePattern.RADIAL) throw new TypeError("targetless spells require radial pattern");
    if (targetingMode!==SpellTargetingMode.NONE && pattern===ProjectilePattern.RADIAL) throw new TypeError("radial pattern requires targetless mode");
    Object.assign(this,{id,cooldownTicks,range,damage,projectileSpeed,projectileCount:pattern===ProjectilePattern.SINGLE?1:projectileCount,spreadRadians,pierceCount,targetingMode,pattern});
    Object.freeze(this);
  }
}
export class SpellRuntimeState {
  constructor() { this.cooldownRemainingTicks=0; this.level=1; }
  advanceTick() { if(this.cooldownRemainingTicks>0)this.cooldownRemainingTicks--; }
  setLevel(level) { if(!Number.isInteger(level)||level<1)throw new RangeError("level must be >= 1");this.level=level; }
  startCooldown(ticks) { this.cooldownRemainingTicks=Math.max(0,ticks); }
}
function distanceSquared(a,b) { const dx=a.x-b.x,dy=a.y-b.y;return dx*dx+dy*dy; }
export class SpellSystem {
  static tryCast(definition,runtime,caster,candidates,rng=null) {
    if (!(definition instanceof SpellDefinition)||!(runtime instanceof SpellRuntimeState)||!caster||!Number.isFinite(caster.x)||!Number.isFinite(caster.y)||!Number.isInteger(caster.id)||!Array.isArray(candidates)) return {outcome:SpellCastOutcome.INVALID_STATE,targetId:-1,projectiles:[]};
    if(runtime.cooldownRemainingTicks>0)return {outcome:SpellCastOutcome.ON_COOLDOWN,targetId:-1,projectiles:[]};
    let target=null;
    if(definition.targetingMode!==SpellTargetingMode.NONE) {
      const eligible=candidates.filter(c=>c&&Number.isInteger(c.id)&&Number.isFinite(c.x)&&Number.isFinite(c.y)&&Number.isFinite(c.health)&&Number.isFinite(c.maxHealth)&&c.health>0&&c.maxHealth>0&&(caster.teamId===0||c.teamId!==caster.teamId)&&distanceSquared(caster,c)<=definition.range*definition.range).sort((a,b)=>a.id-b.id);
      if(!eligible.length)return {outcome:SpellCastOutcome.NO_TARGET,targetId:-1,projectiles:[]};
      if(definition.targetingMode===SpellTargetingMode.NEAREST)target=eligible.slice().sort((a,b)=>distanceSquared(caster,a)-distanceSquared(caster,b)||a.id-b.id)[0];
      else if(definition.targetingMode===SpellTargetingMode.LOWEST_HEALTH)target=eligible.slice().sort((a,b)=>a.health/a.maxHealth-b.health/b.maxHealth||distanceSquared(caster,a)-distanceSquared(caster,b)||a.id-b.id)[0];
      else if(definition.targetingMode===SpellTargetingMode.RANDOM) {
        if(!(rng instanceof SeededRng))return {outcome:SpellCastOutcome.INVALID_STATE,targetId:-1,projectiles:[]};
        target=eligible[rng.nextInt(0,eligible.length)];
      }
    }
    const count=definition.projectileCount,baseAngle=target?Math.atan2(target.y-caster.y,target.x-caster.x):0;
    const projectiles=[];
    for(let i=0;i<count;i++) {
      const angle=definition.pattern===ProjectilePattern.RADIAL?i*Math.PI*2/count:
        definition.pattern===ProjectilePattern.SPREAD?baseAngle+(count===1?0:(i/(count-1)-.5)*definition.spreadRadians):baseAngle;
      projectiles.push(Object.freeze({sourceId:caster.id,targetId:target?.id??-1,index:i,x:caster.x,y:caster.y,
        velocityX:Math.cos(angle)*definition.projectileSpeed,velocityY:Math.sin(angle)*definition.projectileSpeed,
        damage:definition.damage,pierceCount:definition.pierceCount}));
    }
    runtime.startCooldown(definition.cooldownTicks);
    return {outcome:SpellCastOutcome.CAST,targetId:target?.id??-1,projectiles:Object.freeze(projectiles)};
  }
}
