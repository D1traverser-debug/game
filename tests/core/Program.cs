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
    ("max_health_upgrade_can_restore_added_capacity", MaxHealthUpgradeCanRestoreAddedCapacity),
    ("simulation_events_are_monotonic_and_drainable", SimulationEventsAreMonotonicAndDrainable),
    ("simulation_event_time_cannot_move_backwards", SimulationEventTimeCannotMoveBackwards),
    ("valid_player_command_is_accepted", ValidPlayerCommandIsAccepted),
    ("unknown_player_command_is_rejected", UnknownPlayerCommandIsRejected),
    ("duplicate_player_command_is_rejected", DuplicatePlayerCommandIsRejected),
    ("stale_and_future_commands_are_rejected", StaleAndFutureCommandsAreRejected),
    ("invalid_movement_is_rejected", InvalidMovementIsRejected),
    ("unknown_button_bits_are_rejected", UnknownButtonBitsAreRejected),
    ("negative_sequence_is_rejected", NegativeSequenceIsRejected),
    ("negative_client_tick_is_rejected", NegativeClientTickIsRejected),
    ("auto_target_selects_nearest_enemy_not_ally_or_out_of_range", AutoTargetSelectsNearestEnemy),
    ("lowest_health_ratio_targeting_is_deterministic", LowestHealthRatioTargetingIsDeterministic),
    ("random_targeting_uses_seeded_rng", RandomTargetingUsesSeededRng),
    ("spell_cooldown_blocks_recast_until_ticks_elapse", SpellCooldownBlocksRecast),
    ("spread_pattern_is_symmetric", SpreadPatternIsSymmetric),
    ("radial_pattern_is_evenly_spaced_without_target", RadialPatternIsEvenlySpaced),
    ("no_target_does_not_consume_cooldown", NoTargetDoesNotConsumeCooldown),
    ("invalid_targeting_pattern_is_rejected", InvalidTargetingPatternIsRejected),
    ("same_seed_produces_same_projectile_spawns", SameSeedProducesSameProjectileSpawns),
    ("single_pattern_emits_exactly_one_projectile", SinglePatternEmitsOneProjectile),
    ("projectile_moves_and_lifetime_ticks", ProjectileMovesAndLifetimeTicks),
    ("swept_collision_hits_fast_projectile", SweptCollisionHitsFastProjectile),
    ("projectile_hit_applies_damage_and_destroys", ProjectileHitAppliesDamageAndDestroys),
    ("piercing_projectile_hits_in_path_order", PiercingProjectileHitsInPathOrder),
    ("projectile_does_not_hit_same_target_twice", ProjectileDoesNotHitSameTargetTwice),
    ("friendly_fire_disabled_projectile_passes_through_ally", FriendlyFireDisabledProjectilePassesThroughAlly),
    ("friendly_fire_enabled_projectile_hits_ally_first", FriendlyFireEnabledProjectileHitsAllyFirst),
    ("invulnerability_blocks_projectile_damage", InvulnerabilityBlocksProjectileDamage),
    ("projectile_expires_at_lifetime", ProjectileExpiresAtLifetime),
    ("simultaneous_collision_tie_breaks_by_target_id", SimultaneousCollisionTieBreaksByTargetId),
    ("self_damage_policy_applies_to_projectiles", SelfDamagePolicyAppliesToProjectiles),
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

static void SimulationEventsAreMonotonicAndDrainable()
{
    var buffer = new Game.Core.Events.SimulationEventBuffer();
    var first = buffer.Publish(4, Game.Core.Events.SimulationEventType.SpellCast, 1, -1, "spell.arc", 1, 2, 3);
    var second = buffer.Publish(4, Game.Core.Events.SimulationEventType.DamageResolved, 1, 2, "damage.fire", 12, 5, 6);
    Assert.Equal(0L, first.Sequence);
    Assert.Equal(1L, second.Sequence);
    Assert.Equal(2, buffer.Count);
    var drained = buffer.Drain();
    Assert.Equal(2, drained.Length);
    Assert.Equal(0, buffer.Count);
    Assert.Equal(2L, buffer.NextSequence);
}

static void SimulationEventTimeCannotMoveBackwards()
{
    var buffer = new Game.Core.Events.SimulationEventBuffer();
    buffer.Publish(10, Game.Core.Events.SimulationEventType.SpellCast);
    var threw = false;
    try { buffer.Publish(9, Game.Core.Events.SimulationEventType.DamageResolved); }
    catch (InvalidOperationException) { threw = true; }
    Assert.True(threw, "event time moved backwards without rejection");
}

