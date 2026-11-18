# Browser Game Architecture

## Layers
1. Bootstrap and capability detection.
2. Input adapters: keyboard/mouse, Gamepad API, touch → normalized commands.
3. Fixed-step simulation and seeded RNG.
4. Entities: players, enemies, bosses, projectiles, pickups, objectives, hazards.
5. Combat: targeting, spells, collision, damage, statuses, death and revive.
6. Progression: XP, levels, spell slots, elements, infusions, augments, scrolls and unlocks.
7. Versioned content data for wizards, spells, enemies, bosses, objectives, realms and meta.
8. WebGL2 renderer: camera, meshes, materials, lighting, animation, instancing, VFX and culling; 2.5D fallback.
9. DOM UI: menus, lobby, HUD, upgrade cards, codex, settings, pause and results.
10. Audio adapter: music layers, SFX, ambience and independent mix.
11. Versioned persistence, migration, backup/export and recovery.
12. Authoritative WSS networking, snapshots/events and reconnect.
13. Deterministic tests, Playwright, real-device profiling and human acceptance.

The root HTML is a monolithic solo prototype and rollback point, not final architecture. Migrate incrementally into modules.

## Invariants
Simulation is independent of DOM/render/audio. Fixed ticks and seeded gameplay RNG are independent of frame rate. Presentation never consumes gameplay RNG. Server owns networked gameplay-critical state; clients send intent only. Boss telegraph, collision and active damage derive from one attack instance.

## Deployment
Static frontend plus separate WSS room service, TLS, versioned assets, monitoring and rollback. No CDN runtime.


## Browser-native simulation module foundation

`web/src/core` now contains ES modules for fixed-step clock, PCG seeded RNG, combatants/damage policy, sequenced events, input validation, swept-circle projectiles and data-driven spell casting. Node built-in tests cover the contracts. These modules are not yet wired into the legacy HTML game loop; integration and behavior parity are an explicit next gate.


## Runtime integration checkpoint

The live browser loop now uses the modular `FixedStepClock` at 30 Hz. The clock resets on new run and discards fractional debt while outside active play. A legacy fallback remains if the module cannot load in a standalone/file-origin preview. Static packaging copies and hash-verifies all eight ES modules. Other core modules are not yet integrated.
