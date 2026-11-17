# BOSS PILOT 026 — Correct projectile horizon, actual leap time and early retreat

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `eee611d5ab4b91b8d70cc1ccc18001cc5d6bbfa8`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #135 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44017267943

- Deterministic 90-second smoke: PASS. XP, objective, upgrade and browser progression regressions: PASS.
- Seed 1 died at 132.2s after five projectile hits; the first four arrived between 111.7s and 119.6s. The inner 1.8s trigger was nested inside an outer `t<1.35` guard.
- Seed 2 died at 588.8s after two Gnasher hits (317.6 and 318.7 raw) near the left edge; distances from landing points were 59 and 26.2. The pilot assumed a fixed 0.55s movement window even when less leap time remained.
- Seed 3 died at 823.2s from contact while the Crab objective was active. HP was 36.5% at 822.5s; the critical retreat threshold was only 30%.
- No page, console or external-network errors.

## Revision 026 changes

- Correct the outer projectile approach-time guard to 1.8s so the inner threshold is reachable.
- Score Gnasher escape over the actual remaining `stateT`, not a fixed 0.55s.
- Bias leap escape away from the fixed landing point, evaluate all active landing targets, and increase boundary/enemy-clearance weight.
- Raise critical retreat to 55% HP when threats are nearby and strengthen its movement priority.
- Record per-frame Gnasher leap samples to verify actual separation before landing.

## Acceptance

Pending CI readback. Require three natural wins and exact `sol`/`krog`/`mul` coverage in one run. The deterministic 90-second smoke gate remains mandatory. Product remains **NOT_READY**; production `index.html` and CAOS unchanged.