static void ValidPlayerCommandIsAccepted()
{
    var validator = new Game.Core.Networking.PlayerCommandValidator();
    var players = new HashSet<int> { 1, 2, 3, 4 };
    var command = new Game.Core.Networking.PlayerInputCommand(2, 1, 100, 0.6f, 0.8f,
        Game.Core.Networking.PlayerButtons.CastPrimary | Game.Core.Networking.PlayerButtons.Dodge);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.Accepted, validator.Validate(command, players, 100).Outcome);
}

static void UnknownPlayerCommandIsRejected()
{
    var validator = new Game.Core.Networking.PlayerCommandValidator();
    var players = new HashSet<int> { 1, 2, 3, 4 };
    var command = new Game.Core.Networking.PlayerInputCommand(5, 1, 100, 0, 0, Game.Core.Networking.PlayerButtons.None);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.UnknownPlayer, validator.Validate(command, players, 100).Outcome);
}

static void DuplicatePlayerCommandIsRejected()
{
    var validator = new Game.Core.Networking.PlayerCommandValidator();
    var players = new HashSet<int> { 1 };
    var command = new Game.Core.Networking.PlayerInputCommand(1, 7, 100, 0, 0, Game.Core.Networking.PlayerButtons.None);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.Accepted, validator.Validate(command, players, 100).Outcome);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.DuplicateOrOutOfOrder, validator.Validate(command, players, 100).Outcome);
}

static void StaleAndFutureCommandsAreRejected()
{
    var validator = new Game.Core.Networking.PlayerCommandValidator(maxPastTicks: 10, maxFutureTicks: 2);
    var players = new HashSet<int> { 1 };
    var stale = new Game.Core.Networking.PlayerInputCommand(1, 1, 89, 0, 0, Game.Core.Networking.PlayerButtons.None);
    var future = new Game.Core.Networking.PlayerInputCommand(1, 2, 103, 0, 0, Game.Core.Networking.PlayerButtons.None);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.TickOutsideWindow, validator.Validate(stale, players, 100).Outcome);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.TickOutsideWindow, validator.Validate(future, players, 100).Outcome);
}

static void InvalidMovementIsRejected()
{
    var validator = new Game.Core.Networking.PlayerCommandValidator();
    var players = new HashSet<int> { 1 };
    var tooFast = new Game.Core.Networking.PlayerInputCommand(1, 1, 100, 1.0f, 1.0f, Game.Core.Networking.PlayerButtons.None);
    var nan = new Game.Core.Networking.PlayerInputCommand(1, 2, 100, float.NaN, 0.0f, Game.Core.Networking.PlayerButtons.None);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.InvalidMovement, validator.Validate(tooFast, players, 100).Outcome);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.InvalidMovement, validator.Validate(nan, players, 100).Outcome);
}

static void UnknownButtonBitsAreRejected()
{
    var validator = new Game.Core.Networking.PlayerCommandValidator();
    var players = new HashSet<int> { 1 };
    var command = new Game.Core.Networking.PlayerInputCommand(1, 1, 100, 0, 0, (Game.Core.Networking.PlayerButtons)32768);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.InvalidButtons, validator.Validate(command, players, 100).Outcome);
}

static void NegativeSequenceIsRejected()
{
    var validator = new Game.Core.Networking.PlayerCommandValidator();
    var players = new HashSet<int> { 1 };
    var command = new Game.Core.Networking.PlayerInputCommand(1, -1, 100, 0, 0, Game.Core.Networking.PlayerButtons.None);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.DuplicateOrOutOfOrder, validator.Validate(command, players, 100).Outcome);
}

static void NegativeClientTickIsRejected()
{
    var validator = new Game.Core.Networking.PlayerCommandValidator();
    var players = new HashSet<int> { 1 };
    var command = new Game.Core.Networking.PlayerInputCommand(1, 1, -1, 0, 0, Game.Core.Networking.PlayerButtons.None);
    Assert.Equal(Game.Core.Networking.CommandValidationOutcome.TickOutsideWindow, validator.Validate(command, players, 100).Outcome);
}

