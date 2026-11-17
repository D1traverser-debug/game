using System;
using System.Collections.Generic;
using Game.Core.Combat;

namespace Game.Core.Projectiles
{
    public sealed class ProjectileState
    {
        private readonly HashSet<int> _hitTargets = new HashSet<int>();

        public ProjectileState(int id, Spells.ProjectileSpawn spawn, float radius, int lifetimeTicks)
        {
            if (id < 0) throw new ArgumentOutOfRangeException(nameof(id));
            if (!IsFinitePositive(radius)) throw new ArgumentOutOfRangeException(nameof(radius));
            if (lifetimeTicks <= 0) throw new ArgumentOutOfRangeException(nameof(lifetimeTicks));
            if (!IsFinite(spawn.X) || !IsFinite(spawn.Y) ||
                !IsFinite(spawn.VelocityX) || !IsFinite(spawn.VelocityY) ||
                !IsFinitePositive(spawn.Damage))
                throw new ArgumentException("Projectile spawn payload must be finite and have positive damage.", nameof(spawn));

            Id = id;
            SourceId = spawn.SourceId;
            X = spawn.X;
            Y = spawn.Y;
            VelocityX = spawn.VelocityX;
            VelocityY = spawn.VelocityY;
            Damage = spawn.Damage;
            Radius = radius;
            LifetimeTicksRemaining = lifetimeTicks;
            PierceRemaining = spawn.PierceCount;
        }

        public int Id { get; }
        public int SourceId { get; }
        public float X { get; private set; }
        public float Y { get; private set; }
        public float VelocityX { get; }
        public float VelocityY { get; }
        public float Damage { get; }
        public float Radius { get; }
        public int LifetimeTicksRemaining { get; private set; }
        public int PierceRemaining { get; private set; }
        public bool IsAlive { get; private set; } = true;

        internal bool HasHit(int targetId) => _hitTargets.Contains(targetId);
        internal void MarkHit(int targetId) => _hitTargets.Add(targetId);
        internal void ConsumePierce() { if (PierceRemaining > 0) PierceRemaining--; }
        internal void MoveTo(float x, float y) { X = x; Y = y; }
        internal void AdvanceLifetime() { if (LifetimeTicksRemaining > 0) LifetimeTicksRemaining--; }
        internal void Destroy() { IsAlive = false; }

        private static bool IsFinite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
        private static bool IsFinitePositive(float value) => IsFinite(value) && value > 0.0f;
    }

    public readonly struct ProjectileTarget
    {
        public ProjectileTarget(CombatantState combatant, float x, float y, float radius)
        {
            if (combatant == null) throw new ArgumentNullException(nameof(combatant));
            if (!IsFinite(x) || !IsFinite(y)) throw new ArgumentOutOfRangeException(nameof(x));
            if (!IsFiniteNonNegative(radius)) throw new ArgumentOutOfRangeException(nameof(radius));
            Combatant = combatant;
            X = x;
            Y = y;
            Radius = radius;
        }

        public CombatantState Combatant { get; }
        public int Id => Combatant.Id;
        public float X { get; }
        public float Y { get; }
        public float Radius { get; }

        private static bool IsFinite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
        private static bool IsFiniteNonNegative(float value) => IsFinite(value) && value >= 0.0f;
    }

    public readonly struct ProjectileHit
    {
        public ProjectileHit(int projectileId, int targetId, DamageOutcome outcome, float damageApplied)
        {
            ProjectileId = projectileId;
            TargetId = targetId;
            Outcome = outcome;
            DamageApplied = damageApplied;
        }

        public int ProjectileId { get; }
        public int TargetId { get; }
        public DamageOutcome Outcome { get; }
        public float DamageApplied { get; }
    }

    public sealed class ProjectileStepResult
    {
        internal ProjectileStepResult(ProjectileHit[] hits, int destroyedCount)
        {
            Hits = hits;
            DestroyedCount = destroyedCount;
        }

        public ProjectileHit[] Hits { get; }
        public int DestroyedCount { get; }
    }

    /// <summary>
    /// Fixed-tick projectile motion with swept-circle collision, deterministic hit ordering,
    /// pierce accounting and one-hit-per-target protection.
    /// </summary>
    public static class ProjectileSystem
    {
        private readonly struct CollisionCandidate
        {
            public CollisionCandidate(double t, ProjectileTarget target)
            {
                T = t;
                Target = target;
            }
            public double T { get; }
            public ProjectileTarget Target { get; }
        }

