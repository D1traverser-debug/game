# BOSS PILOT 030 — Render RNG isolation and fixed-step pilot

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `60c9ee1a4b339f82907b0a5d3453b9ec6ec71305`  
Production artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #139 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44033773725

- The manual-update wrapper correctly blocked RAF-driven simulation updates, and manual tick counts matched the test-agent tick count.
- The healthy-new-spell policy assertion passed.
- Same-seed replay failed. All seeds 1-12 died before boss spawn; therefore no Boss archetype was observed or naturally defeated.
- Browser errors, console errors and external network requests were zero.

## Residual root cause

The renderer remained active while the pilot manually advanced the game. Source inspection found that `drawWorld()` generated screen-shake offsets with two calls to the shared `rand()` function every rendered frame. That function uses the same global `Math.random` stream as gameplay generation and upgrades. Frame-rate variation therefore changed the sequence of enemy spawns, objective data, drops, and Boss selection even though RAF simulation updates were blocked.

## Revision 030

1. In the temporary test document, replace screen-shake RNG with deterministic time-based offsets.
2. Wrap the render path with a render-phase flag and count any calls to `Math.random` during rendering. Require exactly zero.
3. Keep the existing wrapper that blocks RAF simulation updates and records blocked attempts.
4. Use the production fixed simulation step `1/30`, executing three steps for each 0.1-second pilot input decision.
5. Require identical seed-1 replay, one simulation clock, healthy new-spell choices, natural baseline wins and same-run natural wins for `sol`, `krog`, and `mul`.

No Boss is forced, no production game state is mutated, and no production combat balance or `index.html` change is made.
