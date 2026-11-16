# WEBGL-SLICE-001 — Technical Smoke and Visual Prototype Report

Date: 2026-11-16
Artifact: experiments/webgl-slice.html
Status: TECHNICAL_SMOKE_PASS / VISUAL_NOT_ACCEPTED / PERFORMANCE_NOT_ACCEPTED

## Environment
- Chromium 144.0.7559.96
- Linux test container under Xvfb
- WebGL2 software renderer (SwiftShader)
- Viewport 1440x900, DPR 1
- This is not a representative hardware-GPU benchmark.

## Results
- WebGL2 context: PASS
- Menu to playing state: PASS
- Low-poly 3D scene, player, enemies and terrain render: PASS
- Automatic projectile and enemy update loop: PASS
- Gnasher burrow/leap state code path present: PARTIAL; visual state not independently accepted
- JavaScript page errors: 0
- Console errors: 0
- External network requests: 0
- WebGL error after stress run: 0
- 200-enemy synthetic render profile: 201 active enemies after natural spawn
- Reported software-rendered FPS: 20
- Hardware GPU performance: NOT_TESTED
- 15-minute memory/context stability: NOT_TESTED
- Mobile physical-device test: NOT_TESTED
- Visual comparison acceptance: NOT_ACCEPTED

## Interpretation
The experiment proves that a self-contained HTML can initialize WebGL2, render a 3D world, and batch many instances without external libraries or network requests. It does not prove release-quality art or performance. The 20 FPS result is from SwiftShader software rendering and cannot be used as a hardware-GPU verdict, but it is still a warning that the scene's geometry, batching, and CPU preparation need profiling.

The screenshot from the 200-entity test is retained in the conversation artifact stream; it is not included as a binary in this commit.

## Next controlled experiment
1. Add per-chunk culling and stable static instance buffers.
2. Improve hero/enemy silhouettes, animation, terrain, lighting and shadow readability.
3. Add real hardware browser measurements on a named desktop and mobile device.
4. Compare raw WebGL2 and bundled Three.js on the same scene, not separate demos.
5. Keep the renderer decision open until visual and performance criteria both pass.
