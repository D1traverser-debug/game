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
- Full current-version content breadth: complete wizard roster, all four documented realms, spells, seven elements and ten dual-element combinations, augmentations, scrolls, objectives/variants, enemy/boss roster, quests, trials/covenants and meta progression.
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
