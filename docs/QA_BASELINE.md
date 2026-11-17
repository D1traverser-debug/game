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


## Natural-run pilot #127 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44008420760  
Checkpoint: PASS. Short browser regressions: PASS. Three-seed natural-run matrix: FAIL.

| Seed | End time | Objective | Failure evidence |
|---|---:|---|---|
| 1 | 376.4s | Fungi | Died near (-968,709); early boundary override blocked a valid objective at y=810; repeated contact/projectile hits |
| 2 | 168.9s | Rift | Progress reached 70.32; repeated projectiles landed while Rift evasion was suppressed |
| 3 | 515.2s | Soul Sludge | Repeated Gnasher burrow/leap hits while the pilot continued objective/resource pursuit |

All runs had no page errors, console errors or external requests. Revision 018 changes only test-agent priority and diagnostics; product HTML remains unchanged.


## Natural-run pilot #128 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44009463457  
Checkpoint: PASS. Short browser regressions: PASS. Three-seed natural-run matrix: FAIL.

| Seed | End time | Main failure evidence |
|---|---:|---|
| 1 | 397.3s | Two Gnasher hits (282.4/284.6 raw); friendlyFire hit at 388.2s |
| 2 | 372.6s | Six projectile hits from 334.4s to 350.7s, then Gnasher hit (279.9 raw) |
| 3 | 373.9s | Two Gnasher hits (280.1/280.4 raw) |

No browser, console or external-network errors. Source review identified fixed Gnasher landing-point mechanics and a defensive-card precedence bug in the test pilot. Revision 019 corrects the pilot and adds telemetry; product HTML remains unchanged.


## Natural-run pilot #129 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44012660542  
Checkpoint: PASS. Short browser regressions: PASS. Natural-run matrix: FAIL (2/3 wins).

| Seed | Outcome | Boss | Evidence |
|---|---|---|---|
| 1 | Death at 412.4s | None | Gnasher hit 287.1 raw; player was 18.6 units from recorded landing target; only 13 leap-safe frames |
| 2 | Natural win at 1265.9s | Krog'wa | Level 22; 1657 kills; 3 objectives; 591.6/800 HP |
| 3 | Natural win at 1265.7s | Mul'gath | Level 22; 1617 kills; 2 objectives; 247.1/400 HP |

No browser, console or external-network errors. Exact boss coverage currently lacks Sol'phish. Revision 020 targets multi-Gnasher threat switching and escape displacement near world boundaries; product HTML remains unchanged.


## Natural-run pilot #130 — harness failure
Run: https://github.com/D1traverser-debug/game/actions/runs/44013848128  
Checkpoint: PASS. Short browser regressions: PASS. Natural-run matrix: NOT EXECUTED.

Python failed to parse the test file at line 385 because JavaScript instrumentation was inserted outside the Python string that constructs the temporary browser document. This is a test-harness syntax failure, not a gameplay failure. Revision 021 corrects the Python/JavaScript boundary.


## Natural-run pilot #131 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44014209474  
Checkpoint: PASS. Short browser regressions: PASS. Natural-run matrix: FAIL (2/3 wins).

| Seed | Outcome | Boss | Evidence |
|---|---|---|---|
| 1 | Natural win at 1274.6s | Mul'gath | Level 21; 1394 kills; 3 objectives; 1227.4/1300 HP |
| 2 | Death at 506.8s | None | Three projectile hits (56.8/56.8/56.6) plus contact during fungi progress 19; Gnasher nearby but no Gnasher hit; projectile predicted t=1.31s, miss distance 0 |
| 3 | Natural win at 1229.9s | Sol'phish | Level 22; 1771 kills; 4 objectives; 761.4/1100 HP |

No browser, console or external-network errors. Krog'wa is separately verified by CI #129 seed 2. Revision 022 addresses the vector-override conflict between Gnasher and projectile avoidance.


## Natural-run pilot #132 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44014779710  
Checkpoint: PASS. Short browser regressions: PASS. Natural-run matrix: FAIL (0/3 wins).

