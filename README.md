# Aetherwilds / 以太荒境 — Single-Player Browser Game

Repository: D1traverser-debug/game · Branch: full-game · Status: NOT READY

## Owner-approved product scope
A complete, offline-capable, browser-playable single-player action roguelite:
- One authored realm: 翠影荒野 / Verdant Wilds, with six named districts, seven landmarks, bounded traversal and a live minimap.
- Four playable wizards: Aster, Ember, Briar and Nyx. Each has a unique starting spell, passive trait, active Q ability, base-stat profile and visual treatment.
- One complete solo expedition loop: character selection, movement, automatic spell combat, objectives, XP, upgrades, spell progression, boss fight, victory/defeat, results, camp upgrades and replay.
- Desktop browser first, with keyboard, gamepad and touch input. No runtime CDN dependency.

Online co-op, lobbies, room servers, Unity/native builds and additional realms or character rosters are out of scope.

## Build and verification
- Validate: python scripts/package_web.py --check
- Package: python scripts/package_web.py
- Verify package: python scripts/package_web.py --verify-output
- Unit checks: python -m unittest discover -s tests -p 'test_*.py' -v
- Browser regressions: Playwright scripts under tests/, including single_player_roster_map_regression.py.

The static preview is emitted to dist/ with the HTML and eight runtime modules, byte lengths and SHA-256 hashes. A green CI run proves only the listed automated checks, not visual quality or owner acceptance.


### Current single-player balance checkpoint
The latest candidate includes a slower late-run enemy damage curve, a readable Gnasher landing warning, reduced Gnasher/Crabladon pressure, and more frequent recovery pickups. The four-wizard natural-run matrix is pending revalidation; this is not a release-ready build.


### Current solo survival balance candidate
The latest patch reduces Gnasher leap, enemy contact and ranged projectile damage and ensures an under-defended build can be offered a defensive level-up card. Required browser CI and the four-wizard natural-run matrix are pending; prior natural-run acceptance was 1/4 boss wins, so the product remains NOT READY.


### Boss counterplay candidate
Mul'gath's live healing servants are now explicit auto-target priorities when in range. The natural-run test pilot now reads the boss's committed line/grid telegraph geometry instead of approximating every warning as a circle. Four-wizard boss acceptance is still pending.


## Start the single-player browser game

1. Download the latest `aetherwilds-browser-preview` artifact from the GitHub Actions run and extract the ZIP.
2. On Windows, double-click `PLAY.bat`. On macOS/Linux, run `sh PLAY.sh`.
3. The launcher starts a loopback-only local server and opens the game in your default browser. Keep the terminal window open while playing; press Ctrl+C to stop the server.
4. If Python 3 is not installed on Windows, `PLAY.bat` falls back to opening `index.html` directly. The local server is preferred because it loads the modular runtime and provides more reliable browser storage.

The game is single-player and offline-capable. The local server does not expose the game to the public internet.


### Boss collision and counterplay
Boss body contact is deliberately weaker than a telegraphed boss ability and applies a short knockback plus an independent cooldown. The boss's authored attacks remain the primary high-damage threats and retain their visible warning windows. The current counterplay candidate is awaiting CI and a fresh four-wizard natural run.


### Source build rule
Boss encounter logic lives in `src/game/boss_encounters.js`. After editing it, regenerate the offline browser entry with `python scripts/build_game.py`; `python scripts/build_game.py --check` and the build reproducibility tests verify that the shipped HTML contains the exact source fragment.


### Wizard action readability
The four wizards now show simulation-timed spell-cast sparks, an active-ability sigil pulse and a brief hit reaction. These are layered over their distinct mantle, focus and regalia designs. Full bespoke skeletal rigs and recorded animation clips remain outside this procedural polish pass.
