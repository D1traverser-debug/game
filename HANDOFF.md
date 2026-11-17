# Mandatory Continuation / Recovery Entry

**Read this before making any substantive change, including after a chat interruption.**

## Source-of-truth order
1. Current GitHub `main` tree and exact commit SHA.
2. `docs/PROJECT_STATE.json` and `HANDOFF.md` from that same commit.
3. Latest accepted decision and evidence under `docs/`.
4. Exact source/test artifact at that commit.
5. Conversation summaries are navigation hints only; they never outrank repository state.

If the repository head, state file, and handoff disagree, stop and reconcile the discrepancy before coding. Do not ask the owner to repeat information already recorded here.

## Current checkpoint (after AUDIT-001)
- Active development branch: development.
- Main branch remains the preserved prototype baseline.
- Latest audit: docs/audits/AUDIT-001_BASELINE_SOURCE_AND_QA.md.
- Renderer decision: docs/decisions/ADR-001_RENDERER.md; WebGL 3D + DOM UI selected for a bounded vertical-slice experiment, not yet accepted.
- Mechanic source matrix: docs/MECHANIC_REFERENCE_MATRIX.md.
- P0 findings include forced unlocks, random spell-slot timing, missing 1.2 spells, fake boss/full-run tests, failed performance, and 2D visual mismatch.

## Current checkpoint (bootstrap)
- Repository: `D1traverser-debug/game`
- Product: single-player browser recreation of The Spell Brigade.
- Scope: Reginald + Verdant Meadow only.
- Delivery: one offline, self-contained HTML file.
- Current artifact: root `index.html`, imported from the prior conversation's 2026-11-16 prototype.
- Current status: `NOT_READY`.
- The first repository commit is a baseline capture, not a release.
- Existing prototype has working menus and partial combat/progression, but visual fidelity, exact mechanics, true full-run playability, performance, and human acceptance remain open.

## Recovery procedure
1. Read the current branch and commit SHA from GitHub; fetch the root tree and the full contents of `docs/PROJECT_STATE.json`, `docs/REQUIREMENTS_TRACEABILITY.md`, `docs/DECISION_LOG.md`, `docs/QA_BASELINE.md`, and this file.
2. Read the current `index.html` and test harnesses at that exact commit. Do not rely on an old local copy.
3. Reconcile every pending operation from the last checkpoint:
   - `COMPLETED`: read back the target and verify exact SHA/content.
   - `FAILED`: record failure evidence and root cause.
   - `UNKNOWN_PENDING_READBACK`: do not blindly retry; inspect remote state first.
4. Restore the original goal, exclusions, latest owner correction, accepted decisions, rejected options, open root causes, and next goal-causal action.
5. Continue from the next incomplete acceptance gate. Do not repeat completed research unless source/version drift invalidates it.
6. After each meaningful change, run the smallest relevant regression set, then the full impact set; read back the remote commit and files.
7. Update `docs/PROJECT_STATE.json`, `docs/DECISION_LOG.md`, `docs/QA_BASELINE.md`, and this handoff in the same change set. State exact commit, changed paths, test commands/results, and remaining NOT_TESTED items.

## Cross-conversation invariants
- Preserve one hero, one map, single-player, browser-only, one-file final delivery.
- Do not add online play, AI teammates, more heroes, or more maps.
- Do not call a feature complete because its label, menu entry, or data structure exists.
- Do not treat synthetic state injection, time skipping, forced boss damage, source inspection, or syntax checks as real player acceptance.
- Do not claim human satisfaction, official equivalence, or production readiness without the corresponding evidence.
- Do not modify any CAOS repository, file, branch, PR, plugin, Skill, configuration, or documentation.
- Never overwrite the only known-good artifact without preserving a versioned rollback point.
- When interrupted after a GitHub write, read the target branch/file before retrying.

## Next action
Perform the full source-grounded audit of the current `index.html` against the requirements and original-game references. Reclassify the baseline QA claims, identify shared root causes at L0–L5, compare architecture alternatives, then implement a test-first vertical slice for the highest-impact gameplay loop. Keep project status `NOT_READY`.


