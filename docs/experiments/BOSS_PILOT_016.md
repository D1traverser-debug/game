# BOSS PILOT 016 — Telegraph-aware natural-run agent

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `4b3df2c54937214eeb48ccaac7d9091c68b81b02`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #125 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44006013545

- Seed 1: death at 469.3s, 579 kills, level 17, maxHP 300, armor 9, regen 0. Damage events were enemy projectiles.
- Seed 2: death at 413.8s, 467 kills, level 16, maxHP 400, armor 42, regen 2. Damage included projectiles, friendlyFire, contact and a Gnasher leap (283.8 raw damage before armor).
- Seed 3: death at 115.7s, 119 kills, level 9. Four projectiles hit in 4.3 seconds near the map edge.
- All three runs had zero browser, console and external-network errors.

## Root-cause findings

1. Projectile approach-time sign was inverted. With relative position `r = player - projectile`, future separation is `r-vt`, so an approaching projectile has positive `dot(r,v)`.
2. The pilot chose spell-level cards over defensive cards even when Dodge, Regen, Armor or Max HP were offered.
3. The pilot did not avoid Gnasher's burrow pursuit and fixed leap landing point.
4. The pilot ignored its own damaging spell hazards (meteor, bell, bomb, slam, dice and explosive effects).

## Friendly-fire source rule

Default friendly fire intentionally allows caster self-damage. Optional Harmony Pact disables damage to self and teammates. This is source behavior, not a bug to remove for test convenience. Evidence:
- https://steamdb.info/patchnotes/16553491/
- https://steamcommunity.com/app/2904000/discussions/1/4513255804483189926/

## Revision 016 changes

- Always choose a real defensive stat when one is offered; otherwise prefer spell augments/levels and damage stats.
- Correct projectile closest-approach time sign.
- Steer away from Gnasher burrow positions and leap landing points.
- Avoid friendly-fire and explosive hazard types while preserving production damage rules.
- Record projectile/Gnasher/hazard dodge counters alongside damage events and 15-second traces.

## Acceptance

Pending CI readback. Require three natural wins, exact boss coverage `sol`/`krog`/`mul`, no browser errors and no external requests. A pass remains automated-agent evidence only; human owner playtest, source fidelity, real-device performance, file-origin persistence and visual/audio acceptance remain open.
