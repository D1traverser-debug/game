# BOSS PILOT 027 — Adaptive natural boss-archetype coverage

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `40b48369287c99a20e1a2a17c0ff20f193b4d762`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #136 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44018248222

| Seed | Natural result | Boss | Time | Final HP | Objectives |
|---|---|---|---:|---:|---:|
| 1 | WIN | Krog'wa | 1259.5s | 700/700 | 3 |
| 2 | WIN | Krog'wa | 1286.7s | 300/300 | 3 |
| 3 | WIN | Mul'gath | 1291.7s | 160.9/400 | 3 |

Checkpoint, deterministic 90-second smoke, XP/objective/upgrade/browser regressions passed. All three natural runs won, with no browser, console or external-network errors. Exact boss coverage was only `krog` and `mul`; the CI correctly failed the missing Sol'phish requirement.

Historical independent natural wins exist for Sol'phish (CI #131 seed 3) and Krog'wa (CI #129 seed 2), but these do not replace same-run coverage.

## Revision 027 changes

- Seeds 1-3 remain mandatory full natural runs and must all win.
- Candidate seeds 4-12 are deterministic archetype scouts. The game naturally chooses the boss; no boss ID is forced and no production state is mutated.
- Scouting stops after a boss naturally spawns. If its archetype is missing from the current CI run's natural victories, the same run continues to a full natural boss defeat. Otherwise it is recorded as a scout only.
- Coverage is counted only from actual natural boss victories. Require winning IDs exactly `sol`, `krog`, and `mul`.
- Browser/console and offline/no-external-request checks apply to every attempted seed.

## Acceptance

Pending CI #137. Production `index.html`, combat balance, and CAOS remain unchanged. Product remains **NOT_READY** until the full requirements, fidelity, visual/audio, performance, save compatibility and human acceptance gates pass.
