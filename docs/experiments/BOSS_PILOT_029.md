# BOSS PILOT 029 — Balanced upgrade policy for the natural-run agent

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `2920ae4ada7b7b2bda9efb3180ec483a02cadf6c`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #138 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44032832722

Single-clock assertion and same-seed replay both passed. The seed-1 replay exactly matched the original run. No page errors, console errors or external requests.

| Seed | Outcome | Boss | Evidence |
|---|---|---|---|
| 1 | Death at 376.8s | None | Level 13, 340 kills, 1 objective, 1200 max HP, only Astral and Loaded Dice; last hit was a Gnasher leap for 280.5 damage |
| 2 | Natural win at 1264.1s | Mul'gath | Level 21, 1610 kills, 3 objectives, 484.4/800 HP |
| 3 | Natural win at 1213.6s | Sol'phish | Level 21, 1655 kills, 3 objectives, 253.5/400 HP |
| 6 | Scout only | Mul'gath | Boss naturally spawned at 1142.9s; no victory claimed |
| 9–10 | Scout only | Sol'phish | Boss naturally spawned at 1142.9s; no victory claimed |

## Confirmed pilot defect

Seed 1 reached 1200 maximum HP but had only two spells at low levels by level 13. The upgrade log shows repeated max-HP selections despite healthy HP, then a healthy offer containing a new Wicked Buzzsaw spell at 348.1s was rejected in favor of a dodge stat. This is a policy defect in the automated QA pilot, not evidence that production balance should be changed.

## Revision 029

- Prioritize sustain scrolls when HP is below 80% and defensive stats only when HP is below 62%.
- When healthy, take a new spell before defensive fallback, then scrolls, augments, spell-level bonuses, infusions, spell levels and offensive stats.
- Relegate defensive cards to a fallback when stronger progression is not offered.
- Record HP ratio for every upgrade choice and assert that a healthy new-spell offer is selected.
- Keep the agent restricted to actual upgrade offers, normal movement and ordinary interactions. No resource grants, state mutation, forced boss selection or production balance edits.

## Acceptance

Pending CI #139. Preserve single-clock and same-seed replay gates. Require natural victories for baseline seeds 1/2/3 and all three boss archetypes in one run. Product remains **NOT_READY** until source fidelity, real-device performance, persistence and human acceptance pass.
