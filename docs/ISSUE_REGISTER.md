# Issue Register — Aetherwilds Single-Player Browser

| ID | Priority | Issue | Evidence | Status | Next action |
|---|---:|---|---|---|---|
| WEB-001 | P0 | Four wizards still share a base atlas body; capes, headpieces, palettes and weapons do not constitute four bespoke production rigs | Architecture and visual-identity regression | OPEN | Create and review distinct original silhouettes/rigs at gameplay camera distance |
| WEB-002 | P0 | Production-quality original environment, enemy, animation, spell VFX and UI assets are incomplete | Art/Audio Bible; current atlas/procedural renderer | OPEN | Define asset inventory, visual targets, provenance and acceptance review |
| WEB-003 | P0 | Source-version content manifest is unresolved across the implemented spell pool, augments, elements/infusions, enemies, objectives, bosses, quests and meta progression | Mechanic Reference Matrix; 25 definitions with an 18-ID current solo pool | OPEN | Pin reference version; classify every implemented ID as in-scope, adapted, excluded or unknown |
| WEB-004 | P0 | Physical browser/device compatibility and representative-hardware performance are not accepted | Chromium/Firefox/WebKit automation passes; no physical-device evidence | OPEN | Test iOS Safari/Android Chrome, real controllers, low-end GPU, p95 frame time, memory and 15-minute stability |
| WEB-005 | P0 | Exact-build owner and independent gameplay/visual/audio acceptance remain outstanding | Governance and Release Gates | NOT_TESTED | Conduct unassisted playtest and review the exact candidate; owner alone determines acceptance |
| WEB-006 | P1 | Simulation modularization is partial: fixed-step clock and damage pipeline are integrated; RNG, event buffer, projectile and spell modules remain independent contracts | Architecture and web runtime state | IN_PROGRESS | Integrate one bounded system at a time with behavior-parity tests; do not wholesale-rewrite the monolith |
| WEB-007 | P1 | Music, ambience and SFX are procedural placeholders; mix/loudness and authored asset quality are not approved | Audio regression passes; no owner listening review | PARTIAL | Review on target speakers/headphones and decide authored-asset production needs |
| WEB-008 | P1 | Save import/export file chooser and download behavior on physical/cross-browser targets remain unverified | Chromium save-persistence regression | PARTIAL | Verify real-origin reload, export/import and corruption recovery in Firefox/WebKit and physical devices |
| WEB-009 | P1 | One-click launch and persistent storage have not been verified on the owner's Windows/macOS/Linux hardware | CI package passes; owner hardware untested | NOT_TESTED | Run the packaged launcher on target machines and verify reload persistence |
| WEB-010 | P1 | Real-player exploration of landmark, prop, river and bridge navigation is still required | Shared collision resolver and map regression | OPEN | Play the map without debug assistance and record blocked paths, softlocks and readability issues |

Multiplayer, WSS hosting, additional realms, production WebGL2 and native builds are not open issues: they are explicitly OUT_OF_SCOPE.


## Latest automated evidence — 2026-11-19

CI 44491163465 on 266928c passed 24/24 jobs, including the exact 17-check solo spell catalogue regression, browser compatibility, four-wizard natural boss runs and offline packaging. This closes the catalogue-regression implementation gap for the current candidate; it does not close the broader source-fidelity, production art/audio, physical-device, performance or owner-acceptance issues above.
