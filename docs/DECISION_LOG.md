# Decision Log

## D-001 — Product scope (ACCEPTED, owner instruction)
- One hero: Reginald.
- One map: Verdant Meadow.
- Single-player only.
- No online multiplayer, matchmaking, AI teammates, additional heroes, or maps.
- Final player delivery is one self-contained offline HTML.
- Rationale: finish one high-quality complete experience before expansion.

## D-002 — Repository role (ACCEPTED)
- GitHub `D1traverser-debug/game` is the canonical source of code, requirements, decisions, test evidence, and recovery state.
- Conversation memory is not authoritative.
- Root `index.html` is the current baseline playable artifact. It may be refactored only with rollback and reproducible single-file build preservation.

## D-003 — CAOS boundary (ACCEPTED)
- Apply CAOS governance methods to this project only.
- Do not modify CAOS code, files, branches, PRs, plugins, configuration, or documentation.
- Do not copy CAOS implementation assets into this repository; this project owns its own governance docs.

## D-004 — Fidelity over feature count (ACCEPTED)
- A spell, element, objective, or boss phase is not implemented merely because it has a name or data entry.
- Each mechanic needs source evidence, state-transition definition, visible/audio feedback, balance constraints, and tests.
- Generic multipliers or synthetic forced-state tests cannot substitute for the mechanic.

## D-005 — Original asset boundary (ACCEPTED)
- Implement observable mechanics independently; create original art/audio.
- Do not copy original game source, extracted game assets, music, sound recordings, or animations.
- Fan project is unofficial and must not imply endorsement.

## D-006 — Primary renderer is art-forward 2.5D (ACCEPTED)
- The final product may use a different rendering technique from the original if the complete player experience is equivalent.
- Use Canvas 2D 2.5D with original sprite art, a coherent tile-cached environment, readable spell VFX and depth-sorted actors as the primary path.
- Keep WebGL2 3D as an optional experiment only where actually supported; failure to initialize must fall back to 2.5D without breaking play.
- Rationale: 2.5D now uses an embedded atlas and 24 cached static scene tiles; it is more portable and visually coherent than the current low-poly software-rendered 3D path. This decision does NOT waive the 60 FPS, art, animation or owner-acceptance gates.

## D-007 — Reginald-only spell eligibility (ACCEPTED)
- The Reginald product catalogue is 18 spells: Astral Orbs; Loaded Dice, Tiny Tremors and Wicked Buzzsaw (official 1.2 starters); plus the 14 general spell-quest unlocks.
- Other wizard Ascension signature spells are excluded from Reginald's research, temporary trials, persistent unlocks and level-up offer pool.
- The trial slot is a single-player adaptation for otherwise impossible unlock prerequisites, not an original-game feature; the underlying quest conditions remain source-derived and must be labeled as adaptation where needed.
- Evidence: official 1.2 patch notes, Reginald and Spells wiki pages, and Ascension signature discussion. Sources are listed in MECHANIC_REFERENCE_MATRIX.md.


## D-008 — Natural-run pilot and multi-boss coverage gate (ACCEPTED)
- The full-mission baseline uses the default Reginald loadout. The temporary one-run spell trial is tested by its dedicated regression and must not be silently injected into the boss-coverage baseline.
- Multi-boss automated coverage requires at least three deterministic seeds, each completing a natural run, with the observed boss-ID set exactly equal to `sol`, `krog`, and `mul`.
- The pilot may only supply normal movement, ordinary interaction, and selections from cards actually offered by production. It may not set time, HP, XP, objective progress, enemy/boss state, or victory.
- Card ranking must use actual option identifiers or exact displayed labels. If the pilot fails, incoming damage, build choices, objective progress and movement must be inspected before attributing the result to production balance.
- Automated pilot success is not human owner acceptance and does not waive source-fidelity, performance, persistence, visual/audio or release gates.


