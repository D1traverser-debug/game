# Full-Game Production Roadmap

Status: planning baseline; all milestones remain NOT_STARTED until evidence is attached.

## Phase 0 — Scope and production foundation

**Goal:** eliminate the mismatch between the old prototype and the full-game target.

Deliverables:
- Full-game charter, source-version research register, requirements matrix and issue baseline.
- Unity 6.3 LTS + URP project skeleton and pinned editor/package manifest.
- Art/audio bible, asset provenance rules and import pipeline.
- Simulation/content/presentation/network boundaries.
- CI build, edit-mode/play-mode tests, deterministic seed and performance telemetry.

Exit gate: clean native build, reproducible CI, no legacy HTML coupling, owner can open the Unity project.

## Phase 1 — Production vertical slice (highest priority)

**Content scope:** one original hero, one realm, three spells, one elemental interaction, three enemy archetypes, one objective, one boss.

**Required proof:**
- Complete 10–15 minute run loop with real movement, combat, XP, upgrades, objective, boss and win/defeat.
- Production-quality hero model, rig, locomotion/cast/hit/dodge/death animation.
- Finished environment kit, lighting, materials, props and camera.
- Spell VFX, enemy hit reactions, readable telegraphs, original UI and audio.
- Solo plus 2- and 4-player host-authoritative sessions.
- 60 FPS target at 1080p on frozen PC hardware under representative peak load; p95 frame time and GPU/CPU/memory telemetry.
- No critical desync, softlock, save corruption or unreadable combat.

Exit gate: owner and independent reviewers accept feel, readability, visual/audio quality, multiplayer stability and performance.

## Phase 2 — Core systems

- Complete simulation and damage pipeline.
- Spell/augmentation framework with individual behaviors.
- Seven-element and pair-combination framework, verified interaction matrix.
- XP, levels, spell slots, infusion, reroll/ban/lock, scrolls and chest economy.
- Enemy director, elites, boss framework, objective scheduler and realm hazards.
- Co-op friendly fire, revive, team objectives, individual progression and reconnect rules.
- Versioned save/meta progression and quest event system.

Exit gate: every core system has deterministic tests and live-play evidence; no generic placeholder behavior masquerades as content.

## Phase 3 — Content production

- Full wizard roster and signature spells.
- Full realm set and layout variants.
- Complete spell and augmentation catalogue.
- Enemy and boss roster with distinct state machines.
- Objective catalogue and 1.1+ variants.
- Scrolls, quests, unlocks, trials/covenants, enchantments/masteries, ranks, cosmetics and achievements.
- Original art, animation, VFX, SFX and music for every included item.

Exit gate: content manifest has no unimplemented P0 item; every item has asset provenance, behavior test and acceptance card.

## Phase 4 — Meta, UX and accessibility

- Main menu, lobby, invite, character select, realm/difficulty selection, camp, codex, quests, unlocks, settings and results.
- Controller navigation, remapping, text scaling, color/readability settings, camera comfort, audio mix controls and localization-ready UI.
- Save migration, corruption recovery, backup and reset.
- Tutorial/onboarding and player-facing feedback.

Exit gate: end-to-end usability and persistence acceptance in solo and co-op.

## Phase 5 — Optimization and release

- 1/2/3/4-player stress tests with enemy/projectile/VFX peaks.
- CPU/GPU/memory/network profiling; LOD, culling, pooling, batching and bandwidth optimization.
- Accessibility, localization, crash recovery, security and exploit review.
- Asset/license audit, clean-machine builds, versioning, release notes and rollback.
- Owner and independent full-run playtests.

Exit gate: all P0/P1 release gates pass on the exact native build. No release declaration from CI alone.

## Work sequencing rule

Do not parallelize content count before proving the vertical slice. First validate the complete loop and production pipeline; then scale content using data-driven definitions and repeatable art/audio production.
