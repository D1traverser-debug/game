# Issue Register — Aetherwilds Single-Player Browser

| ID | Priority | Issue | Evidence | Status | Next action |
|---|---:|---|---|---|---|
| WEB-001 | P0 | Four distinct original wizard rows and idle/walk/cast/ability poses now render from a bespoke atlas; final silhouette, gameplay-scale readability and animation acceptance remain outstanding | Wizard visual-identity regression (candidate) | PARTIAL | Review all four silhouettes and action poses in live combat; refine scale, timing and hit feedback from owner playtest |
| WEB-002 | P0 | Original wizard art is integrated; environment atmosphere and spell-impact presentation now have a deterministic candidate pass, while bespoke enemy, spell, UI and complete animation asset coverage remain incomplete | Environment visual regression; atlas-backed renderer; Art/Audio Bible | PARTIAL | Review the exact build in live combat; then continue bespoke enemy/creature animation and spell-specific VFX/UI coverage |
| WEB-003 | P0 | Source-version content manifest is unresolved across the implemented spell pool, augments, elements/infusions, enemies, objectives, bosses, quests and meta progression | Mechanic Reference Matrix; 25 definitions with an 18-ID current solo pool | OPEN | Pin reference version; classify every implemented ID as in-scope, adapted, excluded or unknown |
| WEB-004 | P0 | Physical browser/device compatibility and representative-hardware performance are not accepted | Chromium/Firefox/WebKit automation passes; no physical-device evidence | OPEN | Test iOS Safari/Android Chrome, real controllers, low-end GPU, p95 frame time, memory and 15-minute stability |
| WEB-005 | P0 | Exact-build owner and independent gameplay/visual/audio acceptance remain outstanding | Governance and Release Gates | NOT_TESTED | Conduct unassisted playtest and review the exact candidate; owner alone determines acceptance |
| WEB-006 | P1 | Simulation modularization is partial: fixed-step clock and damage pipeline are integrated; the PCG per-run stream now covers objective selection/generation and fixed world-layout decoration; other gameplay RNG call sites remain legacy | Architecture, Deterministic RNG Audit 001 and Objective RNG Integration 001 | IN_PROGRESS | Verify the objective RNG candidate in CI; then migrate enemy director RNG and entity IDs as a separate bounded slice; do not bulk-replace Math.random or rewrite the monolith |
| WEB-007 | P1 | Four character-specific procedural music motifs and sparse forest ambience calls are integrated; SFX and the overall mix remain procedural and unapproved | Audio regression (candidate); no owner listening review | PARTIAL | Review on target speakers/headphones, tune loudness/fatigue and decide whether authored stems/SFX are required |
| WEB-008 | P1 | Save import/export file chooser and download behavior on physical/cross-browser targets remain unverified | Chromium save-persistence regression | PARTIAL | Verify real-origin reload, export/import and corruption recovery in Firefox/WebKit and physical devices |
| WEB-009 | P1 | One-click launch and persistent storage have not been verified on the owner's Windows/macOS/Linux hardware | CI package passes; owner hardware untested | NOT_TESTED | Run the packaged launcher on target machines and verify reload persistence |
| WEB-010 | P1 | Real-player exploration of landmark, prop, river and bridge navigation is still required | Shared collision resolver and map regression | OPEN | Play the map without debug assistance and record blocked paths, softlocks and readability issues |

Multiplayer, WSS hosting, additional realms, production WebGL2 and native builds are not open issues: they are explicitly OUT_OF_SCOPE.


## Latest automated evidence — 2026-11-19

CI 44491163465 on 266928c passed 24/24 jobs, including the exact 17-check solo spell catalogue regression, browser compatibility, four-wizard natural boss runs and offline packaging. This closes the catalogue-regression implementation gap for the current candidate; it does not close the broader source-fidelity, production art/audio, physical-device, performance or owner-acceptance issues above.


The objective RNG integration is intentionally partial: it does not make enemy/combat/loot/spell/chest/boss outcomes fully replayable. Product status remains NOT_READY until all release gates and owner acceptance pass.


## Latest automated evidence — 2026-11-19 (objective RNG candidate)

Run `44507473452` on candidate commit `b99802cb1bc300a22dce1780d969cd42541db02c` passed 25/25 jobs, including objective RNG isolation/replay checks, Chromium/Firefox/WebKit compatibility and all four natural wizard boss wins. The objective RNG integration slice is closed for automated CI. Full-run RNG coverage is still incomplete: enemy director, combat, loot, level-up, spell, chest and boss randomness remain on legacy call sites. Product status remains NOT_READY; owner and physical-device acceptance remain open.
