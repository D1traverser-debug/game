namespace Game.Core.Combat
{
    public enum DamageKind
    {
        Spell = 0,
        Elemental = 1,
        Hazard = 2,
        Contact = 3,
        SelfInflicted = 4
    }

    public enum DamageOutcome
    {
        Applied = 0,
        Killed = 1,
        BlockedFriendlyFire = 2,
        BlockedSelfDamage = 3,
        BlockedInvulnerability = 4,
        SourceUnavailable = 5,
        TargetAlreadyDead = 6,
        InvalidRequest = 7
    }

    public sealed class DamagePolicy
    {
        // The reference game's default run allows friendly fire; mode modifiers may override this.
        public bool FriendlyFireEnabled { get; set; } = true;
        public bool SelfDamageEnabled { get; set; } = true;
    }

    public sealed class DamageRequest
    {
        public DamageRequest(int sourceId, int targetId, float rawDamage, DamageKind kind)
        {
            SourceId = sourceId;
            TargetId = targetId;
            RawDamage = rawDamage;
            Kind = kind;
        }

        public int SourceId { get; }
        public int TargetId { get; }
        public float RawDamage { get; }
        public DamageKind Kind { get; }
    }

    public sealed class DamageResult
    {
        internal DamageResult(DamageOutcome outcome, float damageApplied, float targetHealthAfter)
        {
            Outcome = outcome;
            DamageApplied = damageApplied;
            TargetHealthAfter = targetHealthAfter;
        }

        public DamageOutcome Outcome { get; }
        public float DamageApplied { get; }
        public float TargetHealthAfter { get; }
        public bool WasApplied => Outcome == DamageOutcome.Applied || Outcome == DamageOutcome.Killed;
        public bool TargetDied => Outcome == DamageOutcome.Killed;
    }

    /// <summary>
    /// Central damage gate. Exact armor/status multipliers are intentionally separate
    /// until the source-version damage contract is researched and pinned.
    /// </summary>
    public static class DamagePipeline
    {
        public static DamageResult Apply(
            CombatantState? source,
            CombatantState? target,
            DamageRequest? request,
            DamagePolicy policy)
        {
            if (policy == null) throw new System.ArgumentNullException(nameof(policy));
            if (source == null || target == null || request == null)
                return new DamageResult(DamageOutcome.InvalidRequest, 0.0f, target?.Health ?? 0.0f);
            if (source.Id != request.SourceId || target.Id != request.TargetId)
                return new DamageResult(DamageOutcome.InvalidRequest, 0.0f, target.Health);
            if (!IsFinitePositive(request.RawDamage))
                return new DamageResult(DamageOutcome.InvalidRequest, 0.0f, target.Health);
            if (!source.IsAlive)
                return new DamageResult(DamageOutcome.SourceUnavailable, 0.0f, target.Health);
            if (!target.IsAlive)
                return new DamageResult(DamageOutcome.TargetAlreadyDead, 0.0f, target.Health);

            var selfHit = source.Id == target.Id;
            var sameTeam = !selfHit && source.TeamId != 0 && source.TeamId == target.TeamId;
            if (selfHit && !policy.SelfDamageEnabled)
                return new DamageResult(DamageOutcome.BlockedSelfDamage, 0.0f, target.Health);
            if (sameTeam && !policy.FriendlyFireEnabled)
                return new DamageResult(DamageOutcome.BlockedFriendlyFire, 0.0f, target.Health);
            if (target.InvulnerabilityTicks > 0)
                return new DamageResult(DamageOutcome.BlockedInvulnerability, 0.0f, target.Health);

            var applied = target.ApplyDamage(request.RawDamage);
            var outcome = target.IsAlive ? DamageOutcome.Applied : DamageOutcome.Killed;
            return new DamageResult(outcome, applied, target.Health);
        }

        private static bool IsFinitePositive(float value)
        {
            return !float.IsNaN(value) && !float.IsInfinity(value) && value > 0.0f;
        }
    }
}
