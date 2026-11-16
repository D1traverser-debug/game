# AUDIT-001 — Baseline Source, Fidelity and QA-Oracle Audit

Date: 2026-11-16
Target: exact baseline index.html at main commit c7980a12e582cf3c265b8bbdaf1e7f16eecfcd6b
Status: CONFIRMED_FINDINGS / NOT_READY

## 1. Original owner goal and scope
Recreate the observable single-player experience of The Spell Brigade as a browser game, not a theme-only imitation:
- Reginald only; Verdant Meadow only; one human player.
- No online multiplayer, matchmaking, AI teammates, additional heroes or maps.
- Final player deliverable: one self-contained offline HTML file.
- Fidelity covers gameplay loop, spells, unlocks, level progression, infusions, augmentations, enemies, objectives, boss, UI/audio feedback, balance, performance, save continuity, and a complete win/lose/retry cycle.

## 2. Evidence reviewed
- Exact baseline artifact: 116,721 bytes; SHA-256 c14e0f3210320453b0b81b6d49fbd55ae372cf36cfe99a91902d089b8672ef3a.
- Previous QA harness: studio_release_qa.py.
- Previous result: studio_release_qa_result.json.
- Official update feed: https://steamcommunity.com/app/2904000/announcements/
- Official Steam product page/screenshots: https://store.steampowered.com/app/2904000/The_Spell_Brigade/
- Reginald: https://thespellbrigade.wiki.gg/wiki/Reginald
- Verdant Meadows: https://thespellbrigade.wiki.gg/wiki/Verdant_Meadows
- Gnasher: https://thespellbrigade.wiki.gg/wiki/Gnasher
- Quests: https://thespellbrigade.wiki.gg/wiki/Quests
- Sol'phish: https://thespellbrigade.wiki.gg/wiki/Sol%27phish

Community pages are research leads, not authoritative executable truth. Source version and confidence must be recorded per mechanic.

## 3. Confirmed code findings

### F-001 — Every spell is force-unlocked on every page load (P0)
Baseline line 139 assigns the full spell catalogue to save.unlocks, excluding only orbital. This overwrites the persisted unlock set whenever the page loads. It defeats quest unlock progression and makes the camp/research UI claim everything is unlocked. The nearby spellMilestones function also unlocks spells by invented kill-count thresholds rather than the source game's individual quest conditions.

Violated invariant: a persisted unlock is granted only by its source-derived quest condition or explicit initial-unlock rule.

### F-002 — New spells can be offered at arbitrary levels (P0)
The baseline offerUpgrade function creates a new-spell option when the player has fewer than four spells and a random roll is below 0.27, regardless of player level. Official 1.1 notes say the third spell is received at player level 13 and the fourth at level 20. A new spell can immediately receive an upgrade; the third and fourth slots receive additional starting levels. The second-slot trigger still requires a pinned source check.

Violated invariant: spell-slot acquisition is governed by source-version progression milestones, not a per-level random chance.

### F-003 — Current 1.2 spell content is incomplete (P0)
Official 1.2.0.20127 (2026-10-06) adds Loaded Dice, Tiny Tremors, and Wicked Buzzsaw, described as unlocked from the start, each with four augmentations. None is present in the baseline spell definition list.

### F-004 — Infusion test has a nondeterministic false-negative path (P1)
The previous test sets one spell to level 13 and injects a large XP amount, then checks randomly generated upgrade cards for an infusion. Because the production upgrade generator can randomly choose a new spell and random active spell, the test does not guarantee that the target spell is selected. The observed level_14_infusion_offered=false is therefore not a valid deterministic verdict on the infusion rule. It exposes both a test-oracle defect and the unlock-pool defect in F-001.

### F-005 — Boss acceptance is synthetic (P0)
The previous harness calls damageBoss(1e7). It proves only that an artificial lethal-damage event transitions to a result screen. It does not verify player-readable telegraphs, avoidance, boss attacks, stagger accumulation, vulnerability, real spell damage, or victory.

### F-006 — Full-run acceptance is synthetic (P0)
runSteps(28750,true) advances simulation time using test hooks and an immortal-player flag. This is not a human-playable run and cannot establish survival, objective completion, progression quality, or real combat balance.

### F-007 — Save/reload acceptance is missing (P0)
Storage was mocked in an about:blank document. JSON round-trip is not a real close/reopen test of the local HTML file. The test environment blocked file:// navigation; that limitation must remain NOT_TESTED.

