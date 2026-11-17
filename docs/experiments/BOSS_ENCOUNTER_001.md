# BOSS ENCOUNTER 001 — Shared attack-state-machine implementation

Date: 2026-11-17  
Branch: `development`  
Implementation commit: `35b4aa2170428f70421470b10c91d2a13c8850a4`  
Artifact: `index.html` — 729,501 bytes  
Artifact SHA-256: `41545a842ec17236896fb2edff63e1ac92c1423eee76cfa4ed2f340a94cac5ee`  
Status: **PARTIAL_COMPONENT_TESTED / PRODUCT NOT_READY**

## Implemented

The boss module is data-driven. Each boss owns three attack definitions, and each attack instance snapshots the target geometry before displaying its warning. The instance advances through telegraph, active, recovery and cooldown; collision resolution uses the stored geometry rather than recalculating the target during the warning.

| Boss | Attack cards | Encounter changes |
|---|---|---|
| Sol'phish | Obelisk strike, radial burst, homing volley | Existing stagger/vulnerability window retained |
| Krog'wa | Inhale/pull, tongue-smash lane, tracking spit | Three health segments; magnetic arena boundary after segment one |
| Mul'gath | Head whip, spike grid, radial head volley | Three health segments; head growth; healing servants; corrupted servant can damage boss |

Homing projectiles have their own steering update and are rendered as hostile projectiles in the active 2D/3D shot paths. The offline root HTML is generated from the boss source fragment with anchor-count checks and idempotent shot-branch insertion.

## CI evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44062145086

- `python scripts/build_game.py --check`: PASS_REPRODUCIBLE.
- `tests/boss_encounter_regression.py`: 15/15 PASS.
- All nine independent browser regression jobs: PASS.
- Zero browser page errors and zero external requests.
- Checkpoint job initially failed only because the state manifest still had the prior artifact's hash and size. This recovery update synchronizes those exact values; a new run must verify the guard.

## Test coverage

The 15 checks cover: three attack cards per boss; valid lifecycle durations and geometry types; Krog'wa first segment/field activation; Mul'gath head growth across segments; snapshotted telegraph geometry; no damage during the warning; active/recovery/cooldown transitions; obelisk hit resolution; field boundary correction; minion approach/healing; corrupted minion collision damage; circle/line/grid collision predicates; homing projectile turning; no runtime exceptions; no external requests.

## Limits / next gates

These are synthetic deterministic component probes. They do not prove complete player combat, full-run survival, natural victory, readable visuals, source-exact timing, or human acceptance. The current suite does not yet prove every rendered telegraph uses the exact active hitbox geometry in both render paths, nor does it cover pause, invulnerability, phase-transition cancellation or duplicate damage on every attack. Numerical durations, radii, speeds and damage are provisional adaptations.

Next: verify the metadata-rebaseline CI run; then capture every boss attack at normal speed and compare warning geometry/lifetime with its active hitbox, test actual dodge/counterplay, add the missing lifecycle edge regressions, and obtain an owner-controlled boss playtest. Do not tune global HP/damage or claim source fidelity based only on this component pass.
