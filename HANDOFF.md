# Mandatory Continuation / Recovery Entry

**Read this before making any substantive change, including after a chat interruption.**

## Source-of-truth order
1. Current GitHub `main` tree and exact commit SHA.
2. `docs/PROJECT_STATE.json` and `HANDOFF.md` from that same commit.
3. Latest accepted decision and evidence under `docs/`.
4. Exact source/test artifact at that commit.
5. Conversation summaries are navigation hints only; they never outrank repository state.

If the repository head, state file, and handoff disagree, stop and reconcile the discrepancy before coding. Do not ask the owner to repeat information already recorded here.

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
