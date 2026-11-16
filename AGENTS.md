# Game Development Agent Instructions

You are working on an independent, unofficial single-player browser recreation of The Spell Brigade. This repository—not the conversation summary—is the canonical project state.

## Mandatory cold-start
Before planning or modifying anything:
1. Fetch the current GitHub `main` and `development` HEAD SHAs.
2. Read `docs/PROJECT_STATE.json`, `HANDOFF.md`, `docs/PROJECT_CHARTER.md`, `docs/REQUIREMENTS_TRACEABILITY.md`, `docs/ISSUE_REGISTER.md`, the latest audit/experiment/decision report, and the current exact `index.html`.
3. Reconcile contradictory evidence. Remote repository state outranks stale chat summaries. Record the last verified product commit and source SHA.
4. For an interrupted or missing write result, classify it as `UNKNOWN_PENDING_READBACK` and inspect the remote target before retrying. Do not blindly repeat external writes.
5. Run `python scripts/verify_project_state.py` or equivalent readback validation, but do not treat mechanical consistency as proof that the game works.
6. Continue from the next player-outcome-critical open issue. Avoid asking the owner to restate documented constraints.

## Non-negotiable scope
- One wizard: Reginald.
- One map/realm: Verdant Meadow.
- Single-player only, no matchmaking, online/co-op, AI teammates, other heroes or maps.
- Final player deliverable: one self-contained, fully offline HTML file that opens directly in a browser.
- A playable faithful recreation, not a mockup, simplified theme, screenshots, or checklist of feature names.
- Original code, artwork, visual effects and sound; do not copy third-party proprietary game assets/source.
- CAOS is a read-only methodological reference. Never modify CAOS code, repo, branches, PRs, files, Skills, plugins, docs, configuration or data.

## Decision and execution loop
Original owner intent → source/version evidence → qualification → L0–L5 causal search → alternative solutions and falsifiers → controlled implementation → deterministic tests → real browser integration → source-fidelity visual/audio/interaction review → independently verified player outcome → learning and regression guard.

Investigate the highest shared cause. Consider a component fix, workflow redesign, architectural change, clean replacement, reuse, or deliberate no-change. Do not default to patch-first, or rewrite-first without evidence. Document trade-offs, rollback, and remaining uncertain assumptions.

## Test integrity
- Synthetic time-jumps, forced boss kills, direct state mutations, mock storage, syntax checks, simulated win screens and a working menu are not a completed gameplay run.
- Keep test-only instrumentation outside the release HTML.
- PASS needs exact source commit, build SHA, procedure, observed outcome and evidence.
- Mark unsupported or blocked items NOT_TESTED, not PASS.
- Current temporary second spell-slot threshold is NOT source-verified; do not promote it to an original-game fact.
- Distinguish full 19-minute unassisted player victory, boss mechanics, mobile device tests, actual file:// save/reload and performance from component tests.
- Human fun, polish and release acceptance cannot be self-certified by the same implementation model.

## Branch and release discipline
- `main`: preserved previous runnable baseline until true release readiness; do not overwrite casually.
- `development`: active work and experiments.
- Root `index.html`: source of the current development player build. Experiments stay under `experiments/`.
- Every meaningful change must update `docs/PROJECT_STATE.json`, `HANDOFF.md`, the issue register and its evidence. Use exact commit hash and artifact SHA.
- Release candidate status requires all P0/P1 product gates to pass, owner playtest, and exact single HTML release verification.
- Do not publish or declare `READY` from CI success, test count, or document completion alone.

## Next verified checkpoint
See `docs/PROJECT_STATE.json`; at 2026-11-16 the product is `NOT_READY`. The debug-stripped 119,417-byte development HTML passed targeted progression and UI smoke checks but still lacks source-complete spell quests, all augmentations, integrated 3D renderer, all bosses, full playthrough, performance, and player acceptance.
