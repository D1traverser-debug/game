# HANDOFF — Aetherwilds Single-Player

## Owner scope — 2026-11-18
The owner narrowed the product to one complete, offline-capable browser single-player game:
- One realm: 翠影荒野 / Verdant Wilds, bounded 2400 × 1800, six districts and seven landmarks.
- Four playable wizards: Aster, Ember, Briar and Nyx.
- One complete solo expedition loop: character select, combat, objectives, upgrades, boss, victory/defeat, results, camp and replay.
- Desktop browser first, mobile touch support, keyboard/mouse and gamepad.
- No multiplayer, lobby, WSS room server, Unity/native build or additional realms/rosters.

## Current checkpoint
- Branch: full-game.
- Root index.html remains the playable runtime.
- Four wizard selection and persistent selected-character state are implemented.
- Each wizard has a distinct starter spell, stat profile, passive, active Q ability, palette/sigil treatment and an in-world headpiece overlay.
- One bounded Verdant Wilds map has six named districts, seven ruins/landmarks, a river, two bridge crossings, a pilgrim road, central rift, visible boundary, map preview and live minimap.
- River/bridge geometry is shared by rendering, map preview and terrain queries; shallow water slows movement to 72%, while bridge corridors preserve normal movement.
- Q activates the wizard ability; M collapses/opens the minimap; touch has a dedicated ability button.
- Map movement and enemy/chest/boss spawn coordinates are clamped to the realm bounds.
- Existing enemy/objective/boss/spell/progression/camp systems are retained.
- Last verified browser baseline: CI run 44491163465 passed 24/24 jobs on commit 266928c87a8ad5c4fd3340f258b34d348aa0ca9f. The objective RNG integration candidate adds a required browser regression; its full CI matrix is pending.
- A malformed HUD gradient expression that prevented the main runtime from parsing has been fixed; both inline scripts pass syntax parsing.

## Important limitations
- The four wizards still share the same base atlas body; distinct headpieces, palettes and sigils improve readability but do not replace four bespoke production character rigs.
- Shallow-water movement and bridge passage are implemented; solid obstacle collision around ruins/props remains unimplemented and needs a deliberate navigation playtest.
- All four heroes need natural full-run balance/boss acceptance.
- Procedural ambient music now has layered chord pads, stereo arpeggios, bass and boss-intensity layers; SFX have shaped envelopes and filtering. This is still procedural placeholder sound design, not a final authored soundtrack or professional mix.
- Original animation/VFX polish, impact variation, spatial mix and final visual/audio review remain incomplete.
- Firefox/WebKit, physical mobile/controller devices, real-origin save reload and owner playtest remain untested.
- Status stays NOT_READY until exact-build owner acceptance.

## Next sequence
1. Complete the objective RNG candidate's full CI matrix, including same-seed traces, different-seed divergence, world-layout independence, render/audio/pause isolation and the four-wizard natural-run gate.
2. If green, migrate enemy-director spawn decisions and entity IDs in a separate bounded RNG slice; preserve all existing solo regressions.
3. Continue combat/loot/spell/chest/boss RNG migration only as individually scoped, behavior-parity-tested changes; do not claim full-run replay until all gameplay entropy is owned.
4. Continue one-realm navigation, obstacle/collision, character identity, VFX/audio and save-recovery work.
5. Complete physical browser/device/controller and representative-hardware performance checks, followed by owner/independent acceptance.

CAOS is read-only. Do not touch CAOS repositories or configuration.


## CI reconciliation — 2026-11-18
- Latest failed run 44276499906 had two independent causes: PROJECT_STATE byte count lagged the exact UTF-8 HTML by one byte; audio test attempted a pointer click on the top-bar sound button while the upgrade modal correctly intercepted pointer events.
- Updated the artifact byte count to 767208 and moved mute/unmute verification to the unobstructed menu before starting the run.
- This fixes the identified test/metadata causes only; rerun CI before recording a pass.
- Product status remains NOT_READY. Remaining product work includes unique in-world wizard silhouettes, solid landmark/prop navigation, all-four-wizard natural full-run coverage, browser/device checks and owner playtest.


## Visual identity pass — 2026-11-18
- Added distinct in-world mantles and signature focus weapons for Aster, Ember, Briar and Nyx. The existing atlas body/headpiece remains the shared base; this improves silhouette/readability without pretending to be four bespoke production rigs.
- Rebuilt the seven ruin instances as seven landmark-specific silhouettes (Sunspire, Oathgate, Moonfen Temple, Mossfall Altar, Starwell, Eastwatch, West Shrine).
- Added short-range nameplates when the player approaches a landmark.
- Added a browser render test that pixel-hashes all four hero renders and all seven landmark renders.
- Current CI is pending. The game remains NOT_READY pending collision/navigation, natural full-run coverage for every wizard, device testing and owner acceptance.


