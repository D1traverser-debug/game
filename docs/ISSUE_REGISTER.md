# Issue Register

| ID | Severity | Finding | Evidence | Status | Next action |
|---|---|---|---|---|---|
| GAME-001 | P0 | Boss victory test is synthetic: calls forced lethal damage | Previous `studio_release_qa.py` calls `damageBoss(1e7)` | OPEN | Build normal-combat boss acceptance |
| GAME-002 | P0 | Full mission timeline test uses time-jump/immortal test hook | Previous QA calls `runSteps(28750,true)` | OPEN | Real unassisted run |
| GAME-003 | P0 | Actual save/reload not tested; localStorage mocked | Previous QA report | OPEN | Actual file close/reopen |
| GAME-004 | P0 | 200 enemy performance baseline fails target (~21.6 FPS) | Previous QA JSON | OPEN | Profile root cause and compare renderer options |
| GAME-005 | P0 | Original spell/enemy/objective/boss behavior not sufficiently source-pinned | Research register | OPEN | Build versioned mechanic reference tables |
| GAME-006 | P0 | Current visual fidelity is below target | Prototype screenshot and source | OPEN | Art direction, assets, animation and VFX plan |
| GAME-007 | P1 | Current unlock and infusion pools may be simplified/inaccurate | Source inspection pending | OPEN | Verify progression and content gates |
| GAME-008 | P1 | Browser file protocol and storage behavior not verified | Test container limitation | OPEN | Test in real Chrome/Edge local file context |

| GAME-009 | P0 | All spells are force-unlocked on every page load | index.html line 139 overwrites save.unlocks | OPEN | Replace with versioned initial unlocks and quest predicates |
| GAME-010 | P0 | Spell-slot acquisition is random at any level | offerUpgrade uses 27% random new-spell chance | OPEN | Implement source-derived slot milestones and immediate spell upgrade |
| GAME-011 | P0 | 1.2.0 spell content is incomplete | Missing Loaded Dice, Tiny Tremors, Wicked Buzzsaw | OPEN | Add distinct spell behavior and four augmentations each |
| GAME-012 | P1 | Level-14 infusion test is nondeterministic | Random candidate generation can omit target infusion | OPEN | Add deterministic candidate-pool and RNG control |
| GAME-013 | P1 | Debug API was embedded in production artifact | 29492caf removes window.__QA from development/index.html; test hooks remain temporary | RESOLVED_IN_DEVELOPMENT | Recheck exact artifact before final release |
| GAME-014 | P0 | Current 2D renderer does not match original 3D visual structure | Steam screenshot review + current Canvas 2D | OPEN | Validate WebGL 3D hybrid vertical slice |

| GAME-015 | P0 | WebGL 3D slice is not yet visually or performance accepted | WEBGL-SLICE-001: 20 FPS on SwiftShader at ~200 entities; hardware untested | OPEN | Improve scene batching/culling and benchmark on real GPU |

| GAME-016 | P0 | Boss encounter pool is incomplete | Original has Sol'phish, Krog'wa and Mul'gath; baseline only implements Sol'phish | OPEN | Research and implement all Verdant Meadows eligible bosses |
| GAME-017 | P0 | Objective catalogue/variants may be incomplete | 1.1 added variants; current implementation has a simplified set | OPEN | Build versioned objective catalogue and solo acceptance tests |
| GAME-018 | P1 | Verdant Meadows enemy roster/behaviors are not fully traced | Gnasher, Buffer, Shield Crab, Crabladon, Teethy Worm, Bloat Crab references | OPEN | Build per-enemy behavior/drop matrix and verify spawn schedule |
| GAME-019 | P0 | Sol'phish encounter lacks source-confirmed summon/stagger details | Wiki describes enemy convergence, red summon circle, targeted runestones, +200% stagger window | OPEN | Implement and test source-derived boss state machine |
| GAME-020 | P1 | Solo-only upgrade filtering is not source-accurate | Official 1.2 removes Healing Slam from solo augmentation pool | OPEN | Add solo eligibility metadata to every upgrade/quest |
| GAME-021 | P1 | Persistent quest/meta progression is incomplete | Original includes wizard rank, enchantments, masteries, scroll unlocks, ascension/covenants and Reginald outfits | OPEN | Scope and implement the Reginald-only subset |

| GAME-022 | P0 | Corrected unlock/slot progression still lacks the real individual quest-event trackers | PROGRESSION-002: old blanket unlock removed; 14 source quests only documented | OPEN | Add event-sourced achievements with positive/negative event sequence tests |
| GAME-023 | P1 | Spell-slot two threshold is a provisional level-2 assumption | No authoritative source version pin for slot two | OPEN | Verify original, then update contract and rerun boundary tests |
| GAME-024 | P0 | Three new 1.2 spells lack individual augmentations and full audiovisual fidelity | PROGRESSION-002 adds only distinct initial attack behavior | OPEN | Research and implement all 12 source augmentations and spell identities |

| GAME-022 | P0 | No full player-driven 19-minute normal-combat win test | Synthetic boss/objective tests are the only acceptance | OPEN | Build independent real-play acceptance loop |
| GAME-023 | P1 | Spell-specific quests for imp/sprout/blades/talon and others are not event-complete | TRIAL-004 implements only a source-derived subset | OPEN | Complete all solo-applicable quest event trackers |
| GAME-024 | P0 | Textured 3D + adaptive scale still misses the FPS target in software tests | TRIAL-004 SwiftShader ~15-25 FPS observed | OPEN | Profile rendering, reduce expensive draw calls, test real GPU |
| GAME-025 | P0 | Complete 3D art/audio quality is not comparable to original title yet | Current low-poly screenshot and absence of production audio/character animation | OPEN | Produce original assets, VFX, SFX and review under peak combat |

| GAME-026 | P1 | XP orb acquisition feels inconsistent in short smoke play | 15-second movement smoke recorded 18 kills but 0 XP collected while orbs remained visible; movement path did not reliably cross pickup radius | OPEN | Test controlled pickup/magnet cases and tune drop placement/magnet radius without inflating XP |
| GAME-027 | P0 | Art-forward 2.5D candidate is not synchronized to repository source | Local candidate SHA-256 de29ddd55575f1fe78c9b525d41709c2d619d41694cac4eb679cd0dd5f41d48f, 718627 bytes; GitHub index.html is still older 3D source | OPEN | Transfer exact candidate bytes into GitHub, fetch back and verify SHA before treating it as repository current |