## Latest work after AUDIT-001
- Added experiments/webgl-slice.html: self-contained raw WebGL2 3D scene and instanced renderer prototype.
- Added tests/webgl-slice-smoke.py and docs/experiments/WEBGL_SLICE_001.md.
- Technical smoke passed under Chromium 144 + Xvfb/SwiftShader: WebGL2, menu-to-play, zero page/console/WebGL errors, zero external requests.
- 200-enemy synthetic scene reported ~20 FPS in software rendering. This is not a hardware performance verdict; GPU benchmark remains NOT_TESTED.
- Current renderer is still rough; no visual acceptance. WebGL 3D + DOM UI is the direction; raw WebGL2 vs bundled Three.js engine choice remains OPEN.
- Next: profile/cull/batch the 3D slice, compare engine choices on identical content, and then implement the versioned progression contract. Do not replace main index.html yet.

## Expanded source research (2026-11-16)
- Official Steam announcement feed was opened directly; latest public post found in this snapshot is the 2026-10-22 performance patch, after 1.2.0.20127 (2026-10-06).
- 1.1 patch lines 317-322 confirm third spell at player level 13, fourth at 20, immediate upgrade on new spell, starting spell levels 3/4 for slots 3/4. Second-slot milestone remains unverified.
- 1.2 patch lines 51-80 confirm Loaded Dice, Tiny Tremors, Wicked Buzzsaw (all unlocked from start), four augmentations each, and 13 named augmentations for older spells. Lines 104-109 confirm specific infusion crit fixes and removal of Healing Slam from solo.
- Current objectives reference confirms 02:00, 06:00, 11:00, 14:00 and boss 19:00; 10 objective types and 1.1 variants need implementation.
- There are three named end-run bosses: Sol'phish, Krog'wa and Mul'gath. The current prototype's Sol'phish-only boss is incomplete.
- Current single-player scope must exclude co-op-only augmentations and teammate-only quests.
- See docs/MECHANIC_REFERENCE_MATRIX.md and docs/ISSUE_REGISTER.md for expanded content and issues.

## Latest code development (PROGRESSION-002)
- development/index.html now includes real source-backed progression changes, SHA-256 a4fe8215c491d2139f8345a8f331482cf9d399a9a5d59742b348a08d32f85095 (121294 bytes), implementation commit 656881540ec26c5d60a580baa2ac42ac21128595.
- The catastrophic force-unlock-on-load assignment was removed; v1-to-v2 save normalization keeps currency/stats and limits untrusted legacy unlocks to 1.2 starters plus recorded quest flags.
- Slot 3 is gated at level 13, slot 4 at level 20, with immediate upgrade; **slot 2 at level 2 is unverified, temporary**.
- Added initial attack scaffolds for Loaded Dice, Tiny Tremors, Wicked Buzzsaw; their four individual augmentations and source-accurate numbers/VFX are still OPEN.
- The local portable Chromium Playwright test passed 17/17 targeted component checks; desktop/mobile interaction smoke passed. Browser navigation is blocked; localStorage was mocked, not a real reload acceptance.
- Test entry: tests/progression_regression.py. Evidence: docs/experiments/PROGRESSION_002.md.
- Do not merge into main or announce product-ready; actual full-run, 3D integrated product, all boss types, audio, visual QA and performance remain incomplete.


## PROGRESSION-002 final post-regression refinement
- The current development/index.html is now the **debug-stripped** 119417-byte candidate, SHA-256 e97ed8770523034ddc71d590a4a7cc3444e8c87811a44f4298910a65597b5190.
- Product code commit: 29492caf5b7db433704f9cfa7543b0e3126b2e6e.
- The ?qa-gated window.__QA with time jump / forced boss kill / direct finish no longer ships inside the HTML.
- tests/progression_regression.py still injects its own isolated temporary test probe into in-memory browser document. All 17 targeted checks passed after the strip; desktop/mobile smoke also passed.
- All previously documented NOT_TESTED/fidelity gaps remain open. Main stays the old baseline.


