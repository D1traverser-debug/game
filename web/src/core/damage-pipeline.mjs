import { CombatantState } from "./combatant.mjs";

export const DamageKind = Object.freeze({ SPELL:"spell", ELEMENTAL:"elemental", HAZARD:"hazard", CONTACT:"contact", SELF:"self" });
export const DamageOutcome = Object.freeze({
  APPLIED:"applied", KILLED:"killed", BLOCKED_FRIENDLY_FIRE:"blocked_friendly_fire",
  BLOCKED_SELF_DAMAGE:"blocked_self_damage", BLOCKED_INVULNERABILITY:"blocked_invulnerability",
  SOURCE_UNAVAILABLE:"source_unavailable", TARGET_ALREADY_DEAD:"target_already_dead", INVALID_REQUEST:"invalid_request"
});
export class DamagePolicy {
  constructor({ friendlyFireEnabled = true, selfDamageEnabled = true } = {}) {
    this.friendlyFireEnabled = !!friendlyFireEnabled;
    this.selfDamageEnabled = !!selfDamageEnabled;
  }
}
export class DamagePipeline {
  static apply(source, target, request, policy = new DamagePolicy()) {
    const health = target instanceof CombatantState ? target.health : 0;
    const result = (outcome, damageApplied = 0) => Object.freeze({ outcome, damageApplied, targetHealthAfter:target?.health ?? 0,
      wasApplied:outcome === DamageOutcome.APPLIED || outcome === DamageOutcome.KILLED, targetDied:outcome === DamageOutcome.KILLED });
    if (!(policy instanceof DamagePolicy) || !(source instanceof CombatantState) || !(target instanceof CombatantState) || !request) return result(DamageOutcome.INVALID_REQUEST);
    if (request.sourceId !== source.id || request.targetId !== target.id || !Number.isFinite(request.rawDamage) || request.rawDamage <= 0) return result(DamageOutcome.INVALID_REQUEST);
    if (!source.isAlive) return result(DamageOutcome.SOURCE_UNAVAILABLE);
    if (!target.isAlive) return result(DamageOutcome.TARGET_ALREADY_DEAD);
    const selfHit = source.id === target.id;
    const sameTeam = !selfHit && source.teamId !== 0 && source.teamId === target.teamId;
    if (selfHit && !policy.selfDamageEnabled) return result(DamageOutcome.BLOCKED_SELF_DAMAGE);
    if (sameTeam && !policy.friendlyFireEnabled) return result(DamageOutcome.BLOCKED_FRIENDLY_FIRE);
    if (target.invulnerabilityTicks > 0) return result(DamageOutcome.BLOCKED_INVULNERABILITY);
    const applied = target.applyDamage(request.rawDamage);
    return result(target.isAlive ? DamageOutcome.APPLIED : DamageOutcome.KILLED, applied);
  }
}
