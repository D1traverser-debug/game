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
- Each wizard has a distinct starter spell, stat profile, passive, active Q ability and palette/sigil treatment.
- One bounded Verdant Wilds map has six named districts, seven ruins/landmarks, a river, two bridges, a pilgrim road, central rift, visible boundary, map preview and live minimap.
- Q activates the wizard ability; M collapses/opens the minimap; touch has a dedicated ability button.
- Map movement and enemy/chest/boss spawn coordinates are clamped to the realm bounds.
- Existing enemy/objective/boss/spell/progression/camp systems are retained.
- Browser regression for roster/map/abilities added; CI status pending.

## Important limitations
- The four playable portraits/characters use palette and sigil treatments of the existing atlas hero, not four bespoke production character rigs.
- One map's environmental interaction and obstacle collision still need playtest review.
- All four heroes need natural full-run balance/boss acceptance.
- Original animation, VFX, music/SFX and final visual/audio review are not complete.
- Firefox/WebKit, physical mobile/controller devices, real-origin save reload and owner playtest remain untested.
- Status stays NOT_READY until exact-build owner acceptance.

## Next sequence
1. Run the roster/map/ability browser regression and the complete CI matrix.
2. Fix failures and preserve all existing solo regressions.
3. Run natural solo missions for each wizard and boss archetype; balance only from recorded evidence.
4. Finish one-realm navigation/obstacle/collision and character visual readability.
5. Complete audio, VFX, save recovery, browser/device performance and owner acceptance.

CAOS is read-only. Do not touch CAOS repositories or configuration.