### F-008 — Performance fails the provisional desktop target (P0)
Previous benchmark at 200 active enemies: 46.39 ms average / 100 ms p95 / approximately 21.6 FPS. A fresh repeat in this environment measured 32.78 ms average / 50 ms p95 / approximately 30.5 FPS. Both fail the 60 FPS target. The variation indicates a noisy environment; renderer comparisons require a frozen device/load profile and repeated runs.

### F-009 — Production artifact contains a debug-control surface (P1)
The shipped HTML includes a query-gated window.__QA object with direct state mutation, time jump, forced boss damage, direct finish, and immortal simulation functions. This does not belong in a release artifact. Tests must instrument a temporary copy or use a separate test bundle.

### F-010 — 2D visual representation is below the source target (P0)
The baseline uses Canvas 2D with simple vector geometry and pre-rendered 2D enemy sprites. Official Steam screenshots show a 3D top-down environment with modeled characters/enemies, layered terrain/props, perspective, dynamic spell VFX, impact feedback, and dense combat. The current artifact does not match that visual structure.

## 4. Root-cause elevation L0–L5

| Layer | Finding |
|---|---|
| L0 runtime | Unlocks, spell offers, infusion test results, boss victory and long-run QA can present misleading states. |
| L1 component | save.unlocks is overwritten; new-spell offers are random; test API can force the result; content definitions are stale/incomplete. |
| L2 workflow | Requirements are not mapped to individual game state transitions; tests mutate the state they claim to verify; progression and unlock rules are mixed in one random upgrade generator. |
| L3 architecture | Game content, player progression, persistent unlocks, simulation, rendering and test controls are tightly coupled inside one HTML script. |
| L4 governance | Feature presence and synthetic state transitions were accepted as product proof; source version was not pinned; no independent product gate rejected the false Boss/full-run PASS. |
| L5 meta-governance | Development optimized for visible feature count and immediate runnable output rather than source fidelity, player outcomes, and evidence quality. The process did not challenge its own test oracle. |

Primary common cause: the project lacks a versioned, source-derived content/progression contract and an independent acceptance boundary. The symptoms are not fixed by changing one number or adding more spell names.

## 5. Competing solution assessment

| Option | Root-cause coverage | Risk | Decision |
|---|---|---|---|
| A. Patch the unlock assignment only | Low: fixes one symptom, leaves invented kill thresholds and slot timing | High residual | Rejected as complete solution |
| B. Rebuild progression as versioned content + quest state machines + deterministic level-up scheduler | High for progression | Medium, testable in isolation | Selected |
| C. Keep every spell unlocked as a simplification | None for fidelity | Fatal product mismatch | Rejected |
| D. Rewrite the entire game before testing the core loop | Potentially broad | High regression and schedule risk | Rejected as first move |
| E. Separate deterministic simulation/content from renderer and UI, then rebuild one vertical slice | High systemic coverage | Medium | Selected as program direction |

## 6. Controlled next experiment
1. Freeze source version as 1.2.0.20127 plus later official notes available by 2026-11-16; record conflicts rather than inventing missing rules.
2. Implement a progression contract for starting spells, spell-slot milestones, quest-gated spells, level-7/14 infusion eligibility, spell levels, and augmentation eligibility.
3. Add deterministic tests for fresh save, existing save migration, unlock conditions, negative conditions, level 12/13/14/19/20/21 boundaries, and locked infusion elements.
4. Verify new 1.2 spells are available at start and each has four distinct augmentation behaviors.
5. Do not claim full fidelity until each included mechanic has a source card, state machine, visual/audio feedback and live-combat test.

## 7. Learning and regression invariants
- Never overwrite persisted unlock state with a content catalogue.
- A content catalogue is not an unlock state.
- A level-up test must deterministically control the candidate pool and RNG.
- A boss test cannot directly set boss HP to zero.
- A full-run test cannot skip the player gameplay loop and still be called a playthrough.
- A persistence test must cross an actual browser reload boundary.
- A source version update requires a content-diff review and regression impact map.
- The executor does not certify its own product outcome.

## 8. Verdict
The baseline is a useful prototype, not a faithful recreation and not a release candidate. The most urgent work is the progression contract and a rendering architecture that can reproduce the source's 3D presentation. Product status remains NOT_READY.
