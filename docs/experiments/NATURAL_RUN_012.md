# NATURAL RUN 012 — First complete non-cheating single-player victory

Date: 2026-11-17
Code artifact: `development/index.html`
Product commit: `9949288069ff71f836216be52f7afaa55915917d`
Artifact SHA-256: `2d9c2cf2e406e68d098a2ade01b3c7bd7805b9b5942f4e5f588b798222b6493a`
Artifact bytes: 721554
CI run: https://github.com/D1traverser-debug/game/actions/runs/43989883310
Verdict: **AUTOMATED_FULL_RUN_PASS_FOR_MULGATH / PRODUCT_NOT_READY**

## Test integrity
The test executes the production update loop. It only supplies directional movement, ordinary interact input for nearby chests and explicit objective items, and choices among the real level-up/augmentation cards offered by the game.

It does NOT set game time, player HP, XP, player position, objective progress, enemy HP, boss HP, boss death, result screen, or win counters. The Mul'gath win is a natural consequence of the production combat loop.

This is an automated pilot, not a human player or a subjective fun/UX evaluation.

## Observed result
- Game time: 1463.17 seconds (24m 23s simulation time).
- Boss spawn gate: 1140 seconds (19m).
- Boss: Mul'gath.
- Boss max HP: 24000.
- Boss naturally defeated: yes.
- Recorded wins/losses: 1 / 0.
- Kills: 732.
- Player level: 19.
- Objectives completed: 4.
- Spells: Astral Orbs level 1 with Orb Split; Tiny Tremors level 2 with Quake Burst and Quake Line; Wicked Buzzsaw level 4 with Saw Twin.
- Upgrade choices: 26.
- Remaining HP: 462.25 / 540.
- Armor: 52.
- Regeneration: 6.
- Damage taken: 1517.40.
- Active enemies at result: 60.
- Browser page errors: 0.
- Browser console errors: 0.
- External network requests: 0.

## Changes under test
1. Time-scaled enemy population director: target `min(64, 18 + floor(time/34))`; adaptive spawn batch size; hard active-enemy cap 64. This prevents the former unbounded wave accumulation (241 active enemies at ~7 minutes).
2. Vitality Forge max-health upgrades restore 25% of the added maximum HP immediately, and the description explains this effect.
3. Natural-run pilot prioritizes a defensive solo build (regen, armor, dodge, max HP), then spell improvements; it only selects cards actually offered by the game.
4. Full-run trace includes player health, max HP, kills, damage taken, armor, regen, damage, cast, crit, spell count, active enemies, objectives and spell levels.

## Remaining validation
- Only Mul'gath has a natural full-run win. Sol'phish and Krog'wa still require their own non-cheating full runs.
- The boss fight lasted approximately 323 seconds after the 19-minute spawn. Validate whether this duration and Mul'gath's healer pressure match source behavior; do not reduce boss HP merely to speed up CI.
- Human owner playtest and fun/readability assessment remain open.
- Local file-origin persistence, close/reopen, and real desktop/mobile hardware performance remain open.
- Original spell/element/augmentation fidelity and all objective variants still require source-by-source review.

## References
- Official developer 1.2 spell patch and start-unlocked 1.2 spells: https://steamcommunity.com/app/2904000/announcements/
- Official 1.1 objective variants and gameplay changes: https://steamcommunity.com/app/2904000/announcements/
- Official October 22 performance patch: https://steamcommunity.com/app/2904000/announcements/

**Release status remains NOT_READY.** A natural automated win is an important milestone, not proof of a commercially acceptable recreation.
