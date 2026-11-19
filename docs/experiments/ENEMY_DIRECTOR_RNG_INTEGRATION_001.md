# Enemy Director RNG Integration 001

Date: 2026-11-19
Branch: `work/enemy-director-rng-001`
Base checkpoint: objective RNG green commit `a6abff5e857142b5153dca659682d5018de34a96`
Status: IMPLEMENTED · CI PENDING · OWNER ACCEPTANCE NOT REQUESTED

Artifact checkpoint: `index.html` 804261 bytes; SHA-256 `0161b492aa0d7079e942513443e27d8e4a25c43fe0f3d52437a859dbc41086bb`. Result screen includes expedition seed, PCG algorithm version and enemy RNG sequence 57630.

## Source audit

`spawnEnemy` used legacy shared randomness for: spawn angle, initial/normal spawn distance, enemy archetype selection, random enemy ID, initial attack timer, initial heal timer, and elite chance. The deterministic population director separately computed a time-scaled target and spawn batch. Enemy IDs are consumed by gnasher warning `sourceId`, projectile `uniqueHits`, and the 2.5D enemy bobbing phase. Boss identity is the stable string `boss`; `bossOwnerId` associates Mul'gath healers with it. Damage-pipeline `nextCombatantId` is a distinct identity namespace and remains unchanged.

## Implementation

- Add a dedicated `enemyRng` PCG stream from the expedition seed with sequence `0xE11E`; it is independent of objective `runRng` and static world `worldRng`.
- Route spawn angle/distance, enemy type roll, initial attack/heal timers, elite probability, boss-healer spawn offsets and objective crab-child spawn offsets through `enemyRng`.
- Replace random enemy IDs with monotonic integer `game.nextEnemyId` allocation. ID allocation consumes no RNG.
- Derive a stable visual bobbing phase from the deterministic ID rather than using random float identity as a visual phase.
- Extract the unchanged population target/cap algorithm into `updateEnemyDirector(dt)` to support direct tests; no target formula, spawn-rate or 64-enemy cap changes.
- Keep combat critical/dodge rolls, elemental procs, drops, spell/upgrade/chest randomness, boss selection and boss attacks on their existing legacy sources.

## Regression coverage

`tests/enemy_director_rng_regression.py` checks same-seed spawn traces, divergence across 32 seeds and all seven archetypes, monotonic unique IDs, render/audio/pause isolation, objective/enemy stream isolation, objective generation isolation, allocator non-consumption, director repeatability and target pacing, 64-enemy cap, RNG metadata, no runtime errors and offline operation. The test probe is injected into an in-memory browser document and is not shipped.

## Non-claims

This slice does not make combat or full-run outcomes deterministic. It does not change enemy base stats, damage, speed, elite threshold, population target, spawn rate, objective targets, map bounds or boss archetype selection. CI and natural-run parity are pending. Product remains `NOT_READY`; CAOS is read-only.


## CI wiring

The QA workflow now allows pull requests targeting `work/objective-rng-integration-001`, the base of this stacked change. This ensures the complete required matrix runs for the enemy-director slice without combining it into the earlier objective RNG PR.


## Natural-run parity checkpoint — 2026-11-19

The first enemy RNG candidate CI run `44525204498` passed the dedicated enemy spawn regression, but natural-run fixtures 45/42/43/48 produced only one boss victory (Ember). Aster/Briar/Nyx survived to the 1500-second cap with Boss HP remaining; no runtime/console/network errors. The test-only pilot was not changed to force damage, HP, boss death or objective completion. A bounded ordered seed sweep is being used to find deterministic replay fixtures per wizard. Production balance and the 1500-second acceptance limit remain unchanged.
