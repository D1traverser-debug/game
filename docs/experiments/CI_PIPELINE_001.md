# CI-PIPELINE-001 — Separate deterministic gates from exploratory natural play

Date: 2026-11-17  
Baseline development HEAD: 698fa9150eba673f33419aec3de1467273e2caeb  
Baseline CI run: https://github.com/D1traverser-debug/game/actions/runs/44043697224

## Observed failure

The existing browser job ran eight independent browser checks sequentially with the adaptive natural-play boss pilot inserted after the first four. The pilot failed its required baseline seeds and caused the remaining five checks to be skipped.

The first four checks passed: progression, 90-second normal-play smoke, objective collection, and character upgrades. The pilot recorded no natural boss victories: seeds 1/2/3 died at 286.1s, 514.5s and 468.9s, before the boss window.

The pilot's harness-integrity checks passed: one simulation clock, zero render-time RNG consumption, production 1/30 timestep, identical seed-1 replay, legal healthy new-spell choices, no browser/console errors and no external requests.

## Root-cause elevation

- L0: one exploratory trajectory failed; later independent regressions did not run.
- L1: the heuristic controller's survival/objective navigation did not reach the boss window.
- L2: the long-horizon pilot was placed inside a sequential blocking test job.
- L3: deterministic contracts and heuristic play exploration had no separate execution boundary.
- L4: CI treated a scripted agent outcome as a blocking acceptance signal, while skipping unrelated tests after failure.
- L5: the process conflated reproducibility with representativeness. A deterministic agent can still be a poor model of human play.

## Decision

1. Keep checkpoint, deterministic component, bounded browser and renderer/content regressions blocking.
2. Run the 19-minute adaptive pilot in a separate nightly/manual workflow.
3. Upload the full JSON report even when the pilot exits non-zero.
4. Keep pilot deaths as diagnostic hypotheses. Do not tune production balance solely to make the agent pass.
5. Keep human owner playtesting and real full-run acceptance as independent release gates.

## Expected result

- Every deterministic regression executes even if the exploratory pilot fails.
- A pilot failure remains visible with its per-seed evidence and cannot suppress unrelated test results.
- The main CI signal becomes interpretable: code contracts and bounded integrations pass/fail independently of heuristic play quality.

## Falsifier

If the separated workflow still blocks deterministic checks, fails to preserve its report, or if the pilot is later validated against representative human outcomes, revisit the decision. This change does not mark any gameplay requirement as passed.