static void AutoTargetSelectsNearestEnemy()
{
    var def = new Game.Core.Spells.SpellDefinition("spell.test_bolt", 5, 10, 12, 8, 1, 0, 0,
        Game.Core.Spells.SpellTargetingMode.NearestEnemy, Game.Core.Spells.ProjectilePattern.Single);
    var runtime = new Game.Core.Spells.SpellRuntimeState();
    var targets = new List<Game.Core.Spells.TargetCandidate>
    {
        new(2, 1, 1, 0, 10, 10),
        new(3, 2, 4, 0, 10, 10),
        new(4, 2, 2, 0, 10, 10),
        new(5, 2, 30, 0, 10, 10),
        new(6, 2, 0.5f, 0, 0, 10)
    };
    var result = Game.Core.Spells.SpellSystem.TryCast(def, runtime, 1, 1, 0, 0, targets);
    Assert.Equal(Game.Core.Spells.SpellCastOutcome.Cast, result.Outcome);
    Assert.Equal(4, result.TargetId);
}

static void LowestHealthRatioTargetingIsDeterministic()
{
    var def = new Game.Core.Spells.SpellDefinition("spell.test_seek", 0, 20, 8, 6, 1, 0, 0,
        Game.Core.Spells.SpellTargetingMode.LowestHealthRatio, Game.Core.Spells.ProjectilePattern.Single);
    var targets = new List<Game.Core.Spells.TargetCandidate>
    {
        new(8, 2, 1, 0, 40, 100),
        new(4, 2, 4, 0, 10, 100),
        new(3, 2, 2, 0, 1, 10)
    };
    var result = Game.Core.Spells.SpellSystem.TryCast(def, new Game.Core.Spells.SpellRuntimeState(),
        1, 1, 0, 0, targets);
    Assert.Equal(3, result.TargetId);
}

static void RandomTargetingUsesSeededRng()
{
    var def = new Game.Core.Spells.SpellDefinition("spell.test_random", 0, 20, 8, 6, 1, 0, 0,
        Game.Core.Spells.SpellTargetingMode.RandomEnemy, Game.Core.Spells.ProjectilePattern.Single);
    var targets = new List<Game.Core.Spells.TargetCandidate>
    {
        new(4, 2, 1, 0, 10, 10),
        new(2, 2, 2, 0, 10, 10),
        new(3, 2, 3, 0, 10, 10)
    };
    var a = Game.Core.Spells.SpellSystem.TryCast(def, new Game.Core.Spells.SpellRuntimeState(),
        1, 1, 0, 0, targets, new DeterministicRng(42));
    var b = Game.Core.Spells.SpellSystem.TryCast(def, new Game.Core.Spells.SpellRuntimeState(),
        1, 1, 0, 0, targets, new DeterministicRng(42));
    Assert.Equal(a.TargetId, b.TargetId);
}

static void SpellCooldownBlocksRecast()
{
    var def = new Game.Core.Spells.SpellDefinition("spell.cooldown", 2, 10, 10, 5, 1, 0, 0,
        Game.Core.Spells.SpellTargetingMode.NearestEnemy, Game.Core.Spells.ProjectilePattern.Single);
    var runtime = new Game.Core.Spells.SpellRuntimeState();
    var targets = new List<Game.Core.Spells.TargetCandidate> { new(2, 2, 1, 0, 10, 10) };
    Assert.Equal(Game.Core.Spells.SpellCastOutcome.Cast,
        Game.Core.Spells.SpellSystem.TryCast(def, runtime, 1, 1, 0, 0, targets).Outcome);
    Assert.Equal(2, runtime.CooldownRemainingTicks);
    Assert.Equal(Game.Core.Spells.SpellCastOutcome.OnCooldown,
        Game.Core.Spells.SpellSystem.TryCast(def, runtime, 1, 1, 0, 0, targets).Outcome);
    runtime.AdvanceTick();
    runtime.AdvanceTick();
    Assert.Equal(Game.Core.Spells.SpellCastOutcome.Cast,
        Game.Core.Spells.SpellSystem.TryCast(def, runtime, 1, 1, 0, 0, targets).Outcome);
}

static void SpreadPatternIsSymmetric()
{
    var def = new Game.Core.Spells.SpellDefinition("spell.fan", 0, 20, 5, 10, 3, 0.4f, 0,
        Game.Core.Spells.SpellTargetingMode.NearestEnemy, Game.Core.Spells.ProjectilePattern.Spread);
    var targets = new List<Game.Core.Spells.TargetCandidate> { new(2, 2, 10, 0, 10, 10) };
    var result = Game.Core.Spells.SpellSystem.TryCast(def, new Game.Core.Spells.SpellRuntimeState(),
        1, 1, 0, 0, targets);
    Assert.Equal(3, result.Projectiles.Length);
    Assert.True(result.Projectiles[0].VelocityY < 0);
    Assert.True(Math.Abs(result.Projectiles[0].VelocityY + result.Projectiles[2].VelocityY) < 1e-4);
    Assert.True(Math.Abs(result.Projectiles[1].VelocityY) < 1e-4);
}

