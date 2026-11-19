# Decision Log

## D-033 — Browser-first delivery (2026-11-18) — HISTORICAL / SUPERSEDED
The original proposal combined a WebGL2-first world, DOM UI and an authoritative WSS co-op service. The browser-first and offline-delivery direction remains valid; the production-WebGL2 and co-op parts were superseded by D-036. Do not use this entry as a current release requirement.

## D-034 — Modular browser architecture (2026-11-18) — ACTIVE, REFINED
Keep the playable browser runtime and rollback path while extracting simulation responsibilities into JavaScript ES modules incrementally. The current implementation uses native ES modules and a generated offline HTML artifact; TypeScript, Vite and a wholesale framework migration are not prerequisites. Every extraction requires behavior-parity tests and an explicit rollback path. Do not claim a module is authoritative until production calls it.

## D-035 — Authoritative co-op (2026-11-18) — SUPERSEDED / OUT_OF_SCOPE
A preliminary 1–4 player authoritative WebSocket design was researched. The owner subsequently narrowed the product to one offline-capable single-player browser game. No co-op runtime, room server, lobby, reconnect or multi-client release gate is authorized under the current scope.

## D-036 — One-realm offline single-player product (2026-11-18) — OWNER-APPROVED
The product is an original-IP browser action roguelite with one Verdant Wilds realm, four wizards (Aster, Ember, Briar and Nyx), seven enemy archetypes, three bosses, nine objective families and a complete solo expedition/camp/replay loop. Desktop browsers are primary; mobile compatibility and keyboard/mouse, gamepad and touch are required. Delivery is an offline-capable static browser package. Online co-op, networking, additional realms, roster expansion and Unity/native builds are out of scope.

## D-037 — Renderer and runtime baseline (2026-11-18) — ACTIVE
The 2.5D atlas renderer with Canvas 2D simulation is the default production path. Raw WebGL2 is an optional experiment, not a mandatory release dependency. No CDN runtime is allowed. A renderer replacement requires evidence from the same scene on representative hardware and must preserve the offline package and gameplay contracts.