## Landmark navigation pass — 2026-11-18
- Added solid collision footprints to all seven authored landmarks.
- Player movement uses axis-separated collision resolution so the wizard slides along structures rather than sticking.
- Nyx's dash respects the same collision boundaries.
- Enemy/boss spawn points, chests and objective spawn locations are moved to nearby open ground; multi-rift nodes are also checked.
- The roster/map browser regression now tests landmark blocking, wall sliding and safe spawn relocation.
- Random meadow trees, bushes and stones remain decorative/non-solid. Natural monster/boss navigation still needs full-run verification.


## Four-wizard natural-run acceptance — 2026-11-18
- Added `tests/wizard_natural_run_regression.py`.
- It reuses the existing deterministic, non-cheating full-run pilot and runs Aster, Ember, Briar and Nyx in separate clean browser contexts with fixed seeds 41–44.
- Each run has up to 1500 in-game seconds and requires a natural boss spawn, natural boss defeat, and a normal result screen.
- The CI job is intentionally temporary `continue-on-error` while balance telemetry is collected. It must be promoted to a blocking release gate once all four characters pass.


## Natural-run harness correction
- First exploratory run did not reach gameplay: the test tried to access the IIFE-scoped `save` variable from Playwright's page context.
- Corrected by injecting a test-only setter inside the game's existing test marker. This does not add a production API or mutate game state outside normal character selection.
- Rerun the four fixed-seed natural runs before drawing any gameplay-balance conclusions.


## Natural-run pilot improvement
- The first complete telemetry pass revealed the test pilot never used the characters' Q abilities. This is not a valid test of the full character kit.
- The pilot now uses each character's real ability when ready and when its role makes sense: Aster/Ember on nearby threats, Briar under pressure or when wounded, Nyx when surrounded.
- Added an in-scope getter for the selected character; the previous `selected: null` value came from trying to read an IIFE-scoped variable outside the game closure, not from a failed selection.
- The first no-Q runs did die before the boss (Aster 664s, Ember 634s, Briar 106s, Nyx 554s). Do not tune balance from those runs; rerun with Q enabled.


## Natural-run probe injection correction
- The previous selected-character getter was not present on `window` at runtime. The test now injects it adjacent to the pilot's existing `window.__setRunSeed` hook inside the game closure.
- The Q-ability pilot logic remains injected into the full-run harness. No production game API was added.


## Natural prop collision and AI navigation — 2026-11-19

- Trees, stones and bushes now have small solid footprints; grass and flowers remain passable.
- Decorative blockers are excluded from landmark buffers, the central start/rift safe zone, the river and bridge corridors, and from overlapping prop clusters.
- Enemy locomotion, ranged spacing, corruption movement, Gnasher leap movement, bosses, boss healers, crabs, beasts and scared fungi use the same collision-aware axis-slide resolver.
- Boss/minion spawn positions are relocated to clear ground.
- The map regression now checks prop collision, wall sliding and safe relocation.
- This is a code-level navigation pass; natural-run tests and human exploration are still required.


## Save recovery and collision-aware one-realm build — 2026-11-19

- The save system now keeps a last-known-good backup in localStorage.
- If the primary record is malformed, it is quarantined and the backup is restored.
- If both records are malformed, both raw values are preserved in a recovery archive and a clean schema-v4 save is initialized.
- Gold, runs, wins and best-time fields are normalized before persistence.
- Browser regression now exercises primary corruption recovery and the both-copies-corrupt fallback.
- The one-realm collision pass makes trees, stones and bushes solid, while preserving clear landmark, river, bridge and start/rift corridors. Player, enemy, boss, healer and moving objective actors share the same movement resolver.
- Product status remains NOT_READY until natural full-run acceptance and device/performance/art/audio review.


## Character selection canvas-layout repair — 2026-11-19

- Local visual inspection of the exact CI package exposed a global canvas rule leaking into the character-selection portrait and map-preview canvases. They were positioned as full-screen layers and the map preview covered the modal.
- Portrait and map-preview canvases now explicitly use normal document flow; the character grid is top-aligned and the desktop modal uses the available viewport height more effectively.
- Local Chromium verified the desktop layout at 1280×800: four character cards, portrait containment, map-preview containment and the primary start action all fit inside the modal.
- Local Chromium verified the mobile layout at 390×844: the modal scrolls, all four cards remain available and the primary start action enters gameplay without JS/console errors.
- Added these layout assertions to the roster/map regression. Updated the four-wizard natural-run harness to wait for the actual active selection screen and dynamically populated cards, and to emit useful diagnostics if selection fails.
- CI is pending. Natural full-run boss victories for all four wizards are still not established; do not tune balance until the test reaches gameplay and produces evidence.


