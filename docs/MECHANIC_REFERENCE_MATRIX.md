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
