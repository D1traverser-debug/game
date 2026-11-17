# BOSS PILOT 019 — Fixed Gnasher landing escape and threat-aware build policy

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `bf6bf43bfa842a74feb98872a3a9d502241cad7b`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #128 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44009463457

- Seed 1 died at 397.3s; two Gnasher hits were 282.4/284.6 raw, with friendlyFire at 388.2s.
- Seed 2 died at 372.6s; six projectile hits landed between 334.4s and 350.7s, followed by a 279.9 raw Gnasher hit.
- Seed 3 died at 373.9s; two Gnasher hits were 280.1/280.4 raw.
- Checkpoint and short browser regressions passed; no page, console or external-network errors.

## Source-level root cause

Gnasher's production state machine:
1. Burrow follows the player at 3x speed for 1.25s.
2. On burrow completion, it snapshots the player's coordinates into `leapX/leapY`.
3. It moves toward that fixed point for 0.55s.
4. On landing, it damages the player if within 60 units.

The prior pilot steered relative to the enemy's interpolated current position, not the fixed landing point. That is the wrong reference frame for the landing dodge.

The upgrade chooser also returned a `newSpell` before checking defensive stats. Seed 3 selected a new spell at 220s while Dodge was offered. Projectile prediction considered up to 1.35s, but emergency evasion activated only for t<0.85s and miss distance<72, and was scaled by nearby-enemy pressure.

## Revision 019 changes

- Score 16 candidate movement headings over the Gnasher's 0.55s landing window; maximize separation from fixed `leapX/leapY` while penalizing enemy, hazard, projectile and edge risk.
- During burrow, prefer a lateral heading that preserves room for the subsequent leap escape.
- Suspend objective, loot and interaction pursuit while Gnasher is in its active attack window.
- Prioritize defensive stats and sustain scrolls ahead of new-spell offers.
- Activate projectile evasion for predicted approaches up to 1.35s / 92-unit miss distance, independent of nearby-enemy pressure; imminent hazards also activate evasion.
- Add damage-time telemetry for player movement/invulnerability, Gnasher state timer and fixed landing point, and nearest projectile time-to-closest-approach.

## Acceptance

Pending CI readback. Require three natural wins and exact `sol`/`krog`/`mul` coverage. This revision changes the QA agent only; `index.html` and production combat remain unchanged. Product remains **NOT_READY**.
