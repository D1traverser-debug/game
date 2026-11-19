# Objective RNG Integration 001

Date: 2026-11-19
Branch: `work/objective-rng-integration-001`
Base: `full-game` at `d9abb5401ad7f68e886958f910868363c1c046e0`
Implementation commit: `9f9bf30df53fcde93b05ec035e2588b5dd163c73`
Status: IMPLEMENTED · CI PENDING · OWNER ACCEPTANCE NOT REQUESTED

## Scope

Integrate deterministic entropy into one bounded gameplay subsystem: objective selection and generation. Keep the change isolated from combat balance, map dimensions, objective targets, enemy tuning and unrelated random call sites.

## Implementation

- Embed the canonical `web/src/core/seeded-rng.mjs` implementation into `index.html` through `scripts/build_game.py`. The generated browser artifact does not require a successful RNG module import.
- Initialize each expedition with `runSeed`, `runRng` and the PCG algorithm version. `startRun(seed)` accepts an explicit unsigned 32-bit seed for controlled reproduction; ordinary start/replay calls generate a fresh seed.
- Route objective type, variant probability/choice, origin offsets, object placement offsets and brazier sequence order through the per-run PCG stream.
- Replace the objective sequence's random-comparator sort with Fisher–Yates.
- Route collision-bearing static meadow decoration through a separate fixed `WORLD_LAYOUT_SEED` and `WORLD_LAYOUT_VERSION`; the map's blocking geometry no longer varies with the run seed.
- Keep camera shake on the presentation helper and procedural audio noise on its private LCG.
- Display run seed and RNG algorithm version on the result screen.

## Acceptance coverage added

`tests/objective_rng_regression.py` checks:
1. Same seed and same initial state produce identical objective traces.
2. Different seeds diverge across a 32-seed sample.
3. World-layout signature is independent of run seed.
4. Extra render calls do not advance run RNG.
5. Audio dispatch/noise and mute state do not advance run RNG.
6. A paused frame and resume do not advance run RNG.
7. Explicit same-seed replay reproduces the objective trace; ordinary new runs receive fresh seeds.
8. Run seed and algorithm version appear in the result screen.
9. No runtime/console errors or external network requests.

The natural-run harnesses also pass their fixed seeds into the new run RNG, preserving reproducible full-run test inputs while the other legacy random systems remain separately seeded.

## Boundary and non-claims

This slice does not make the entire game deterministic. Enemy director, combat, loot, level-up offers, spell execution, chest placement and boss selection still use legacy random call sites. It does not change gameplay balance or map geometry. Product status remains `NOT_READY`.

CAOS is read-only and was not modified.
