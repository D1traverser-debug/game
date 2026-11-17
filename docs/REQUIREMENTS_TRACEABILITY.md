# Product Requirements and Traceability

Status at baseline: all requirements below are authoritative project requirements or research candidates; source-derived details remain subject to version pinning and validation. Nothing in this matrix is considered passed merely because a corresponding label or code path exists.

| ID | Requirement | Priority | Acceptance evidence | Status |
|---|---|---:|---|---|
| SCOPE-01 | Exactly one playable hero: Reginald | P0 | No hero picker; all run stats/signature behavior match Reginald | PARTIAL |
| SCOPE-02 | Exactly one realm: Verdant Meadow | P0 | One playable map; biome hazards/enemies and boundaries match source | PARTIAL |
| SCOPE-03 | Single-player only; no co-op, AI teammates, online rooms or matchmaking | P0 | Source and runtime inventory show no such systems | PASS_SCOPE |
| DELIVERY-01 | Final build is one self-contained offline HTML | P0 | Network-disabled browser run; one file; no external requests/assets | PARTIAL |
| CORE-01 | Full title/menu/settings/manual/camp/run/result/retry loop | P0 | Real browser user flow and save continuity | PARTIAL |
| CORE-02 | Movement, collision, damage, knockback, invulnerability, death and feedback | P0 | Deterministic unit tests plus player combat tests | NOT_TESTED |
| CORE-03 | Automatic targeting and spell firing behavior is faithful and legible | P0 | Target-selection and real combat comparison | PARTIAL |
| HERO-01 | Reginald's signature Astral Orbs behavior and unique stats | P0 | Source-derived stats + observed behavior tests | PARTIAL |
| SPELL-01 | Every included spell has its own identity, projectile/area behavior, targeting, cooldown, VFX, audio, upgrades and augmentations | P0 | Per-spell acceptance cards and live-run verification | NOT_TESTED |
| SPELL-02 | Spell acquisition/unlock rules are accurate for the pinned source version | P1 | Unlock quest tests, pool eligibility, no unavailable spell offered | NOT_TESTED |
| PROG-01 | XP collection, level thresholds, level-up choice, reroll/banish/lock behavior | P0 | Boundary and sequence tests; no lost or duplicated pending choices | PARTIAL |
| PROG-02 | Element infusion unlock progression and level milestones are correct | P0 | Source-pinned tests for levels 7/14 and locked element availability | PARTIAL |
| PROG-03 | Five elements and all supported pair combinations have distinct correct effects | P0 | 5 single-element + 10 pair-combination matrix; damage/status tests | NOT_TESTED |
| PROG-04 | Scrolls, chests, rarity, stack limits, rerolls, bans and augment pools are faithful | P1 | Pool/weight/stacking and gameplay tests | NOT_TESTED |
| PROG-05 | Meta progression, camp enchantments, unlocks, run statistics and reset rules | P1 | Persistence and unlock progression tests | PARTIAL |
| ENEMY-01 | Enemy roster and behavior are specific to Verdant Meadow | P0 | Per-enemy state machine, target, attack, damage, death/drop tests | PARTIAL |
| ENEMY-02 | Gnasher burrow, invulnerability while underground, approach, leap and landing damage | P0 | Timed behavior/state tests + combat observation | PARTIAL_COMPONENT_PASS |
| MISSION-01 | Objective schedule, spawn bounds, rules, success/fail, timers, bounds, rewards and variants are source-accurate | P0 | Objective-by-objective test matrix; reachable target tests | PARTIAL_9_TYPES_SYNTHETIC |
| BOSS-01 | Sol'phish obelisk/runestone strikes, radial projectiles, homing projectiles, stagger, vulnerability, damage and outro | P0 | Attack-by-attack real-combat tests; telegraph-before-hit; no forced damage | PARTIAL_COMPONENT_TESTED |
| BOSS-02 | Krog'wa three-segment encounter with magnetic-field phase change, inhale/pull, tongue-smash charge and tracking spit | P0 | Phase-boundary, field-boundary, attack telegraph/hitbox/counterplay tests and natural damage pipeline | PARTIAL_COMPONENT_TESTED |
| BOSS-03 | Mul'gath three-segment encounter with phase-driven head growth, head whip, spike grid and linked healing minions; corruption can damage the boss | P0 | Head/phase state tests, grid-cell telegraph and dodge tests, minion approach/corruption/collision tests | PARTIAL_COMPONENT_TESTED |
| BOSS-04 | Shared boss attack lifecycle separates telegraph, active hitbox, recovery, phase transition and visual feedback | P0 | Deterministic attack-card suite; same geometry drives rendering and collision; pause/invulnerability/phase transition regressions | PARTIAL_COMPONENT_TESTED |
| BALANCE-01 | Threat settings, spawn curve, enemy HP/damage, XP/economy and build viability | P0 | Repeated full runs with recorded outcomes and balance analysis | NOT_TESTED |
| UX-01 | Clear HUD, map navigation, objective feedback, level-up/scroll flow, pause, result and retry | P0 | Usability review and complete player flow | PARTIAL |
| UX-02 | Keyboard and touch controls; responsive desktop/mobile layouts | P1 | Browser/device matrix and real touch interaction | PARTIAL |
| UX-03 | Audio controls, readable sound cues, mute behavior, original sound design | P1 | Sound inventory, mute/volume tests, audio review | PARTIAL |
| SAVE-01 | Robust save/load, version migration, corruption recovery, reset confirmation | P0 | Actual close/reopen, schema migration, corruption and reset tests | NOT_TESTED |
| PERF-01 | Target 60 FPS desktop and at least 30 FPS on agreed mobile reference device under representative peak combat load | P0 | Repeatable benchmark on named devices; average and p95 frame time | FAIL_BASELINE |
| VIS-01 | Original art has readable silhouettes, animation, impact, spell identity, enemy telegraphs and coherent environment | P0 | Screenshot/video review at normal and peak combat density | PARTIAL_2_5D_ATLAS_NOT_ACCEPTED |
| QA-01 | No uncaught runtime errors, softlocks, unfinishable objectives, dead upgrade choices or invalid victory states | P0 | Automated regression, fault injection and player-driven run | NOT_TESTED |
| RELEASE-01 | Exact release artifact reproducibly built, hashed, offline tested and published | P0 | Build manifest, SHA-256, release URL and clean-machine test | NOT_READY |
| ACCEPT-01 | Independent technical review and owner playtest; no unresolved P0/P1 defect | P0 | Signed acceptance report and owner approval | NOT_READY |

