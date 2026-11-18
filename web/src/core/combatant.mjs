export class CombatantState {
  constructor({ id, teamId = 0, health, maxHealth = health, invulnerabilityTicks = 0 }) {
    if (!Number.isInteger(id) || id < 0) throw new RangeError("id must be a non-negative integer");
    if (!Number.isInteger(teamId)) throw new RangeError("teamId must be an integer");
    if (!Number.isFinite(maxHealth) || maxHealth <= 0) throw new RangeError("maxHealth must be finite and positive");
    if (!Number.isFinite(health) || health < 0 || health > maxHealth) throw new RangeError("health must be within [0, maxHealth]");
    if (!Number.isInteger(invulnerabilityTicks) || invulnerabilityTicks < 0) throw new RangeError("invulnerabilityTicks must be non-negative");
    this.id = id;
    this.teamId = teamId;
    this.maxHealth = maxHealth;
    this.health = health;
    this.invulnerabilityTicks = invulnerabilityTicks;
  }
  get isAlive() { return this.health > 0; }
  applyDamage(rawDamage) {
    if (!Number.isFinite(rawDamage) || rawDamage <= 0) throw new RangeError("damage must be finite and positive");
    const applied = Math.min(this.health, rawDamage);
    this.health = Math.max(0, this.health - applied);
    return applied;
  }
  advanceTick() {
    if (this.invulnerabilityTicks > 0) this.invulnerabilityTicks -= 1;
  }
}
