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

| GAME-026 | P1 | XP orb acquisition appeared absent in an early low-movement smoke | Follow-up directional movement test collected 14 XP and displayed an upgrade choice; early run had not crossed pickup radius | RESOLVED_AS_FALSE_ALARM | Keep monitoring pickup pacing during longer normal play; no pickup code change justified yet |
| GAME-027 | P0 | Art-forward 2.5D candidate was not synchronized to repository source | Resolved: development/index.html exact bytes verified, 717368 bytes, SHA-256 21fbfcdf3149c5d2eee188a213bf66c3fba5a6b777e7c868a5ddb823a79c0239 | RESOLVED | Keep state checkpoint and release artifact hashes synchronized |

| GAME-028 | P1 | A duplicate legacy v2enemy function shadowed the atlas-backed renderer | The later procedural function declaration replaced the intended atlas renderer; runtime rendered simplified blobs despite an embedded atlas | RESOLVED | Removed the superseded function and added a browser regression that proves atlas draw calls and static cache creation |
| GAME-029 | P0 | Non-Reginald signature spells were offered in a Reginald-only game | Seven other-wizard/unsupported entries were exposed in the trial UI and spell pool; legacy saves could retain them | RESOLVED | Added REGINALD_SPELL_IDS (18 entries), filtered save migration, quest grants, research UI and level-up pool; 13/13 scope checks pass |
| GAME-030 | P0 | 2.5D renderer misses 60 FPS desktop target under synthetic peak enemy load | 197 active enemies produced ~48.7–51.1 FPS at 1440x900 in headless Chromium; ~60 FPS mobile viewport; real hardware not measured | OPEN | Profile remaining dynamic draw cost and validate on named real desktop/mobile devices |

| GAME-031 | P1 | Progression regression still asserted save schema v2 after product migrated to v3 | CI 43916812249: 16/17 checks; stale schema assertion was the sole progression failure | RESOLVED | Test now asserts schema v3; retain migration and unlock checks |
| GAME-032 | P1 | Atlas renderer regression probe inserted literal backslash-n, so its test hook was never defined | CI 43916819843: test-only injected source failed with ReferenceError __artProbe is not defined | RESOLVED | Probe now injects a real newline; re-run full CI |
| GAME-033 | P0 | 2.5D full 19-minute natural-combat mission and boss victory remain unverified | Current browser tests are component/synthetic; no forced boss victory can count as product acceptance | OPEN | Add a non-cheating automated playthrough and human acceptance run; do not mutate boss HP/time/win state |

| GAME-034 | P0 | Normal/scared fungi, Soul Sludge and standard Spell Core objectives had no contact-collection update path | Natural-run source trace showed Soul Sludge progress stuck at 0; source wiki confirms Soul Sludge is completed by walking over purple ground. Normal fungi and standard cores had the same missing handler | RESOLVED_IN_CODE | Implement contact collection in updateObjective; 9/9 objective component checks pass, full mission still pending |
| GAME-035 | P1 | Full-mission Playwright harness used synchronous set_default_timeout as await and passed unsupported timeout to Page.evaluate | CI failures were test API misuse, not production gameplay | RESOLVED | Use synchronous page.set_default_timeout and asyncio.wait_for around evaluate |
| GAME-036 | P0 | Natural mission pilot dies before boss during first/second objective pressure | Run 43928161064: died at 154.3s, HP 10.7/100, 89.3 damage taken, level 9, 135 kills, Rift progress 53.82/100; no runtime errors. Pilot did not seek health/magnet drops | OPEN | Pilot now targets actual health/magnet drops; rerun and inspect trace; separately verify source-accurate player upgrade pool and balance |

| GAME-037 | P0 | Enemy wave pressure accumulated to 241 active enemies by 7 minutes, causing inevitable crowd death | Replaced unbounded time-multiplied waves with time-scaled active population target capped at 64; full mission pilot now passes | RESOLVED_IN_CODE_AND_AUTOMATED_RUN | Continue balance validation with three boss archetypes and human play |
| GAME-038 | P1 | Max-HP upgrades increased the health ceiling without immediate sustain, making vitality picks weak during long runs | Vitality Forge now restores 25% of added max HP; character upgrade regression validates the effect | RESOLVED_IN_CODE | Compare healing amount with original and balance after multi-build testing |
| GAME-039 | P0 | Natural full-run and boss win had not been demonstrated | Automated no-state-mutation full run defeated Mul'gath at 1463.17s; 732 kills, level 19, 4 objectives, 462/540 HP | PARTIALLY_RESOLVED | Repeat full natural runs for Sol'phish and Krog'wa; obtain human owner acceptance |
