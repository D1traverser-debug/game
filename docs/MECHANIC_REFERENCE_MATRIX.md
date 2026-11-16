# Mechanic Reference Matrix — Current Evidence Snapshot

This matrix distinguishes verified source facts, community-reported facts, and implementation assumptions. A mechanic is not accepted until it has a version pin and an observable test.

| System | Current evidence | Confidence | Required implementation/test |
|---|---|---|---|
| Product format | Steam page describes Survivors-like, top-down, single-player plus online co-op | Official product page | We intentionally implement single-player only |
| Reginald | Signature Astral Orbs; +2 Luck; +10% health potion/magnet find chance; +25% spell size and -12% cooldown (community reference) | Medium | Verify values in current game; model passive and signature modifier separately |
| Initial spells | 1.2.0.20127 adds Loaded Dice, Tiny Tremors, Wicked Buzzsaw as unlocked from start | Official patch notes | Add all three; ensure only source-defined initial set is unlocked |
| Spell slots | Update 1.1: 3rd spell at player level 13; 4th at level 20; new spell gets immediate upgrade; 3rd/4th spells start at levels 3/4 | Official patch notes | Deterministic boundary tests at levels 12/13/19/20; verify 2nd-slot milestone |
| Spell unlocks | Many spells unlocked by spell-specific quests; wiki lists 21 spell quests | Community reference | Implement individual quest predicates; never use arbitrary kill-count substitute |
| Infusions | Community guide reports spell infusion at levels 7 and 14 for normal wizard; another wizard may differ | Community reference | Verify Reginald milestones; test 6/7/13/14 boundaries and all available element pairs |
| Elements | Fire, Lightning, Acid, Ice, Dark | Community reference and current code | Per-element damage/status/tick/stack/crit tests |
| Augmentations | Official 1.2.0.20127 adds 13 augmentations including 4 for each new spell and 13 for older spells | Official patch notes | Capture all current augmentation names/effects; do not substitute generic stats |
| Verdant Meadow | First realm; Gnasher unique; no environmental hazards listed on wiki | Community reference | Verify terrain, layout variants, destructible props, roads and boundaries |
| Gnasher | Roar → burrow → fast underground approach (invulnerable) → leap; nearby enemies can be damaged on landing | Community reference | State-machine tests, hitbox/timing tests, damage and drop tests |
| Objectives | Update 1.1 introduced objective variants; map-specific changes | Official patch notes | Recreate only Verdant Meadow objective types and their unlocked variants |
| Sol'phish | Historical official patch records intro/outro, burst attack and stagger; community wiki describes runestones and +200% damage during stagger | Official historical patch + community | Confirm current attack timing, telegraphs, stagger, vulnerability, damage and death |
| Performance | Official Oct 22 patch specifically addressed stability/performance in Endless | Official patch feed | Treat peak-entity performance as a release gate |
| Visual target | Official Steam screenshots show modeled 3D characters, 3D environment, top-down camera, dense spell VFX and HUD | Official Steam screenshots | Compare our independent art/animation readability to these references |

## Source register
- Official Steam page/screenshots: https://store.steampowered.com/app/2904000/The_Spell_Brigade/
- Official developer announcements/patch notes: https://steamcommunity.com/app/2904000/announcements/
- Reginald: https://thespellbrigade.wiki.gg/wiki/Reginald
- Verdant Meadows: https://thespellbrigade.wiki.gg/wiki/Verdant_Meadows
- Gnasher: https://thespellbrigade.wiki.gg/wiki/Gnasher
- Quests: https://thespellbrigade.wiki.gg/wiki/Quests
- Sol'phish: https://thespellbrigade.wiki.gg/wiki/Sol%27phish

Source version note: the latest fully identified official spell update in this snapshot is 1.2.0.20127 dated 2026-10-06; the developer posted a performance patch on 2026-10-22. Any later update found before release must trigger a source-diff review.

## Current-version source detail expansion (2026-11-16)

### Run and objectives
- The Objectives reference states four scheduled objectives at 02:00, 06:00, 11:00 and 14:00, followed by the boss at 19:00. This supersedes the older 1.0 guide's 10:00 entry for the third objective. Source: https://thespellbrigade.wiki.gg/wiki/Objectives
- Objective reward is a unique spell upgrade/augmentation choice, not simply generic gold/XP.
- XP orb values listed by the community reference: common 7 XP; rare 12; epic 17; legendary 21. Verify actual run multipliers and magnet behavior.
- Base objective types: Bewitching Fungi (19 per wizard), Crush the Statues (8 per wizard), Hunt Down the Golden Crab, Sacrifice, Seal the Rift, Soul Sludge, Unstable Spell Cores (5 for solo), Herd the Mana Beasts, Light the Braziers, and the boss objective.
- Update 1.1 added objective variants: multi-rift, Death Shrine sacrifice, scared/explosive mushrooms, Golden Crablodon and Golden Mothercrab, statues holding larger enemies, heavier Spell Cores, darker vision-obscuring Soul Sludge, following Mana Beasts, and sequence-based Braziers. Include variants applicable to Verdant Meadows and keep map-specific variants excluded.
- Objective unlock quests include: 5 completions unlock Sacrifice; 12 unlock Spell Core; 25 unlock Brazier; 40 unlock Mana Beast. Track persistent completion count and unlocked variants.

