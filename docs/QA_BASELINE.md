# QA Baseline — Aetherwilds Single-Player Browser

## Exact verified automation baseline

- Repository: D1traverser-debug/game
- Branch: full-game
- Verified commit: 63fd96aeeaacabffd2fc0f211b3d973cd2e9e83a
- GitHub Actions run: https://github.com/D1traverser-debug/game/actions/runs/44484418951
- Result: 24/24 jobs passed, no failed or skipped jobs.
- Offline HTML: 799,918 UTF-8 bytes; SHA-256 8bc83ce3ee62a8c65b583376b2d6b9d488953ef54d7d680dc3ddb2ae1d4ff5d3.
- Checkpoint: PASS_MECHANICAL_ONLY; 15 Python unit tests passed.
- Browser matrix: Chromium, Firefox and WebKit desktop/mobile smoke all passed.
- Natural solo expedition: Aster defeated Sol'phish; Ember defeated Sol'phish; Briar defeated Mul'gath; Nyx defeated Krog'wa. 4/4 automated natural wins.

## Coverage represented by the run

- Reproducible offline package and project-scope checkpoint.
- JavaScript simulation contracts, fixed-step clock and damage-pipeline integration.
- Desktop/mobile launch, menu, roster selection, simulation timer, pause/resume and offline request checks in Chromium/Firefox/WebKit.
- Roster/map/collision, objectives, upgrades, enemy balance, save persistence, controller mapping and audio mixer/SFX.
- Boss telegraphs and encounters, 1.2 starter spells/augments, visual identity and experimental WebGL2 integration.
- Four separate natural-play expeditions using ordinary game update, damage, upgrade and boss-death paths. No direct HP, XP, boss-health or victory mutation.

## Interpretation and limitations

This is an automated baseline, not release acceptance. The WebGL2 integration and component probes include synthetic/test-only instrumentation; they do not make WebGL2 the production renderer. Browser automation is not a physical iOS/Android device test, a real hardware-controller test, or a human playtest. A natural-run agent is not a human assessment of difficulty, clarity, enjoyment or source fidelity.

Still open: bespoke character rigs and authored animation, production art/VFX/UI/audio, content/source-version reconciliation, physical-device and representative-hardware performance, real-player map exploration, owner listening review, and owner/independent acceptance. Product status remains NOT_READY.
