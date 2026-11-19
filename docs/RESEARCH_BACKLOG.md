# Research Backlog — Aetherwilds Single-Player

This backlog is limited to the owner-approved product: one Verdant Wilds realm, four wizards, seven enemy archetypes, three bosses, nine objective families and an offline-capable solo expedition. Source-game research is reference evidence only; it does not authorize implementing the source game's full roster, multiple realms or co-op.

## Current product research

| Topic | Required evidence | Current state |
|---|---|---|
| Four wizard identities | Stats, starter spell, passive, active ability, movement/role and visual readability | Implemented; human balance/visual review OPEN |
| Shared solo spell pool | Stable IDs, starter eligibility, quest unlocks, targeting, cooldown, damage, level/augment behavior | 18 IDs currently eligible; full source/version reconciliation OPEN |
| Spell definitions | Runtime contains 25 definitions; only the 18-ID solo pool is eligible for research/unlock/level-up | Seven non-pool definitions need explicit disposition; do not silently expose them |
| 1.2 starter augmentations | Four choices for each of Loaded Dice, Tiny Tremors and Wicked Buzzsaw; distinguish official behavior from original adaptations | Prototype options exist; individual behavior and source evidence need review |
| Elements and infusions | Five primary-element candidates, advanced effects, pair matrix, order, stacking, duration, damage, status, crit and visuals | Inventory discrepancy unresolved |
| Seven enemy archetypes | Spawn curve, HP, speed, contact/projectile damage, AI state machine, telegraphs, drops and navigation | Implemented; balance and human readability review OPEN |
| Three boss archetypes | Attack definitions, telegraph geometry, active/recovery windows, phase transitions, healing counterplay and death | Implemented; repeated natural runs and human review OPEN |
| Nine objective families | Spawn bounds, collection, navigation, completion, timeout, rewards and softlock handling | Implemented; real-player exploration review OPEN |
| Progression and persistence | XP thresholds, level-up queue, spell slots, scrolls, chests, trials, camp costs, migration and recovery | Automated regressions pass; full content reconciliation OPEN |
| Realm navigation | Six districts, seven landmarks, river/bridges, props, collision, boundaries and minimap | Automated map/collision checks pass; human exploration OPEN |
| Audio and presentation | Character-specific feedback, VFX readability, music/SFX mix, volume persistence and provenance | Procedural candidate exists; owner listening/visual review OPEN |
| Performance | Peak combat load, frame-time distribution, memory and 15-minute stability on representative hardware | Synthetic sample only; physical profiling NOT_TESTED |

## Source-reference protocol

1. Pin the reference game version/date before treating a mechanic as current.
2. Record whether evidence is official, in-game observation, community secondary source or an original Aetherwilds adaptation.
3. Separate source-game facts from product requirements. Mechanics requiring source-game co-op, extra realms or non-roster characters are reference-only and OUT_OF_SCOPE here.
4. Never infer an undocumented mechanic from a name, icon or wiki summary.
5. Record uncertainty and rejected hypotheses in the Mechanic Reference Matrix; do not silently promote them into code.
