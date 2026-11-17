using System;
using System.Collections.Generic;
using Game.Core.Determinism;

namespace Game.Core.Spells
{
    public enum SpellTargetingMode
    {
        NearestEnemy = 0,
        LowestHealthRatio = 1,
        RandomEnemy = 2,
        None = 3
    }

    public enum ProjectilePattern
    {
        Single = 0,
        Spread = 1,
        Radial = 2
    }

    public enum SpellCastOutcome
    {
        Cast = 0,
        OnCooldown = 1,
        NoTarget = 2,
        InvalidState = 3
    }

    public sealed class SpellDefinition
    {
        public SpellDefinition(string id, int cooldownTicks, float range, float damage,
            float projectileSpeed, int projectileCount, float spreadRadians, int pierceCount,
            SpellTargetingMode targetingMode, ProjectilePattern pattern)
        {
            if (string.IsNullOrWhiteSpace(id)) throw new ArgumentException("A stable spell ID is required.", nameof(id));
            if (cooldownTicks < 0) throw new ArgumentOutOfRangeException(nameof(cooldownTicks));
            if (!IsFinitePositive(range)) throw new ArgumentOutOfRangeException(nameof(range));
            if (!IsFinitePositive(damage)) throw new ArgumentOutOfRangeException(nameof(damage));
            if (!IsFinitePositive(projectileSpeed)) throw new ArgumentOutOfRangeException(nameof(projectileSpeed));
            if (projectileCount <= 0) throw new ArgumentOutOfRangeException(nameof(projectileCount));
            if (!IsFiniteNonNegative(spreadRadians) || spreadRadians > Math.PI * 2.0)
                throw new ArgumentOutOfRangeException(nameof(spreadRadians));
            if (pierceCount < 0) throw new ArgumentOutOfRangeException(nameof(pierceCount));
            if (targetingMode == SpellTargetingMode.None && pattern != ProjectilePattern.Radial)
                throw new ArgumentException("Targetless casts currently require a radial projectile pattern.", nameof(pattern));
            if (targetingMode != SpellTargetingMode.None && pattern == ProjectilePattern.Radial)
                throw new ArgumentException("Radial patterns use targetless casting in this kernel.", nameof(targetingMode));

            Id = id;
            CooldownTicks = cooldownTicks;
            Range = range;
            Damage = damage;
            ProjectileSpeed = projectileSpeed;
            ProjectileCount = pattern == ProjectilePattern.Single ? 1 : projectileCount;
            SpreadRadians = spreadRadians;
            PierceCount = pierceCount;
            TargetingMode = targetingMode;
            Pattern = pattern;
        }

        public string Id { get; }
        public int CooldownTicks { get; }
        public float Range { get; }
        public float Damage { get; }
        public float ProjectileSpeed { get; }
        public int ProjectileCount { get; }
        public float SpreadRadians { get; }
        public int PierceCount { get; }
        public SpellTargetingMode TargetingMode { get; }
        public ProjectilePattern Pattern { get; }

        private static bool IsFinitePositive(float value) =>
            !float.IsNaN(value) && !float.IsInfinity(value) && value > 0.0f;
        private static bool IsFiniteNonNegative(float value) =>
            !float.IsNaN(value) && !float.IsInfinity(value) && value >= 0.0f;
    }

    public sealed class SpellRuntimeState
    {
        public int CooldownRemainingTicks { get; private set; }
        public int Level { get; private set; } = 1;

        public void AdvanceTick()
        {
            if (CooldownRemainingTicks > 0) CooldownRemainingTicks--;
        }

        public void SetLevel(int level)
        {
            if (level < 1) throw new ArgumentOutOfRangeException(nameof(level));
            Level = level;
        }

        internal void StartCooldown(int ticks)
        {
            CooldownRemainingTicks = Math.Max(0, ticks);
        }
    }

    public readonly struct TargetCandidate
    {
        public TargetCandidate(int id, int teamId, float x, float y, float health, float maxHealth)
        {
            if (id < 0) throw new ArgumentOutOfRangeException(nameof(id));
            if (!IsFinite(x) || !IsFinite(y)) throw new ArgumentOutOfRangeException(nameof(x));
            if (!IsFiniteNonNegative(health)) throw new ArgumentOutOfRangeException(nameof(health));
            if (!IsFinitePositive(maxHealth)) throw new ArgumentOutOfRangeException(nameof(maxHealth));
            Id = id;
            TeamId = teamId;
            X = x;
            Y = y;
            Health = health;
            MaxHealth = maxHealth;
        }

        public int Id { get; }
        public int TeamId { get; }
        public float X { get; }
        public float Y { get; }
        public float Health { get; }
        public float MaxHealth { get; }
        public bool IsAlive => Health > 0.0f;
        public float HealthRatio => Health / MaxHealth;

        private static bool IsFinite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
        private static bool IsFinitePositive(float value) => IsFinite(value) && value > 0.0f;
        private static bool IsFiniteNonNegative(float value) => IsFinite(value) && value >= 0.0f;
    }

    public readonly struct ProjectileSpawn
    {
        public ProjectileSpawn(int sourceId, int targetId, int index, float x, float y,
            float velocityX, float velocityY, float damage, int pierceCount)
        {
            SourceId = sourceId;
            TargetId = targetId;
            Index = index;
            X = x;
            Y = y;
            VelocityX = velocityX;
            VelocityY = velocityY;
            Damage = damage;
            PierceCount = pierceCount;
        }

        public int SourceId { get; }
        public int TargetId { get; }
        public int Index { get; }
        public float X { get; }
        public float Y { get; }
        public float VelocityX { get; }
        public float VelocityY { get; }
        public float Damage { get; }
        public int PierceCount { get; }
    }

