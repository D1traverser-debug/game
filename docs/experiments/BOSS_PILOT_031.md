# BOSS PILOT 031 — Isolate screen-shake RNG in both renderers

Date: 2026-11-17  
Branch: `development`  
Pre-change HEAD: `f49f7a6ab7f7495d5d5129c702fe2e395adf508a`  
Production artifact: `index.html` unchanged  
Product status: **NOT_READY**

## CI #140 evidence

Run: https://github.com/D1traverser-debug/game/actions/runs/44035681214

- Checkpoint, progression, 90-second normal-play, objective collection and character-upgrade regressions passed.
- The natural-run pilot failed at its source preflight assertion before opening any browser context. No natural-run seed executed, so CI #140 provides no new survival or boss-coverage result.
- The failing assertion was valid: `rand(-g.shake,g.shake)` remained in the test document.

## Root cause

Revision 030 replaced the legacy 2D renderer's screen-shake RNG calls, but source inspection found a second, atlas-backed 2.5D renderer with another pair of RNG-based camera shake calls:

```js
ctx.translate(-cx+(g?.shake?rand(-g.shake,g.shake):0),-cy+(g?.shake?rand(-g.shake,g.shake):0));
```

Those calls also consumed the seeded gameplay RNG in a frame-rate-dependent manner.

## Revision 031 changes

- Add a unique source anchor and exact-count assertion for the atlas-backed 2.5D shake path.
- Replace both X/Y shake offsets in the temporary QA document with deterministic time-based sine/cosine offsets.
- Retain the source assertion that no `rand(-g.shake,g.shake)` token remains in the test document.
- Retain runtime render-phase RNG counting, production `SIM_STEP=1/30`, manual tick equality, blocked RAF evidence and identical seed-1 replay.
- No production `index.html`, game balance or CAOS changes.

## Acceptance

Pending CI #141. First require both-renderer RNG preflight and deterministic replay gates. Then require natural baseline wins for seeds 1/2/3 and same-run natural victories for `sol`, `krog` and `mul`, with no browser/console errors or external requests. Product remains **NOT_READY**.
