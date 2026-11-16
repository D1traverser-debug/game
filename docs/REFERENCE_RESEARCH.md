# Original-Game Reference Research Register

Research snapshot date: 2026-11-16. Source versions must be pinned per mechanic.

## Product identity and update context
- Official Steam announcements: https://steamcommunity.com/app/2904000/announcements/
- The official announcement feed includes the 1.2.0.20127 spell patch dated 2026-10-06. It adds Loaded Dice, Tiny Tremors, Wicked Buzzsaw and new augmentations for existing spells. Therefore older spell lists are not a complete current reference.
- The same official feed includes a performance patch dated 2026-10-22. It explicitly discusses stability/performance work for Endless runs. Performance is a core product-quality concern, not polish to defer indefinitely.

## Scope: Reginald
- Community reference: https://thespellbrigade.wiki.gg/wiki/Reginald
- Reported identity: Reginald, "The Apprentice"; signature spell Astral Orbs.
- Reported unique bonuses: +2 Luck and +10% chance to find Health Potions and Magnets.
- Reported signature spell modifiers: +25% spell size and -12% cooldown.
- These numbers require confirmation against the pinned game version before implementation is marked accurate.

## Scope: Verdant Meadow
- Community reference: https://thespellbrigade.wiki.gg/wiki/Verdant_Meadows
- First realm/map, lush grassland/flower field presentation.
- Unique enemy: Gnasher.
- No environmental hazards are listed for this realm in the current community page.
- Gnasher behavior reference: https://thespellbrigade.wiki.gg/wiki/Gnasher — surfaces, roars, burrows, travels underground toward the player while mostly invulnerable, then leaps from below and damages nearby enemies on landing. Community data reports it drops a purple XP orb.
- These are behavioral targets; exact timings and damage values need versioned confirmation.

## Spell progression and infusions
- Community reference: https://thespellbrigade.wiki.gg/wiki/Quests
- A community guide reports normal spell infusion milestones at levels 7 and 14; another wizard may differ. Reginald must be tested against the selected source version.
- Element set commonly documented: Fire, Lightning, Acid, Ice, Dark. Pair combinations need their own verified behavior matrix; do not implement all pairs as generic damage multipliers.
- Spell unlocks are quest-gated in the source game. A local static list of all spells does not prove the original unlock progression.

## Sol'phish
- Historical official patch reference: https://steamdb.info/patchnotes/17171436/
- Patch 0.7.2.2392 (2025-01-29) records a boss intro/outro, burst attack, and stagger capability for Sol'phish. This is historical evidence only; current behavior must be checked against later updates and actual gameplay.
- Do not invent multi-phase behavior as a substitute for source fidelity. Telegraph, burst timing, stagger threshold, vulnerability window, and recovery need independent observation.

## Important version and evidence caveats
- Community wiki pages can be incomplete or stale; do not use them as a single source of truth.
- The official announcement feed is dynamic; capture the exact announcement and date when a new behavior is adopted.
- The reference links above are research starting points, not a claim that the original executable was inspected.
- We must not copy extracted proprietary assets, source code, animations, sound, music, or game data files. Use independent implementation and original visual/audio assets.