## D-009 — Preserve default self-damage and model optional Harmony Pact (ACCEPTED)
- The default game rule permits caster self-damage from friendly-fire spell hazards; this is intentional source behavior, not an accidental test artifact.
- Harmony Pact is a separate covenant that disables damage to self and teammates. It is a backlog feature to scope, not an implicit global default.
- Natural-run acceptance must avoid self-damage hazards through movement and build decisions. It must not silently suppress production damage to obtain a green run.
- Evidence: official 0.7.0 patch notes https://steamdb.info/patchnotes/16553491/ and developer response https://steamcommunity.com/app/2904000/discussions/1/4513255804483189926/.


## D-010 — Keep the natural-run pilot out of map-edge and objective deadlocks (ACCEPTED)
- Loot targets outside a safe interior envelope must not pull the pilot into an unreachable world boundary.
- When near a clamped world edge, inward movement is a hard constraint, not a weak additive preference.
- During Rift capture, remove outward radial dodge force while preserving tangential movement; objective progress must not be reset by avoidable steering drift.
- Gnasher avoidance must include lateral movement during burrow/leap, not only direct retreat.
- These are QA-agent controls only. Do not change production map bounds, objective rules or enemy damage without separate source/player evidence.


## D-011 — Emergency threat priority overrides objective progress (ACCEPTED)
- Immediate incoming projectiles and Gnasher burrow/leap threats outrank objective capture and optional loot.
- Rift containment is a normal objective preference, not an absolute movement lock; imminent lethal tells may justify a temporary exit.
- Hard inward boundary steering activates only near the actual world clamp. Perimeter objectives remain reachable.
- When Gnasher is in a burrow/leap sequence, suspend objective and loot pursuit and use a lateral escape vector.
- These are automated QA-agent rules only. Do not change production objective radius, map bounds or enemy damage without separate source/player evidence.


## D-012 — Treat Gnasher leap as a fixed landing-point attack (ACCEPTED)
- Gnasher burrow follows the player for 1.25 seconds at 3x movement speed, then captures `leapX/leapY` and completes a 0.55-second leap.
- The landing hit checks a 60-unit radius around the fixed target point. The QA pilot must score its escape path against that point, not against the enemy's interpolated current position.
- Defensive stats and sustain scrolls must not be silently outranked by a new-spell offer when survival is the active gate.
- Projectile/hazard avoidance activation must not depend solely on nearby-enemy distance.
- This decision governs the QA pilot only. Production enemy damage and behavior remain unchanged pending source fidelity and human playtest evidence.


## D-013 — Lock Gnasher escape per attack and score all landing zones (ACCEPTED)
- A Gnasher leap is a fixed-point landing attack. The pilot must maximize separation from all simultaneously active landing points, not just the nearest enemy's current position.
- Recomputing the selected direction every frame can oscillate when multiple Gnashers change rank. Lock the chosen heading for that individual attack phase.
- Score actual movement after world-boundary clamping; a nominal heading that only yields a few pixels of displacement is not a valid escape.
- Exact attacker identity and all nearby Gnasher landing targets must be captured when a hit occurs.
- This is test-agent policy only. Do not modify production Gnasher damage or telegraphs until a competent agent and owner playtest demonstrate a production defect.


## D-014 — Keep browser instrumentation inside its host-language string (ACCEPTED)
- Test-only JavaScript injected into a browser document must be represented as Python string data in the Python harness; raw JavaScript declarations must never appear at Python module scope.
- Add an exact-one-occurrence anchor assertion before replacing production source in the temporary document.
- A Python parse failure invalidates the run; do not interpret it as a gameplay result.


## D-015 — Merge concurrent emergency steering vectors (ACCEPTED)
- A Gnasher threat must not erase an independently predicted projectile or active hazard threat.
- Keep Gnasher escape as the primary route, but add separately tracked projectile and hazard avoidance vectors before final input normalization.
- The test must preserve evidence that each threat class is detected and that its steering contribution survives the final merge.
- This is QA-agent behavior only; production damage and attack timing remain unchanged.


