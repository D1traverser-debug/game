# Browser Runtime and Renderer Decision

## Selected platform
Browser website. Unity/native delivery is superseded.

## Target stack
Modular TypeScript frontend (Vite candidate); WebGL2 3D world; DOM UI; secure WebSocket co-op service; bundled runtime dependencies only. Three.js is the leading renderer candidate, not yet locked. Compare it against the existing raw-WebGL2 path on the same scene and devices. Keep 2.5D Canvas fallback until WebGL2 is accepted.

## Current baseline
Root HTML is a self-contained solo prototype. 2.5D atlas is default; raw WebGL2 is experimental. Neither has passed commercial visual or physical-device acceptance.

## Bake-off
Same scene in both renderers: animated hero, three enemies, terrain/materials, lighting, projectile, impact VFX and representative HUD. Measure startup, CPU/GPU frame time, draw calls, memory, asset size and sustained FPS on the same desktop/mobile devices. Review animation, camera, readability and VFX at normal speed.

## Acceptance
Desktop Chromium/Firefox/WebKit and physical mobile Safari/Android Chrome; input, tab resume, WebGL2 fallback, save/reload, 15-minute stability and peak combat load. No CDN runtime.