static void RadialPatternIsEvenlySpaced()
{
    var def = new Game.Core.Spells.SpellDefinition("spell.pulse", 0, 20, 7, 10, 4, 0, 0,
        Game.Core.Spells.SpellTargetingMode.None, Game.Core.Spells.ProjectilePattern.Radial);
    var result = Game.Core.Spells.SpellSystem.TryCast(def, new Game.Core.Spells.SpellRuntimeState(),
        1, 1, 2, 3, Array.Empty<Game.Core.Spells.TargetCandidate>());
    Assert.Equal(Game.Core.Spells.SpellCastOutcome.Cast, result.Outcome);
    Assert.Equal(-1, result.TargetId);
    Assert.Equal(4, result.Projectiles.Length);
    Assert.True(Math.Abs(result.Projectiles[0].VelocityX - 10) < 1e-4);
    Assert.True(Math.Abs(result.Projectiles[1].VelocityY - 10) < 1e-4);
    Assert.True(Math.Abs(result.Projectiles[2].VelocityX + 10) < 1e-4);
    Assert.True(Math.Abs(result.Projectiles[3].VelocityY + 10) < 1e-4);
}

static void NoTargetDoesNotConsumeCooldown()
{
    var def = new Game.Core.Spells.SpellDefinition("spell.empty", 9, 5, 7, 8, 1, 0, 0,
        Game.Core.Spells.SpellTargetingMode.NearestEnemy, Game.Core.Spells.ProjectilePattern.Single);
    var runtime = new Game.Core.Spells.SpellRuntimeState();
    var result = Game.Core.Spells.SpellSystem.TryCast(def, runtime, 1, 1, 0, 0,
        new List<Game.Core.Spells.TargetCandidate> { new(2, 2, 8, 0, 10, 10) });
    Assert.Equal(Game.Core.Spells.SpellCastOutcome.NoTarget, result.Outcome);
    Assert.Equal(0, runtime.CooldownRemainingTicks);
}

static void InvalidTargetingPatternIsRejected()
{
    var threw = false;
    try
    {
        _ = new Game.Core.Spells.SpellDefinition("spell.invalid", 1, 5, 1, 1, 3, 0, 0,
            Game.Core.Spells.SpellTargetingMode.None, Game.Core.Spells.ProjectilePattern.Spread);
    }
    catch (ArgumentException) { threw = true; }
    Assert.True(threw, "targetless spread spell was accepted");
}

static void SameSeedProducesSameProjectileSpawns()
{
    var def = new Game.Core.Spells.SpellDefinition("spell.random", 0, 20, 8, 6, 3, 0.6f, 1,
        Game.Core.Spells.SpellTargetingMode.RandomEnemy, Game.Core.Spells.ProjectilePattern.Spread);
    var targets = new List<Game.Core.Spells.TargetCandidate>
    {
        new(2, 2, 10, 0, 10, 10), new(3, 2, 0, 10, 10, 10), new(4, 2, -10, 0, 10, 10)
    };
    var a = Game.Core.Spells.SpellSystem.TryCast(def, new Game.Core.Spells.SpellRuntimeState(),
        1, 1, 0, 0, targets, new DeterministicRng(987));
    var b = Game.Core.Spells.SpellSystem.TryCast(def, new Game.Core.Spells.SpellRuntimeState(),
        1, 1, 0, 0, targets, new DeterministicRng(987));
    Assert.Equal(a.TargetId, b.TargetId);
    for (var i = 0; i < a.Projectiles.Length; i++)
    {
        Assert.Equal(a.Projectiles[i].VelocityX, b.Projectiles[i].VelocityX, 1e-5f);
        Assert.Equal(a.Projectiles[i].VelocityY, b.Projectiles[i].VelocityY, 1e-5f);
    }
}

static void SinglePatternEmitsOneProjectile()
{
    var def = new Game.Core.Spells.SpellDefinition("spell.single", 0, 10, 5, 4, 7, 1.2f, 0,
        Game.Core.Spells.SpellTargetingMode.NearestEnemy, Game.Core.Spells.ProjectilePattern.Single);
    var targets = new List<Game.Core.Spells.TargetCandidate> { new(2, 2, 1, 0, 10, 10) };
    var result = Game.Core.Spells.SpellSystem.TryCast(def, new Game.Core.Spells.SpellRuntimeState(),
        1, 1, 0, 0, targets);
    Assert.Equal(1, result.Projectiles.Length);
}

