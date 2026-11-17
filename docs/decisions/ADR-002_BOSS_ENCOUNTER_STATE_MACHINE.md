# ADR-002 — Boss Encounter State Machine

Status: ACCEPTED  
Date: 2026-11-17  
Scope: D1traverser-debug/game only  
Parent governance: CAOS is read-only; this ADR does not authorize any CAOS changes.

## Context

The current boss implementation is a compact per-boss conditional inside updateBossEncounter. It has one generic phase field, shared timers and circular delayed hazards. Krog'wa is approximated by a leap/acid ring; Mul'gath by fan projectiles and healing servants. The code does not model the documented three-segment phase changes, head growth, magnetic-field phase or complete attack identities. Attack timing, telegraph rendering and hit resolution are not represented by one shared contract.

This is a product-level defect, not a request to add isolated attack effects.

## Source evidence and confidence

| Boss | Evidence-backed identity | Source confidence / limitation |
|---|---|---|
| Sol'phish | Targeted obelisk/runestone strikes, radial projectiles, homing projectiles, stagger/vulnerability | Community boss reference; official 0.13 notes independently confirm obelisk attack. Exact timings remain unpinned. |
| Krog'wa | Three health segments; magnetic field after the first segment; inhale/pull, tongue charge, tracking spit | Community boss reference; official 0.13 notes independently confirm tongue-smash. Exact field radius and attack timings remain unpinned. |
| Mul'gath | Three health segments; head count increases by phase; head whip, ground spike grid, linked minions; corrupted minions can collide with and damage boss | Community boss reference; official 1.1 notes corroborate minion corruption and phase-transition resistance behavior. Additional video-reported rock walls/orb absorption/spin are low confidence and excluded from baseline. |

References:
- Official announcements and patch notes: https://steamcommunity.com/app/2904000/announcements/
- Official EA Update 13 patch notes: https://steamdb.info/patchnotes/20496068/
- Community boss summary (last modified 2026-08-01): https://namu.moe/w/The%20Spell%20Brigade
- Older gameplay transcript (additional low-confidence Mul'gath observations): https://www.dailymotion.com/video/xa9kq46

## Decision

Replace the current boss-specific timer branches with a shared, typed attack lifecycle:

1. READY — choose an eligible attack from the current boss phase.
2. TELEGRAPH — snapshot target/angle/geometry and render a clear warning.
3. ACTIVE — resolve the attack against the same geometry that was telegraphed.
4. RECOVERY — boss is committed and cannot start another attack.
5. COOLDOWN — attack becomes eligible again after its cooldown.

Each attack definition must own:
- stable attack ID and boss owner;
- eligible phase(s);
- windup, active and recovery duration;
- telegraph geometry and presentation cue;
- active collision geometry;
- player counterplay (move out, sidestep, cross the lane, interrupt, or use cover);
- damage/status effect and damage source ID;
- cooldown and phase-transition cancellation behavior.

Rendering and collision must consume the same attack instance. Do not duplicate geometry constants in draw and update paths.

## Encounter state

Common state:
- phaseIndex, phaseTransitionTimer, attackState, attackCooldown, attackSequence;
- stagger, vulnerability and boss immunity/freeze windows;
- active attack instances and summon ownership.

Krog'wa:
- three health segments;
- field/arena transition after the first segment is depleted;
- inhale/pull, tongue-smash charge and tracking spit.

Mul'gath:
- three health segments;
- head count grows with phase;
- head whip, spike-grid eruption and linked healing minions;
- minions approach the boss; corrupted minions can collide with and damage the boss.

Sol'phish:
- preserve stagger/vulnerability and implement the source-backed obelisk, radial and homing attack set.

## Non-goals for this iteration

- Do not change current boss HP or global player damage to make the automated pilot pass.
- Do not claim exact source timing or damage when no pinned reference exists.
- Do not implement rock-wall/orb-absorption/spin variants until current-version evidence confirms them.
- Do not copy original proprietary source, art, animations, fonts or sound recordings.
- Do not add multiplayer or additional maps/heroes.

## Required tests

- Phase boundary tests at just above, exactly at and just below each segment threshold.
- Every attack: telegraph exists before active hitbox; a player outside the telegraph is not hit; a player inside the resolved hitbox is hit once.
- Phase transition cancels stale telegraphs and cannot resolve the same attack twice.
- Player invulnerability, boss stagger, freeze/immunity, pause and boss death cannot cause duplicate resolution.
- Mul'gath minions approach the boss, can be corrupted and damage the boss on collision.
- Both 2.5D and WebGL render paths show the same telegraph geometry.
- Seeded replay remains deterministic; no browser errors or external network requests.
- No boss victory test may directly set boss HP to zero or force the result.

## Numerical tuning policy

Current HP/damage scale remains unchanged during architecture and attack implementation. Windup, recovery, radius, speed and damage values are provisional adaptation parameters. They must be calibrated only after attack cards pass and representative play sessions are reviewed.