## CI test-harness correction — 2026-11-19

- The first layout-fix CI attempt exposed a Python syntax typo in the added roster test (the JavaScript `const` keyword was used in Python); corrected.
- The natural-run browser document failed to parse because the test-only Q-ability pilot redeclared `hpRatio` in an existing function scope. Renamed all injected ability-policy locals to unique `__wizardAbility*` identifiers.
- The checkpoint guard reported the exact candidate HTML size as 781674 bytes; synchronized PROJECT_STATE to the CI-measured size.
- These are test/handoff metadata corrections. No production combat values were changed. Rerun CI before recording any natural-run gameplay result.


## Regression fixture isolation — 2026-11-19

- The roster regression's Nyx dash check reused the 90 generated map-prop colliders from an earlier collision test. It now clears and restores only that test fixture so the dash ability is exercised on a known clear lane; production collision behavior is unchanged.
- The mobile start assertion now reads the IIFE-local game state through the test-only probe, instead of trying to access lexical variables from the browser global scope.
- The natural-run test's source assertion now matches the unique renamed ability-policy identifier. CI rerun pending.


## Natural-run and boss-pull fixture correction — 2026-11-19

- Four-wizard natural-run selection now reads the selected state from the actual production character card. It no longer attempts to read localStorage from Playwright's opaque about:blank document.
- Actual persistent selection, reload, corrupted-save recovery and backup behavior remain covered by tests/save_persistence_regression.py on a real localhost origin.
- Boss pull snapshot coverage now searches for a map lane where the player can move without hitting a solid landmark or prop. The production collision resolver remains enabled.
- This commit changes regression fixtures only; it does not tune combat or make the game easier. CI must still validate the result.


## Boss magnetic-field regression fixture — 2026-11-19

- The Krog'wa arena-field test now finds an unobstructed map point outside the field radius and verifies that the magnetic pull reduces distance to the field center.
- The previous fixed test coordinate could overlap a solid landmark, so the collision resolver correctly blocked movement and produced a false negative.
- No boss attack or player collision behavior was changed. Re-run CI to confirm.


## Single-player save export/import — 2026-11-19

- Camp now provides JSON export and import.
- Export format is versioned with the AETHERWILDS_SAVE identifier and the current save schema.
- Import rejects files above 512 KB, unknown format versions, future save schemas, malformed objects and invalid persistent currency/counters.
- Valid imports are normalized through the same save migration path and persisted immediately.
- Before import, the prior primary and backup records are copied into the recovery archive.
- Browser regression covers download payload, restore of gold and selected wizard, and rejection of unsupported format versions without overwriting the current save.
- Fixed the duplicated word in the menu's realm title.


## Natural-run telemetry expansion — 2026-11-19

- The natural-run regression now records the last damage sources, Gnasher hits, boss HP, selected upgrades, and objective progress timeline for each wizard.
- This is diagnostic instrumentation only. It does not alter production gameplay or relax the natural-victory acceptance criteria.
- Use the resulting evidence to identify whether deaths are caused by contact damage, ranged projectiles, Gnasher leaps, boss attacks, poor upgrade choices or objective routing before changing balance.


## Gamepad input completion — 2026-11-19

- Added standard Gamepad API mapping: left stick moves, button 0 (A/Cross) interacts, button 1 (B/Circle) activates the selected wizard's ability, and button 9 (Start) pauses/resumes.
- Interaction, ability and pause actions trigger only on button-down edges; holding a button cannot repeat the action.
- Added controller instructions to the field manual.
- Added a Chromium browser regression for analog movement, deadzone, edge-triggered interaction/ability and pause/resume.
- Physical controller pairing and browser/device-specific Gamepad API behavior remain untested.


## Solo enemy-balance and Gnasher telegraph checkpoint — 2026-11-19

