using System;
using System.Collections.Generic;
using Game.Core.Combat;
using Game.Core.Determinism;
using Game.Core.Simulation;

var tests = new List<(string Name, Action Run)>
{
    ("fixed_step_advances_exact_ticks", FixedStepAdvancesExactTicks),
    ("paused_wall_time_is_not_accumulated", PausedWallTimeIsNotAccumulated),
    ("step_cap_preserves_backlog", StepCapPreservesBacklog),
    ("same_seed_produces_same_rng_stream", SameSeedProducesSameRngStream),
    ("rng_integer_range_is_exclusive_and_bounded", RngIntegerRangeIsExclusiveAndBounded),
    ("friendly_fire_enabled_applies_ally_damage", FriendlyFireEnabledAppliesAllyDamage),
    ("friendly_fire_disabled_blocks_ally_damage", FriendlyFireDisabledBlocksAllyDamage),
    ("self_damage_policy_is_independent", SelfDamagePolicyIsIndependent),
    ("invulnerability_blocks_damage", InvulnerabilityBlocksDamage),
    ("lethal_damage_transitions_once_to_dead", LethalDamageTransitionsOnceToDead),
    ("invalid_damage_is_rejected", InvalidDamageIsRejected),
    ("max_health_upgrade_can_restore_added_capacity", MaxHealthUpgradeCanRestoreAddedCapacity)
};

var failures = 0;
foreach (var test in tests)
{
    try
    {
        test.Run();
        Console.WriteLine($"PASS {test.Name}");
    }
    catch (Exception ex)
    {
        failures++;
        Console.WriteLine($"FAIL {test.Name}: {ex.Message}");
    }
}
Console.WriteLine($"RESULT {tests.Count - failures}/{tests.Count}");
return failures == 0 ? 0 : 1;

static void FixedStepAdvancesExactTicks()
{
    var clock = new SimulationClock(0.02, 10);
    var observed = new List<long>();
    var count = clock.Advance(0.10, false, (tick, dt) => observed.Add(tick));
    Assert.Equal(5, count);
    Assert.Equal(5L, clock.Tick);
    Assert.Equal(0L, observed[0]);
    Assert.Equal(4L, observed[4]);
}

static void PausedWallTimeIsNotAccumulated()
{
    var clock = new SimulationClock(0.02, 10);
    Assert.Equal(0, clock.Advance(1.0, true, (_, _) => throw new Exception("paused tick ran")));
    Assert.Equal(0L, clock.Tick);
    Assert.Equal(0.0, clock.PendingSeconds, 1e-9);
    Assert.Equal(1, clock.Advance(0.02, false, (_, _) => { }));
    Assert.Equal(1L, clock.Tick);
}

static void StepCapPreservesBacklog()
{
    var clock = new SimulationClock(0.1, 2);
    Assert.Equal(2, clock.Advance(0.5, false, (_, _) => { }));
    Assert.Equal(0.3, clock.PendingSeconds, 1e-8);
    Assert.Equal(2, clock.Advance(0.0, false, (_, _) => { }));
    Assert.Equal(0.1, clock.PendingSeconds, 1e-8);
}

static void SameSeedProducesSameRngStream()
{
    var a = new DeterministicRng(20261118UL);
    var b = new DeterministicRng(20261118UL);
    for (var i = 0; i < 1000; i++) Assert.Equal(a.NextUInt(), b.NextUInt());
}

static void RngIntegerRangeIsExclusiveAndBounded()
{
    var rng = new DeterministicRng(7UL);
    for (var i = 0; i < 10000; i++)
    {
        var value = rng.NextInt(-3, 9);
        Assert.True(value >= -3 && value < 9, "value outside requested range");
    }
}

static void FriendlyFireEnabledAppliesAllyDamage()
{
    var source = new CombatantState(1, 1, 100);
    var target = new CombatantState(2, 1, 100);
    var result = DamagePipeline.Apply(source, target, new DamageRequest(1, 2, 12, DamageKind.Spell), new DamagePolicy());
    Assert.Equal(DamageOutcome.Applied, result.Outcome);
    Assert.Equal(12.0f, result.DamageApplied, 1e-5f);
    Assert.Equal(88.0f, target.Health, 1e-5f);
}

