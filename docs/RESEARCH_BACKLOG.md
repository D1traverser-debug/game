# Research Backlog

Research must produce observable mechanics and testable rules, not just descriptive notes.

| Topic | Required evidence | Current state |
|---|---|---|
| Reginald base stats and Astral Orbs | Current-version official or in-game observation; targeting, orbit, hit cadence, damage, cooldown, size | PARTIAL |
| Spell list and unlock rules | Current patch notes + quest conditions + gameplay observation | OPEN |
| Five element base effects | Per-element trigger, duration, tick, scaling, visuals, audio | OPEN |
| Ten pairwise infusions | Pair matrix; interaction order, damage, status, stacking, crit, target caps | OPEN |
| Augmentations | Every included spell's augmentation choices and effect stacking | OPEN |
| Scrolls and chest behavior | Drop pools, rarity, stack limits, bans/rerolls, effects | OPEN |
| XP and level-up | XP values, magnet range, thresholds, multi-level queue, grace window | OPEN |
| Verdant Meadow enemies | Spawn schedule, HP, speed, contact/attack damage, AI state machines, drops | OPEN |
| Gnasher | Roar, burrow, underground invulnerability, approach, leap, landing AoE | PARTIAL |
| Objectives | All included objective types, success/fail conditions, timers, bounds, rewards | OPEN |
| Sol'phish | Intro, attack tells, burst, projectile patterns, stagger, vulnerability, outro | PARTIAL |
| Threat levels | Exact enemy/player scaling and spawn curve | OPEN |
| Meta progression | Camp enchantment tiers, costs, unlocks, persistent stats | OPEN |
| UI/audio | Original feedback hierarchy, sound event matrix, settings | OPEN |
| Version drift | Current official update date and affected mechanics | OPEN |

## Newly qualified high-priority work
- Determine second spell slot milestone from current 1.1/1.2 source.
- Build the 25-spell catalogue and identify Reginald-eligible spell pool; include 1.2 new spells and four augmentations each.
- Implement the 14 spell-specific unlock quests and 4 element unlock quests; keep title/outfit-only quests distinct.
- Research and implement Krog'wa and Mul'gath; confirm boss randomization and Verdant Meadows eligibility.
- Model the red summoning circle and Sol'phish runestone/stagger mechanics; use current source version.
- Implement all Verdant Meadows objective variants introduced by 1.1, with per-solo target counts.
- Trace common enemy roster and XP drop tables: Buffer, Shield Crab, Crabladon, Teethy Worm, Bloat Crab, Gnasher and remaining common types.
- Implement solo-only content filters; exclude Healing Slam and other co-op-only content.
- Add Reginald outfit quests, Wizard Rank, Enchantments, Masteries, Scroll unlocks, Ascension/Covenant subset that remains meaningful in solo play.


## Full-game production research — 2026-11-18

- Pin the latest source version before each content freeze; check for the announced post-1.2 major update.
- Reconcile the full wizard roster (community guide reports 15) and every wizard's passive, stats, signature spell, unlock quest and co-op-specific interactions.
- Reconcile all four realms and their layout variants, hazards, destructible props, enemy rosters, objectives and boss eligibility.
- Build complete spell/augmentation catalogues; include the three 1.2 spells and distinguish official effects from undocumented adaptations.
- Build the seven-element and ten-pair interaction matrix; confirm stacking, status, crit, friendly-fire and co-op rules.
- Map co-op rules: friendly fire, revive, team objectives, individual/shared level-up timing, disconnect/reconnect and player death/return.
- Research current scroll, trial, covenant, mastery, enchantment, rank, quest, outfit and achievement progression.
- Record gameplay timing and damage only when supported by current-version observation; do not inherit provisional prototype numbers.
