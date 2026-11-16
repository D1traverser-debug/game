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
