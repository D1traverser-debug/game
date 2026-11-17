# HANDOFF — Full-Game Production

## Current authoritative checkpoint — 2026-11-18

- Active branch: `full-game`.
- Branch base: `d9e9e390af320bf8245eac5c92f54bb8965a31ad` (the latest documented development checkpoint).
- `main` remains preserved at `eace4cb66f282d35c663f3a13d6e39ff8a15e0b8`.
- `development` remains the legacy single-player Reginald / Verdant Meadows browser prototype.
- Legacy browser artifact: 734,011 bytes, SHA-256 `7a98c8989cbfb85f53063f69507c023f3bd899ed1b1eba97271fb44c45955bd9`.
- Legacy CI #44131377996 passed 10/10 jobs; boss component regression passed 26/26. This is prototype evidence only, not full-game acceptance.
- Full-game product status: **NOT_READY**.

## Owner's new directive

Build a complete independent game that can substitute for The Spell Brigade in gameplay depth. Gameplay mechanics may be independently reimplemented; the shipped game must have original title, characters, world, models, textures, animations, UI expression, text, music and sound recordings.

The previous Reginald-only / Verdant Meadows-only / solo-only / single offline HTML restrictions are superseded on `full-game`. They remain historical constraints for the legacy prototype.

## Full-game target

- Solo and 1–4 player online co-op.
- Full current-version content breadth: complete wizard roster, all four documented realms, spells, the complete primary-element and advanced-infusion catalogue (element counts remain disputed), augmentations, scrolls, objectives/variants, enemy/boss roster, quests, trials/covenants and meta progression.
- Provisional community inventory: 15 wizards, four realms, seven elements, ten dual combinations, 78 achievements. Counts require source-version reconciliation.
- Windows PC first; keyboard/mouse and controller. Steam distribution target; other platforms/cross-play are later gates.
- Engine direction: Unity 6.3 LTS + URP for a bounded vertical slice. Engine choice remains conditional on measured performance, 4-client networking and owner workflow.
- CAOS repository/assets remain read-only.

## Source snapshot

Official reference evidence available at this checkpoint:
- Steam product page: solo + 1–4 online co-op, team objectives, cross-platform multiplayer feature listing.
- Update 1.1 Realm Sweep: 2026-09-02; new wizard Eugenie, Seismic Slam, 10 quests, objective variants, realm/map variants and destructible props.
- Update 1.2.0.20127: 2026-10-06; Loaded Dice, Tiny Tremors, Wicked Buzzsaw, four augmentations each, and 13 named older-spell augmentations.
- Performance patch: 2026-10-22.
- Full source links and uncertainty are recorded in `docs/REFERENCE_RESEARCH.md`.

## Next action

Create the Unity 6.3 LTS URP project skeleton. Then build one polished vertical slice that proves:
1. One original hero and one fully authored realm.
2. Three distinct spells and one meaningful elemental interaction.
3. Three enemy archetypes, one objective and one boss.
4. Original character/enemy animation, environment art, spell VFX, UI, SFX and adaptive music.
5. Solo and 1–4 player host-authoritative play.
6. Stable performance under representative enemy/projectile load.

Do not mass-produce placeholder heroes, spells or maps before this slice passes. Keep the browser prototype isolated. Update state, decisions, issues and evidence after each meaningful change.


## Scope-guard CI correction — 2026-11-18

- First full-game CI: `44141591159`. Reproducible legacy artifact check PASS; new full-game scope guard PASS; browser objective and art renderer/boss jobs passed; checkpoint job failed only because the negative-control fixture still set `multiplayer=True` (the new required value), so it did not create drift.
- Corrected the fixture to set `multiplayer=False` and added an active-branch drift negative control. No production game code or content changed.
- Rerun required. Full-game product remains NOT_READY.


## Full-game branch mechanical CI — GREEN (2026-11-18)

