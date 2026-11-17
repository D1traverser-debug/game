# BOSS PILOT 023 — Restore dynamic Gnasher evasion and extend projectile lookahead

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `50e2d55891f9186f13269d92968f1ddcf40c8c41`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #132 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44014779710

- Seed 1 died at 466.9s after Gnasher hits at 368.3s, 456.4s and 466.9s. Only 20 leap-safe frames were recorded; CI #131's dynamic controller had 327 and won.
- Seed 2 died at 187.3s during Rift after repeated projectile hits. The first recorded hit had predicted closest approach t=1.47s and miss distance 2.7, just outside the 1.35s trigger.
- Seed 3 died at 661.0s to a 329.4 raw Gnasher hit at 48.1 units from the landing point.
- Checkpoint and short browser regressions passed; no browser, console or external-network errors.

## Revision 023 changes

- Revert the per-Gnasher direction lock; restore dynamic per-frame escape scoring that produced natural wins on seeds 1 and 3 in CI #131.
- Extend projectile emergency detection from 1.35s/92 units to 1.8s/110 units.
- Increase predicted projectile sidestep contribution to match the wider collision envelope.
- Preserve separate projectile/hazard vector blending with Gnasher escape.

## Acceptance

Pending CI readback. Require three natural wins and exact `sol`/`krog`/`mul` coverage in one run. Product remains **NOT_READY**; production `index.html` and CAOS remain untouched.
