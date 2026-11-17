# Baseline QA and Evidence Reclassification

Artifact: prior conversation file `咒语旅团-单人网页版.html`  
Size: 116,721 bytes  
SHA-256: `c14e0f3210320453b0b81b6d49fbd55ae372cf36cfe99a91902d089b8672ef3a`  
Baseline date: 2026-11-16  
Current product verdict: **NOT_READY**

## Previously reported automated checks
The previous test report recorded document load through Playwright `page.set_content`, menu/start, keyboard movement, pause/resume, upgrade/augmentation/infusion offer and apply, element status effects, quest target boundary checks, boss spawn, mobile start, joystick visibility, no horizontal overflow, a synthetic 19-minute timeline jump, and no captured page errors.

These are useful component/integration probes, not full product acceptance.

## Reclassification / known invalid inferences
1. Boss victory: the test calls `damageBoss(1e7)`; it proves a forced lethal-damage state transition, not that the player can read, dodge, stagger, and defeat Sol'phish through normal combat.
2. Full mission timeline: `runSteps(28750,true)` advances simulated time with test hooks. It does not prove a human can survive and complete all objectives.
3. Persistence: storage was mocked in an `about:blank` context. JSON serialization round-trip is not an actual close/reopen test of a local HTML file.
4. File protocol: the test container blocked direct `file://` navigation; direct double-click launch remains unverified.
5. Performance: 200 active enemies produced average frame interval 46.39 ms, p95 100 ms, approximately 21.6 FPS in the reported environment. This fails the intended desktop target.
6. Visual quality: existing vector art and simple geometry do not yet establish original-game-level clarity, animation, VFX, environment density, or impact.
7. Human acceptance: no recorded independent human playtest or satisfaction result exists.
8. Source fidelity: some numbers and timings came from unpinned or community sources. The current implementation must not treat them as confirmed canonical data.

## Honest baseline matrix
| Area | Status | Evidence / gap |
|---|---|---|
| Single-file structure | PASS_STATIC | One HTML with inline style/script; external asset/network audit still needs repeat |
| Menu and start | PASS_COMPONENT | Playwright set_content |
| Keyboard movement | PASS_COMPONENT | Synthetic browser input |
| Pause/resume | PASS_COMPONENT | Synthetic browser input |
| Progression and infusion | PARTIAL_COMPONENT | Offers/apply path tested; full source accuracy and all combos unverified |
| Objective system | PARTIAL_COMPONENT | Some target bounds and schedule simulation only |
| Enemy AI | NOT_TESTED | No per-archetype full behavior acceptance |
| Gnasher | NOT_TESTED | No timed behavior state test and player observation |
| Boss | FAIL_ACCEPTANCE | Spawn path tested; kill forced with 1e7 damage |
| Full real run | NOT_TESTED | Time jumped by test harness |
| Save/reload | NOT_TESTED | Mock storage only |
| Mobile | PARTIAL_COMPONENT | Layout and joystick visibility, not device usability |
| Performance | FAIL | 200 enemy test ~21.6 FPS |
| Visual/audio | NOT_READY | No independent quality review |
| Independent player acceptance | NOT_TESTED | No human test evidence |

## Required retest corrections
- Separate test-only hooks from production artifact; no test hook should ship in the final HTML.
- Add an unassisted play mode: no forced damage, time jump, immortal mode, direct state mutation, or synthetic reward.
- Build a deterministic simulation suite for edge cases, but pair it with real browser play.
- Boss acceptance must use actual spell attacks and real attack telegraphs.
- Full-run acceptance must be completed by a human or an independently controlled player agent without debug APIs.
- Save acceptance must close and reopen the actual file in at least two supported browsers.
- Benchmark at fixed device/browser/resolution and repeat at least five times; report average and p95 frame time.


## Seeded multi-boss pilot audit — 2026-11-17