## Repository-level recovery and test harness (2026-11-16)
- AGENTS.md added as the root AI development entry: recover exact current GitHub state before acting, preserve owner scope, run evidence-first/decision loop, never alter CAOS.
- scripts/verify_project_state.py checks product scope, exact candidate SHA and byte count, debug-surface prohibition, and required recovery docs. It prints PASS_MECHANICAL_ONLY, **not** GAME_READY.
- tests/test_state_guard.py has a positive control and four corruption/mutation tests; all 5 passed locally.
- tests/progression_regression.py now uses installed Chromium when available, otherwise Playwright's browser; 17/17 locally with temporarily mocked storage.
- .github/workflows/qa.yml added. Live GitHub Actions execution is not yet verified; do not promote CI to PASS until readback of actual run.
- The latest product artifact is still development/index.html SHA-256 e97ed8770523034ddc71d590a4a7cc3444e8c87811a44f4298910a65597b5190, size 119417 bytes, product code commit 29492caf5b7db433704f9cfa7543b0e3126b2e6e.
- Fresh-chat automatic cold-start selection/execution is NOT_TESTED; the handoff protocol is installed, not independently proven.


## INCIDENT-001 — GitHub write byte identity and CI
- The first GitHub checkpoint job FAILED because the file read/import process omitted the final LF byte; source was 119416 bytes in GitHub vs 119417 in the local recorded artifact. Browser component test passed, but that does not override the checksum failure.
- Restored exact original trailing LF in both branches: main commit eace4cb66f282d35c663f3a13d6e39ff8a15e0b8, development product commit 44938fb8557a856d794e7a0ceff45ccd71faedeb.
- Canonical hashes remain main c14e0f3210320453b0b81b6d49fbd55ae372cf36cfe99a91902d089b8672ef3a (116721 B) and dev e97ed8770523034ddc71d590a4a7cc3444e8c87811a44f4298910a65597b5190 (119417 B).
- See docs/audits/INCIDENT_001_BYTE_FIDELITY.md for evidence, root-cause escalation and re-test requirement.
- Do not assert byte exactness from parsed Files content; verify remote actual bytes and SHA. Fresh CI status must be read back.

## Verified GitHub CI after byte-fidelity repair
- Exact candidate build SHA-256 e97ed8770523034ddc71d590a4a7cc3444e8c87811a44f4298910a65597b5190 / product commit 44938fb8557a856d794e7a0ceff45ccd71faedeb.
- Real GitHub Actions run 43838646149 completed SUCCESS. Both checkpoint (exact file SHA/scope + negative mutation tests) and browser-component (Playwright regression) jobs succeeded.
- This proves source integrity and scripted component paths only, NOT 3D fidelity, full real gameplay, hardware FPS, file:// persistence or owner approval.
- If the latest development HEAD differs by documentation-only commits, do not mistake the earlier green run for a run at the later SHA; fetch the latest run when needed.

## INTEGRATION-003 — Latest integrated 3D candidate (2026-11-16)
- DEVELOPMENT code: index.html SHA-256 `07bd70906f1020f2c5343d0ab4c16950a863cfc8b42e639fdaa74ef938fae648`; size 148704 bytes; code commit `ac295edce42e1f0781694168d3d82aca1463c48e`.
- Backup before overwrite: archive/2d-progression-before-3d.html; main remains the previous 2D baseline. **Do not replace main with unaccepted 3D experiment.**
- Three-boss/9-objective 3D integration and source-data corrections are present. Test-only diagnostic probes were injected into browser memory, NOT shipped in index.html.
- Local Node.js both-script syntax: PASS; Playwright 17/17 progression: PASS; synthetic browser integration passed all 9 objective generators, 3 boss constructors/updates, Gnasher invulnerability, and new spell augment counts. No JS exceptions/network requests in the tested scenarios.
- `file://` and localhost URL navigation returned net::ERR_BLOCKED_BY_ADMINISTRATOR, so actual persisted close/reopen remains NOT_TESTED.
- Visual polish, hardware performance, source-faithful boss mechanics, spell unlock quest tracking, naturally played 19-minute run and owner acceptance remain OPEN. **Product status NOT_READY.**
- Latest report: docs/experiments/INTEGRATION_003.md.
- Latest test scripts: tests/game3d_integration.py, tests/progression_regression.py.
- Historical GitHub Action green run 43838646149 applies to the old 2D commit only; check the newest 3D commit workflow before claiming CI status.
- Mandatory next action: inspect the latest branch HEAD and current project state, then continue highest-impact source-faithful gameplay, art and performance work. CAOS stays read-only.

