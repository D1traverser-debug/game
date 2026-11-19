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
