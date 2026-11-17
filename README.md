# Independent Co-op Roguelite — Full-Game Production

**Repository:** [D1traverser-debug/game](https://github.com/D1traverser-debug/game)  
**Reference:** The Spell Brigade (gameplay research only)  
**Product direction:** original-IP, stylized 3D, 1–4 player co-op survivors-like roguelite.  
**Production branch:** `full-game`  
**Legacy prototype:** `development` — single-player Reginald / Verdant Meadows browser build.

> Status: **NOT READY — full-game scope re-baselined; production engine vertical slice not yet built.**

This repository is the durable source of truth for product scope, source-version research, architecture, original assets, code, tests, evidence, and cross-session recovery. A passing test count, prototype, or polished screenshot is not a complete game.

## Current product target

- Solo play and 1–4 player online co-op.
- Full content target based on the current reference snapshot: the complete wizard roster, all four documented realms, spell catalogue, seven elements and ten dual-element combinations, objectives/variants, enemies/bosses, progression, quests, scrolls, trials/covenants, and meta systems. Counts and mechanics remain version-pinned research items, not assumed facts.
- Windows PC first; keyboard/mouse and controller. Steam distribution is a target, not a claim of an existing release. Console/cross-play are later platform gates.
- Production engine decision for the vertical slice: Unity 6.3 LTS + URP. See `docs/ENGINE_EVALUATION.md`.
- Original game title, characters, names, art, animation, UI expression, writing, music, and sound recordings are not shipped. Gameplay mechanics are independently implemented from observable research. The shipped game must have its own IP and brand.

## Important branch boundary

- `main`: preserved original browser baseline; do not overwrite.
- `development`: legacy single-player browser prototype; useful for mechanics research, regression evidence, and rollback.
- `full-game`: active full-game production branch. Do not assume the old single-file HTML contract still applies.
- The old 734,011-byte HTML prototype is not the full-game release candidate.

## Canonical project entrypoints

1. `docs/PROJECT_STATE.json` — machine-readable canonical checkpoint.
2. `HANDOFF.md` — cross-session recovery and next action.
3. `docs/FULL_GAME_PRODUCT_BRIEF.md` — approved full-game product target.
4. `docs/FULL_GAME_ROADMAP.md` — phased production plan and gates.
5. `docs/ENGINE_EVALUATION.md` — engine and platform decision.
6. `docs/ART_AUDIO_BIBLE.md` — original visual/audio quality bar.
7. `docs/NETWORK_ARCHITECTURE.md` — multiplayer model.
8. `docs/REQUIREMENTS_TRACEABILITY.md` — requirements and acceptance evidence.
9. `docs/REFERENCE_RESEARCH.md` and `docs/MECHANIC_REFERENCE_MATRIX.md` — source facts, assumptions, and version pins.
10. `docs/DECISION_LOG.md` and `docs/ISSUE_REGISTER.md` — decisions, risks, and root causes.

## Production rule

Build a complete, polished vertical slice before mass-producing content. The first slice must prove the actual camera, one finished hero, one finished realm, representative enemy AI, spell/element interactions, objective loop, boss encounter, audio, performance, and 1–4 player networking. Do not build fifteen placeholder characters or four empty maps and call that progress.

## Release rule

Do not mark the product READY until all P0/P1 requirements pass on the exact native build, including real player-driven full runs, genuine boss victories, 4-player network tests, save/load, controller input, performance, visual/audio review, independent acceptance, and asset-license/provenance audit.
