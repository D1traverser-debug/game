# QA SMOKE 025 — Deterministic and threat-aware 90-second baseline

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `13ed1c29e22d3e69d4098a6f78db0f9870b30724`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #134 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44016473737

- The old normal-play smoke died at 82.8s with 77 kills, level 8 and 0 HP.
- There were no page errors, console errors or external network requests.
- The smoke harness was nondeterministic and strategically weak: no RNG seed, always selected the first upgrade option, chased XP only, ignored health orbs and threat avoidance, and recorded no damage events.

## Revision 025 changes

- Fix RNG seed to `20261117` before starting the run.
- Prioritize defensive stats and sustain scrolls when offered; choose a new spell/augment only when no survival option is available.
- Prioritize health orbs below 76% HP.
- Add basic separation from enemies, predictive projectile sidesteps, hazard avoidance and inward steering near world edges.
- Record the last 25 damage events for failure diagnosis.

## Acceptance

Pending CI readback. The 90-second survival gate remains mandatory. This is test-harness work only; no production damage, enemy or player balance values are changed. Natural-run boss matrix remains pending behind this gate.