- Reduced enemy damage scaling to `1 + gameTime / 1800`.
- Gnasher base damage is lower; leap damage is now 0.9× its scaled base damage rather than 1.7×.
- Gnasher contact damage is 9% of its scaled base damage; its burrow pursuit is 2.4× movement speed and its attack recovery is longer.
- Every Gnasher leap now commits a visible, zero-damage purple landing warning at the exact landing point for the 0.55-second leap window.
- Crabladon base contact damage and ranged projectile damage were reduced; health and magnet pickup drops are more frequent.
- Enemy population target grows more slowly late in a run.
- Added `tests/enemy_balance_regression.py` to verify actual runtime damage formulas and the real burrow-to-leap warning transition.
- The four-wizard natural-run matrix must be rerun. This change is not yet proof of a complete run or player acceptance.


## Natural-run harness synchronization — 2026-11-19

The balance patch extracted enemy damage into named helpers. The long-run Playwright instrumentation still expected the previous inline formulas and aborted before simulating any wizard. Updated the test-only instrumentation to wrap `gnasherLeapDamage`, `enemyContactDamage` and the new ranged damage coefficient. This is a harness fix, not a gameplay result; the four-wizard natural run must be rerun.


## Single-player survival balance follow-up — 2026-11-19

- Reviewed the exact four-wizard natural-run telemetry from CI #44447174307. All four character-selection paths worked and the browser had no runtime, console or external-network errors, but only Briar defeated a boss (1/4).
- Aster died at 384.7s after three Gnasher leap hits of roughly 93 raw damage each. Ember died at 278s after accumulated contact/friendly-fire hits. Nyx died at 812.3s from repeated Crabladon contact.
- Reduced Gnasher leap damage from 0.90× to 0.32× its scaled base damage and general enemy contact damage from 0.09× to 0.045×. Reduced ranged projectile damage from 0.52× to 0.36×.
- Added a defensive level-up fallback: when a character remains below the minimum survival targets and the three naturally rolled cards contain no defensive stat, replace the third card with a valid max-HP, armor, regeneration or dodge option. The player still chooses; this does not auto-apply stats.
- Strengthened the enemy-balance regression to measure actual post-armor damage for a late Gnasher leap and late Crabladon contact. Strengthened character-upgrade regression to require a defensive option for an underbuilt character.
- CI for this candidate is pending. Do not claim all four wizard runs pass until the natural-run matrix is rerun.


## Natural-run harness coefficient sync — 2026-11-19

- The balance candidate passed the strengthened enemy damage regression, including post-armor Gnasher and Crabladon damage budgets.
- The first four-wizard natural-run retry aborted before starting because its test-only ranged-shot instrumentation still matched the old 0.52 projectile coefficient after production changed to 0.36.
- Updated the instrumentation and tagged-shot replacement to the current 0.36 coefficient. No gameplay code changed in this correction; rerun CI before reading any natural-run outcome.


## Boss counterplay and natural-run pilot correction — 2026-11-19

- The four-wizard run after the survival patch improved to 2/4 wins: Ember and Nyx defeated their bosses; Aster reached Sol but died under repeated boss contact/projectile pressure; Briar survived to the 25-minute cap with Mul'gath still at 8,594 / 24,000 HP.
- Production auto-cast targeting now prioritizes an in-range live Mul'gath healing servant over the boss or nearby enemies. This makes the healing mechanic's intended counterplay discoverable without changing target behavior in other boss encounters.
- The natural-run pilot now evaluates the committed line segment and every point in grid-shaped boss telegraphs, rather than treating all boss warnings as circles at the boss center. It also keeps explicit separation from boss contact range.
- Added a boss regression proving a homing spell targets an in-range Mul'gath healer even when the boss itself is closer.
- CI and a fresh four-wizard run are pending. Do not interpret the pilot correction as a natural win until the rerun completes.


## Offline browser package launchers — 2026-11-19

- Added `PLAY.bat` for Windows and `PLAY.sh` for macOS/Linux.
- Added `scripts/serve_web.py`, a Python 3 static server bound only to `127.0.0.1`; it selects the next free port in a short range and optionally opens the default browser.
- The package builder now includes both launchers and the server, records their paths/loopback endpoint in the manifest, and verifies byte-identical copies.
- If Python is missing on Windows, `PLAY.bat` falls back to opening the standalone HTML. The local server remains preferred for module loading and storage consistency.
- CI and owner-machine launch verification are pending. This is still an offline local website package, not a publicly hosted site.


## Boss body-contact counterplay — 2026-11-19

