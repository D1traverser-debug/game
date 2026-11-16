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
