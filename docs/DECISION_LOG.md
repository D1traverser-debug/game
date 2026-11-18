# Decision Log

## D-033 — Browser-first delivery (2026-11-18)
Accepted by owner. Complete product is a browser website. Target WebGL2 3D world + DOM UI, with 2.5D fallback. Static frontend plus separate authoritative WSS co-op service. Unity/native delivery superseded. Renderer choice remains open pending same-scene real-device comparison.

## D-034 — Modular browser architecture (2026-11-18)
Keep current single-file HTML as playable rollback/mechanics reference. Migrate production systems to modular TypeScript with simulation/content/render/UI/audio/input/persistence boundaries; do not extend the monolith indefinitely.

## D-035 — Authoritative co-op (2026-11-18)
Design accepted; implementation not started. 1–4 player rooms use secure WebSockets; server owns gameplay-critical state, clients submit validated intent.
