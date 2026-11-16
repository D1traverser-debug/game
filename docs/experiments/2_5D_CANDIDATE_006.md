# 2.5D-CANDIDATE-006 — Art-forward single-player browser build

Date: 2026-11-17
Status: LOCAL_CANDIDATE / COMPONENT_SMOKE_PASS / NOT_READY

## Candidate artifact
- File: `咒语旅团-单人网页版-2.5D验收候选.html`
- Size: 718,627 bytes
- SHA-256: `de29ddd55575f1fe78c9b525d41709c2d619d41694cac4eb679cd0dd5f41d48f`
- Self-contained: inline CSS/JS and embedded WebP sprite atlas; no external runtime requests.
- Scope: one hero (Reginald), one map (Verdant Meadows), one player, offline single HTML.
- This exact file is a local conversation artifact and is NOT committed to GitHub. Repository `development/index.html` remains an older implementation.

## Art direction
- Select 2.5D sprite-based rendering as the primary target rather than making unsupported WebGL2 a required runtime dependency.
- 4x4 embedded art atlas includes hero, enemies, bosses, plant, orbs, fungi and statue.
- Procedural ground texture, path, trees, flowers, ruins, rocks, depth sorting, shadows, spell orbs and HUD.
- 3D experimental renderer remains optional. If WebGL2 is unavailable, the 3D toggle is disabled and 2.5D is selected explicitly; no false claim that 3D is running.

## Actual browser smoke
Playwright Chromium in a controlled in-memory document (not file://):
- Desktop 1440x900: menu -> start -> HUD; 2.5D; pause/resume; no visible NaN; no JS exceptions; no console errors; no external requests — PASS.
- Mobile 390x844: menu -> start -> HUD; joystick visible; pause/resume; no visible NaN; no JS exceptions; no console errors; no external requests — PASS.
- Normal 15-second play with short directional inputs: 18 kills, HP 100/100, 0/18 XP; no JS/console errors or external requests. XP orbs visible in the scene but were not collected. This identifies a pickup pacing issue to investigate; do not call progression passed.
- A separate browser FPS sample counted 60 requestAnimationFrames/sec at 1280x800 and 390x844 for the 2.5D and 3D fallback modes in the software test environment. This is cadence under the test browser's frame cap, NOT a real-device GPU benchmark.
- Direct file:// navigation is blocked by this environment; browser storage close/reopen NOT_TESTED.
- A WebGL2 capability probe returned false in the current test sandbox; this is why the 3D control is now disabled there.

## Next work
1. Synchronize the exact 2.5D artifact into GitHub and verify fetched bytes/hash.
2. Investigate XP orb collection and magnet pacing using deterministic tests.
3. Run controlled upgrade/infusion/quest/objective interactions with no forced win hooks.
4. Add a long-duration 19-minute run and genuine boss kill acceptance.
5. Test file:// persistence in a normal user Chrome/Edge browser and real hardware FPS.
6. Continue source fidelity and original art/audio polish.
