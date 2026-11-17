# BOSS PILOT 022 — Concurrent Gnasher and projectile avoidance

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `d63a61aa7cdd486c1abb983b096112892416e1a8`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #131 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44014209474

- Seed 1 naturally defeated Mul'gath at 1274.6s: level 21, 1394 kills, 3 objectives, 1227.4/1300 HP.
- Seed 2 died at 506.8s during fungi progress 19 after projectile hits of 56.8, 56.8 and 56.6 plus contact. Gnasher was burrowing 16.3 units away but did not hit. At 504.8s an incoming projectile had predicted closest approach t=1.31s and zero miss distance.
- Seed 3 naturally defeated Sol'phish at 1229.9s: level 22, 1771 kills, 4 objectives, 761.4/1100 HP.
- Checkpoint and short browser regressions passed; no browser, console or external-network errors.

## Root cause

The pilot correctly detected the incoming projectile, but the Gnasher emergency branch replaced the complete movement vector with the Gnasher escape vector. The projectile avoidance vector was therefore discarded during the exact window when both threats were active.

## Revision 022 changes

- Track projectile and hazard steering separately from general enemy repulsion.
- Preserve the Gnasher escape heading while blending projectile/hazard vectors into the final movement vector.
- Increase the contribution of imminent projectile/hazard vectors so they can override a Gnasher route when collision is predicted.
- Record the merged component vectors in the 15-second trace.

## Acceptance

Pending CI readback. Require three natural wins and exact `sol`/`krog`/`mul` coverage in one run. Krog'wa is independently verified in CI #129 seed 2; the next run must retain that route while keeping the Sol and Mul wins. Product remains **NOT_READY**; production HTML unchanged.
