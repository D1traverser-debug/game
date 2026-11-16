# INTEGRATION-003 — Integrated 3D Single-file Browser Game

Date: 2026-11-16
Current source: development/index.html
Candidate SHA-256: 07bd70906f1020f2c5343d0ab4c16950a863cfc8b42e639fdaa74ef938fae648
Size: 148,704 UTF-8 bytes
Status: PROTOTYPE_COMPONENT_TEST_PASS / PRODUCT_NOT_READY

## What is now implemented
- A single offline HTML with HTML/CSS/JS inlined.
- WebGL2 instanced 3D terrain, camera, independently authored wizard/enemy low-poly meshes, trees, roads, objective markers, projectiles, pickups and boss silhouettes. Existing Canvas2D renderer remains as a fallback.
- Integrated with the previous player movement, combat, XP, spell progression, level-13/20 slots, infusion, spell augments, objectives, HUD, pause/camp/result and localStorage code.
- 9 types of objectives including fungi, statues, crab, rift, sludge, sacrifice, cores, braziers and mana beasts, with simplified post-completion variants.
- 3 boss IDs and combat state machines: Sol'phish, Krog'wa, Mul'gath. Krog'wa and parts of Mul'gath are independent approximations and require source-version validation.
- 1.2 spell starter pool: Loaded Dice, Tiny Tremors and Wicked Buzzsaw. Each has 4 currently prototype-specific augments; 13 official older-spell augmentations have at least partial implementations.
- Source-grounded XP orb rewards now use normal 7, rare 12, epic 17 and legendary 21 XP, replacing the previous 0.3/1 XP common drop under the simplified spawning model.
- Gnasher burrow damage immunity; before this patch target selection excluded burrow but the damage pipeline did not.
- Dynamic boss HUD labels and a smoother green field + meandering road instead of the previous checkerboard.
- Production HTML does not expose window.__QA; integration tests inject temporary probes into a test-only page.

## Tests actually executed
1. Node.js syntax of both embedded scripts: PASS.
2. Playwright visible Chromium under Linux Xvfb/SwiftShader:
   - menu, game start, 3D context, HUD, pause and resume PASS;
   - no captured JavaScript exceptions, console errors or external network requests;
   - WebGL2 gl.getError returned 0.
3. Synthetic browser diagnostic (test hook NOT committed in production HTML):
   - all 9 objective generation and reachability bounds PASS;
   - all 3 bosses instantiate and advance their attack timers PASS;
   - Gnasher burrow damage immunity and resumed vulnerability PASS;
   - each of the 3 new 1.2 spells has 4 defined augment options PASS;
   - these are component checks, NOT actual player success.
4. Existing Playwright spell progression regression: 17/17 PASS after adapting the script-tag count from one to two scripts.
5. SHA-256 from local final artifact: 07bd70906f1020f2c5343d0ab4c16950a863cfc8b42e639fdaa74ef938fae648, size 148704.
6. File navigation and localhost URL navigation were both blocked by the test container policy (net::ERR_BLOCKED_BY_ADMINISTRATOR), so actual browser-origin save/close/reopen remain NOT_TESTED.

## Performance and visual limitations
- The prior 2D baseline with 200 enemies measured about 21.6 FPS in a software-runner test.
- Integrated WebGL software renderer showed approximately 18-25 FPS in observed test snapshots; no valid real-hardware FPS acceptance exists.
- Renderer was smoothed and internal resolution bounded to 0.83 DPR, but not independently benchmarked for target 60 FPS desktop / 30 FPS mobile.
- Original commercial game's model geometry, materials, animation, camera composition, effects and production audio are substantially higher fidelity.
- Programmatically generated low-poly art is NOT equivalent to the original visuals.
- Krog'wa and Mul'gath patterns, several objective variants, elemental pair mechanics, full spell unlock quest event tracking and many older spell augmentations remain incomplete.
- No human-controlled 19-minute full playthrough or normal boss kill has been verified; synthetic boss tests cannot substitute.

## Test evidence & reproduction
- CI: tests/progression_regression.py, tests/game3d_integration.py, scripts/verify_project_state.py and tests/test_state_guard.py.
- Command: python tests/progression_regression.py
- Command: python tests/game3d_integration.py
- Reports from the local test run: game3d_component_report.json, game3d_persistence_report.json (blocked), and screenshots are retained in this ChatGPT conversation, not part of the production artifact.
- Original-game sources: official Steam updates and community wiki, see docs/MECHANIC_REFERENCE_MATRIX.md.

## Independent acceptance verdict
**NOT_READY**. The deliverable is a materially improved integrated 3D game prototype. It is not yet a high-fidelity, commercially accepted recreation. The code, tests and recovery state are archived to enable continued source-grounded development.
