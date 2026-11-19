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
- Browser regression now covers roster, abilities, map districts, river slowdown and bridge passage; CI status pending.
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
1. Run roster/map/ability/audio browser regressions and the complete CI matrix.
2. Fix failures and preserve all existing solo regressions.
3. Run natural solo missions for each wizard and boss archetype; balance only from recorded evidence.
4. Finish one-realm navigation/obstacle/collision and character visual readability.
5. Complete audio, VFX, save recovery, browser/device performance and owner acceptance.

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