static void FriendlyFireDisabledBlocksAllyDamage()
{
    var source = new CombatantState(1, 1, 100);
    var target = new CombatantState(2, 1, 100);
    var policy = new DamagePolicy { FriendlyFireEnabled = false };
    var result = DamagePipeline.Apply(source, target, new DamageRequest(1, 2, 12, DamageKind.Spell), policy);
    Assert.Equal(DamageOutcome.BlockedFriendlyFire, result.Outcome);
    Assert.Equal(100.0f, target.Health, 1e-5f);
}

static void SelfDamagePolicyIsIndependent()
{
    var player = new CombatantState(1, 1, 100);
    var policy = new DamagePolicy { SelfDamageEnabled = false };
    var result = DamagePipeline.Apply(player, player, new DamageRequest(1, 1, 12, DamageKind.Hazard), policy);
    Assert.Equal(DamageOutcome.BlockedSelfDamage, result.Outcome);
    Assert.Equal(100.0f, player.Health, 1e-5f);
}

static void InvulnerabilityBlocksDamage()
{
    var source = new CombatantState(1, 1, 100);
    var target = new CombatantState(2, 2, 100);
    target.GrantInvulnerability(2);
    var result = DamagePipeline.Apply(source, target, new DamageRequest(1, 2, 20, DamageKind.Elemental), new DamagePolicy());
    Assert.Equal(DamageOutcome.BlockedInvulnerability, result.Outcome);
    target.AdvanceSimulationTick();
    Assert.Equal(1, target.InvulnerabilityTicks);
}

static void LethalDamageTransitionsOnceToDead()
{
    var source = new CombatantState(1, 1, 100);
    var target = new CombatantState(2, 2, 10);
    var first = DamagePipeline.Apply(source, target, new DamageRequest(1, 2, 10, DamageKind.Spell), new DamagePolicy());
    var second = DamagePipeline.Apply(source, target, new DamageRequest(1, 2, 10, DamageKind.Spell), new DamagePolicy());
    Assert.Equal(DamageOutcome.Killed, first.Outcome);
    Assert.True(first.TargetDied);
    Assert.Equal(DamageOutcome.TargetAlreadyDead, second.Outcome);
    Assert.Equal(0.0f, target.Health, 1e-5f);
}

static void InvalidDamageIsRejected()
{
    var source = new CombatantState(1, 1, 100);
    var target = new CombatantState(2, 2, 100);
    var result = DamagePipeline.Apply(source, target, new DamageRequest(1, 2, float.NaN, DamageKind.Spell), new DamagePolicy());
    Assert.Equal(DamageOutcome.InvalidRequest, result.Outcome);
    Assert.Equal(100.0f, target.Health, 1e-5f);
}

static void MaxHealthUpgradeCanRestoreAddedCapacity()
{
    var attacker = new CombatantState(2, 2, 100);
    var player = new CombatantState(1, 1, 100);
    DamagePipeline.Apply(attacker, player, new DamageRequest(2, 1, 40, DamageKind.Spell), new DamagePolicy());
    player.SetMaxHealth(140, true);
    Assert.Equal(100.0f, player.Health, 1e-5f);
    Assert.Equal(140.0f, player.MaxHealth, 1e-5f);
}

static class Assert
{
    public static void True(bool condition, string message = "assertion failed")
    {
        if (!condition) throw new Exception(message);
    }
    public static void Equal<T>(T expected, T actual)
    {
        if (!EqualityComparer<T>.Default.Equals(expected, actual))
            throw new Exception($"expected {expected}, got {actual}");
    }
    public static void Equal(float expected, float actual, float tolerance)
    {
        if (Math.Abs(expected - actual) > tolerance)
            throw new Exception($"expected {expected}, got {actual}");
    }
    public static void Equal(double expected, double actual, double tolerance)
    {
        if (Math.Abs(expected - actual) > tolerance)
            throw new Exception($"expected {expected}, got {actual}");
    }
}