| Seed | End time | Main failure |
|---|---:|---|
| 1 | 466.9s | Three Gnasher hits; only 20 leap-safe frames (CI #131 dynamic controller had 327) |
| 2 | 187.3s | Repeated projectile hits during Rift; first predicted approach t=1.47s exceeded the 1.35s trigger |
| 3 | 661.0s | Gnasher hit 329.4 raw at 48.1 units from landing point |

No browser, console or external-network errors. Revision 023 reverts the harmful Gnasher lock and extends projectile detection horizon.


## Natural-run pilot #133 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44015470700  
Checkpoint: PASS. Natural-run matrix: FAIL (2/3 wins).

| Seed | Outcome | Boss | Evidence |
|---|---|---|---|
| 1 | Death at 1237.7s | Sol'phish | Reached boss; six Gnasher hits; final raw hit 434 at 31.8 units from landing target near left edge |
| 2 | Natural win at 1217.1s | Krog'wa | Level 22; 1992 kills; 254.6/300 HP |
| 3 | Natural win at 1390.7s | Krog'wa | Level 20; 1485 kills; 482.1/700 HP |

No browser, console or external-network errors. Mul'gath is independently verified in CI #131 seed 1. Revision 024 adds dynamic all-landing scoring and actual post-clamp travel.


## Normal-play smoke #134 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44016473737  
Checkpoint: PASS. Normal-play smoke: FAIL at 82.8s (77 kills, level 8, 0 HP). No runtime/console/network errors.

The old smoke agent was unseeded, selected the first upgrade option, chased XP only, ignored health orbs and threat telegraphs, and did not capture damage events. Revision 025 adds deterministic seed 20261117, defensive/sustain upgrade selection, health priority, enemy/projectile/hazard avoidance, and damage telemetry. The survival assertion is retained.


## Natural-run pilot #135 — 2026-11-17
Run: https://github.com/D1traverser-debug/game/actions/runs/44017267943  
Checkpoint: PASS. Deterministic 90-second smoke: PASS. XP/objective/upgrade/browser regressions: PASS. Natural-run matrix: FAIL (0/3 wins).

| Seed | Death | Failure |
|---|---:|---|
| 1 | 132.2s | Five projectile hits; first four from 111.7–119.6s; 1.8s threshold was blocked by outer 1.35s guard |
| 2 | 588.8s | Two Gnasher hits near left edge; 59 and 26.2 units from landing points; planner assumed fixed 0.55s |
| 3 | 823.2s | Contact damage during Crab objective; HP 36.5% one second before death; retreat threshold 30% was too late |

No page, console or external-network errors. Revision 026 corrects these three controller defects while preserving the 90-second survival gate.


## Natural-run pilot #137 — nondeterministic double-clock failure (2026-11-17)
Run: https://github.com/D1traverser-debug/game/actions/runs/44030442251  
Checkpoint, progression, 90-second normal-play, objective and upgrade regressions: PASS. Natural-run matrix: FAIL. No page, console or external-network errors.

| Seed | Result | Evidence |
|---|---|---|
| 1 | Death at 492.97s | Level 16, 508 kills, 1 objective; no boss |
| 2 | Natural Krog'wa win at 1196.4s | Level 22, 2062 kills, 3 objectives |
| 3 | Death at 123.87s | Level 8, 107 kills, 0 objectives; no boss |
| 9 | Krog'wa spawned; scout only | 1142.9s, 651.6/900 HP; no victory claimed |
| 10–11 | Death during Mul'gath attempt | Boss spawned; neither run won |
| 12 | Natural Mul'gath win at 1206.33s | Level 23, 2242 kills, 3 objectives |

The same seed 1 had naturally defeated Krog'wa in CI #136 at 1259.5s, but died at 492.97s in CI #137. Root cause was confirmed in the test architecture: the manual agent called `update(0.1)` while the production `requestAnimationFrame` loop also called `update(SIM_STEP)`. The two clocks advanced one game concurrently and consumed seeded randomness in different orders. Revision 028 gates production-frame updates during manual simulation, adds a one-clock assertion and same-seed replay, and compacts logs. This is a test-harness correction, not a production gameplay change.


## Natural-run pilot #138 — deterministic outcomes and upgrade-policy defect (2026-11-17)
Run: https://github.com/D1traverser-debug/game/actions/runs/44032832722  
Checkpoint, progression, 90-second normal-play, objective and upgrade regressions: PASS. Single-clock assertion: PASS. Same-seed seed-1 replay: PASS (identical signature). Browser/console errors and external requests: zero. Natural-run matrix: FAIL.

| Seed | Outcome | Boss | Evidence |
|---|---|---|---|
| 1 | Death at 376.8s | None | Level 13, 340 kills, 1 objective, 1200 max HP, only Astral and Loaded Dice; last hit was a Gnasher leap for 280.5 damage |
| 2 | Natural win at 1264.1s | Mul'gath | Level 21, 1610 kills, 3 objectives, 484.4/800 HP |
| 3 | Natural win at 1213.6s | Sol'phish | Level 21, 1655 kills, 3 objectives, 253.5/400 HP |
| 6 | Scout only | Mul'gath | Boss naturally spawned at 1142.9s; no victory claimed |
| 9–10 | Scout only | Sol'phish | Boss naturally spawned at 1142.9s; no victory claimed |

The single-clock correction made the run deterministic. Seed 1's upgrade log then exposed a pilot defect: defensive max-HP cards were selected even when health was full, and a healthy offer containing a new Wicked Buzzsaw spell was rejected in favor of dodge. Revision 029 changes only the pilot's choice policy and adds a regression assertion. No production balance changes.