## TRIAL-004 — Latest game file and playable systems (2026-11-16)
- Product code commit: `b21cdba002dc78167cc62601d3a93723d969f191`.
- development/index.html is **153894 bytes**, SHA-256 `0c8d9de43c8fe30f3cad8bd47d657056e1d84bf4a54869229b585b944c281a6a`. Treat as prototype, **NOT_READY**.
- A procedural grass texture and adaptive WebGL resolution scaling were added. SwiftShader software-rendered FPS is still low, about 15–25 FPS in reported scenes; real GPU acceptance remains NOT_TESTED.
- To respect the single-Reginald scope while unblocking spell-specific quests, the camp now allows a temporary next-run spell trial without permanent unlock. Source-grounded quest event trackers grant spells permanently after satisfying conditions. This is an explicitly labeled solo adaptation, NOT a claim of exact original behavior.
- Local targeted browser trial regression: 11/11 PASS. Existing progression 17/17 PASS. Synthetic 3-boss / 9-objective / Gnasher component checks PASS. No uncaught page errors or external requests in these tests.
- New test: `tests/trial_unlock_regression.py` and CI job. Evidence: `docs/experiments/TRIAL_004.md`.
- Current main branch remains the archived 2D baseline; do NOT publish or merge development until full acceptance.
- **Current remaining P0:** source-accurate artwork, boss mechanics, all objective variants, spell/element pair completeness, real unassisted 19-min run, hardware FPS and browser save/reload; user acceptance NOT_TESTED.

## CI-005 — Exact 3D candidate verified by GitHub Actions (2026-11-16)
- Run: https://github.com/D1traverser-debug/game/actions/runs/43848382432
- Run completed SUCCESS on development docs checkpoint `0b513f19a67393fcfdff64fd37c444571aa31f7b`, with the exact game artifact pinned as SHA-256 `0c8d9de43c8fe30f3cad8bd47d657056e1d84bf4a54869229b585b944c281a6a`, 153894 bytes, product commit `b21cdba002dc78167cc62601d3a93723d969f191`.
- Both checkpoint and browser-component jobs succeeded. Browser steps: 17 progression, 3-boss/9-objective/Gnasher immunity, 11 solo spell trial/quest event checks.
- The earlier failure at run 43848226627 was a stale checkpoint SHA/size mismatch; browser tests passed. The checkpoint was then corrected to the exact artifact SHA/bytes and the new run passed.
- This is mechanical + component regression evidence only. It does not prove real local-file storage, human 19-minute completion, genuine boss kill, high-fidelity art/audio or real-GPU performance.

## 2.5D art-forward candidate — 2026-11-17 (local artifact, NOT yet synced)
- Candidate file in this conversation: `咒语旅团-单人网页版-2.5D验收候选.html`
- Exact bytes: 718627; SHA-256: `de29ddd55575f1fe78c9b525d41709c2d619d41694cac4eb679cd0dd5f41d48f`.
- It includes a 4x4 embedded sprite atlas, sprite-based Reginald and monster rendering, a textured Verdant Meadows field, ruins/trees/flowers, combat effects, HUD and the existing single-player mechanics. The file has no external runtime asset requests.
- It is the preferred art-direction candidate: high-quality 2.5D instead of insisting on a 3D renderer unavailable in all browser environments. A WebGL2 experimental mode remains optional only where actually supported.
- Fixed a false UI promise: if WebGL2 initialization fails, the 3D selector is disabled and the game remains in 2.5D.
- Local Playwright tests: desktop 1440x900 and mobile 390x844 each passed start, HUD, pause/resume, no NaN text, no JS/console errors, and zero external requests. 15-second normal play smoke recorded 18 kills; XP remained 0 while orbs were visible. This is a gameplay pacing issue to investigate, not a passing progression test.
- The 2.5D file has NOT been committed to GitHub. Current repository `development/index.html` remains the older 3D candidate. Do not claim the local candidate is in GitHub until its exact bytes are synchronized and fetched back.
- Full 19-minute playthrough, genuine boss kill, real localStorage reload, real-device performance, content fidelity and owner acceptance remain NOT_TESTED. Product status stays NOT_READY.

