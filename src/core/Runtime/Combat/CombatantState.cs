using System;

namespace Game.Core.Combat
{
    public sealed class CombatantState
    {
        public CombatantState(int id, int teamId, float maxHealth)
        {
            if (id < 0) throw new ArgumentOutOfRangeException(nameof(id));
            if (!IsFinitePositive(maxHealth)) throw new ArgumentOutOfRangeException(nameof(maxHealth));
            Id = id;
            TeamId = teamId;
            MaxHealth = maxHealth;
            Health = maxHealth;
        }

        public int Id { get; }
        public int TeamId { get; }
        public float MaxHealth { get; private set; }
        public float Health { get; private set; }
        public int InvulnerabilityTicks { get; private set; }
        public bool IsAlive => Health > 0.0f;

        public void GrantInvulnerability(int ticks)
        {
            if (ticks < 0) throw new ArgumentOutOfRangeException(nameof(ticks));
            InvulnerabilityTicks = Math.Max(InvulnerabilityTicks, ticks);
        }

        public void AdvanceSimulationTick()
        {
            if (InvulnerabilityTicks > 0) InvulnerabilityTicks--;
        }

        public void SetMaxHealth(float value, bool restoreAddedCapacity)
        {
            if (!IsFinitePositive(value)) throw new ArgumentOutOfRangeException(nameof(value));
            var added = Math.Max(0.0f, value - MaxHealth);
            MaxHealth = value;
            Health = Math.Min(MaxHealth, Health + (restoreAddedCapacity ? added : 0.0f));
        }

        internal float ApplyDamage(float amount)
        {
            if (!IsFinitePositive(amount) || !IsAlive) return 0.0f;
            var applied = Math.Min(Health, amount);
            Health -= applied;
            if (Health < 0.0001f) Health = 0.0f;
            return applied;
        }

        private static bool IsFinitePositive(float value)
        {
            return !float.IsNaN(value) && !float.IsInfinity(value) && value > 0.0f;
        }
    }
}
