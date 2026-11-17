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


## 1.1 / 1.2 progression and visual evidence (added 2026-11-16)
- Official Update 1.1 notes say the third spell is acquired at player level 13 and the fourth at level 20; a new spell can receive an immediate upgrade, with the third and fourth spells immediately raised to levels 3 and 4. Source: https://steamcommunity.com/app/2904000/announcements/
- Official 1.2.0.20127 spell patch (2026-10-06) adds Loaded Dice, Tiny Tremors and Wicked Buzzsaw, described as unlocked from the start, each with four augmentations. It also adds 13 augmentations for existing spells. Source: https://steamcommunity.com/app/2904000/announcements/
- Official Steam screenshots show a 3D top-down arena, modeled characters/enemies, terrain/props, layered spell effects and HUD. Source: https://store.steampowered.com/app/2904000/The_Spell_Brigade/
- Official 2026-10-22 performance patch explicitly addresses stability/performance in Endless runs. Source: https://steamcommunity.com/app/2904000/announcements/
- Current implementation's 2D Canvas art and random spell acquisition are not faithful to this evidence.

## Official 1.2 source reconciliation — 2026-11-17
The official developer announcement dated 2026-10-06 (patch 1.2.0.20127) confirms:
- Loaded Dice, Tiny Tremors and Wicked Buzzsaw are start-unlocked.
- Each of these three new spells has four augmentations.
- The announcement publishes thirteen new older-spell augmentations by name and effect: Aura Beam, Baby Sprout, Chthonic Pull, Counter Talon, Massive Missile, Piercing Blades, Pulling Whirl, Scepter Link, Solar Zenith, Super Star, Unrung Bells, Waxing Moon and Wing Split.
- The announcement does not disclose the twelve new-spell augmentation names or detailed effects. Our four choices per new spell are independent original designs; their labels and mechanics must not be represented as exact source data.
- Solo mode excludes Healing Slam from the augmentation pool.
Source: https://steamcommunity.com/app/2904000/allnews/ (6 Oct 2026 entry, lines 43–109 when opened on 2026-11-17).


## Friendly fire and self-damage — source reconciliation (2026-11-17)
- The original game can damage the caster with their own spells when default friendly fire is active.
- The official 0.7.0 update introduced Harmony Pact, which disables friendly fire so players cannot hurt themselves or teammates. This is an optional run modifier, not the default baseline. Source: https://steamdb.info/patchnotes/16553491/
- A developer response confirms that self/team damage is deliberate and that specific augmentations can convert friendly-fire damage into healing. Source: https://steamcommunity.com/app/2904000/discussions/1/4513255804483189926/
- Therefore the prototype's `friendlyFire` damage from meteor/bell/bomb/slam/dice hazards is not automatically a production bug. The natural-run pilot must dodge these hazards. A Harmony Pact selector is a separate source-fidelity backlog item; do not silently disable self-damage in the default run.


## Boss attack fidelity gaps — source evidence (2026-11-17)
- **Krog'wa:** official EA Update 13 notes state that Krog'wa has tornado attacks and that its tongue-smash attack can be used against enemies when corrupted; the same notes say tornado damage was increased. Sources: https://steamdb.info/patchnotes/20496068/ and https://store.steampowered.com/news/posts/?enddate=1761142398&feed=steam_community_announcements. The current prototype implements a leap/acid-ring sequence only, so this is a confirmed content gap.
- **Mul'gath:** official 1.1 notes confirm healing minions and that corrupted minions can damage Mul'gath on collision. A gameplay transcript also shows spike-grid attacks, rock walls, orb absorption/healing and a spinning multi-head attack. The transcript is observational community evidence, not an official specification: https://www.dailymotion.com/video/xa9kq46. The current prototype has a projectile fan and healer minions but no verified full phase/attack set.
- Exact phase timing, hitboxes, damage, and telegraph durations remain UNKNOWN_PENDING_READBACK. Capture current-version gameplay and corroborate before freezing numbers.
