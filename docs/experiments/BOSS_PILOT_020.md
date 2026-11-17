# BOSS PILOT 020 — Multi-Gnasher landing-zone avoidance

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `2deee6e2855234552f2a5de3b0cc7ab4d002eb8f`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #129 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44012660542

- Seed 1 died at 412.4s to a 287.1 raw Gnasher hit. Player was at (1145.2,650.0), only 18.6 units from the recorded landing target (1157.2,637.9). Only 13 leap-safe frames were recorded.
- Seed 2 naturally defeated Krog'wa at 1265.9s: level 22, 1657 kills, 3 objectives, 591.6/800 HP.
- Seed 3 naturally defeated Mul'gath at 1265.7s: level 22, 1617 kills, 2 objectives, 247.1/400 HP.
- Checkpoint and short browser regressions passed; no page, console or external-network errors. Boss coverage is `krog` and `mul`; `sol` is missing.

## Root-cause evidence

Seed 1's trace showed a Gnasher leap while the player was at y=863.7, only 36.3 units from the lower world edge. The selected escape heading was (0.92,0.38), partly pointing into the edge. The previous controller also selected one active Gnasher and recomputed its heading every frame, so threat switching could change the escape vector during a single attack window.

## Revision 020 changes

- Evaluate all simultaneously active Gnasher leap landing points, not only one selected enemy.
- Lock one escape heading for each Gnasher's current burrow/leap phase; recompute only when its state or landing target changes.
- Score actual displacement after world-boundary clamping, not just nominal direction.
- Penalize predicted enemy, hazard and projectile occupancy at the future player position.
- Capture the exact Gnasher attacker and all nearby Gnasher states/landing points on damage.

## Acceptance

Pending CI readback. Require three natural wins and exact `sol`/`krog`/`mul` coverage. Keep production `index.html` unchanged. Product remains **NOT_READY**.


## CI #130 execution status
The first attempt to validate this revision did not execute the natural-run matrix. The Python harness failed at line 385 because the injected JavaScript declaration was outside the Python string. CI checkpoint passed; no gameplay conclusion can be drawn. Revision 021 corrects this host-language boundary.
