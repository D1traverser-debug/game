# Browser Runtime and Renderer Decision

## Selected platform
Offline-capable static browser game. Desktop Chromium/Firefox/WebKit are primary compatibility targets; mobile browser compatibility is required. No Unity/native build, public hosting service or CDN runtime is in scope.

## Target stack
- Native JavaScript ES modules for bounded simulation/runtime responsibilities.
- Generated offline HTML entry point plus locally packaged modules and launcher.
- Canvas 2D simulation with the 2.5D atlas renderer as the primary presentation path.
- Raw WebGL2 remains an optional experimental renderer; it is not a release dependency.
- DOM-based menus, HUD, settings, camp and result screens.
- Keyboard/mouse, Gamepad API and touch input adapters.
- Versioned browser persistence and explicit recovery behavior.

TypeScript, Vite, Three.js, WSS and server authority are not current requirements. Re-evaluate only if an observed product constraint justifies the added build/runtime complexity and the owner approves the scope change.

## Current baseline
The root index.html remains a large playable runtime and rollback surface. The fixed-step clock and central damage pipeline are integrated; seeded RNG, event buffer, input validation, projectile and spell modules remain incremental contracts. The package includes no external runtime CDN. The 2.5D renderer is default; WebGL2 integration is experimental.

## Renderer decision rule
Do not replace the renderer because a technology appears more advanced. First measure the current 2.5D path on representative hardware. A same-scene bake-off is warranted only if it can answer a concrete visual/performance question. Compare startup, CPU/GPU frame time, draw calls, memory, asset size, readability and sustained peak-combat behavior. Keep the current path as rollback until the candidate wins the measured comparison without changing gameplay semantics.

## Acceptance
Automated Chromium/Firefox/WebKit desktop/mobile smoke is necessary but not sufficient. Physical iOS Safari and Android Chrome, real controllers, owner-machine launch, 15-minute stability, performance and human visual/audio review remain open. No renderer or platform change can be marked accepted from synthetic tests alone.
