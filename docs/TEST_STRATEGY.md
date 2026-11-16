# Test Strategy

## Test pyramid
- Pure logic tests: damage pipeline, status effects, targeting, level-up queue, objective state machines, save schema.
- Deterministic simulation tests: fixed seed, fixed timestep, fixed input scripts, explicit expected state invariants.
- Browser integration: menu, controls, HUD, upgrade choices, pause/resume, camp, results, save/load.
- Real-play acceptance: unassisted full run and boss fight without debug hooks.
- Visual/audio: screenshot/video comparison, telegraph readability, effect clarity, sound event and mute controls.
- Performance: fixed entity profiles, repeatable samples, average/p95 frame time and memory.
- Compatibility: current Chrome/Edge/Firefox desktop; Android Chrome and iOS Safari where available.

## Test integrity rules
- Test-only instrumentation must be injected into a temporary copy and never shipped in the final HTML.
- Label synthetic time, forced HP, immortality, mocked storage and direct state mutation explicitly.
- No test can pass by directly setting the output state it is meant to verify.
- Boss victory tests must not call a helper that directly kills the boss.
- Full-run tests must not skip the actual gameplay loop.
- Persistence must use real browser storage across an actual close/reopen.
- Every regression test must have at least one negative/mutation case where practical.

## Performance methodology
Freeze test device/browser and load profile before comparing optimization candidates. Use at least five runs, warm-up, same scene/entity count, same viewport/DPR, report median, mean, p95 and worst frame. Optimization must not alter hit detection, damage, or telegraph behavior.
