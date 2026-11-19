# Aetherwilds / 以太荒境 — Single-Player Browser Game

Repository: D1traverser-debug/game · Branch: full-game · Status: NOT READY

## Owner-approved product scope
A complete, offline-capable, browser-playable original-IP single-player action roguelite:
- One authored realm: 翠影荒野 / Verdant Wilds, with six named districts, seven landmarks, bounded traversal and a live minimap.
- Four playable wizards: Aster, Ember, Briar and Nyx. Each has a distinct starting spell, passive trait, active Q ability, base-stat profile and visual treatment.
- One complete solo expedition loop: character selection, movement, automatic spell combat, objectives, XP, upgrades, spell progression, boss fight, victory/defeat, results, camp upgrades and replay.
- Desktop browser first, with keyboard/mouse, gamepad and touch input. No runtime CDN dependency.

Online co-op, lobbies, room servers, Unity/native builds, additional realms and roster expansion are OUT_OF_SCOPE.

## Latest verified automation baseline
- Commit: 63fd96aeeaacabffd2fc0f211b3d973cd2e9e83a
- CI: https://github.com/D1traverser-debug/game/actions/runs/44484418951
- Result: 24/24 jobs passed.
- Offline HTML: 799,918 bytes · SHA-256 8bc83ce3ee62a8c65b583376b2d6b9d488953ef54d7d680dc3ddb2ae1d4ff5d3.
- Browser matrix: Chromium, Firefox and WebKit desktop/mobile smoke passed.
- Natural solo expedition: Aster/Sol'phish, Ember/Sol'phish, Briar/Mul'gath and Nyx/Krog'wa all achieved automated natural boss wins (4/4).

This is an automated verification baseline, not human playtest or owner acceptance. Physical devices, real controllers, representative-hardware performance, bespoke art/animation, authored audio and content/source-version reconciliation remain open. Product status stays NOT_READY.

## Build and verification
- Validate: python scripts/package_web.py --check
- Regenerate the Boss source fragment: python scripts/build_game.py
- Verify Boss source/build equality: python scripts/build_game.py --check
- Package: python scripts/package_web.py
- Verify package: python scripts/package_web.py --verify-output
- Unit checks: python -m unittest discover -s tests -p 'test_*.py' -v
- Browser regressions: Playwright scripts under tests/; CI runs the required browser and component matrix.

The static preview is emitted to dist/ with the HTML, local runtime modules, launchers, byte lengths and SHA-256 hashes. A green CI run proves only the listed automated checks, not visual quality or owner acceptance.

## Start the single-player browser game
1. Download the latest aetherwilds-browser-preview artifact from the GitHub Actions run and extract the ZIP.
2. On Windows, double-click PLAY.bat. On macOS/Linux, run sh PLAY.sh.
3. The launcher starts a loopback-only local server and opens the game in your default browser. Keep the terminal window open while playing; press Ctrl+C to stop the server.
4. If Python 3 is not installed on Windows, PLAY.bat falls back to opening index.html directly. The local server is preferred because it loads the modular runtime and provides more reliable browser storage.

The game is single-player and offline-capable. The local server does not expose the game to the public internet.

## Boss counterplay
Boss body contact is deliberately weaker than a telegraphed boss ability and applies a short knockback plus an independent cooldown. Boss skill telegraphs and projectiles remain separate. Mul'gath's live healing servants are valid auto-target priorities when in range. Browser regression and the four-wizard natural-run gate passed on the verified baseline; human balance acceptance remains open.

## Source/build rule
Boss encounter logic lives in src/game/boss_encounters.js. After editing it, regenerate the offline browser entry with python scripts/build_game.py; python scripts/build_game.py --check and the build reproducibility tests verify that the shipped HTML contains the exact source fragment.

## Wizard action readability
The four wizards show simulation-timed spell-cast sparks, an active-ability sigil pulse and a brief hit reaction layered over their current mantle, focus and regalia silhouettes. These are procedural feedback, not bespoke skeletal rigs or authored animation clips.

## Audio
The offline score layers harmony, bass, per-wizard melodies, plucked harmonics and deterministic percussion. Boss phases and critical health add tension layers. Independent persistent music, combat SFX, ambience and UI volumes plus master mute are implemented. Listening review and professionally authored/recorded asset production remain separate acceptance items.
