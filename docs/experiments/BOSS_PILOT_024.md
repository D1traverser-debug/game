# BOSS PILOT 024 — Dynamic multi-landing Gnasher escape

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `030dcc6e8bbd93562bbfbb352d3e3fce2a92c373`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #133 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44015470700

- Seed 1 reached Sol'phish but died at 1237.7s after six Gnasher hits. Final raw hit 255.3*1.7=434.0 landed 31.8 units from target (-1138,384.6); player was at (-1165,367.6), with 107.6/500 HP, 119 armor and 3 regen. It was near the left edge; only 164 leap-safe frames across 626 were recorded.
- Seed 2 naturally defeated Krog'wa at 1217.1s: level 22, 1992 kills, 254.6/300 HP.
- Seed 3 naturally defeated Krog'wa at 1390.7s: level 20, 1485 kills, 482.1/700 HP.
- Checkpoint passed; no browser, console or external-network errors. Boss IDs in this run were `sol` and `krog`; Mul'gath is separately verified in CI #131 seed 1.

## Revision 024 changes

- Remove per-Gnasher direction locks; recompute the escape heading each frame.
- Score actual player displacement after map-boundary clamping.
- Evaluate minimum separation from all active Gnasher leap landing points.
- Retain enemy/hazard/projectile occupancy penalties and the 1.8s projectile horizon.

## Acceptance

Pending CI readback. Require three natural wins and exact `sol`/`krog`/`mul` coverage in one run. Product remains **NOT_READY**; production `index.html` and CAOS unchanged.
