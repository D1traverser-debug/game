# BOSS PILOT 017 — Edge escape, Rift retention and Gnasher sidestep

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `63da60b639dac6f73e7ecd1254acee10b4deff55`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #126 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44007214721

- Seed 1 naturally defeated Krog'wa at 1259.7s: level 21, 1479 kills, four level-5 spells, 1000 max HP, 167 HP remaining.
- Seed 2 died at 767.3s at (-1200,-900); Rift progress reset, followed by stacked projectile/contact damage. The additive boundary correction was too weak.
- Seed 3 died at 1062.8s to a Gnasher hit of 402.7 raw damage. Retreat-only steering did not create enough lateral displacement during burrow/leap.
- Checkpoint and short browser regressions passed; natural-run matrix failed. No page, console or external-network errors. Only `krog` was recorded.

## Revision 017 changes

- Restrict optional loot targets to a safe interior envelope.
- Replace weak additive boundary force with hard inward steering near the clamped map edge.
- During Rift capture, remove outward radial evasion while preserving tangential dodges.
- At critical health and close threat distance, escape from the nearest enemy instead of continuing an objective/loot route.
- Combine retreat and lateral sidestep during Gnasher burrow; use lateral displacement during leap.
- Record target coordinates, player position, edge distance and nearest Gnasher state at damage time.

## Product issue kept separate

The prototype's Krog'wa attack set is incomplete (official sources identify tornadoes and tongue-smash); Mul'gath's current attack set is also incomplete versus gameplay evidence (spike grids, rock walls, orb absorption and spin). Tracked as GAME-042. No production boss code was changed in this revision.

## Acceptance

Pending CI readback. Require three natural wins and exact `sol`/`krog`/`mul` coverage. Automated agent success is not human playtest or release acceptance.
