# Project Charter

## Product
An independently implemented, single-player browser recreation of the observable gameplay systems and play experience of **The Spell Brigade**, limited to one wizard and one realm.

## Owner-defined constraints
- One hero: Reginald.
- One map: Verdant Meadow.
- One player; no co-op or online multiplayer.
- No AI companions or teammates.
- No additional heroes or maps.
- Final deliverable: a single HTML file that can be opened directly in a browser and run offline.

## Quality intent
"Recreation" means fidelity to the original's gameplay loop, combat behavior, spell identities, progression, infusion/augmentation interactions, enemy behavior, mission objectives, boss encounter, pacing, UI feedback, sound feedback, and complete win/lose/retry loop. A themed arena with generic auto-attacks does not meet the definition.

## Independent implementation boundary
We may reproduce observable mechanics and independently authored behavior. We must not copy proprietary source code, extracted game data, original artwork, animations, fonts, sound recordings, or music. Visuals/audio must be independently created while matching the functional readability and overall quality target as closely as practical. This is an unofficial fan project.

## Definition of Done
A release candidate is done only when:
1. The requirements traceability matrix has no unaccepted P0/P1 requirement.
2. The complete 19-minute (or source-verified current-version) run is playable by a human from start to victory or defeat without test hooks.
3. Boss mechanics can be understood, avoided, staggered, and defeated through normal gameplay.
4. Progression and all included spell/infusion/augmentation combinations work in live combat.
5. Save/load survives actual browser close/reopen and corrupted/old save recovery.
6. Desktop and mobile input work without layout or input deadlocks.
7. Performance meets the frozen target on documented reference devices.
8. Visual and audio reviews find no blocking quality defects.
9. Independent review and owner playtest are completed.
10. The exact final HTML is self-contained, offline, versioned, hash-verified, and reproducibly generated from the repository.
