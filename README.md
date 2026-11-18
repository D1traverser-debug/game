# Aetherwilds / 以太荒境 — Browser Game

**Repository:** D1traverser-debug/game · **Branch:** `full-game` · **Status:** NOT READY

## Product target
An original-IP action roguelite delivered as a browser-playable website. Solo and 1–4 player online co-op are in scope. Desktop browsers are primary; mobile compatibility is required. Inputs: keyboard/mouse, controller and touch.

Target presentation: WebGL2 3D world with DOM UI. The current 2.5D atlas renderer remains a fallback; raw WebGL2 versus a bundled engine such as Three.js must be compared on the same scene and real devices. No runtime CDN dependency.

Online co-op requires a separate authoritative WebSocket room service. Clients submit player intent; the room owns gameplay-critical state.

## Current playable baseline
Root `index.html` is a one-hero, one-realm, single-player prototype. It has movement, automatic spells, XP/upgrades, 25 spell definitions, five primary-element definitions, fifteen candidate infusion effects, nine objective types, three boss archetypes, local progression, a 2.5D atlas renderer and an experimental WebGL2 path. It is not the complete game, multiplayer build or commercial-quality release.

## Build
- Validate: `python scripts/package_web.py --check`
- Package: `python scripts/package_web.py`
- Verify output: `python scripts/package_web.py --verify-output`
- Unit checks: `python -m unittest discover -s tests -p 'test_*.py' -v`
- Browser regressions: Playwright scripts under `tests/`.

The preview package is emitted to `dist/` with a byte-identical HTML file and SHA-256 manifest. This is a delivery bridge; the final production runtime must be modular.

## Canonical records
See `docs/PROJECT_STATE.json`, `HANDOFF.md`, `docs/PROJECT_CHARTER.md`, `docs/FULL_GAME_PRODUCT_BRIEF.md`, `docs/FULL_GAME_ROADMAP.md`, `docs/ENGINE_EVALUATION.md`, `docs/ARCHITECTURE.md`, `docs/NETWORK_ARCHITECTURE.md`, `docs/ART_AUDIO_BIBLE.md`, `docs/ISSUE_REGISTER.md` and `docs/RELEASE_GATES.md`.

The old Unity/C# experiment is historical only, not active runtime or CI. A green CI run does not prove full-game readiness.


## Browser runtime modules
The production browser loop imports `web/src/core/fixed-step-clock.mjs` at 30 Hz. The static package copies the complete `web/src/core/*.mjs` runtime directory to `dist/web/src/core/` and verifies each file by byte length and SHA-256. Other core modules remain under incremental integration and are not yet authoritative for gameplay.
