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
