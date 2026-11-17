# BOSS PILOT 018 — Unified threat priority for natural runs

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `87a660c443d93719d34221a652a2fc5cd573d928`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #127 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44008420760

- Seed 1 died at 376.4s near a fungi objective at (-968,709). A hard boundary margin at x=980/y=720 blocked a valid objective at y=810; contact/projectile hits finished the player.
- Seed 2 died at 168.9s during Rift after progress reached 70.32. The .32 evasion multiplier and radial suppression prevented sufficient projectile dodging.
- Seed 3 died at 515.2s during Soul Sludge after repeated Gnasher hits; objective/resource pursuit continued during burrow/leap.
- Checkpoint and short browser regressions passed; no page, console or external-network errors.

## Revision 018 policy

1. Immediate incoming projectiles and Gnasher burrow/leap override objectives and optional loot.
2. Rift containment is preferred, but imminent projectiles can trigger emergency movement outside the circle.
3. Hard inward steering applies only near the actual world clamp, not at a broad margin that blocks valid perimeter objectives.
4. Gnasher escape suspends objective/loot pursuit and combines retreat with lateral movement.
5. Optional health/XP/magnet targets remain inside a safe envelope; objectives are not filtered by that envelope.

## Acceptance

Pending CI readback. Require three natural wins and exact `sol`/`krog`/`mul` coverage. Keep product HTML unchanged until the agent's priority behavior is demonstrated. Boss attack fidelity remains an independent P0 issue (GAME-042).
