# Architecture and Delivery Strategy

## Product boundary
The runtime product is one offline HTML file. The engineering repository may contain modular source, design data, test harnesses, and build scripts. The build must inline all CSS, JavaScript, and original assets and must not depend on network fetches or a local server.

## Recommended target architecture
1. Game shell: menu, manual, camp, settings, HUD, pause, upgrade/scroll modal, results.
2. Simulation core: fixed-step or bounded-delta simulation; deterministic random seed option for tests; explicit run state machine.
3. Entities: player, enemy archetypes, boss, projectiles, pickups, objectives, chests, terrain/decor.
4. Combat: targeting, spell-specific attack models, hit detection, damage pipeline, status effects, crit, armor, knockback, stagger, death and drops.
5. Progression: XP, level-up queue, reroll/banish/lock, spell levels, infusion milestones, augmentations, scrolls, meta unlocks.
6. Content data: versioned definitions for spells, elements, pairs, enemies, objectives, scrolls, augmentations, difficulty and boss attacks.
7. Presentation: camera, world rendering, character/enemy animation, spell VFX, telegraphs, UI feedback, particles and screen effects.
8. Audio: original SFX/music layers, event-driven audio bus, volume/mute and accessibility.
9. Persistence: versioned schema, validation, migration, backup and corruption recovery.
10. Quality harness: deterministic simulation tests, browser integration, performance telemetry, screenshot review, and player playtest capture.

## Rendering decision
The current prototype is Canvas 2D with vector/programmatic art. Do not assume that moving to WebGL/3D is automatically the best solution. Compare:
- A. High-quality 2D/2.5D Canvas with custom sprite sheets and animation.
- B. WebGL/Three.js with custom low-poly 3D assets.
- C. Hybrid rendering.
Compare source visual fidelity, single-file packaging, load time, performance, asset creation cost, animation pipeline, and mobile support. Do not select based on visual fashion or library familiarity. A production build may inline a locally bundled engine/library, but cannot require CDN/network access.

## Final artifact
- Root `index.html` is the public-ready candidate path.
- Build must be deterministic and produce a self-contained file.
- Release report must include source commit, build command, artifact SHA-256, byte size, offline network audit, browser/device matrix, and known limitations.
