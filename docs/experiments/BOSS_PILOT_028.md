# BOSS PILOT 028 — Single-clock deterministic natural-run harness

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `722ab20bd14d9efd93cc0221e85fca8b25804263`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #137 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44030442251

Checkpoint, progression, 90-second normal-play, objective and upgrade regressions passed. Natural-run matrix failed. There were no page errors, console errors or external requests.

| Seed | Result | Evidence |
|---|---|---|
| 1 | Death at 492.97s | Level 16, 508 kills, 1 objective; no boss |
| 2 | Natural Krog'wa win at 1196.4s | Level 22, 2062 kills, 3 objectives |
| 3 | Death at 123.87s | Level 8, 107 kills, 0 objectives; no boss |
| 9 | Krog'wa spawned; scout only | 1142.9s, 651.6/900 HP; no victory claimed |
| 10–11 | Died during Mul'gath attempts | Boss spawned; neither run won |
| 12 | Natural Mul'gath win at 1206.33s | Level 23, 2242 kills, 3 objectives |

The same seed 1 naturally defeated Krog'wa in CI #136 at 1259.5s but died at 492.97s in CI #137. The discrepancy is not evidence of a production balance change.

## Confirmed root cause

The temporary QA document ran two simulation clocks simultaneously:

1. The manual pilot called `update(0.1)` inside `__fullRun`.
2. The production `requestAnimationFrame` loop continued calling `update(SIM_STEP)` whenever the screen was playing.

The two clocks advanced the same game concurrently and consumed the seeded `Math.random` stream in different orders. The test was therefore not deterministic even though it installed an RNG seed. The previous report also serialized large unbounded traces, making CI logs unnecessarily large.

## Revision 028

- Keep the production RAF render loop active, but wrap the temporary document's `update` binding so RAF calls are blocked while the manual pilot owns simulation.
- Permit the real production update only inside the pilot's guarded manual tick.
- Record manual update count and blocked RAF update count for each run.
- Add hard CI assertions that manual update count equals harness tick count and that seed 1 produces the same outcome signature in a fresh browser context.
- Compact per-run state, retaining the last 10 damage events, Gnasher hits, trace samples and upgrade selections for diagnosis.
- Do not change production `index.html`, boss selection, boss HP, enemy damage or game balance.

## Acceptance

Pending CI #138. First verify the single-clock gate and deterministic replay. Then preserve the mandatory natural wins for baseline seeds 1/2/3 and obtain natural victories for all three archetypes in the same CI run. Product remains **NOT_READY** until full source fidelity, real-device performance, save/reload and independent human acceptance are complete.
