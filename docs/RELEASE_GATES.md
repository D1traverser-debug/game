# Release Gates

Release status may only advance in this order:

1. RESEARCH_BASELINED — source versions, scope, and mechanic evidence pinned.
2. REQUIREMENTS_BASELINED — requirements traced to evidence and tests.
3. CORE_LOOP_ACCEPTED — normal movement/combat/XP/upgrade/objective loop is enjoyable and stable.
4. CONTENT_FIDELITY_ACCEPTED — included spells, elements, enemies, objectives, scrolls, and boss behavior are individually verified.
5. VISUAL_AUDIO_ACCEPTED — silhouettes, animation, VFX, sound, UI, readability and feedback pass review.
6. BALANCE_ACCEPTED — representative builds and threat levels can finish; no dominant/broken/softlocked strategy.
7. PERFORMANCE_ACCEPTED — desktop/mobile targets pass repeated benchmarks.
8. SAVE_COMPAT_ACCEPTED — real browser reload, migration, corruption recovery and reset pass.
9. PLAYER_ACCEPTED — independent owner/player playtest has no blocking usability or fun defects.
10. RELEASE_CANDIDATE — exact source commit and generated artifact pass the full acceptance matrix.
11. PUBLISHED — hosted URL (if requested), release artifact and rollback plan are verified.

A gate cannot be skipped because a later stage appears visually complete. Every failed gate creates a qualified issue and root-cause record. A release is blocked by any unresolved P0/P1 issue.

## Provisional performance targets
- Desktop: target 60 FPS, p95 frame time <= 25 ms under agreed representative peak load.
- Mobile: target >= 30 FPS, p95 frame time <= 40 ms under agreed representative load.
- Freeze reference devices before release benchmarking. Report browser, OS, CPU/GPU/device, viewport, DPR, active entities, run duration and repeated sample distribution.


## Full-game production gates (added 2026-11-18)

The previous single-player browser gates remain applicable only to the legacy prototype. The full-game release additionally requires:
- **NETWORK_ACCEPTED:** real 1-, 2-, 3- and 4-player sessions; host authority; latency/loss tests; friendly fire; revive; pause/level-up; join/leave/reconnect; no state divergence or softlock.
- **CONTENT_ACCEPTED:** source-version manifest complete for the shipped roster, realms, spells, elements, augmentations, enemies, objectives, bosses, quests, scrolls and meta systems.
- **ASSET_PROVENANCE_ACCEPTED:** every model, texture, animation, font, music cue and sound recording has an editable source or lawful license record and a usage manifest.
- **ART_AUDIO_ACCEPTED:** independent review of character/world quality, animation, VFX, readability, UI, music, SFX and mix at normal and peak combat density.
- **NATIVE_BUILD_ACCEPTED:** reproducible Windows build on a clean machine, input/controller matrix, save/load, crash recovery and rollback.
