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