- The four-wizard natural-run trace on commit `5d6aedb` showed Aster and Ember dying during Sol'phish after repeated `source: boss` body-contact calls at 32 raw damage; Krog used 41. These are distinct from telegraphed boss attacks and their projectiles.
- Boss body contact is now treated as a low-damage bump: Sol/Mul 10 raw, Krog 12 raw.
- Each body contact applies 34–52 units of physical pushback and has a separate 1.1-second contact cooldown.
- The telegraphed boss attack definitions and their damage values are unchanged.
- Added deterministic browser checks for damage values, pushback, cooldown and source classification.
- Candidate CI and the fresh four-wizard natural run are pending. Do not claim balance acceptance until both results are inspected.


## Canonical boss source rebuild — 2026-11-19

- The first boss-contact candidate exposed a build-boundary defect: the generated root HTML was edited directly while the canonical source fragment remained unchanged.
- Moved the boss-contact implementation into `src/game/boss_encounters.js` and regenerated `index.html` using the exact `scripts/build_game.py` fragment and homing-projectile replacement rules.
- The deterministic build test now checks that the exact canonical boss module is embedded in the shipped HTML.
- Candidate CI and four-wizard natural-run validation are pending.


## Wizard action feedback animation — 2026-11-19

- Added fixed-step-decayed `castPulse`, `abilityPulse` and `hurtPulse` state to the player.
- Spell casts animate the wizard's focus/staff and emit character-color casting sparks.
- Active abilities produce a wider animated sigil ring; hit reactions add a brief red rim flash.
- The four characters retain distinct mantle, focus and regalia shapes; action feedback is layered over each character's existing identity.
- Extended browser visual regression to compare idle/cast/ability frames for all four wizards. CI pending.
- This is readable procedural animation polish, not a claim that bespoke skeletal rigs or authored animation clips are complete.


## Adaptive procedural soundtrack — 2026-11-19

- Rebuilt the music sequencer as a denser 8th-note arrangement with sustained pads, bass, character-specific melodic motifs, plucked upper harmonics and deterministic synthesized percussion.
- The score adapts to boss presence/phase and critical player health; no global gameplay RNG is used to generate noise.
- A cached deterministic noise buffer feeds filtered snare/hat/impact layers. Character motifs differ for Aster, Ember, Briar and Nyx.
- Extended the browser audio regression to verify the percussion buffer, character motif and boss/low-health adaptive layers.
- This is an original procedural score candidate, not professionally recorded music. CI and listening review are pending.


## Audio mixer, SFX and cross-browser release gate — 2026-11-19

- Added a dedicated audio settings screen with independent persistent music, combat SFX, forest ambience and UI volumes (0–100%) plus master mute and preview.
- Existing adaptive character-motif score follows the music channel. A subtle looped forest ambience follows the ambience channel.
- Added named/throttled one-shot cues for character-specific casts and abilities, elemental impacts, damage, pickups, objective completion, boss arrival/stagger, ghost phase, chests and run results.
- The audio engine remains fully procedural and offline; no external audio files or CDN runtime were introduced.
- Added a CI matrix for Chromium, Firefox and WebKit covering desktop and mobile single-player flows.
- The baseline natural run completed 4/4 wizard boss victories. Its job is now a required gate rather than continue-on-error.
- Product status remains NOT_READY pending new CI, owner listening/visual acceptance and physical-device performance testing.


## Scope, shared spell catalogue and CI reconciliation — 2026-11-19

- Owner-approved scope is one offline single-player browser game: one Verdant Wilds realm, four original wizards, one complete solo loop. Source-game co-op, WSS, additional realms, roster expansion, Unity/native delivery and mandatory production WebGL2 are OUT_OF_SCOPE.
- Commit 841178169fb2b3c8ea833a9a4a7fcb6f5f365465 reconciled the runtime spell allowlist and project governance. GitHub Actions run 44487444334 passed 24/24 jobs, including Chromium, Firefox and WebKit desktop/mobile smoke, the shared spell catalogue regression, four-wizard natural boss runs and offline package verification.
- Verified HTML artifact: 799,965 bytes; SHA-256 8faf86ac248a15f89d12a74dd052458bf3ea5dfcb680417a880f1fca828d0f85. CI artifact ID 14511171526; compressed ZIP 514,531 bytes. Download: https://github.com/D1traverser-debug/game/actions/runs/44487444334/artifacts/14511171526
- The current playable spell pool has 18 IDs: four wizard starters plus fourteen shared quest unlocks. The runtime still carries 25 definitions; seven unsupported legacy signatures are excluded from research, quest, trial and level-up eligibility. This is a product allowlist, not a claim of complete source-game parity.
- The 18-ID shared pool passed the current 13-check browser regression. A follow-up test-hardening pass is being prepared to assert the exact 25-definition inventory, exact 18-ID eligible set, all 14 quest entries, four unique wizard starters and size-upgrade eligibility.
- Product status remains NOT_READY. Bespoke character rigs/animation, authored art/VFX/UI/audio, source-version content reconciliation, physical device/controller testing, representative-hardware performance, real-player map exploration and owner/independent acceptance remain open.
- CAOS remains read-only; all work is confined to this game repository.


