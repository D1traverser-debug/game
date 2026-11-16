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