## 2.5D_ATLAS_SCOPE_AND_STATIC_CACHE_008 — Current canonical checkpoint (2026-11-17)
- Canonical product source is now development/index.html; exact 717368-byte content was read back from GitHub and compared to the source candidate.
- Product commit: 17070bc703b7bd7800b4bb67d6a5c40288a9bfee.
- SHA-256: 21fbfcdf3149c5d2eee188a213bf66c3fba5a6b777e7c868a5ddb823a79c0239.
- Main remains the preserved earlier baseline. Do not merge or publish while status is NOT_READY.
- Fixed a real renderer-shadowing bug: a later duplicate v2enemy declaration overrode the intended atlas renderer. It is removed; the 1024x1024 embedded sprite atlas is now used by enemy draw calls.
- 480 static meadow props and seven ruin landmarks are baked at run start into 24 visible 512x512 tiles. Per-frame dynamic entities remain depth-sorted.
- Source audit now restricts Reginald to 18 spells: his Astral Orbs, the three official 1.2 starters, and the 14 general spell-quest spells. Hex Bomb, Necro Whirl, Spear Barrage, Swirl Sickle, Scepter Mesh, Seismic Slam and the unsupported orbital placeholder are excluded from research/trials/unlocks.
- Save normalization now drops non-Reginald spell unlocks, quest flags and trial selections from legacy saves.
- New CI tests: tests/art_renderer_regression.py and tests/reginald_spell_scope_regression.py; both pass locally (9/9 and 13/13 checks respectively).
- Normal 15-second movement smoke: 12 kills, XP collected, level 2 reached, upgrade screen opened, 100/100 HP, no runtime errors.
- Synthetic stress with 197 active enemies: desktop ~48.7 FPS (1440x900), mobile viewport ~60 FPS (390x844). Desktop target remains unmet; headless synthetic benchmark is not a real-device acceptance.
- Browser container blocks file:// navigation by administrator policy, so actual file-origin localStorage close/reopen remains NOT_TESTED.
- Full 19-minute mission, naturally defeated boss, source-accurate spell/augmentations, objective variants, real-device performance, audio/art acceptance and owner playtest remain OPEN.
- CAOS remains read-only; no CAOS files, branches, PRs, configuration or documentation were changed.

## QA repair — 2026-11-17
- Canonical candidate: development/index.html, product commit `17070bc703b7bd7800b4bb67d6a5c40288a9bfee`, SHA-256 `21fbfcdf3149c5d2eee188a213bf66c3fba5a6b777e7c868a5ddb823a79c0239`, 717368 bytes. PROJECT_STATE is synchronized to the actual CI-computed digest and size.
- CI found a stale progression assertion expecting save schema v2 although production normalizeSave writes schema v3. The test now asserts v3; other progression checks remain.
- CI found atlas renderer regression's test-only probe was injected with a literal backslash-n, so `__artProbe` was never defined. Fixed injection to use a real newline; no production game code was changed for this test harness issue.
- GAME-031 and GAME-032 record these QA defects and repairs; GAME-033 remains OPEN for a full normal-combat mission and natural boss victory. Do not mutate boss HP/time/win state and call that acceptance.
- Latest CI runs after these corrections: 43917069068 and 43917060710; inspect final job logs before claiming green.
- Product remains NOT_READY. No CAOS assets or repositories touched.

