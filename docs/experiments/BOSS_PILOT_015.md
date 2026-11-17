# BOSS PILOT 015 — Multi-boss natural-run acceptance harness repair

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `48f7132abcdaaab89dd9fb97d4688ed40a21036a`  
Product artifact: `index.html` unchanged  
Product status: **NOT_READY**

## Observed failure

GitHub Actions run [44003040650](https://github.com/D1traverser-debug/game/actions/runs/44003040650) completed with checkpoint PASS and browser-component FAIL. Seed 1 died at 155.5 in-game seconds, level 10, 141 kills, HP 0/100, 134.18 damage taken, two level-1 spells, no armor/regen, and one objective. There were no page errors, console errors, or external requests.

## Root causes

1. **Impossible CI matrix:** the workflow invoked the test with only seed 1, while the test required exact coverage of all three boss IDs. The configured command could never satisfy the coverage predicate.
2. **Incorrect scroll ranking:** the pilot compared English internal IDs such as `growth` against Chinese display strings such as `健康成长`. All comparisons missed, so selection fell back to offer order. In the failing trace, `灵药恒存` was selected while `健康成长` and `魔力汲取` were offered.
3. **Weak card priority:** the pilot selected generic stats ahead of available spell-level cards, leaving both equipped spells at level 1 by level 10.
4. **Non-baseline loadout:** the boss test selected a temporary Solar Pulse trial. Trial loadout behavior already has a dedicated regression and should not contaminate the default-loadout natural-run baseline.

These findings establish test-harness defects. They do not, by themselves, establish that production combat balance is correct or incorrect.

## Revision 015 changes

- Remove the temporary trial from the natural-run baseline.
- Rank scrolls by their actual Chinese display names.
- Prioritize new spells, useful spell augmentations/levels, and critical defensive options over marginal economy/mobility stats.
- Use only existing free rerolls when health is critical and no defensive/sustain/spell option is offered; never spend HP to reroll.
- Record 15-second player/objective traces and incoming damage events in the temporary browser document only.
- Run seeds 1, 2, and 3 in CI and require three natural wins plus exact `sol`/`krog`/`mul` coverage.

## Acceptance and limitations

The result is **PENDING CI** until the new run is read back from GitHub. The production HTML is unchanged. Even a green three-seed run would prove only automated natural-play coverage; it would not prove human fun/UX acceptance, full source fidelity, real-device performance, local-file persistence, or release readiness.
