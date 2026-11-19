# Deterministic Gameplay RNG — Boundary Audit 001

Date: 2026-11-19
Branch: `full-game`
Status: AUDIT COMPLETE · OBJECTIVE RNG SLICE IMPLEMENTED · CI PENDING · FULL RUN RNG INCOMPLETE
Scope: source inspection only. No gameplay behavior or random-call site was changed in this audit.

## Current evidence

The browser runtime already advances gameplay through a fixed-step update (1/30 s), and `web/src/core/seeded-rng.mjs` provides a PCG-XSH-RR 32-bit stream. The module has unit coverage for repeatability, bounded integers and unit floats. `web/src/core/spell-system.mjs` already requires a `SeededRng` instance when `SpellTargetingMode.RANDOM` is selected.

However, the monolithic production browser runtime does not yet inject this module into its game state. Source inspection found:
- 28 textual `Math.random()` occurrences, including the two generic `rand` / `pick` helper definitions.
- 45 `rand(` references and 11 `pick(` references.
- The generic `rand` helper is shared by gameplay and rendering, so a global replacement would make render cadence consume gameplay entropy.
- Two random-comparator shuffles use `sort(() => Math.random() - .5)`; this is not a valid uniform shuffle and is not a stable deterministic ordering.
- Procedural ground texture and audio noise use their own local deterministic LCGs. They are presentation-only and should remain independent from gameplay RNG.

## Call-site classification

| Area | Current random behavior | Correct stream / treatment |
|---|---|---|
| Enemy director | Spawn angle/distance, enemy type, elite chance, attack/heal timers, random entity ID | Gameplay stream; replace random IDs with monotonic entity IDs in a separate, tested change |
| Combat | Critical hits, freeze chance, dodge, mana-siphon chance | Gameplay stream |
| Death and loot | Baby Sprout proc, XP value variation, health/magnet drops, scattered bonus orbs | Gameplay stream |
| Level-up and rewards | Rarity, stat/spell choices, chance gates, banish index, scroll/augment ordering | Gameplay stream; use Fisher–Yates, not random sort comparators |
| Spell execution | Dice face, meteor proc, projectile spread, target/impact offsets | Gameplay stream |
| Objectives | Objective type, variant, sequence order, spawn positions, crab movement and minion offsets | Gameplay stream |
| Chests and bosses | Chest location, boss archetype/location, healer spawn offsets | Gameplay stream |
| Static world decoration | `generateDecor` positions, prop types, sizes, rotations and collision-bearing obstacles | Separate fixed world-layout stream; do not consume the per-run stream |
| Camera shake | `drawWorld` uses `rand` during rendering | Presentation-only stream or deterministic visual function; never consume gameplay RNG |
| Background texture | Local LCG with fixed seed in ground-brush generation | Presentation-only; leave isolated |
| Audio noise | Local LCG in `studioNoiseHit` buffer generation | Audio-only; leave isolated |

## Root cause and architectural constraint

The problem is not the absence of a PRNG implementation. It is the absence of explicit entropy ownership. The current top-level `rand` and `pick` helpers hide whether a caller is part of simulation, world generation, rendering or UI. Replacing `Math.random` globally would cause screenshots, frame rate, camera shake or render order to alter future combat and reward outcomes.

The game needs independent streams with explicit lifetimes:
1. **Run RNG** — initialized once per expedition from a recorded run seed; used only by simulation decisions.
2. **World-layout RNG** — fixed/versioned seed for static terrain decoration and collision props; independent of the run.
3. **Presentation RNG** — optional and non-authoritative; rendering must not advance the run stream.
4. **Audio RNG** — existing procedural noise remains isolated.

A run seed should be visible in run results or diagnostics so a bug can be reproduced. Replay must either preserve the same seed when explicitly requested or create a new seed; ordinary replay must not accidentally reuse the previous stream. The RNG algorithm/version must be recorded with the seed because changes in draw order change the resulting run.

## Bounded integration plan

Do not rewrite all random call sites at once. The first integration slice should be one contained subsystem with a clear trace, preferably **objective selection and objective generation**:
- Add a per-run `SeededRng` instance to the game state.
- Expose narrowly named `gameRandom()`, `gameRand(min,max)`, `gamePick(items)` and a Fisher–Yates shuffle that require the active run RNG.
- Route only `startObjective` and its helper calls through the run stream in the first slice.
- Keep `generateDecor`, camera shake, ground texture and audio noise on their own streams.
- Ensure new-run/replay initialization explicitly resets or regenerates the seed.
- Add a test-only trace containing seed, RNG version, objective type/variant, target count, objective coordinates and generated object coordinates.