    public sealed class SpellCastResult
    {
        internal SpellCastResult(SpellCastOutcome outcome, int targetId, ProjectileSpawn[] projectiles)
        {
            Outcome = outcome;
            TargetId = targetId;
            Projectiles = projectiles;
        }

        public SpellCastOutcome Outcome { get; }
        public int TargetId { get; }
        public ProjectileSpawn[] Projectiles { get; }
        public bool WasCast => Outcome == SpellCastOutcome.Cast;
    }

    /// <summary>
    /// Data-driven auto-target spell execution. It emits deterministic projectile spawn
    /// commands; world collision and damage are resolved by the simulation, not by rendering.
    /// </summary>
    public static class SpellSystem
    {
        public static SpellCastResult TryCast(
            SpellDefinition definition,
            SpellRuntimeState? runtime,
            int casterId,
            int casterTeamId,
            float casterX,
            float casterY,
            IReadOnlyList<TargetCandidate> candidates,
            DeterministicRng? rng = null)
        {
            if (definition == null || runtime == null || candidates == null ||
                !IsFinite(casterX) || !IsFinite(casterY))
                return new SpellCastResult(SpellCastOutcome.InvalidState, -1, Array.Empty<ProjectileSpawn>());

            if (runtime.CooldownRemainingTicks > 0)
                return new SpellCastResult(SpellCastOutcome.OnCooldown, -1, Array.Empty<ProjectileSpawn>());

            TargetCandidate? target = null;
            if (definition.TargetingMode != SpellTargetingMode.None)
            {
                var eligible = new List<TargetCandidate>();
                var rangeSquared = definition.Range * definition.Range;
                for (var i = 0; i < candidates.Count; i++)
                {
                    var candidate = candidates[i];
                    if (!candidate.IsAlive || candidate.Id == casterId || candidate.TeamId == casterTeamId)
                        continue;
                    var dx = candidate.X - casterX;
                    var dy = candidate.Y - casterY;
                    if (dx * dx + dy * dy <= rangeSquared) eligible.Add(candidate);
                }

                if (eligible.Count == 0)
                    return new SpellCastResult(SpellCastOutcome.NoTarget, -1, Array.Empty<ProjectileSpawn>());

                eligible.Sort((a, b) => a.Id.CompareTo(b.Id));
                target = SelectTarget(eligible, definition.TargetingMode, casterX, casterY, rng);
                if (!target.HasValue)
                    return new SpellCastResult(SpellCastOutcome.InvalidState, -1, Array.Empty<ProjectileSpawn>());
            }

            var baseAngle = target.HasValue
                ? Math.Atan2(target.Value.Y - casterY, target.Value.X - casterX)
                : 0.0;
            var output = new ProjectileSpawn[definition.ProjectileCount];

            for (var i = 0; i < output.Length; i++)
            {
                var angle = baseAngle;
                if (definition.Pattern == ProjectilePattern.Spread && output.Length > 1)
                {
                    var step = definition.SpreadRadians / (output.Length - 1);
                    angle += -definition.SpreadRadians * 0.5 + step * i;
                }
                else if (definition.Pattern == ProjectilePattern.Radial)
                {
                    angle = i * (Math.PI * 2.0 / output.Length);
                }

                var vx = (float)(Math.Cos(angle) * definition.ProjectileSpeed);
                var vy = (float)(Math.Sin(angle) * definition.ProjectileSpeed);
                output[i] = new ProjectileSpawn(casterId, target?.Id ?? -1, i,
                    casterX, casterY, vx, vy, definition.Damage, definition.PierceCount);
            }

            runtime.StartCooldown(definition.CooldownTicks);
            return new SpellCastResult(SpellCastOutcome.Cast, target?.Id ?? -1, output);
        }

        private static TargetCandidate? SelectTarget(List<TargetCandidate> eligible,
            SpellTargetingMode mode, float casterX, float casterY, DeterministicRng? rng)
        {
            if (mode == SpellTargetingMode.RandomEnemy)
            {
                if (rng == null) return null;
                return eligible[rng.NextInt(0, eligible.Count)];
            }

            var best = eligible[0];
            var bestDistance = DistanceSquared(best, casterX, casterY);
            for (var i = 1; i < eligible.Count; i++)
            {
                var candidate = eligible[i];
                var distance = DistanceSquared(candidate, casterX, casterY);
                if (mode == SpellTargetingMode.NearestEnemy)
                {
                    if (distance < bestDistance || (distance == bestDistance && candidate.Id < best.Id))
                    {
                        best = candidate;
                        bestDistance = distance;
                    }
                }
                else if (mode == SpellTargetingMode.LowestHealthRatio)
                {
                    if (candidate.HealthRatio < best.HealthRatio ||
                        (candidate.HealthRatio == best.HealthRatio &&
                         (distance < bestDistance || (distance == bestDistance && candidate.Id < best.Id))))
                    {
                        best = candidate;
                        bestDistance = distance;
                    }
                }
            }
            return best;
        }

        private static float DistanceSquared(TargetCandidate target, float x, float y)
        {
            var dx = target.X - x;
            var dy = target.Y - y;
            return dx * dx + dy * dy;
        }

        private static bool IsFinite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
    }
}
