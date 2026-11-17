# BOSS TELEGRAPH LIFECYCLE REPAIR — 2026-11-18

## Scope

Reginald only / Verdant Meadow only / single-player / offline single HTML. Main baseline is preserved. CAOS is read-only.

## Test-first evidence

CI #44128548427 (commit 3efbbe965246bb2eae212a4e8bbf635853adbe15):
- Existing 15 boss checks passed.
- Ten new checks were added.
- Seven new checks failed against the previous implementation: telegraph payload ownership, freeze cancellation, phase-transition cancellation, stagger cancellation, snapshotted pull origin, radial projectile origin, homing projectile origin and boss movement commitment.
- Pause clock, invulnerability handling, no browser errors and no external requests passed.
- Failure was isolated to the boss encounter regression; the other nine CI jobs passed.

## Root causes

1. Warning hazards had independent timers and no attack-instance identity.
2. Phase transition and stagger cleared the attack pointer but left warning hazards behind.
3. Freeze paused the attack timer while the general hazard loop continued aging the warning.
4. Pull and projectile launch code used the boss's current coordinates instead of the snapshotted origin.
5. The boss continued chasing during a telegraph whose geometry was already snapshotted.
6. Both renderers treated all boss warnings as generic circular hazards.

## Candidate changes

- Every attack receives a monotonically increasing token.
- One warning payload carries the immutable geometry, shape, attack ID and projectile count.
- Cancellation removes only the warning belonging to that attack.
- Freeze cancels a pending telegraph; phase transition and stagger cancel the current attack.
- Pull and projectile launches use the geometry snapshot.
- Boss movement is committed during telegraph/active stages.
- 2.5D and WebGL2 paths render circle, line, grid, radial, target and pull warnings from the same geometry payload.
- Regression smoke exercises all nine attack cards in both render paths where WebGL2 is available.

## Candidate artifact

- `index.html`: 734011 UTF-8 bytes.
- SHA-256: `7a98c8989cbfb85f53063f69507c023f3bd899ed1b1eba97271fb44c45955bd9`.
- `scripts/build_game.py --check` and full CI: pending.

## Acceptance boundary

Passing deterministic tests does not prove that warnings are readable at normal speed or that a human can dodge every attack. Owner-controlled playtest, source-exact timing/damage, natural full-run boss victories, real file-origin persistence, hardware performance and final visual/audio acceptance remain open. Product status remains **NOT_READY**.