static void ProjectileMovesAndLifetimeTicks()
{
    var source = new CombatantState(1, 1, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, -1, 0, 0, 0, 2, 0, 5, 0);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.1f, 3);
    var combatants = new Dictionary<int, CombatantState> { [1] = source };
    Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile },
        Array.Empty<Game.Core.Projectiles.ProjectileTarget>(), combatants, 0.5, new DamagePolicy());
    Assert.Equal(1.0f, projectile.X, 1e-5f);
    Assert.Equal(2, projectile.LifetimeTicksRemaining);
    Assert.True(projectile.IsAlive);
}

static void SweptCollisionHitsFastProjectile()
{
    var source = new CombatantState(1, 1, 100);
    var target = new CombatantState(2, 2, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, 2, 0, 0, 0, 100, 0, 10, 0);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.1f, 5);
    var targets = new[] { new Game.Core.Projectiles.ProjectileTarget(target, 5, 0, 0.4f) };
    var combatants = new Dictionary<int, CombatantState> { [1] = source, [2] = target };
    var result = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 0.1, new DamagePolicy());
    Assert.Equal(1, result.Hits.Length);
    Assert.Equal(90.0f, target.Health, 1e-5f);
}

static void ProjectileHitAppliesDamageAndDestroys()
{
    var source = new CombatantState(1, 1, 100);
    var target = new CombatantState(2, 2, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, 2, 0, 0, 0, 10, 0, 15, 0);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.2f, 10);
    var targets = new[] { new Game.Core.Projectiles.ProjectileTarget(target, 5, 0, 0.5f) };
    var combatants = new Dictionary<int, CombatantState> { [1] = source, [2] = target };
    var result = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 1.0, new DamagePolicy());
    Assert.Equal(1, result.Hits.Length);
    Assert.Equal(85.0f, target.Health, 1e-5f);
    Assert.True(!projectile.IsAlive);
}

static void PiercingProjectileHitsInPathOrder()
{
    var source = new CombatantState(1, 1, 100);
    var far = new CombatantState(2, 2, 100);
    var near = new CombatantState(10, 2, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, -1, 0, 0, 0, 10, 0, 10, 1);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.1f, 5);
    var targets = new[]
    {
        new Game.Core.Projectiles.ProjectileTarget(far, 6, 0, 0.4f),
        new Game.Core.Projectiles.ProjectileTarget(near, 3, 0, 0.4f)
    };
    var combatants = new Dictionary<int, CombatantState> { [1] = source, [2] = far, [10] = near };
    var result = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 1.0, new DamagePolicy());
    Assert.Equal(2, result.Hits.Length);
    Assert.Equal(10, result.Hits[0].TargetId);
    Assert.Equal(2, result.Hits[1].TargetId);
    Assert.Equal(90.0f, near.Health, 1e-5f);
    Assert.Equal(90.0f, far.Health, 1e-5f);
    Assert.True(!projectile.IsAlive);
}

static void ProjectileDoesNotHitSameTargetTwice()
{
    var source = new CombatantState(1, 1, 100);
    var target = new CombatantState(2, 2, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, 2, 0, 0, 0, 1, 0, 10, 2);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 1.0f, 5);
    var targets = new[] { new Game.Core.Projectiles.ProjectileTarget(target, 1, 0, 1.0f) };
    var combatants = new Dictionary<int, CombatantState> { [1] = source, [2] = target };
    var first = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 0.1, new DamagePolicy());
    var second = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 0.1, new DamagePolicy());
    Assert.Equal(1, first.Hits.Length);
    Assert.Equal(0, second.Hits.Length);
    Assert.Equal(90.0f, target.Health, 1e-5f);
}