## Source version policy
Record the game source version/date for every mechanic. Public wiki/community data is a research lead, not unquestionable authority. Prefer official developer announcements/patch notes, then corroborated gameplay evidence, then community wiki/guide. If sources conflict or are version-ambiguous, record the conflict and test the behavior instead of silently choosing a number.

## Baseline truth
The existing prototype has some menus, combat and progression code. Its previous QA was not a full product acceptance: forced boss damage, synthetic time jumps, mocked storage, and a poor 200-enemy performance result must be labelled accurately. See `QA_BASELINE.md`.

| SPELL-SCOPE-01 | Only Reginald-eligible spells may appear in his research, trial, save unlocks and level-up pool | P0 | Source-backed 18-spell allowlist, legacy-save migration and browser regression | PASS_COMPONENT |
| ART-RENDER-02 | Atlas-backed enemy sprites and cached static meadow props must be the active renderer, not shadowed dead code | P1 | Runtime atlas draw-call probe, one canonical renderer declaration, 24-tile cache test | PASS_COMPONENT |

| RUN-ACCEPT-02 | 90 seconds of normal combat with real movement and offered upgrade selection, no forced XP/damage/result | P1 | Playwright normal-play smoke; 83 kills, level 8, 8 real upgrades, 100/100 HP, no errors/network | PASS_AUTOMATED_SMOKE_ONLY |
| SPELL-1.2-ADAPT-01 | Three new 1.2 starter spells have four distinct, functioning augmentations each | P0 | Individual effect probes per augment, not only catalogue counts | PARTIAL_MECHANIC_EXISTS |
| SOURCE-TRUTH-01 | Officially undocumented new-spell augmentation names/effects must be identified as independent adaptations | P0 | UI copy and source matrix clearly separate source facts from original designs | PASS_DOCUMENTED / UI_POLISH |


Boss component evidence (2026-11-17): CI 44062145086 passed 15/15 deterministic boss probes on development commit 35b4aa2. This upgrades the implementation status from missing/simplified mechanics to partial component coverage only. It does not satisfy the source-accurate natural-combat, visual readability, counterplay, pause/invulnerability, human-play or balance acceptance criteria in the BOSS rows.