Latest inspected CI: [run 44003040650](https://github.com/D1traverser-debug/game/actions/runs/44003040650), development HEAD `48f7132abcdaaab89dd9fb97d4688ed40a21036a`.

- Checkpoint job: PASS.
- Browser-component job: FAIL at `tests/boss_archetype_full_runs.py 1`.
- Seed 1 ended at 155.5 in-game seconds before the boss window: 141 kills, level 10, HP 0/100, damageTaken 134.18, two level-1 spells, zero armor/regen, one objective. Browser, console and external-network error lists were empty.
- The CI configuration supplied one seed, but the test predicate required all three boss IDs (`sol`, `krog`, `mul`). This made the configured gate impossible to satisfy even if the one run won.
- The pilot's scroll comparator used English internal IDs against Chinese display names; the run selected `灵药恒存` despite `健康成长` and `魔力汲取` being offered. It also chose generic stat cards over available spell-level cards. The test selected a temporary Solar Pulse trial, so it was not a default-loadout baseline run.
- These are verified QA-harness defects. The run is insufficient evidence to change production balance.
- Revision 015 removes the trial from this acceptance path, ranks actual displayed scrolls and meaningful spell/defense cards, logs damage sources and objective state, and changes CI to seeds 1/2/3. Result remains PENDING until GitHub Actions readback.
- This is automated pilot evidence only. It does not establish human fun/UX acceptance, source fidelity, real-device performance, or release readiness.


## Three-seed pilot run #125 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44006013545  
Commit: `4b3df2c54937214eeb48ccaac7d9091c68b81b02`  
Checkpoint: PASS. Browser-component: FAIL at the natural-run matrix.

| Seed | End time | Level / kills | HP ceiling | Main damage evidence | Result |
|---|---:|---:|---:|---|---|
| 1 | 469.3s | 17 / 579 | 300 | Repeated enemy projectiles; 9 armor, 0 regen | Died before boss |
| 2 | 413.8s | 16 / 467 | 400 | Projectiles, friendlyFire, contact, Gnasher leap (283.8 raw) | Died before boss |
| 3 | 115.7s | 9 / 119 | 100 | Four projectiles in 4.3s near map edge | Died before objective |

All runs had no page, console or external-network errors. The failure is not a browser-runtime failure.

### Pilot root causes
- Projectile prediction used the wrong sign for closest approach. With `r = player - projectile`, future separation is `r - v*t`; an approaching projectile has positive `dot(r,v)`.
- The pilot chose spell levels ahead of available defensive stats, including Dodge and Regen.
- It did not steer away from Gnasher's recorded leap landing point or its own damaging spell hazards.

### Source-fidelity clarification
Default friendly fire includes caster self-damage. Optional Harmony Pact disables self/team damage. Preserve the default behavior; do not remove `friendlyFire` to force a green run. Sources: https://steamdb.info/patchnotes/16553491/ and https://steamcommunity.com/app/2904000/discussions/1/4513255804483189926/.

Revision 016 applies test-only corrections. Production balance remains unchanged pending a competent, telegraph-aware pilot rerun.


## Natural-run pilot #126 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44007214721  
Commit: `63da60b639dac6f73e7ecd1254acee10b4deff55`  
Checkpoint: PASS. Short browser regressions: PASS. Three-seed natural-run matrix: FAIL.

| Seed | Outcome | Evidence |
|---|---|---|
| 1 | Natural Krog'wa win | 1259.7s; level 21; 1479 kills; 4 spells at level 5; 1000 max HP; 167 HP remaining |
| 2 | Death before boss | 767.3s at (-1200,-900); Rift progress reset; stacked projectile/contact damage; boundary steering failed to escape corner |
| 3 | Death before boss | 1062.8s; Gnasher raw hit 402.7; retreat-only avoidance did not create enough lateral displacement |

All runs had no page errors, console errors or external requests. Only boss ID `krog` was recorded. Exact three-boss coverage remains unproven.

Revision 017 adds hard inward steering, safe loot targeting, Rift tangential evasion, critical-health escape and lateral Gnasher sidesteps. Product HTML remains unchanged. Separately, GAME-042 records incomplete boss attack fidelity: official notes mention Krog'wa tornadoes/tongue-smash; community gameplay evidence shows Mul'gath grid spikes, rock walls, orb absorption and spin attacks. These product mechanics remain open.