static void FriendlyFireDisabledProjectilePassesThroughAlly()
{
    var source = new CombatantState(1, 1, 100);
    var ally = new CombatantState(2, 1, 100);
    var enemy = new CombatantState(3, 2, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, -1, 0, 0, 0, 10, 0, 12, 0);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.1f, 5);
    var targets = new[]
    {
        new Game.Core.Projectiles.ProjectileTarget(ally, 3, 0, 0.4f),
        new Game.Core.Projectiles.ProjectileTarget(enemy, 6, 0, 0.4f)
    };
    var combatants = new Dictionary<int, CombatantState> { [1] = source, [2] = ally, [3] = enemy };
    var result = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 1.0,
        new DamagePolicy { FriendlyFireEnabled = false });
    Assert.Equal(1, result.Hits.Length);
    Assert.Equal(3, result.Hits[0].TargetId);
    Assert.Equal(100.0f, ally.Health, 1e-5f);
    Assert.Equal(88.0f, enemy.Health, 1e-5f);
}

static void FriendlyFireEnabledProjectileHitsAllyFirst()
{
    var source = new CombatantState(1, 1, 100);
    var ally = new CombatantState(2, 1, 100);
    var enemy = new CombatantState(3, 2, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, -1, 0, 0, 0, 10, 0, 12, 0);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.1f, 5);
    var targets = new[]
    {
        new Game.Core.Projectiles.ProjectileTarget(enemy, 6, 0, 0.4f),
        new Game.Core.Projectiles.ProjectileTarget(ally, 3, 0, 0.4f)
    };
    var combatants = new Dictionary<int, CombatantState> { [1] = source, [2] = ally, [3] = enemy };
    var result = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 1.0, new DamagePolicy());
    Assert.Equal(1, result.Hits.Length);
    Assert.Equal(2, result.Hits[0].TargetId);
    Assert.Equal(88.0f, ally.Health, 1e-5f);
    Assert.Equal(100.0f, enemy.Health, 1e-5f);
}

static void InvulnerabilityBlocksProjectileDamage()
{
    var source = new CombatantState(1, 1, 100);
    var target = new CombatantState(2, 2, 100);
    target.GrantInvulnerability(2);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, 2, 0, 0, 0, 10, 0, 12, 0);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.1f, 5);
    var targets = new[] { new Game.Core.Projectiles.ProjectileTarget(target, 3, 0, 0.4f) };
    var combatants = new Dictionary<int, CombatantState> { [1] = source, [2] = target };
    var result = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 0.5, new DamagePolicy());
    Assert.Equal(1, result.Hits.Length);
    Assert.Equal(DamageOutcome.BlockedInvulnerability, result.Hits[0].Outcome);
    Assert.Equal(100.0f, target.Health, 1e-5f);
    Assert.True(!projectile.IsAlive);
}

static void ProjectileExpiresAtLifetime()
{
    var source = new CombatantState(1, 1, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, -1, 0, 0, 0, 1, 0, 5, 0);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.1f, 1);
    var combatants = new Dictionary<int, CombatantState> { [1] = source };
    var result = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile },
        Array.Empty<Game.Core.Projectiles.ProjectileTarget>(), combatants, 0.1, new DamagePolicy());
    Assert.Equal(1, result.DestroyedCount);
    Assert.True(!projectile.IsAlive);
}

static void SimultaneousCollisionTieBreaksByTargetId()
{
    var source = new CombatantState(1, 1, 100);
    var higher = new CombatantState(9, 2, 100);
    var lower = new CombatantState(2, 2, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, -1, 0, 0, 0, 10, 0, 10, 0);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.2f, 5);
    var targets = new[]
    {
        new Game.Core.Projectiles.ProjectileTarget(higher, 5, 0, 0.5f),
        new Game.Core.Projectiles.ProjectileTarget(lower, 5, 0, 0.5f)
    };
    var combatants = new Dictionary<int, CombatantState> { [1] = source, [9] = higher, [2] = lower };
    var result = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 1.0, new DamagePolicy());
    Assert.Equal(1, result.Hits.Length);
    Assert.Equal(2, result.Hits[0].TargetId);
}

static void SelfDamagePolicyAppliesToProjectiles()
{
    var player = new CombatantState(1, 1, 100);
    var spawn = new Game.Core.Spells.ProjectileSpawn(1, 1, 0, 0, 0, 1, 0, 15, 0);
    var projectile = new Game.Core.Projectiles.ProjectileState(1, spawn, 0.1f, 5);
    var targets = new[] { new Game.Core.Projectiles.ProjectileTarget(player, 0, 0, 0.5f) };
    var combatants = new Dictionary<int, CombatantState> { [1] = player };
    var result = Game.Core.Projectiles.ProjectileSystem.Step(new[] { projectile }, targets, combatants, 0.1, new DamagePolicy());
    Assert.Equal(1, result.Hits.Length);
    Assert.Equal(85.0f, player.Health, 1e-5f);
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