## Required acceptance tests for the first slice

1. Same seed + same initial state yields byte-identical objective trace.
2. Different seeds produce different traces across a statistically meaningful sample.
3. Rendering at different frame rates or forcing extra draw calls does not change the objective trace or run RNG state.
4. Muting/disabling audio does not change the objective trace.
5. Pause/resume does not consume run RNG while simulation ticks are stopped.
6. Replaying with an explicitly reused seed reproduces the same objective trace; a new run without an explicit seed receives a new seed.
7. The existing 24-job browser CI, natural boss runs and offline package remain green.

## Non-goals

- No global `Math.random` replacement.
- No change to combat balance, spawn rates, loot probabilities, level-up weights, boss behavior or map geometry.
- No attempt to make wall-clock UI animation or audio scheduling deterministic.
- No multiplayer or networking work; multiplayer is OUT_OF_SCOPE.
- No change to CAOS. This audit and all game work remain in the game repository.

## Audit conclusion

The deterministic RNG module is soundly isolated as a core contract, but it is not yet authoritative for the browser simulation. The correct next action is one subsystem integration with render/audio independence tests, not a bulk rewrite. Product status remains NOT_READY.


## Objective-generation integration candidate — 2026-11-19

The first bounded slice is implemented on `work/objective-rng-integration-001`:
- The canonical `SeededRng` module is embedded into `index.html` by `scripts/build_game.py`; the generated artifact remains usable without a module import succeeding under a local/offline preview.
- Each expedition gets a fresh unsigned 32-bit `runSeed`, a `runRng`, and a visible seed/algorithm result entry. Passing an explicit seed to `startRun(seed)` reproduces the objective stream; ordinary replay calls `startRun()` and gets a fresh seed.
- Objective type choice, variant chance/choice, objective origin and object placement, and brazier order now use the per-run PCG stream. The random-comparator objective shuffle is replaced with Fisher–Yates.
- Collision-bearing static world decoration now uses the independent fixed `WORLD_LAYOUT_SEED` / `WORLD_LAYOUT_VERSION` stream. `worldFindOpenPoint` therefore sees a stable world layout across run seeds.
- Camera shake still uses the legacy presentation helper; audio noise keeps its private LCG. Neither advances `runRng`.
- Natural-run test seed injection now passes the same fixed seed into the per-run PCG stream as well as the legacy `Math.random` stream.
- Added `tests/objective_rng_regression.py` for same-seed trace, different-seed divergence, world-layout independence, render/audio/pause isolation, fresh-run seeds, result-screen seed visibility and offline/no-error checks. Added it to the required browser-component CI matrix.

CI is pending. This does not claim full-run deterministic replay: enemy director, combat, loot, level-up, spell, chest and boss randomness remain to be migrated. No gameplay balance, map bounds, enemy values or objective targets were changed. CAOS remains read-only.


## CI evidence update — 2026-11-19

The first candidate run `44505974849` passed the offline package integrity check and the new objective RNG browser regression. The project-state checkpoint initially failed because the recorded HTML byte count was stale (803533 vs actual 803536); the metadata has been corrected to the package's measured byte count and SHA-256. Full required CI rerun remains pending.


## Objective RNG slice closed — CI PASS — 2026-11-19

The bounded objective RNG slice is now automated-CI green. Run `44507473452` passed 25/25 jobs on `b99802cb1bc300a22dce1780d969cd42541db02c`. The objective-specific regression passed 32/32 unique traces across nine objective families and verified world-layout independence, render/audio/pause isolation, fresh run seeds, result diagnostics and offline/no-error behavior. Four natural wizard runs all defeated a boss and reached the result screen. See `docs/experiments/OBJECTIVE_RNG_INTEGRATION_001.md` for the exact seeds, outcomes and artifact hashes.

Next audit boundary: enemy director spawn decisions and entity identity allocation. Inspect every relevant random call and ID generation site, distinguish spawn scheduling/selection/position from combat, loot and presentation, and define a minimal replay trace before implementation. No global random replacement.