        public static ProjectileStepResult Step(
            IReadOnlyList<ProjectileState> projectiles,
            IReadOnlyList<ProjectileTarget> targets,
            IReadOnlyDictionary<int, CombatantState> combatants,
            double deltaSeconds,
            DamagePolicy damagePolicy)
        {
            if (projectiles == null) throw new ArgumentNullException(nameof(projectiles));
            if (targets == null) throw new ArgumentNullException(nameof(targets));
            if (combatants == null) throw new ArgumentNullException(nameof(combatants));
            if (damagePolicy == null) throw new ArgumentNullException(nameof(damagePolicy));
            if (double.IsNaN(deltaSeconds) || double.IsInfinity(deltaSeconds) || deltaSeconds <= 0.0)
                throw new ArgumentOutOfRangeException(nameof(deltaSeconds));

            var hits = new List<ProjectileHit>();
            var destroyed = 0;

            for (var p = 0; p < projectiles.Count; p++)
            {
                var projectile = projectiles[p];
                if (!projectile.IsAlive) continue;
                if (projectile.LifetimeTicksRemaining <= 0 ||
                    !combatants.TryGetValue(projectile.SourceId, out var source) ||
                    !source.IsAlive)
                {
                    projectile.Destroy();
                    destroyed++;
                    continue;
                }

                var startX = projectile.X;
                var startY = projectile.Y;
                var endX = startX + (float)(projectile.VelocityX * deltaSeconds);
                var endY = startY + (float)(projectile.VelocityY * deltaSeconds);
                var collisions = new List<CollisionCandidate>();

                for (var t = 0; t < targets.Count; t++)
                {
                    var target = targets[t];
                    if (!target.Combatant.IsAlive || projectile.HasHit(target.Id)) continue;
                    if (target.Id == source.Id && !damagePolicy.SelfDamageEnabled) continue;
                    if (target.Id != source.Id && source.TeamId != 0 &&
                        target.Combatant.TeamId == source.TeamId && !damagePolicy.FriendlyFireEnabled)
                        continue;

                    var combinedRadius = projectile.Radius + target.Radius;
                    if (TryGetSegmentCircleHit(startX, startY, endX, endY,
                        target.X, target.Y, combinedRadius, out var hitT))
                        collisions.Add(new CollisionCandidate(hitT, target));
                }

                collisions.Sort((a, b) =>
                {
                    var byTime = a.T.CompareTo(b.T);
                    return byTime != 0 ? byTime : a.Target.Id.CompareTo(b.Target.Id);
                });

                for (var c = 0; c < collisions.Count; c++)
                {
                    var target = collisions[c].Target;
                    if (!projectile.IsAlive || projectile.HasHit(target.Id) || !target.Combatant.IsAlive)
                        continue;

                    var damage = DamagePipeline.Apply(source, target.Combatant,
                        new DamageRequest(source.Id, target.Id, projectile.Damage, DamageKind.Spell),
                        damagePolicy);
                    projectile.MarkHit(target.Id);
                    hits.Add(new ProjectileHit(projectile.Id, target.Id, damage.Outcome, damage.DamageApplied));

                    if (projectile.PierceRemaining > 0)
                        projectile.ConsumePierce();
                    else
                    {
                        projectile.Destroy();
                        destroyed++;
                    }
                }

                projectile.MoveTo(endX, endY);
                projectile.AdvanceLifetime();
                if (projectile.IsAlive && projectile.LifetimeTicksRemaining <= 0)
                {
                    projectile.Destroy();
                    destroyed++;
                }
            }

            return new ProjectileStepResult(hits.ToArray(), destroyed);
        }

        private static bool TryGetSegmentCircleHit(float x0, float y0, float x1, float y1,
            float cx, float cy, float radius, out double hitT)
        {
            var dx = (double)x1 - x0;
            var dy = (double)y1 - y0;
            var fx = (double)x0 - cx;
            var fy = (double)y0 - cy;
            var c = fx * fx + fy * fy - (double)radius * radius;
            if (c <= 0.0)
            {
                hitT = 0.0;
                return true;
            }

            var a = dx * dx + dy * dy;
            if (a <= 1e-12)
            {
                hitT = 0.0;
                return false;
            }

            var b = 2.0 * (fx * dx + fy * dy);
            var discriminant = b * b - 4.0 * a * c;
            if (discriminant < 0.0)
            {
                hitT = 0.0;
                return false;
            }

            var root = Math.Sqrt(discriminant);
            var first = (-b - root) / (2.0 * a);
            var second = (-b + root) / (2.0 * a);
            if (first >= 0.0 && first <= 1.0)
            {
                hitT = first;
                return true;
            }
            if (second >= 0.0 && second <= 1.0)
            {
                hitT = second;
                return true;
            }

            hitT = 0.0;
            return false;
        }
    }
}
