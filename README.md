# The Spell Brigade — Single-player Browser Recreation

**Repository:** [D1traverser-debug/game](https://github.com/D1traverser-debug/game)  
**Product scope:** one wizard (Reginald), one realm (Verdant Meadow), single-player, browser-delivered.  
**Final player artifact:** one self-contained offline HTML file.

> Status: **NOT READY — prototype baseline under reconstruction.** This repository is the durable source of truth for requirements, decisions, code, tests, evidence, and cross-conversation recovery. A passing syntax check or a working menu is not a release.

## Non-negotiable scope
- One hero: Reginald.
- One map/realm: Verdant Meadow.
- Single-player only.
- No multiplayer, matchmaking, online rooms, AI teammates, or additional playable heroes/maps.
- Final build must be a single HTML file that opens directly in current desktop browsers without a server, install step, network access, or external runtime assets.
- Develop and test to reproduce the original's observable single-player systems and moment-to-moment experience, not merely its theme or feature names.
- Use independently created code, visual assets, and audio. Do not copy proprietary game assets, source code, music, or extracted game files. This is an unofficial fan recreation, not an official product.

## Canonical project entrypoints
1. `docs/PROJECT_STATE.json` — machine-readable canonical checkpoint.
2. `HANDOFF.md` — mandatory cross-conversation recovery instructions and next action.
3. `docs/REQUIREMENTS_TRACEABILITY.md` — product requirements and evidence links.
4. `docs/DECISION_LOG.md` — accepted decisions and rejected alternatives.
5. `docs/QA_BASELINE.md` — baseline test evidence and honest limitations.
6. `docs/GOVERNANCE.md` — project-specific adaptation of CAOS governance; no CAOS assets are copied or modified.

## Development
The root `index.html` is the current single-file prototype and current runnable artifact. Future engineering may use modular source and automated build tooling, but the release gate must produce and verify one self-contained `index.html`. Any refactor must preserve the single-file delivery contract.

## Release rule
Do not mark the project READY until the complete acceptance matrix is passed against the exact release artifact, including real player-driven full-run completion, genuine boss combat, save/reload, desktop and mobile input, performance, visual review, and independent acceptance. See `docs/RELEASE_GATES.md`.
