# Agent Instructions — Aetherwilds Browser Game

The repository is canonical. Read PROJECT_STATE and HANDOFF before acting.

Owner directive: complete commercial-quality browser game, not Unity/native. Original-IP action roguelite; solo and 1–4 player online co-op; desktop browsers first, mobile compatibility; keyboard/mouse, controller and touch. Target WebGL2 3D world + DOM UI, with 2.5D fallback. Renderer choice raw WebGL2 vs bundled Three.js requires same-scene real-device evidence. Co-op uses authoritative WSS rooms. Unity/C# is historical only. CAOS is read-only.

Engineering loop: intent → source/version evidence → requirements → root-cause analysis → compare repair/refactor/rebuild/reuse → implementation → deterministic tests → real browser/device integration → independent visual/audio/gameplay/network review → acceptance. Do not patch symptoms first.

Invariants: simulation independent of DOM/render/audio; fixed tick and seeded RNG independent of frame rate; presentation never consumes gameplay RNG; server owns network gameplay state; clients submit intent only; content has stable IDs and provenance; test hooks never ship.

Synthetic mutations and component tests are not player-run acceptance. Report what each test proves and what remains untested. CI cannot certify fun, quality or release readiness.

Next: verify browser package/CI, build polished browser vertical slice, benchmark renderers, implement WSS co-op. Do not ask owner to repeat browser target.
