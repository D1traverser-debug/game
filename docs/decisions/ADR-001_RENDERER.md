# ADR-001 — Rendering Architecture for the Faithful Single-Player Recreation

Date: 2026-11-16
Status: SELECTED_FOR_CONTROLLED_PROTOTYPE
Decision scope: rendering architecture only; does not expand product scope.

## 1. Evidence and constraints
- Original Steam screenshots show a 3D top-down/oblique world, modeled characters and enemies, terrain/props, large spell VFX, hit numbers, HUD, and dense combat.
- Current prototype is Canvas 2D. At 200 active enemies the reported average frame interval was 46.39 ms (p95 100 ms, approximately 21.6 FPS); a repeat was 32.78 ms (p95 50 ms, approximately 30.5 FPS). Both fail the provisional desktop target and the renderer does not match the original visual structure.
- Final player deliverable must remain one offline HTML file.
- No external network assets, CDN runtime, server, install step, or proprietary extracted assets may be required.
- Browser support includes desktop and mobile; visual quality and performance are both P0.

## 2. Alternatives

### A — Continue Canvas 2D / 2.5D
Advantages: simplest single-file packaging, easy UI and effects, low setup cost.
Disadvantages: source uses a 3D modeled scene and characters; reproducing depth, lighting, shadows, perspective, animation and high-density VFX with 2D sprites requires a large bespoke asset pipeline. Existing 200-entity baseline already fails performance.
Verdict: rejected as final visual architecture; may remain useful for UI overlays or specific effects.

### B — Hand-written WebGL renderer
Advantages: full GPU control, minimal runtime dependency, excellent potential for instancing and custom effects.
Disadvantages: high engineering cost for cameras, mesh/material pipeline, shadows, animation, resource lifecycle, batching, post-processing, picking and device compatibility. Risk of spending too long building an engine rather than the game.
Verdict: not selected as first route; retain as fallback if a bundled engine cannot meet single-file/performance requirements.

### C — WebGL 3D world + DOM UI, using a bundled Three.js runtime (hybrid)
Advantages: 3D camera, meshes, materials, lighting, animation and instancing; DOM remains ideal for menus/HUD/cards; bundled library can be embedded into a single offline HTML; custom procedural low-poly assets avoid proprietary asset copying.
Disadvantages: library adds bundle size; file:// module/CSP behavior must be verified; mobile GPU/performance and memory need testing; custom models and animation still require production work.
Verdict: selected for a bounded vertical-slice experiment, not yet accepted as final architecture.

## 3. Decision
Build one isolated vertical slice:
- orthographic/oblique camera and a compact Verdant Meadow patch;
- Reginald as an independently modeled animated 3D character;
- one Gnasher enemy with chase/burrow/leap states;
- one Astral Orb spell with target, hit, damage, impact VFX and audio cue;
- 50/100/200 enemy load profiles;
- desktop and mobile browser checks;
- export to one offline HTML with no network requests.

## 4. Pre-registered acceptance / falsifiers
The decision is supported only if the slice:
1. Looks materially closer to the original screenshot structure than the current 2D baseline in blind side-by-side review.
2. Preserves readable silhouettes, attack telegraphs and spell impact under 100+ active entities.
3. Meets 60 FPS desktop target and >=30 FPS mobile target on named reference devices under agreed load; benchmark five repeated runs after warm-up.
4. Opens directly as a local HTML file in supported browsers and makes zero network requests.
5. Does not cause uncontrolled memory growth or context loss during a 15-minute stress run.
6. Can be bundled reproducibly with exact engine version/license and source commit recorded.

If any P0 criterion fails, profile the cause and compare a targeted WebGL implementation or a hybrid sprite/mesh strategy.

## 5. Rollback
Keep the current 2D baseline on main. All renderer experiments remain on development in a separate prototype path until the vertical slice passes. No destructive replacement of the baseline.
