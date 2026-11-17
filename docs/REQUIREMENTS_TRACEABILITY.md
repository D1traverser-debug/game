# Product Requirements and Traceability — Full Game

The full-game scope re-baseline dated 2026-11-18 supersedes the original single-player browser constraints. All source-derived content must be pinned to a specific game version and confidence level. Community wiki data is a research lead, not a final specification.

| ID | Requirement | Priority | Acceptance evidence | Status |
|---|---|---:|---|---|
| SCOPE-01 | Complete playable wizard roster; provisional target 15, each with unique passive/stats/signature spell | P0 | Versioned roster manifest; every wizard selectable and live-play accepted | BASELINED_TARGET |
| SCOPE-02 | Four documented realms: Verdant Meadows, Frozen Ancients, Pyrestorm Pit, Astral Riftlands | P0 | Realm manifest; unique layouts, enemy tables, hazards, objectives and boss eligibility | BASELINED_TARGET |
| SCOPE-03 | Solo and 1–4 player online co-op | P0 | Real 1/2/3/4-client sessions; join/leave/reconnect and full-run acceptance | BASELINED_TARGET |
| SCOPE-04 | Windows PC first; keyboard/mouse and controller; native Unity build | P0 | Clean-machine native build, input matrix and release artifact verification | SELECTED_FOR_SLICE |
| IP-01 | Original title, characters, world, visual identity, UI expression, writing, music and sound | P0 | Art/audio bible, asset provenance audit, independent review | NOT_STARTED |
| CORE-01 | Full title/menu/lobby/camp/settings/run/pause/upgrade/results/retry loop | P0 | Human-driven flow in solo and online sessions | NOT_TESTED |
| CORE-02 | Movement, collision, damage, knockback, invulnerability, death and revive | P0 | Deterministic tests plus real combat and network tests | PARTIAL_LEGACY |
| CORE-03 | Automatic targeting, spell firing, projectile travel, collision, pierce and lifetime | P0 | Per-spell target/trajectory/cadence/collision tests and live combat | PARTIAL_CORE |
| SPELL-01 | Complete source-version spell catalogue with distinct identity, behavior, VFX, SFX, upgrades and augmentations | P0 | Spell cards, behavior tests, live-play and audiovisual review | PARTIAL_CORE_FRAMEWORK |
| ELEMENT-01 | Complete source-version primary-element and advanced-infusion catalogue | P0 | Reconcile five-primary/fifteen-advanced detailed matrix against seven-identity/ten-combo community summary; implement each effect and test crit/status/stacking/teammate rules | SOURCE_DISCREPANCY_OPEN |
| PROG-01 | XP, level-up, spell slots/levels, infusion, reroll/ban/lock and augmentation flow | P0 | Boundary/sequence tests and live run | PARTIAL_LEGACY |
| PROG-02 | Scrolls, chests, rarity, stack limits, quests, unlocks and meta progression | P0 | Pool eligibility, persistence and progression acceptance | NOT_TESTED |
| ENEMY-01 | Complete current-version enemy roster with unique behavior, attacks, drops and audiovisual feedback | P0 | Per-enemy state/attack/drop cards and live encounters | PARTIAL_LEGACY |
| MISSION-01 | Full objective catalogue and 1.1+ variants, including co-op/team rules | P0 | Objective-by-objective completion, failure, bounds and softlock tests | PARTIAL_LEGACY |
| BOSS-01 | Full current-version boss roster and source-grounded phase/attack/counterplay | P0 | Attack cards, telegraph/hitbox parity, natural victories and human play | PARTIAL_LEGACY |
| COOP-01 | Friendly fire, revives, team objectives and player interaction rules | P0 | 2–4 player network tests including edge cases | NOT_TESTED |
| NETWORK-01 | Host/server-authoritative simulation with validated client input | P0 | Latency/loss/desync/cheat-resistance tests and replay evidence | NOT_STARTED |
| NETWORK-02 | Lobby, invite, relay/transport, disconnect/reconnect and host-loss behavior | P0 | Real network session matrix | NOT_STARTED |
| REALM-01 | Unique biome layouts, destructible props, map variants and environmental mechanics | P0 | Per-realm traversal, collision, hazard and performance tests | NOT_TESTED |
| UX-01 | Legible HUD, lobby, objectives, level-up/scroll flow, pause, results and retry | P0 | Usability review in solo and four-player combat | PARTIAL_LEGACY |
| UX-02 | Keyboard/mouse and controller; scalable UI and accessibility settings | P1 | Hardware interaction matrix | NOT_TESTED |
| AUDIO-01 | Original adaptive score, realm/boss themes, spell/enemy/UI SFX, spatial audio and mix controls | P0 | Audio event coverage, mute/volume tests and independent mix review | NOT_STARTED |
| ART-01 | Original stylized 3D character, enemy, realm, animation, VFX and UI asset production | P0 | Vertical-slice art review and peak-combat readability | PARTIAL_LEGACY |
| SAVE-01 | Versioned save/load, migration, corruption recovery, unlock and settings persistence | P0 | Actual native close/reopen and fault injection | NOT_TESTED |
| PERF-01 | Stable 60 FPS target at 1080p on frozen reference PC under peak solo/4-player load | P0 | Five repeated benchmark runs with CPU/GPU/memory/network telemetry | NOT_TESTED |
| QA-01 | No crashes, softlocks, desyncs, unfinishable objectives or invalid progression | P0 | Automated regressions plus player-driven sessions | NOT_TESTED |
| RELEASE-01 | Reproducible, versioned native release with asset/license manifest | P0 | Clean-machine build, hashes, provenance and rollback | NOT_READY |
| ACCEPT-01 | Independent review and owner playtest | P0 | Signed acceptance record and no unresolved blocker | NOT_READY |

## Source-version policy

The initial research snapshot is the official 1.1 Realm Sweep update (2026-09-02), 1.2.0.20127 spell patch (2026-10-06), and performance patch (2026-10-22), with any later official update incorporated only after readback. The 1–4 player online co-op description is official. The 15-wizard and four-realm inventory is community-reported and remains provisional. Element classification is disputed: one detailed matrix reports five primary elements plus fifteen advanced infusion effects, while another community guide reports seven element identities and ten dual combinations. Resolve against the selected source version before freezing.

## Legacy evidence

The browser prototype contains partial Reginald/Verdant Meadows systems. Its 10/10 CI workflow and 26/26 boss component probes are prototype regression evidence only. They do not pass the new full-game, multiplayer, native-build, asset-quality, audio, or full-content requirements.
