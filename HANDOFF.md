# HANDOFF — Aetherwilds Browser Game

## Current checkpoint — 2026-11-18
- Active branch: `full-game`; working title: Aetherwilds / 以太荒境.
- Delivery target: browser website, not Unity/native.
- Modes: solo plus planned 1–4 player online co-op.
- Status: **NOT_READY**.
- Current playable artifact: one-hero/one-realm/solo prototype in root `index.html`.
- 2.5D atlas renderer is default; raw WebGL2 path is experimental.
- Static preview packaging and browser-scope CI are added in this checkpoint.
- Unity/C# experiments are historical only. CAOS remains read-only.

## Existing browser baseline
Movement, automatic spell casting, XP/upgrades, 25 spell definitions, five primary elements, fifteen candidate infusion effects, nine objective types, three boss archetypes, local progression, DOM UI, synthesized prototype audio, atlas-backed 2.5D rendering and experimental raw WebGL2.

This is not full content, online co-op or commercial-quality acceptance.

## Next sequence
1. Verify static package and CI.
2. Keep current HTML as rollback; migrate production systems into modular TypeScript.
3. Benchmark raw WebGL2 vs bundled Three.js on one representative scene and real desktop/mobile devices.
4. Build one complete, polished solo vertical slice.
5. Implement authoritative WSS rooms, lobby/invites, reconnect and 1/2/3/4-client tests.
6. Expand the source-reconciled roster, realms and systems.
7. Deploy the exact website and room service with TLS, monitoring and rollback.
8. Run owner and independent full-game acceptance on the hosted build.

Do not resume Unity work. Do not call READY from packaging or CI. Do not ask the owner to repeat the browser target.