## Exact spell-catalogue regression and latest CI — 2026-11-19

- Latest verified branch head: 266928c87a8ad5c4fd3340f258b34d348aa0ca9f.
- GitHub Actions run 44491163465 completed SUCCESS: 24/24 jobs passed, no failed or skipped jobs. Run: https://github.com/D1traverser-debug/game/actions/runs/44491163465
- The initial hardening candidate failed because its injected test probe attempted to read SIZE_UPGRADE_SPELLS while that Set was local to offerUpgrade. The fix moved the unchanged Set to shared scope; no upgrade values or runtime eligibility rules changed.
- The exact catalogue browser regression then passed 17/17 checks: 25 runtime definitions, 18 eligible solo IDs, 14 shared quest unlocks, four unique starters, initial save contents, legacy exclusion, size-upgrade eligibility, research UI, v3 migration, quest grant/rejection, atlas load, zero runtime errors and zero external requests.
- Browser matrix: Chromium, Firefox and WebKit desktop/mobile smoke passed. Natural-run matrix: Aster/Sol'phish, Ember/Sol'phish, Briar/Mul'gath and Nyx/Krog'wa all achieved automated boss wins (4/4).
- Offline artifact: [aetherwilds-browser-preview](https://github.com/D1traverser-debug/game/actions/runs/44491163465/artifacts/14513370931); artifact ID 14513370931; ZIP 514,562 bytes. HTML source is 800,030 bytes, SHA-256 b985aa5f1227ed10e55d6ed3522f12fe5cf45c2e83b38568e09f0e8aada2a34d.
- Product remains NOT_READY. Automation does not substitute for human playtest, physical iOS/Android/controller tests, representative hardware performance, source-version content reconciliation, final art/audio, or owner/independent acceptance.
- Next engineering slice is a bounded deterministic gameplay-RNG audit and integration. Classify current random calls first; preserve separate render/audio randomness and avoid a bulk rewrite. CAOS repository remains outside this game task and unchanged.


## Deterministic RNG boundary audit — 2026-11-19

- Audit document: `docs/experiments/DETERMINISTIC_RNG_AUDIT_001.md`.
- Source inspection found 28 textual `Math.random()` occurrences (including generic `rand`/`pick` definitions), 45 `rand(` references and 11 `pick(` references. Gameplay, collision-bearing world layout, rendering and audio currently have mixed entropy ownership.
- Existing `web/src/core/seeded-rng.mjs` is a PCG-XSH-RR implementation with unit tests; `web/src/core/spell-system.mjs` already uses it for random targeting. The production browser simulation does not yet inject it.
- Do not globally replace `Math.random`: camera shake and static decor must not consume the per-run stream; local background/audio LCGs remain isolated. Random-comparator sorts must be replaced by deterministic Fisher–Yates only when their subsystem is integrated.
- Next bounded slice: per-run RNG for objective selection/generation, with same-seed trace, different-seed divergence, render/audio isolation, pause/resume and replay-seed tests. No runtime code changed during this audit.
- CAOS remains outside this game task and unchanged.


## Objective RNG integration candidate — 2026-11-19

- Integrated the canonical PCG-XSH-RR module into the generated browser HTML through `scripts/build_game.py`; no runtime RNG-module import is required.
- Each expedition now has an explicit run seed and per-run RNG. Objective type, variant, origin, object placement and brazier sequence use that stream. The result screen displays the seed and algorithm version; normal replay creates a new seed, while `startRun(seed)` supports explicit reproduction.
- Static collision-bearing meadow decoration now uses a fixed/versioned world-layout stream so open-point collision resolution is stable across run seeds. Render camera shake and procedural audio remain isolated from the per-run stream.
- Added a browser regression for same-seed/different-seed behavior, world-layout independence, render/audio/pause isolation, replay/new-seed behavior and result-screen diagnostics; added it to the required browser-component matrix.
- Natural-run test harnesses now seed the new per-run stream with their existing fixed test seeds as well as the legacy stream.
- Candidate branch: `work/objective-rng-integration-001`; implementation commit `9f9bf30df53fcde93b05ec035e2588b5dd163c73`; CI pending. Product status remains NOT_READY, and the rest of gameplay randomness remains unmigrated. CAOS remains read-only.


### CI checkpoint correction — 2026-11-19

Run `44505974849` verified the offline package (`803536` bytes; SHA-256 `ce35b6d2402a004f467e7d579283f3ae4f5bfdb44cb6e0e46fd886a644f0f667`) and the new `objective_rng_regression` browser test passed. The browser test reported 32/32 distinct objective traces across all nine objective families, eight distinct fresh run seeds, and passing render/audio/pause isolation, world-layout stability, result-screen seed visibility and offline/no-error checks. The checkpoint job then rejected stale project metadata (`803533` recorded versus `803536` actual). The metadata is corrected; full CI rerun is pending. No merge or owner acceptance has occurred.


## Objective RNG integration — full CI PASS — 2026-11-19

- Candidate branch: `work/objective-rng-integration-001`; tested commit `b99802cb1bc300a22dce1780d969cd42541db02c`.
- GitHub Actions run `44507473452` completed SUCCESS, **25/25 jobs passed**: checkpoint, package, web-core, fixed-step/damage integration, objective RNG, progression/objective collection/upgrade/audio/controller/save, browser compatibility (Chromium/Firefox/WebKit), visual regressions and four-wizard natural-run gate.
- Objective RNG browser test: 32/32 unique traces across all nine objective families; world layout independent of run seed; render/audio/pause/resume do not advance run RNG; eight fresh ordinary run seeds; result screen shows seed and algorithm; no runtime errors or external requests.
- Four natural runs all defeated their bosses and reached the result screen: Aster seed 45 / Mul'gath / 1322.9s; Ember seed 42 / Sol'phish / 1242.5s; Briar seed 43 / Sol'phish / 1190.8s; Nyx seed 48 / Mul'gath / 1226.4s. The four seed fixtures were recalibrated in the test harness only because separating static world-layout entropy changed legacy random draw consumption; no production combat or balance values were changed for this recalibration.
- Package artifact: [aetherwilds-browser-preview](https://github.com/D1traverser-debug/game/actions/runs/44507473452/artifacts/14519897430), ID `14519897430`, ZIP 516232 bytes, SHA-256 `bb95c95e44437837782173cfa1da6b59b72546045785dcdf7ab16f13ca45dff1`. Embedded `index.html`: 803536 bytes, SHA-256 `ce35b6d2402a004f467e7d579283f3ae4f5bfdb44cb6e0e46fd886a644f0f667`.
- This closes the objective RNG integration's automated CI gate, not the product release gate. The PR remains draft/unmerged; owner playtest, physical device/controller checks, performance and final art/audio acceptance remain open. Product remains `NOT_READY`.
- Next bounded engineering task: audit enemy-director spawn randomness and entity ID allocation; write a testable migration plan before touching runtime behavior. Do not bulk-replace `Math.random` and do not claim full-run replay.
- CAOS remains read-only and unchanged.


## Production art and audio identity pass — 2026-11-19

- Candidate branch: `work/production-art-vfx-audio-002`; based on the objective-RNG integration branch. Latest candidate commit at handoff: `12aaef008a703cfaaec21566dae429f363223d81`.
- Added `assets/wizard_4x4_pack.avif.b64`: original project-generated 4×4 wizard atlas, 384×384, alpha channel, 96×96 cells. Rows: Aster / Ember / Briar / Nyx. Columns: idle / walk / cast / ability.
- Embedded the atlas in the single-file offline HTML through `scripts/build_game.py`. Runtime does not fetch an external asset or CDN. If AVIF fails to decode, the existing procedural fallback remains available.
- Character selection portraits and live player rendering use the same character-specific source art. Pose selection follows movement, cast and ability pulses; separate deterministic orbit VFX identify the four elements.
- Adaptive score now uses four character-specific interval motifs and adds sparse forest bird calls on the ambience channel. Existing boss tension, percussion, independent volume controls and mute behavior remain.
- Added/expanded `wizard_visual_identity_regression.py`, `art_renderer_regression.py` and `audio_engine_regression.py` for atlas decode, four unique heroes/portraits, four action poses, moving VFX, live sprite draw, unique music motifs and offline/no-error checks.
- Exact embedded `index.html`: 842422 UTF-8 bytes; SHA-256 `f25f45870d83db5a40bbafded5068d5ddca1e544c67cf051d983ac401b021fc9`. Project state metadata synchronized.
- CI has not yet run on this candidate. Product status remains `NOT_READY`; owner review, physical device checks, full environment/enemy/spell/UI art coverage, authored-audio decision and final acceptance remain open. This is a presentation slice, not a claim that the full game is complete.
- CAOS remains read-only and unchanged.

- CI plumbing: the objective-RNG base branch now triggers the full PR matrix for objective/enemy feature branches and runs `python scripts/build_game.py --check` before packaging, so the embedded wizard atlas must be reproducible from its versioned source asset.


## Environment atmosphere and spell-impact candidate — 2026-11-20

- Stacked branch: `work/production-environment-vfx-001`, based on the green original wizard art/audio candidate `db0c29119cb0da62f977d9300b57343f476275dd`.
- Added deterministic animated river shimmer, world-anchored ambient motes, three pre-baked grain frames and layered spell beam/slash/burst/ring rendering to the 2.5D Canvas path.
- Presentation code uses `V2.age` and stable coordinate hashes only; no `Math.random`, world-layout RNG or per-run RNG calls were added.
- Added `tests/environment_visual_regression.py` and wired it into the required browser-content-visual matrix. CI pending.
- This does not close bespoke enemy animation, full spell-specific VFX, UI art, source-game fidelity, owner visual acceptance or physical-device/performance gates. Product remains `NOT_READY`; CAOS remains read-only.


## Creature art candidate — 2026-11-20

- Continued from the latest passing environment/VFX candidate (4ac13f24a116f6fa64e389c8da3309e4a838fa3a) on isolated branch work/production-creature-art-001; the stale work/production-art-vfx-audio-001 branch was not used.
- Added seven original enemy silhouettes with five cached poses each and three distinct boss renderers. Mul'gath's head growth and Krog'wa's tongue-smash pose follow existing encounter state; no combat numbers, spawn rates or gameplay outcomes were changed.
- Added a dedicated browser visual regression and promoted it to the required content/visual CI matrix.
- Product status remains NOT_READY. The custom 2D art is an original substitute, not source-game 3D asset parity. Human review, spell-specific VFX, UI art, audio listening, physical-device performance and source-version fidelity remain open.
- CAOS remains read-only and untouched.


## Creature art regression repair and full CI pass — 2026-11-20

- Candidate branch: `work/production-creature-art-001`; commit `df507720bfb678993a9f54f7e0cb1697a8f81e0f`.
- The first CI run (`44652465370`) exposed two test-harness mismatches, not a confirmed production renderer failure: `v2buildCreatureCache` is module-scoped and must be called through the injected probe closure; the art-renderer test still required legacy generic-atlas draws after enemies had moved to bespoke cached canvases.
- Corrected the probe to build the cache inside `window.__creatureProbe.cache()`. Changed the live-renderer probe to count the actual cached-creature `ctx.drawImage(sprite, ...)` call and removed the obsolete generic-atlas draw requirement. No production simulation, balance, RNG or rendering code changed in this repair.
- CI run `44653857044` completed **27/27 jobs PASS**. Deterministic build: `index.html` 857515 UTF-8 bytes, SHA-256 `ee959e218fc95cdeb65274c3ac953ddcae7b10a8f10bbb5f6fc734ca0ad33e23`; checkpoint `PASS_MECHANICAL_ONLY`.
- Visual regression: all seven enemy silhouettes distinct; five cached poses per archetype; four visible action poses; three distinct bosses; Mul'gath phase/head growth and Krog'wa tongue-smash presentation pass. Live renderer produced 143 cached-creature draw calls in the smoke sample, with seven cache types, 24 static meadow tiles and no runtime errors/external requests.
- Browser matrix: Chromium, Firefox and WebKit desktop/mobile smoke passed. Natural-run gate: Aster seed 45 defeated Mul'gath; Ember seed 42 defeated Sol'phish; Briar seed 43 defeated Sol'phish; Nyx seed 48 defeated Mul'gath (4/4).
- Offline artifact: [aetherwilds-browser-preview](https://github.com/D1traverser-debug/game/actions/runs/44653857044/artifacts/14592656128), ID `14592656128`, ZIP 550823 bytes, SHA-256 `8e32cabd2207d18d174030cf492f7475a92546326e87279cf5ac34b7ef9d0a49`.
- This closes the creature-art candidate's automated gate, not product acceptance. Source-game 3D parity, normal-scale owner visual review, full spell-specific VFX, UI art, owner listening review, physical devices, representative hardware performance and full source-version fidelity remain open. Product remains `NOT_READY`; CAOS remains read-only.
- Next bounded engineering slice: spell-specific VFX across all 25 runtime spell definitions, with deterministic/offline visual regression; then UI art hierarchy. Do not alter combat numbers or gameplay RNG as part of the presentation slice.
