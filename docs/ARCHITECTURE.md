# Production Architecture — Full-Game 3D Co-op Roguelite

## Product/runtime boundary

The full-game branch targets a native Windows PC game built with Unity 6.3 LTS and URP. The single-file offline HTML constraint belongs only to the legacy browser prototype. Do not make the full-game runtime depend on the old HTML architecture.

## Engine and project structure

- Unity 6.3 LTS, URP, C#.
- Data-driven content definitions via ScriptableObjects and versioned runtime IDs.
- Addressables or an equivalent deterministic asset-loading layer after bundle-size and patching requirements are validated.
- Blender source projects retained for original meshes/rigs; export through a reproducible import pipeline.
- Unity Test Framework for edit-mode, play-mode, integration and performance checks.
- CI builds must pin Unity editor and package versions. Secrets/licenses are never committed.

## Runtime layers

1. **Bootstrap / platform:** app lifecycle, platform services, input, settings, crash/reporting.
2. **Session:** solo session, lobby, invite, connection state, host authority, reconnect/disconnect handling.
3. **Simulation:** fixed tick, seeded RNG, run clock, pause and run-state machine.
4. **Entities:** players, enemies, bosses, projectiles, pickups, objectives, interactables and world hazards.
5. **Combat:** target selection, spell execution, hit detection, damage pipeline, friendly fire, statuses, crit, armor, knockback, stagger, death and revive.
6. **Progression:** XP, levels, spell slots, spell levels, infusion, augmentations, scrolls, reroll/ban/lock, quests and meta unlocks.
7. **Content:** versioned definitions for wizards, spells, elements, pairs, augmentations, enemies, bosses, objectives, realms, difficulty and trials/covenants.
8. **World:** realm layouts, terrain, props, hazards, navigation and spawn directors.
9. **Presentation:** camera, character/enemy animation, VFX, hit feedback, telegraphs, post-processing and UI.
10. **Audio:** event-driven SFX, adaptive music, spatialization, snapshots, mix buses and accessibility controls.
11. **Persistence:** schema versioning, validation, migration, backups and corruption recovery.
12. **Quality:** deterministic simulation tests, network simulation, full-run pilots, frame-time telemetry, screenshot/video review, and human playtest capture.

## Engine-independent simulation core

The domain simulation lives in `src/core` as a .NET Standard 2.1 library. It owns fixed-step time, gameplay RNG and combat rules. Unity presentation, audio, UI and network transports consume core state/events; they do not own or mutate the rules. The core is tested with a standalone .NET 8 contract runner so it can be verified before the Unity Editor project is available.

## Typed events and command validation

The core exposes immutable, monotonic simulation events for presentation/audio/network adapters. Host-side command validation rejects unknown players, replayed/out-of-order sequences, stale/future ticks, invalid movement vectors and unknown button bits. This is an input-envelope gate, not a complete anti-cheat system or a transport implementation.

## Simulation and networking boundary

Gameplay-critical state is owned by the host/server. Clients submit input intent and receive authoritative snapshots/events. Rendering, audio, camera shake, particles and UI may observe simulation events but cannot mutate simulation or consume gameplay RNG. See `NETWORK_ARCHITECTURE.md`.

## Content architecture

Each content item has a stable ID, source-version card, source-confidence tag, unlock rule, gameplay data, presentation references, audio events, tests, and balance notes. Data-driven definitions configure behavior; they do not replace spell-specific code where unique behavior is required.

## Performance strategy

Profile before optimizing. Use pooled projectiles/VFX, spatial partitioning, batched/instanced rendering where useful, bounded enemy populations, LOD/culling, allocation-free hot paths, and network interest management. Benchmark CPU, GPU, memory, network bandwidth and frame-time p95 under repeatable 1-, 2- and 4-player load.

## Asset and audio pipeline

All original assets retain editable source, export settings, license/provenance, version, usage manifest and review status. See `ART_AUDIO_BIBLE.md`. Never use the original game's extracted files or recordings.

## Legacy prototype

`development/index.html` is retained as a behavioral reference and rollback artifact. Reuse mechanics only after extracting explicit requirements and tests. Do not port its monolithic structure wholesale.
