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
- Krog'wa (medium-confidence community evidence; Namu mirror page last edited 2026-08-01): three health segments; after one segment is depleted a magnetic field constrains the arena; documented patterns are inhale/pull, tongue charge and tracking spit. Official 0.13 notes independently confirm a tongue-smash attack and list Krog'wa's health at 165,000. The same patch note mentions tornado damage, but official 1.1 notes place tornadoes in the Pyrestorm Pit environment; do not attribute tornadoes to the Verdant Meadow boss baseline without further evidence. Sources: https://namu.moe/w/The%20Spell%20Brigade ; https://steamcommunity.com/app/2904000/announcements/ ; https://steamdb.info/patchnotes/20496068/
- Mul'gath (medium-confidence community evidence): three health segments; head count increases after each segment; attacks include head whip, ground spike grid and linked small minions that move toward the boss. Official 1.1 notes confirm healing minions can be corrupted and damage Mul'gath on collision, confirm boss corruption behavior and reference phase-transition damage resistance. A June 2026 gameplay transcript additionally reports rock walls, orb absorption and spin; those are low-confidence/version-ambiguous candidates and are excluded from the acceptance baseline pending current-version corroboration. Sources: https://namu.moe/w/The%20Spell%20Brigade ; https://steamcommunity.com/app/2904000/announcements/ ; https://www.dailymotion.com/video/xa9kq46
- Sol'phish: retain the source-backed targeted obelisk/runestone, radial projectile, homing projectile and stagger/vulnerability pattern. Official 0.13 notes confirm Sol'phish can be corrupted and use the obelisk attack on enemies; community boss reference describes the runestone/radial/homing pattern and stagger meter. Source: https://steamcommunity.com/app/2904000/announcements/ ; https://namu.moe/w/The%20Spell%20Brigade
- Version discipline: the community boss summary predates 1.2 and attack timing/radii/damage are not pinned. Phase count and attack identity are evidence-backed design inputs; exact numerical tuning remains provisional.

### Spell and quest progression
- The 1.1 official patch explicitly sets the third spell slot at player level 13 and fourth at level 20. When a new spell is acquired, an upgrade can be chosen immediately; the third/fourth slots start at spell levels 3/4. The second-slot milestone is still unverified and must not be guessed.
- The community Quests reference lists spell unlock conditions for Solar Pulse, Moonerang, Arcane Broadsword, Aether Beam, Magic Missile, Rocky Road, Aurora Wings, Cardinal Runes, Talon Slash, Falling Stars, Vengeful Sprout, Phantom Blades, Impish Havoc and Bell March.
- The same quest list reports five infusions unlock Double Infusions; Fire damage 777,777 unlocks Lightning; 14,400 Lightning hits unlock Acid; 2,727,272 Acid damage unlocks Ice; 11,700 Ice hits unlock Dark. Corruption count and all-infusions title are separate quest objectives.
- Reginald-specific outfit quests: create a Void infusion as Reginald; augment Astral Orbs four times in one mission; collect a Legendary Improvement. These are meta/unlock progression, not extra heroes.
- The community wiki lists 22 spells; official 1.2 adds 3, so the current referenced catalogue has at least 25. Seismic Slam is Eugenie's signature spell and is not part of Reginald's eligible catalogue; exclude it from his pool.

### Infusion matrix
Basic: Fire, Lightning, Acid, Ice, Dark.
Advanced self-pairs: Wildfire (Fire+Fire), Thunder (Lightning+Lightning), Corrosion (Acid+Acid), Frost (Ice+Ice), Void (Dark+Dark).
Advanced mixed pairs: Plasma (Fire+Lightning), Flux (Acid+Lightning), Shadowbolt (Dark+Lightning), Glint (Ice+Lightning), Brimstone (Fire+Acid), Hellfire (Dark+Fire), Frostbite (Ice+Fire), Miasma (Acid+Ice), Blight (Dark+Acid), Wither (Ice+Dark).
The exact status/chain/crit behavior must be modeled separately per pair. Do not implement a generic pair damage multiplier.
Official 1.2 fixes Plasma burn damage to account for initial crit, and fixes Flux/Glint/Shadowbolt lightning damage to scale with crit from the initial hit. Acid duration resets on each hit instead of stacking duration. These are mandatory regression cases.