## Normal-play smoke and source audit — 2026-11-17
- New non-cheating 90-second normal-play smoke is in `tests/normal_play_smoke.py`. It uses the real update loop, movement input, actual XP drops/pickups and the production upgrade handler; it does not write XP, damage enemies, set mission time or force outcomes.
- GitHub Actions run 43918259686 passed all jobs. The 90-second normal-play run recorded: 90.47 simulated seconds, 83 kills, level 8, 8 actual upgrade choices, 100/100 HP, 18 XP toward the next level, no runtime/console errors and no external requests. This is an automated short-run smoke, not full mission acceptance.
- Product copy for the three new 1.2 spell augmentation sets was polished: the rough “Prototype” label is removed, and Buzzsaw descriptions now match implemented behavior (Piercing Teeth pierces; Heavy Teeth grants +25% base damage; Magnetic Edge pulls enemies; Twin Saw fires two saws).
- Important fidelity distinction: official 1.2 notes confirm four augmentations for each of the three new spells but do not disclose their names or detailed effects. Those twelve are our own named original adaptations, not source-confirmed exact augmentations. See `docs/MECHANIC_REFERENCE_MATRIX.md` and `docs/REFERENCE_RESEARCH.md`.
- Current code hash/bytes after the UI polish: `587113d2dcc3641314ff914234c64c9fa61b922a83592d3d6b8a94636ab0f128`, 717383 bytes; product commit `632868c3e16077281758d1db18358317e2af33be`. Checkpoint sync is committed separately; wait for the resulting CI before claiming green.

## Objective collection root-cause repair — 2026-11-17
- Natural-run trace showed a hard gameplay blocker: Soul Sludge objective progress stayed at 0 because the production update loop had no collection handler. Source reference says Soul Sludge is completed by walking over purple ground patches.
- Same code audit found normal/scared fungi and standard Spell Cores also lacked contact collection. Added contact collection for these, retained explosive fungi proximity detonation and the distinct heavy-core pickup/carry/delivery interaction.
- New `tests/objective_collection_regression.py` passes 9/9: normal/scared/explosive fungi, normal/dark sludge, normal/heavy cores, no runtime errors and offline behavior. This is component coverage, not a complete run.
- The previous natural pilot run died at 154.3s during a Rift objective: 10.7/100 HP, 89.3 damage taken, level 9, 135 kills, Rift progress 53.82/100. No browser errors or external requests. This remains an open gameplay/balance gate.
- Updated the non-cheating full-run pilot to seek actual health and magnet drops when needed. It still only supplies movement, normal interaction and choices from real upgrade cards; it does not mutate HP, XP, enemy/boss HP, time or victory.
- Product commit: `ae820ed62f3ad4e27c160cfd6ecc3c91abd9e061`. Exact artifact: 718366 bytes, SHA-256 `46f3c1c5ad7806fe45bc226e2df55b14de19c975182b619dd0db11524841923d`.
- CAOS remains read-only. `main` remains the preserved baseline; work continues on `development`.

## NATURAL RUN 012 — First non-cheating full mission win (2026-11-17)
- CI: https://github.com/D1traverser-debug/game/actions/runs/43989883310 — checkpoint and all browser-component steps PASS.
- The Playwright pilot ran the production update loop, only supplied movement, normal interact, and choices from actually offered cards. It did NOT mutate time, player HP/position/XP, objectives, enemy/boss HP, boss death, result or wins.
- Natural result: gameTime 1463.17s; Mul'gath spawned after 1140s and was naturally defeated; 732 kills; level 19; 4 objectives; 3 spells; 26 upgrade choices; 462.25/540 HP; armor 52; regen 6; 1 win/0 losses; no JS/console errors or external requests.
- This is the first complete automated pilot victory. It is not a human player acceptance test.
- The boss fight lasted about 323 seconds after spawn; compare against source evidence before balancing.
- Only Mul'gath has a natural full-run win. Sol'phish and Krog'wa full-run victories, owner playtest, file-origin persistence, real hardware performance and full source fidelity remain OPEN.
- Product status remains NOT_READY; main branch remains preserved; CAOS remains read-only.
- Evidence: `docs/experiments/NATURAL_RUN_012.md`.