### Verdant Meadows
- It is the starting realm. The player unlocks the next realm after surviving 12 minutes; this is a separate quest, not the end-of-run boss time.
- No environmental hazards are listed for Verdant Meadows. Roads provide a movement-speed boost that lasts after leaving the road; 1.1 reworked these roads.
- 1.1 added multiple layout variants and additional/destructible props to each realm. One map scope still includes Verdant Meadows' supported layout variants.
- Gnasher is the map-exclusive enemy. It roars, burrows, becomes invulnerable while underground, tracks toward the player, then leaps and damages nearby enemies on landing.
- Other documented enemies that can appear in Verdant Meadows include Buffer, Shield Crab, Crabladon, Teethy Worm and Bloat Crab. The full spawn roster and timings need source/version confirmation.

### Boss pool
- The original has three named end-of-run bosses: Sol'phish, Krog'wa and Mul'gath. A 1.0 community guide describes Sol'phish as one of three possible bosses (1/3); a current quest reference lists defeat quests for all three. Do not treat a Sol'phish-only encounter as complete. Verify current boss selection weights and whether every boss can spawn in Verdant Meadows.
- Sol'phish source description: enemies converge on a red summoning circle; stepping on it damages the player (reported 100 on Moderate); Sol'phish emerges after a short delay; her movement speed and enemy speed increase as the fight continues; she calls down targeted rune-engraved stones; the stones can damage enemies and Sol'phish; stagger builds from damage and creates a several-second stationary window with +200% damage taken; reported 50% slow resistance; defeat drops 4 blue, 2 purple and 4 pink XP orbs. Source: https://thespellbrigade.wiki.gg/wiki/Sol%27phish
- Krog'wa and Mul'gath mechanics are NOT YET RESEARCHED. No invented attack pattern may be substituted.

### Spell and quest progression
- The 1.1 official patch explicitly sets the third spell slot at player level 13 and fourth at level 20. When a new spell is acquired, an upgrade can be chosen immediately; the third/fourth slots start at spell levels 3/4. The second-slot milestone is still unverified and must not be guessed.
- The community Quests reference lists spell unlock conditions for Solar Pulse, Moonerang, Arcane Broadsword, Aether Beam, Magic Missile, Rocky Road, Aurora Wings, Cardinal Runes, Talon Slash, Falling Stars, Vengeful Sprout, Phantom Blades, Impish Havoc and Bell March.
- The same quest list reports five infusions unlock Double Infusions; Fire damage 777,777 unlocks Lightning; 14,400 Lightning hits unlock Acid; 2,727,272 Acid damage unlocks Ice; 11,700 Ice hits unlock Dark. Corruption count and all-infusions title are separate quest objectives.
- Reginald-specific outfit quests: create a Void infusion as Reginald; augment Astral Orbs four times in one mission; collect a Legendary Improvement. These are meta/unlock progression, not extra heroes.
- The community wiki lists 22 spells; official 1.2 adds 3, so the current referenced catalogue has at least 25. Verify whether Eugenie's Seismic Slam is available to Reginald before including it in his random spell pool.

### Infusion matrix
Basic: Fire, Lightning, Acid, Ice, Dark.
Advanced self-pairs: Wildfire (Fire+Fire), Thunder (Lightning+Lightning), Corrosion (Acid+Acid), Frost (Ice+Ice), Void (Dark+Dark).
Advanced mixed pairs: Plasma (Fire+Lightning), Flux (Acid+Lightning), Shadowbolt (Dark+Lightning), Glint (Ice+Lightning), Brimstone (Fire+Acid), Hellfire (Dark+Fire), Frostbite (Ice+Fire), Miasma (Acid+Ice), Blight (Dark+Acid), Wither (Ice+Dark).
The exact status/chain/crit behavior must be modeled separately per pair. Do not implement a generic pair damage multiplier.
Official 1.2 fixes Plasma burn damage to account for initial crit, and fixes Flux/Glint/Shadowbolt lightning damage to scale with crit from the initial hit. Acid duration resets on each hit instead of stacking duration. These are mandatory regression cases.

### Solo-only content boundary
- Official 1.2 explicitly removed Healing Slam from the augmentation pool in solo play because it is co-op-only. The single-player pool must filter co-op-only upgrades and quests, not merely omit networking.
- Some quest achievements require teammates (revives, ally healing, friendly-fire against teammate, etc.). They must be marked unavailable/inapplicable in the solo product, or replaced only if the original has a true solo equivalent. Do not silently invent a substitute.
