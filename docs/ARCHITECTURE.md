# Architecture — Single-Player Browser Game

## Runtime layers
1. Bootstrap, offline capability and input setup.
2. Input adapters: keyboard/mouse, Gamepad API and touch.
3. Fixed-step simulation clock and gameplay state.
4. World map: one bounded realm, six districts, landmarks, navigation and map data.
5. Entities: one local player, enemies, bosses, projectiles, pickups, objectives and hazards.
6. Combat: targeting, spells, active wizard abilities, collision, damage, status and death.
7. Progression: XP, levels, spell slots, elements, infusions, augments, scrolls and unlocks.
8. Character data: four stable wizard IDs, base stats, starter spells, passives, active abilities and visual palettes.
9. Presentation: 2.5D atlas renderer, environment layers, minimap, UI, camera, VFX and animation.
10. Audio adapter: music, SFX, ambience, UI and mute/volume controls.
11. Versioned persistence, migration and recovery.
12. Deterministic contracts, Playwright integration, natural-play pilots and owner acceptance.

The root index.html remains a large legacy runtime and rollback surface. Modular core files are being integrated incrementally with browser parity tests. Do not claim standalone modules are authoritative until production calls them.

## Invariants
Simulation is independent of DOM/render/audio. Fixed ticks are independent of frame rate. Presentation does not consume gameplay RNG. The player remains inside the authored map bounds. Character selection persists safely. Every active ability has a defined cooldown and effect. No production debug mutation hooks or external CDN dependencies.

## Out of scope
Network authority, rooms, lobbies, reconnect, multiplayer replication, additional realms and Unity/native runtime.


## Realm and character presentation
The 2.5D renderer now uses seven distinct landmark structures and nearby nameplates rather than repeating one ruin wall. Each of the four wizards has a unique mantle silhouette and signature focus/weapon overlay in addition to its palette, headpiece and sigil. The base atlas body is still shared; fully bespoke skeletal rigs and animation clips are not yet implemented.


## One-realm natural-prop collision and navigation

The shared world collision resolver now combines seven authored landmark footprints with generated tree, stone and bush footprints. Decorative solid props are rejected from landmark buffers, the central start/rift safe zone, river/bridge corridors and overlapping prop clusters. Player movement, enemy locomotion, boss locomotion, boss minions and moving objective actors use the same axis-separated slide resolver. Grass and flowers remain passable.


## Solo enemy pressure and telegraph rules

Enemy damage now scales with `1 + elapsedSeconds / 1800`. Gnasher leap damage, contact damage and burrow speed are isolated behind named functions so their balance can be regression-tested. The Gnasher leap snapshots its landing position and creates a zero-damage warning hazard at that exact point before resolving the leap. Enemy density grows more slowly in long runs; health and magnet drops provide additional recovery opportunities. These changes require full-run balance validation and do not imply human acceptance.


## Solo survival balance and level-up offer policy

A Gnasher leap is a telegraphed heavy hit, not a near-full-health one-shot. Standard enemy contact must remain sustainable when several enemies overlap the player. The current balance coefficients are 0.32× scaled Gnasher base damage and 0.045× scaled enemy contact damage; ranged enemy projectiles use 0.36×. Level-up offers guarantee one defensive stat choice when the character remains below the survival targets and no defensive stat was naturally rolled. This is an offer, not an automatic player-stat mutation. Validate through post-armor damage budgets and four-wizard natural-run telemetry.


## Boss healing counterplay

During the Mul'gath encounter, auto-cast spells prioritize an in-range live healing servant. This exposes the intended counterplay in a game with automatic targeting; the priority is limited to the Mul'gath encounter and falls back to normal nearest-target behavior when no servant is in range. Boss telegraph shapes remain committed at attack start and must be evaluated as circles, lines, or grids by any automated player policy.


## Boss body-contact contract

Boss body collision is a low-damage bump, distinct from committed telegraphed attacks. Sol and Mul contact for 10 raw damage; Krog contacts for 12. Contact pushes the player 34–52 world units and uses a 1.1-second cooldown. Boss skill telegraphs, projectiles and their damage remain independent. Browser regression verifies the contact contract; full-run and human balance acceptance remain separate.


## Canonical source/build boundary

Boss encounter logic is authored in `src/game/boss_encounters.js`. The root `index.html` is a generated, offline browser artifact and must be refreshed with `python scripts/build_game.py`; direct edits to the embedded fragment are rejected by `tests/test_build_reproducible.py`. This keeps the boss implementation and shipped HTML byte-aligned.