### Solo-only content boundary
- Official 1.2 explicitly removed Healing Slam from the augmentation pool in solo play because it is co-op-only. The single-player pool must filter co-op-only upgrades and quests, not merely omit networking.
- Some quest achievements require teammates (revives, ally healing, friendly-fire against teammate, etc.). They must be marked unavailable/inapplicable in the solo product, or replaced only if the original has a true solo equivalent. Do not silently invent a substitute.

### Reginald solo spell allowlist — source audit 2026-11-17
The current Reginald-only build exposes 18 spells:
- Signature: Astral Orbs.
- 1.2 starters (officially unlocked from the start): Loaded Dice, Tiny Tremors, Wicked Buzzsaw.
- 14 general spell-quest unlocks: Magic Missile, Solar Pulse, Moonerang, Arcane Broadsword, Aether Beam, Falling Stars, Phantom Blades, Cardinal Runes, Rocky Road, Aurora Wings, Bell March, Vengeful Sprout, Talon Slash, Impish Havoc.

Do not expose other wizard Ascension signatures to Reginald: Hex Bomb (Campanelli), Necro Whirl (Kavin), Spear Barrage (Wizard King), Swirl Sickle (Hatti), Scepter Mesh (Moon Mage), Seismic Slam (Eugenie), and Chthonic Charge (Sun Mage). The prototype's orbital/Astral Orbs+ placeholder is not a verified source spell and is excluded. Save migration must remove any legacy unlock/trial flag for these non-Reginald entries.

Sources:
- Official 1.2.0.20127 patch announcement (three starters and 13 new augmentations): https://steamcommunity.com/app/2904000/announcements/
- Spell Quests (14 general spell unlock quests and element/infusion quest conditions): https://thespellbrigade.wiki.gg/wiki/Quests
- All wizard spells catalogue: https://thespellbrigade.wiki.gg/wiki/Spells
- Reginald signature and traits: https://thespellbrigade.wiki.gg/wiki/Reginald
- Ascension signature mapping discussion (secondary corroboration): https://steamcommunity.com/app/2904000/discussions/0/838375062933398814/

The wiki and community discussion are secondary sources. Reconfirm against the target game build where possible. The 1.2 starter status is grounded in the official patch announcement. Do not claim the complete source game contains only 18 spells; this allowlist is specific to the one-hero Reginald product.

## Official 1.2 spell-content reconciliation (2026-11-17)
- The developer's 1.2.0.20127 notes explicitly confirm three new start-unlocked spells and four augmentations for each: Loaded Dice, Tiny Tremors and Wicked Buzzsaw. The public notes describe the core spell behavior and augmentation count, but do **not** publish the names or detailed effects of those twelve new augmentations.
- The same notes list thirteen augmentations for older spells: Aura Beam (Aether Beam), Baby Sprout (Vengeful Sprout), Chthonic Pull (Chthonic Charge), Counter Talon (Talon Slash), Massive Missile (Magic Missile), Piercing Blades (Phantom Blades), Pulling Whirl (Necro Whirl), Scepter Link (Scepter Mesh), Solar Zenith (Solar Pulse), Super Star (Falling Stars), Unrung Bells (Bell March), Waxing Moon (Moonerang), Wing Split (Aurora Wings).
- Only the Reginald-eligible subset belongs in this one-hero product. Non-Reginald signature spells and their augmentations remain excluded.
- The four augmentations for each 1.2 starter are our own named, original gameplay adaptations because official notes provide only the count, not their source names/effects. Do not label those twelve as source-faithful. Their actual mechanics must be tested individually.
- Official source: https://steamcommunity.com/app/2904000/allnews/ (6 Oct 2026, patch 1.2.0.20127); the same feed's 22 Oct 2026 performance patch makes high-entity stability a first-class quality requirement.


### Friendly fire / Harmony Pact
| Mechanic | Current baseline | Evidence | Implementation rule |
|---|---|---|---|
| Caster self-damage | Default friendly fire can damage the caster with their own spell hazards | Official Harmony Pact patch notes say the covenant prevents damage to self and teammates; developer response confirms default self/team damage is intentional | Preserve self-damage in the default baseline; pilot must evade; do not misclassify `friendlyFire` damage as a bug |
| Harmony Pact | Optional covenant disables friendly fire | https://steamdb.info/patchnotes/16553491/ | Track as a separate source-fidelity feature; add only if run modifiers are in the single-player scope |
