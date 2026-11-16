# TRIAL-004 — Solo Spell Trial Unlock and Adaptive 3D Rendering

Date: 2026-11-16
Code branch: development
File: index.html
Product commit: b21cdba002dc78167cc62601d3a93723d969f191
Artifact: 153894 UTF-8 bytes, SHA-256 0c8d9de43c8fe30f3cad8bd47d657056e1d84bf4a54869229b585b944c281a6a
Verdict: COMPONENT_PASS / NOT_PRODUCT_READY

## Game changes

1. **Visually richer 3D terrain**: a deterministic procedural grass texture is generated locally in WebGL; improved green palette and paths. No external image or network is required.
2. **Adaptive rendering resolution**: WebGL qualityScale drops toward 0.58 when the measured frame rate is poor, reducing pixels processed; rises cautiously when the scene is fast. Core simulation targets 30 Hz.
3. **One-wizard trial**: because some spell-specific quests are impossible to fulfill without first equipping the locked spell, the camp Research UI now allows temporary trial selection for the next run. Trial is not a permanent unlock.
4. **Quest event pipeline**: permanently grants newly confirmed spells after source-derived gameplay event conditions. Examples: Solar Pulse hitting 10 enemies per cast 99 times; Arcane Broadsword 9 single-cast kills; Falling Stars firing 4 stars; Magic Missile 4 critical hits on one projectile; Aurora Wings 5 unique hits; Moonerang 12 unique hits; Bell March 18 target explosion; Cardinal Runes 3 rune hits; Rocky Road 850 critical rocks.
5. **Idempotency**: quest flags persist and repeat grant calls return false. Initial spells remain source version 1.2 starters without incorrectly unlocking the whole catalogue.

The one-wizard trial is a clearly signposted adaptation, not an assertion that the original game uses the same mechanism. Missing quest event trackers remain OPEN.

## Local browser verification
- Playwright progression suite: 17/17 PASS.
- Three-boss / nine-objective / Gnasher invulnerability browser suite: PASS.
- Dedicated solo spell trial browser suite: 11/11 PASS; menu → camp → trial choice → run → level-2 slot → equip; permanent quest grant, duplicate rejection, 4-star cast event, zero runtime exceptions and zero external requests.
- All browser suites inject diagnostics only into an in-memory document; no test-only functions are shipped in the HTML.
- Node.js syntax of both embedded game scripts: PASS.
- Actual browser file:// load/reload: NOT_TESTED due container policy.
- Real human/agent completed 19-min run: NOT_TESTED.
- GPU performance: NOT_TESTED; software SwiftShader scenes observed ~15–25 FPS at adaptive scale 0.58; misses production performance goal.
- Original-quality 3D models, VFX, audio, boss details and player satisfaction: NOT_ACCEPTED.

## Learnings
- A one-hero restriction may make original spell quest prerequisites impossible; a transparent local solo adaptation prevents dead progression but must be recorded as a fidelity exception.
- Initial render success and visually improved ground do not prove acceptable FPS. Dynamic resolution is a mitigation, not a root-cause fix for dense geometry or expensive draw calls.
- Do not upgrade a component result into full product readiness.
