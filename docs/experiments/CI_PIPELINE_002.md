# CI-PIPELINE-002 — Fix closure-scope test invocation and isolate each regression

Date: 2026-11-17  
Baseline development HEAD: 0ce3072ce697956d8c15ef322783ad8a060c7541  
Baseline CI run: https://github.com/D1traverser-debug/game/actions/runs/44052717364

## Finding

The first pipeline split allowed the 3D integration test to run after the natural-play pilot had been removed. It passed all 22 checks. The next trial-unlock test failed with ReferenceError: startRun is not defined.

The production runtime intentionally wraps game state and functions in an IIFE. The test already injects a probe inside that IIFE, but one final step bypassed it and called startRun from the global page context. This was a test-driver scope defect.

## Change

- Add a restart method to the temporary in-IIFE trial probe; it invokes the private startRun function from its legitimate lexical scope.
- Change the Python driver to call the probe, not a global production symbol.
- Run the four core and four content/visual browser regressions as separate fail-fast-disabled matrices. A failing test no longer suppresses unrelated results.
- Keep the product HTML unchanged and keep all test-only functions out of the release artifact.

## Acceptance

- The trial test must pass all existing assertions.
- All eight independent browser regression jobs must reach a terminal result, regardless of another test's failure.
- The checkpoint hash and byte-count guard must continue to pass.
- Product status remains NOT_READY; this pipeline correction is not a gameplay acceptance.