## D-016 — Reject locked Gnasher steering when it reduces observed evasion (ACCEPTED)
- CI evidence takes precedence over a theoretically cleaner lock: dynamic per-frame Gnasher scoring produced 327 leap-safe frames and a natural win on seed 1, while the locked policy produced 20 and a death.
- Restore the empirically successful dynamic controller; do not retain a lock solely because it appears more stable.
- Expand projectile lookahead to at least 1.8s when the predicted miss distance is within the collision envelope.
- This remains QA-agent tuning; do not change production attack timing or damage to compensate.


## D-017 — Dynamic all-landing scoring with actual movement distance (ACCEPTED)
- Keep Gnasher escape dynamic per frame; a direction lock regressed observed survival.
- Score candidate movement by actual displacement after clamping, not only by nominal heading or landing-point distance.
- When multiple Gnashers are in leap state, maximize minimum separation from all their fixed landing points.
- Preserve the 1.8-second projectile lookahead validated in CI #133 seeds 2 and 3.
- QA-agent change only; no production damage adjustment without source and human-play evidence.


## D-018 — A survival smoke must use a deterministic, minimally competent pilot (ACCEPTED)
- Fix the RNG seed so a regression is reproducible.
- The smoke pilot may use only legal movement, pickup and upgrade actions; it must not mutate combat state, grant resources, skip time or force a result.
- It should prioritize health when injured, avoid visible threats and select defensive/sustain upgrades when offered.
- Keep the 90-second survival assertion; do not turn a failed smoke into a pass by removing the survival requirement.
- If the competent seeded pilot still dies, use recorded damage evidence to investigate source fidelity and production balance separately.


## D-019 — Use remaining attack time and retreat before critical HP (ACCEPTED)
- Projectile lookahead conditions must be checked at the outermost guard; an inner 1.8s threshold nested under a 1.35s guard is not an effective 1.8s predictor.
- For Gnasher leap, predict player displacement over the attack's remaining `stateT`, not a fixed full 0.55s window.
- At low HP, suspend objective/loot pursuit and prioritize survival before the player reaches 30% HP; use 55% as the pilot retreat threshold under nearby threat.
- Keep all changes in the QA agent until human/source evidence justifies production balance changes.


## D-020 — Separate baseline survival from adaptive boss-archetype discovery (ACCEPTED)
- Keep seeds 1, 2 and 3 as mandatory full natural-run regressions; all three must win.
- Boss archetype selection remains entirely natural and RNG-driven. Do not patch `spawnBoss`, force a boss ID, alter boss HP, or mutate game state.
- Candidate seeds may stop after the naturally selected boss spawns. If that archetype is not yet represented by a natural victory in the current CI run, continue the same run to a natural boss defeat; otherwise record the scout without claiming a victory.
- Count archetype coverage only from runs that naturally defeat the boss. Require winning IDs exactly `sol`, `krog`, and `mul`.
- Preserve browser/console and offline/no-external-request checks for every attempted run.

## D-021 — A deterministic browser pilot must own the only simulation clock (ACCEPTED)
- The test agent may advance game state manually only when the production RAF loop is prevented from advancing it.
- Keep rendering active, but gate the production `update(SIM_STEP)` call in the temporary test document while the manual pilot owns simulation.
- Count manual ticks and require one manual update for every harness tick. Record blocked RAF update attempts as evidence that the gate is active.
- Repeat at least one seeded run in a fresh browser context and require identical outcome signatures.
- Keep deterministic RNG seeding and compact per-run diagnostics. Do not change production balance or game code to compensate for a test-harness race.
- A same-seed result that changes between CI runs invalidates natural-run evidence until the clock ownership is fixed and replayed.


## D-022 — Preserve offensive progression in the QA pilot while gating defense by actual risk (ACCEPTED)
- A test pilot is not competent merely because it maximizes survivability stats; it must maintain sufficient damage progression to control the encounter population.
- When HP is healthy, prioritize new spell acquisition, spell levels, spell augmentations, infusions and direct damage/cast/critical stats before defensive fallback.
- When HP is low, sustain scrolls and defensive upgrades may take priority. Do not remove defensive choices; make them conditional on observed risk.
- Record HP ratio at every real upgrade offer and assert that a healthy new-spell offer is selected. Keep the pilot limited to actual offered cards and legal game inputs.
- This is test-agent strategy only. Do not change production damage, enemy pressure, boss HP or player balance from an automated pilot failure alone.


