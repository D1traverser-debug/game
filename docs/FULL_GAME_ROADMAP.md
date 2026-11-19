# Roadmap — One-Realm Single-Player Release

## Phase 1 — Playable structure
- Four-wizard selection and persistent choice.
- Per-wizard starter spell, passive, active ability, stats and in-world identity.
- One bounded realm with named districts, landmarks, river/bridges, roads, minimap and boundary feedback.
- Complete menu → run → boss → result → camp → replay loop.

## Phase 2 — Combat and content quality
- Audit all seven enemy archetypes and three bosses for telegraphs, hitboxes, damage, recovery and death.
- Audit nine objective families for spawn bounds, navigation, collection, completion, timeout and softlock handling.
- Audit spell catalogue, levels, augments, elements and scrolls; remove dead or misleading choices.
- Balance all four wizards through repeatable natural runs on standard/severe/hardcore threat; validate telegraph readability, enemy damage curves, healing cadence and boss survival.

## Phase 3 — Presentation and UX
- Distinct hero silhouettes/palettes and readable attack/ability feedback.
- Realm-specific terrain, landmarks, props, water, lighting, atmosphere and objective markers.
- Character select, HUD, minimap, ability cooldown, upgrade, pause, result and camp UI.
- Original music/SFX, separate volume controls, hit reactions, spell impact and boss cues.
- Desktop, mobile and controller interaction review.

## Phase 4 — Reliability and acceptance
- Reproducible offline package, save migration and corrupted-save recovery.
- Chromium/Firefox/WebKit plus physical mobile checks.
- Natural full-run wins/defeats for all four characters and all three bosses.
- Performance and memory profiling on representative hardware.
- Owner playtest and independent gameplay/visual review.

No networking, extra realms, Unity/native build or larger character roster is planned.


## Production art/audio pass — 2026-11-19 candidate

A first original-IP wizard identity pass is integrated: four unique sprite rows, four action poses per wizard, selection portraits, movement/cast/ability-driven pose selection and character-specific animated orbit VFX. The procedural score now has four distinct character motifs and sparse forest ambience calls. The pass is awaiting CI and live browser inspection; it does not close the remaining environment/enemy/spell/UI art inventory, recorded audio decision, owner listening review or release acceptance.


## Environment/VFX presentation candidate — 2026-11-20

A bounded renderer pass adds animated water caustics, deterministic world-space ambience, a subtle moving grain layer and richer spell-impact geometry. The automated visual gate verifies these effects are wired into the 2.5D play path and remain independent of gameplay randomness. Next priorities remain authored enemy/creature animation, spell-specific VFX, UI hierarchy, source-version content reconciliation and human playtest.
