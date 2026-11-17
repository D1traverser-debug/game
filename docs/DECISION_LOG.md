# Decision Log

## D-001 — Product scope (ACCEPTED, owner instruction)
- One hero: Reginald.
- One map: Verdant Meadow.
- Single-player only.
- No online multiplayer, matchmaking, AI teammates, additional heroes, or maps.
- Final player delivery is one self-contained offline HTML.
- Rationale: finish one high-quality complete experience before expansion.

## D-002 — Repository role (ACCEPTED)
- GitHub `D1traverser-debug/game` is the canonical source of code, requirements, decisions, test evidence, and recovery state.
- Conversation memory is not authoritative.
- Root `index.html` is the current baseline playable artifact. It may be refactored only with rollback and reproducible single-file build preservation.

## D-003 — CAOS boundary (ACCEPTED)
- Apply CAOS governance methods to this project only.
- Do not modify CAOS code, files, branches, PRs, plugins, configuration, or documentation.
- Do not copy CAOS implementation assets into this repository; this project owns its own governance docs.

## D-004 — Fidelity over feature count (ACCEPTED)
- A spell, element, objective, or boss phase is not implemented merely because it has a name or data entry.
- Each mechanic needs source evidence, state-transition definition, visible/audio feedback, balance constraints, and tests.
- Generic multipliers or synthetic forced-state tests cannot substitute for the mechanic.

## D-005 — Original asset boundary (ACCEPTED)
- Implement observable mechanics independently; create original art/audio.
- Do not copy original game source, extracted game assets, music, sound recordings, or animations.
- Fan project is unofficial and must not imply endorsement.

## D-006 — Primary renderer is art-forward 2.5D (ACCEPTED)
- The final product may use a different rendering technique from the original if the complete player experience is equivalent.
- Use Canvas 2D 2.5D with original sprite art, a coherent tile-cached environment, readable spell VFX and depth-sorted actors as the primary path.
- Keep WebGL2 3D as an optional experiment only where actually supported; failure to initialize must fall back to 2.5D without breaking play.
- Rationale: 2.5D now uses an embedded atlas and 24 cached static scene tiles; it is more portable and visually coherent than the current low-poly software-rendered 3D path. This decision does NOT waive the 60 FPS, art, animation or owner-acceptance gates.

## D-007 — Reginald-only spell eligibility (ACCEPTED)
- The Reginald product catalogue is 18 spells: Astral Orbs; Loaded Dice, Tiny Tremors and Wicked Buzzsaw (official 1.2 starters); plus the 14 general spell-quest unlocks.
- Other wizard Ascension signature spells are excluded from Reginald's research, temporary trials, persistent unlocks and level-up offer pool.
- The trial slot is a single-player adaptation for otherwise impossible unlock prerequisites, not an original-game feature; the underlying quest conditions remain source-derived and must be labeled as adaptation where needed.
- Evidence: official 1.2 patch notes, Reginald and Spells wiki pages, and Ascension signature discussion. Sources are listed in MECHANIC_REFERENCE_MATRIX.md.


## D-008 — Natural-run pilot and multi-boss coverage gate (ACCEPTED)
- The full-mission baseline uses the default Reginald loadout. The temporary one-run spell trial is tested by its dedicated regression and must not be silently injected into the boss-coverage baseline.
- Multi-boss automated coverage requires at least three deterministic seeds, each completing a natural run, with the observed boss-ID set exactly equal to `sol`, `krog`, and `mul`.
- The pilot may only supply normal movement, ordinary interaction, and selections from cards actually offered by production. It may not set time, HP, XP, objective progress, enemy/boss state, or victory.
- Card ranking must use actual option identifiers or exact displayed labels. If the pilot fails, incoming damage, build choices, objective progress and movement must be inspected before attributing the result to production balance.
- Automated pilot success is not human owner acceptance and does not waive source-fidelity, performance, persistence, visual/audio or release gates.


## D-009 — Preserve default self-damage and model optional Harmony Pact (ACCEPTED)
- The default game rule permits caster self-damage from friendly-fire spell hazards; this is intentional source behavior, not an accidental test artifact.
- Harmony Pact is a separate covenant that disables damage to self and teammates. It is a backlog feature to scope, not an implicit global default.
- Natural-run acceptance must avoid self-damage hazards through movement and build decisions. It must not silently suppress production damage to obtain a green run.
- Evidence: official 0.7.0 patch notes https://steamdb.info/patchnotes/16553491/ and developer response https://steamcommunity.com/app/2904000/discussions/1/4513255804483189926/.


## D-010 — Keep the natural-run pilot out of map-edge and objective deadlocks (ACCEPTED)
- Loot targets outside a safe interior envelope must not pull the pilot into an unreachable world boundary.
- When near a clamped world edge, inward movement is a hard constraint, not a weak additive preference.
- During Rift capture, remove outward radial dodge force while preserving tangential movement; objective progress must not be reset by avoidable steering drift.
- Gnasher avoidance must include lateral movement during burrow/leap, not only direct retreat.
- These are QA-agent controls only. Do not change production map bounds, objective rules or enemy damage without separate source/player evidence.


## D-011 — Emergency threat priority overrides objective progress (ACCEPTED)
- Immediate incoming projectiles and Gnasher burrow/leap threats outrank objective capture and optional loot.
- Rift containment is a normal objective preference, not an absolute movement lock; imminent lethal tells may justify a temporary exit.
- Hard inward boundary steering activates only near the actual world clamp. Perimeter objectives remain reachable.
- When Gnasher is in a burrow/leap sequence, suspend objective and loot pursuit and use a lateral escape vector.
- These are automated QA-agent rules only. Do not change production objective radius, map bounds or enemy damage without separate source/player evidence.
