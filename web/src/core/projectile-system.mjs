import { DamagePipeline, DamageOutcome, DamagePolicy } from "./damage-pipeline.mjs";
import { CombatantState } from "./combatant.mjs";

export class ProjectileState {
  constructor({ id, spawn, radius, lifetimeTicks }) {
    if (!Number.isInteger(id) || id < 0) throw new RangeError("projectile id must be non-negative");
    if (!spawn || ![spawn.x,spawn.y,spawn.velocityX,spawn.velocityY,spawn.damage].every(Number.isFinite) || spawn.damage <= 0) throw new TypeError("invalid projectile spawn");
    if (!Number.isFinite(radius) || radius <= 0 || !Number.isInteger(lifetimeTicks) || lifetimeTicks <= 0) throw new RangeError("invalid projectile radius/lifetime");
    if (!Number.isInteger(spawn.sourceId) || spawn.sourceId < 0 || !Number.isInteger(spawn.pierceCount ?? 0) || (spawn.pierceCount ?? 0) < 0) throw new RangeError("invalid projectile source/pierce");
    this.id=id; this.sourceId=spawn.sourceId; this.x=spawn.x; this.y=spawn.y;
    this.velocityX=spawn.velocityX; this.velocityY=spawn.velocityY; this.damage=spawn.damage;
    this.radius=radius; this.lifetimeTicksRemaining=lifetimeTicks; this.pierceRemaining=spawn.pierceCount ?? 0;
    this.hitTargets=new Set(); this.isAlive=true;
  }
  destroy() { this.isAlive=false; }
}
function segmentCircleHit(x0,y0,x1,y1,cx,cy,radius) {
  const dx=x1-x0, dy=y1-y0, fx=x0-cx, fy=y0-cy;
  const a=dx*dx+dy*dy, c=fx*fx+fy*fy-radius*radius;
  if (c <= 0) return 0;
  if (a <= Number.EPSILON) return null;
  const b=2*(fx*dx+fy*dy), discriminant=b*b-4*a*c;
  if (discriminant < 0) return null;
  const t=(-b-Math.sqrt(discriminant))/(2*a);
  return t>=0 && t<=1 ? t : null;
}
export class ProjectileSystem {
  static step(projectiles, targets, combatants, deltaSeconds, damagePolicy = new DamagePolicy()) {
    if (!Array.isArray(projectiles) || !Array.isArray(targets) || !(combatants instanceof Map)) throw new TypeError("arrays and combatant Map are required");
    if (!Number.isFinite(deltaSeconds) || deltaSeconds <= 0) throw new RangeError("deltaSeconds must be positive");
    const hits=[]; let destroyedCount=0;
    for (const projectile of projectiles) {
      if (!(projectile instanceof ProjectileState) || !projectile.isAlive) continue;
      const source=combatants.get(projectile.sourceId);
      if (projectile.lifetimeTicksRemaining<=0 || !source?.isAlive) { projectile.destroy(); destroyedCount++; continue; }
      const x0=projectile.x,y0=projectile.y,x1=x0+projectile.velocityX*deltaSeconds,y1=y0+projectile.velocityY*deltaSeconds;
      const candidates=[];
      for (const target of targets) {
        if (!(target?.combatant instanceof CombatantState) || !target.combatant.isAlive || projectile.hitTargets.has(target.combatant.id)) continue;
        if (!Number.isFinite(target.x)||!Number.isFinite(target.y)||!Number.isFinite(target.radius)||target.radius<0) continue;
        const sameTeam=target.combatant.id!==source.id && source.teamId!==0 && target.combatant.teamId===source.teamId;
        if (target.combatant.id===source.id && !damagePolicy.selfDamageEnabled) continue;
        if (sameTeam && !damagePolicy.friendlyFireEnabled) continue;
        const t=segmentCircleHit(x0,y0,x1,y1,target.x,target.y,projectile.radius+target.radius);
        if (t!==null) candidates.push({t,target});
      }
      candidates.sort((a,b)=>a.t-b.t || a.target.combatant.id-b.target.combatant.id);
      for (const candidate of candidates) {
        const target=candidate.target.combatant;
        if (!target.isAlive || projectile.hitTargets.has(target.id)) continue;
        projectile.hitTargets.add(target.id);
        const result=DamagePipeline.apply(source,target,{sourceId:source.id,targetId:target.id,rawDamage:projectile.damage},damagePolicy);
        hits.push(Object.freeze({projectileId:projectile.id,targetId:target.id,outcome:result.outcome,damageApplied:result.damageApplied}));
        if (projectile.pierceRemaining>0) projectile.pierceRemaining--;
        else { projectile.destroy(); destroyedCount++; break; }
      }
      if (projectile.isAlive) {
        projectile.x=x1; projectile.y=y1; projectile.lifetimeTicksRemaining--;
        if (projectile.lifetimeTicksRemaining<=0) { projectile.destroy(); destroyedCount++; }
      }
    }
    return Object.freeze({hits:Object.freeze(hits),destroyedCount});
  }
}