- Commit: `daead42f4790e5afb8b2343f8271894fac0895b3`.
- CI: [44141825172](https://github.com/D1traverser-debug/game/actions/runs/44141825172), 10/10 jobs PASS.
- Scope guard now validates the expanded full-game contract and checks the exact legacy browser artifact as a preserved reference.
- All nine legacy browser regression jobs passed on the full-game branch.
- This is repository/legacy-prototype integrity only. No Unity project, native build, multiplayer, production art/audio or full-game player acceptance exists yet.


## Simulation core foundation — 2026-11-18 (CI pending)

- Added `src/core/Game.Core.csproj` targeting .NET Standard 2.1, with no UnityEngine or third-party package dependency.
- Added fixed-step `SimulationClock`: explicit pause behavior, bounded per-frame steps, preserved backlog.
- Added PCG seeded `DeterministicRng`; rendering/UI/audio must never consume gameplay RNG.
- Added central `DamagePipeline` with independently configurable friendly-fire/self-damage policy and invulnerability gate. Exact armor and damage formulas remain unfrozen pending source research.
- Added standalone .NET 8 contract runner with 12 deterministic tests.
- GitHub Actions now builds the core and runs the contract runner. Await CI before marking the foundation PASS.


## Engine-independent simulation core — GREEN CI (2026-11-18)

- Commit: `aace5c6c223d0532260fb99c7a93d6accc2774be`.
- CI [44142826420](https://github.com/D1traverser-debug/game/actions/runs/44142826420): **11/11 jobs PASS**.
- `src/core/Game.Core.csproj` targets .NET Standard 2.1 and compiles cleanly.
- Standalone .NET 8 test runner: **12/12 PASS** (fixed-step/pause/backlog, seeded PCG RNG, friendly fire, self-damage, invulnerability, lethal transition, invalid damage, max-health capacity).
- Checkpoint guard and all nine legacy browser regression jobs passed.
- No Unity project/native build or full-game gameplay/network/asset acceptance exists yet.


## Typed events and network input validation — CI pending

- Added immutable `SimulationEvent` and single-threaded monotonic `SimulationEventBuffer` for deterministic presentation/audio/network observation.
- Added `PlayerInputCommand`, allowed button flags and `PlayerCommandValidator` for registered-player membership, monotonic sequence, host tick window, finite bounded movement and valid input bits.
- These are engine-independent contracts, not a transport, lobby, anti-cheat solution or complete co-op implementation.
- Eight new deterministic tests added; CI pending.


## Unity project skeleton — committed (Editor validation pending)

- Pinned minimum Editor: Unity 6.3 LTS `6000.3.27f2`, the security-patched 6.3 LTS version published 2026-10-30.
- URP dependency declared: 17.3.0.
- Local UPM package `com.d1traverser.game-core` points to `../src/core`; code is organized under `src/core/Runtime` with `Game.Core.asmdef`.
- `unity/ProjectSettings/ProjectVersion.txt` and `unity/Packages/manifest.json` committed.
- Editor has not been launched in this environment. Package resolution, URP asset assignment, scene import and Windows build are NOT_TESTED.
- The core command validator now rejects negative sequence and client tick values. Expanded test suite: 22 contracts expected; CI pending.


## Unity skeleton / core package validation — CI green (2026-11-18)

- CI [44144343912](https://github.com/D1traverser-debug/game/actions/runs/44144343912): 11/11 jobs PASS.
- Core sources moved under `src/core/Runtime` and packaged as `com.d1traverser.game-core`; .NET Standard 2.1 build PASS, 22/22 contracts PASS.
- Unity Editor pinned to `6000.3.27f2`, URP 17.3.0 dependency declared, local package path `file:../src/core`.
- Editor has not been launched. URP asset assignment, scene, Windows build, controller, networking, production art/audio and playtest remain NOT_TESTED.
- Next: validate Unity project/package structure in CI, then open with the pinned Editor.


## Unity structure guard correction — CI pending

- First run #44144743422 verified 13/17 checks. Only four ignore-rule checks failed because the script expected literal names while the .gitignore correctly uses case-insensitive patterns.
- Updated the validator to match the exact patterns already committed. No Unity project files or production code changed.
- Rerun pending; Editor package resolution remains NOT_TESTED.


## Element inventory research correction — 2026-11-18

The previous brief's "seven elements + ten combinations" wording was too definitive. The detailed reference matrix records five primary elements and fifteen advanced infusion candidates (five self-pairs plus ten mixed pairs), while another community guide summarizes seven identities and ten combinations. Official 1.2 notes confirm some advanced infusions but not the complete matrix. The current product scope now marks this as a source discrepancy, not a frozen count. Reconcile the in-game infusion UI before implementing the full catalogue.


## Unity project structure guard — GREEN CI (2026-11-18)

- CI [44144872368](https://github.com/D1traverser-debug/game/actions/runs/44144872368): **12/12 jobs PASS**.
- Unity project structure: **17/17 PASS**.
- Game.Core: **22/22 PASS**.
- Legacy browser regression: **9/9 PASS**.
- The run validates the project files and local package path, not an actual Unity Editor launch. Package resolution, URP asset assignment, scene, native build, online co-op and production assets remain NOT_TESTED.
- The element/infusion source discrepancy has been recorded: detailed matrix says 5 primary + 15 advanced candidates; another community guide says 7 identities + 10 combinations. Do not freeze the count until in-game verification.


## Spell execution kernel — CI pending

- Added `SpellDefinition`, `SpellRuntimeState`, `TargetCandidate`, `ProjectileSpawn` and `SpellSystem`.
- Target modes: nearest enemy, lowest health ratio and deterministic random enemy; ally/dead/out-of-range targets are filtered.
- Projectile patterns: single, symmetric spread and targetless radial.
- Cooldown advances in simulation ticks; no target does not consume cooldown.
- Output is deterministic projectile spawn data; projectile travel/collision, damage integration, element/status/augmentation logic and non-projectile spell behaviors remain open.
- Ten new contract tests added; CI pending.
