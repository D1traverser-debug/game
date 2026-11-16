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
| GAME-013 | P1 | Debug API is embedded in production artifact | ?qa exposes direct mutation/time-jump/forced-boss helpers | OPEN | Separate test instrumentation from release build |
| GAME-014 | P0 | Current 2D renderer does not match original 3D visual structure | Steam screenshot review + current Canvas 2D | OPEN | Validate WebGL 3D hybrid vertical slice |

| GAME-015 | P0 | WebGL 3D slice is not yet visually or performance accepted | WEBGL-SLICE-001: 20 FPS on SwiftShader at ~200 entities; hardware untested | OPEN | Improve scene batching/culling and benchmark on real GPU |