## D-023 — Rendering must not consume the deterministic simulation RNG (ACCEPTED)
- The gameplay RNG stream is seeded for repeatable simulations. Rendering must not advance that stream.
- CI #139 showed that blocking RAF simulation updates was insufficient: `drawWorld()` still called `rand()` twice per frame for screen-shake offsets, making spawns, drops, objectives and boss selection depend on browser frame cadence.
- In the temporary QA document only, use deterministic time-based screen-shake offsets and instrument all render calls to `Math.random`; require zero render-phase RNG calls.
- Advance the manual pilot at the production `SIM_STEP=1/30`, using three simulation steps per 0.1-second input decision. Require manual tick count to equal simulation tick count.
- Keep production `index.html`, game balance and source behavior unchanged. Re-run identical seed 1 in a fresh browser context and require the outcome signature to match.


## D-024 — Isolate RNG from every renderer, not only the legacy 2D path (ACCEPTED)
- A deterministic game test must audit every rendering implementation that can be active or selected, including the atlas-backed 2.5D camera path.
- CI #140 showed that replacing the legacy 2D screen-shake calls was insufficient: the second renderer still called `rand()` twice per frame for camera X/Y shake.
- In the temporary QA document, replace screen-shake randomness in both renderers with deterministic time-based offsets. Keep a source assertion that no `rand(-g.shake,g.shake)` call remains and a runtime counter requiring zero render-phase `Math.random` calls.
- Do not modify production render behavior merely to make the test pass. Keep production `index.html` and combat balance unchanged until a separate product requirement justifies a production change.


## D-025 — Separate deterministic CI gates from heuristic long-run exploration (ACCEPTED)

**Evidence**
- CI #141 (run 44043697224, development commit 698fa9150eba673f33419aec3de1467273e2caeb) passed the checkpoint and the first four browser regressions.
- The adaptive 24-seed natural-play job then failed its required baseline: seeds 1/2/3 died at 286.1s, 514.5s and 468.9s, before the 19-minute boss window. No natural boss victory was recorded.
- The same run passed single-clock ownership, render-RNG isolation, fixed 1/30 simulation step, identical seed-1 replay, healthy new-spell choice, browser-error and offline-request checks.
- Because the heuristic pilot failed, five unrelated deterministic/content-renderer tests were skipped by the sequential job. The run did not establish that a human cannot complete the game.

**Decision**
- Keep deterministic checkpoint and bounded browser regressions as blocking CI.
- Move the long-horizon heuristic pilot to a separate nightly/manual workflow and preserve its JSON report as an artifact.
- Keep pilot failures visible and actionable, but classify them as exploratory evidence until corroborated by a production defect or human play.
- Never modify production damage, HP, spawn rates or boss mechanics solely to satisfy the heuristic pilot.

**Falsifiers / review**
- If the exploratory agent becomes a validated representative player model with documented skill envelope and independent correlation to human outcomes, its role may be reconsidered.
- Any future change to the pilot must retain legal inputs, no state mutation, deterministic replay and complete per-seed evidence.


## D-026 — Test closure-private game functions through in-scope probes (ACCEPTED)

- Production game functions remain private inside the runtime IIFE; do not export internal mutation APIs solely to satisfy tests.
- Browser component tests may inject a temporary probe at the approved in-IIFE marker, where it can call private functions through lexical scope.
- The Python test driver must call the injected probe, not call a private production function from the page's global scope.
- Keep probes in the in-memory test document only. Verify the release HTML still has no production debug surface.
- A ReferenceError caused by a test calling an inaccessible private symbol is a test-harness defect until a separate runtime failure is demonstrated.
