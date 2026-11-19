# Requirements Traceability — Aetherwilds Single-Player Browser

Scope authority: docs/PROJECT_CHARTER.md and docs/FULL_GAME_PRODUCT_BRIEF.md. Source-game research is evidence for mechanics, not permission to expand the product into additional characters, realms or multiplayer.

| ID | Requirement | Priority | Evidence | Status |
|---|---|---:|---|---|
| WEB-PLAT-01 | Offline-capable static browser game; no Unity/native delivery | P0 | Owner-approved charter and package workflow | SELECTED |
| WEB-PLAT-02 | Desktop Chromium/Firefox/WebKit and mobile-browser compatibility | P0 | CI run 44491163465: all three browser smoke jobs passed | AUTOMATED_PASS; physical devices NOT_TESTED |
| WEB-INPUT-01 | Keyboard/mouse, gamepad and touch input | P0 | Controller and mobile-flow regressions in CI 44491163465 | AUTOMATED_PASS; physical controllers NOT_TESTED |
| WEB-ROSTER-01 | Four selectable wizards with distinct stats, starter spell, passive, active ability and visual treatment | P0 | Roster/map and visual regressions; four-wizard natural-run matrix | AUTOMATED_PASS for selection/behavior; bespoke rigs NOT_COMPLETE |
| WEB-WORLD-01 | One bounded 2400 × 1800 realm, six districts, seven landmarks, river/bridges, roads, minimap and boundary feedback | P0 | Map/collision regression in CI 44491163465 | AUTOMATED_PASS; owner exploration NOT_TESTED |
| WEB-GAME-01 | Complete solo loop: menu → selection → expedition → objectives/upgrades → boss → result → camp → replay | P0 | Component regressions and four natural boss wins on commit 266928c | AUTOMATED_PASS; human acceptance NOT_TESTED |
| WEB-CONTENT-01 | All included enemies, bosses, objectives, spells, augments, elements and scrolls have coherent, tested behavior | P0 | Mechanic Reference Matrix and source-backed regressions | PARTIAL; source-version reconciliation remains OPEN |
| WEB-RENDER-01 | 2.5D atlas/Canvas 2D is the primary renderer; WebGL2 is an optional experiment, not a mandatory production dependency | P1 | Architecture decision and renderer integration tests | IMPLEMENTED; visual/device acceptance NOT_TESTED |
| WEB-ART-01 | Original readable character, realm, enemy, animation, VFX, UI and audio presentation | P0 | Art/Audio Bible and visual regressions | PARTIAL; shared base body and procedural placeholder assets remain |
| WEB-SAVE-01 | Persistent character choice, currency, upgrades, unlocks, records, migration and corrupted-save recovery | P0 | Save-persistence regression in CI 44491163465 | AUTOMATED_PASS in CI; physical/cross-browser file workflows NOT_TESTED |
| WEB-PACKAGE-01 | Reproducible offline package, launcher and byte/hash manifest with no CDN runtime | P0 | Package job in CI 44491163465; artifact 800030 bytes | AUTOMATED_PASS on commit 266928c |
| WEB-PERF-01 | Representative-hardware frame-time, memory and sustained-session acceptance | P0 | Synthetic stress sample only | NOT_TESTED on target hardware |
| WEB-ACCEPT-01 | Owner and independent gameplay/visual/audio acceptance of the exact build | P0 | No owner acceptance evidence | NOT_TESTED |

## Explicitly out of scope

| ID | Requirement | Status | Scope authority |
|---|---|---|---|
| WEB-COOP-01 | Online co-op, 1–4 player rooms, WSS authority, lobbies, invites and reconnect | OUT_OF_SCOPE | Project Charter |
| WEB-OPS-01 | Public hosting, room servers, TLS operations, live-service monitoring and rollback | OUT_OF_SCOPE | Offline static delivery decision |
| WEB-NATIVE-01 | Unity or native desktop/mobile build | OUT_OF_SCOPE | Project Charter |
| WEB-REALM-02 | Additional realms or map expansion | OUT_OF_SCOPE | Fixed one-realm scope |
| WEB-ROSTER-02 | Expansion beyond Aster, Ember, Briar and Nyx | OUT_OF_SCOPE | Fixed four-wizard scope |

A historical source-game mechanic or architecture proposal does not become a product requirement unless it is explicitly inside the owner-approved scope. AUTOMATED_PASS is not equivalent to human acceptance or READY.


## Latest verification checkpoint — 2026-11-19

- CI run 44491163465 on commit 266928c passed 24/24 jobs.
- Exact shared solo spell catalogue regression passed 17/17 checks; the 25-definition runtime inventory, 18 eligible IDs, 14 shared quest unlocks, four unique starters, migration and size-upgrade eligibility were asserted.
- Chromium, Firefox and WebKit desktop/mobile smoke passed; four automated natural wizard runs won their bosses; offline package artifact 14513370931 was produced.
- This is automated evidence only. Owner playtest, physical devices, target-hardware performance, source-version reconciliation and production art/audio acceptance remain open.
