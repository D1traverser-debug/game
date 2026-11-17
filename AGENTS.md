# Full-Game Development Agent Instructions

The repository—not chat summaries—is the canonical source of truth. The active product is an original-IP, full-game co-op roguelite inspired by the observable gameplay systems of The Spell Brigade. The old browser build is a legacy prototype only.

## Mandatory cold-start

1. Fetch the current GitHub `main`, `development`, and `full-game` HEAD SHAs.
2. Read `docs/PROJECT_STATE.json`, `HANDOFF.md`, `docs/PROJECT_CHARTER.md`, `docs/FULL_GAME_PRODUCT_BRIEF.md`, `docs/FULL_GAME_ROADMAP.md`, `docs/REQUIREMENTS_TRACEABILITY.md`, `docs/ISSUE_REGISTER.md`, the latest decision/experiment report, and current engine project files.
3. Reconcile remote evidence; never rely on stale chat summaries. Inspect the legacy `development/index.html` only as a reference artifact.
4. For an interrupted write, classify it as `UNKNOWN_PENDING_READBACK`; inspect the remote target before retrying.
5. Run available repository and engine checks. A mechanical check is not product acceptance.
6. Continue from the next player-outcome-critical open issue. Do not ask the owner to repeat documented constraints.

## Owner's current full-game directive

- Complete independent game, not a one-hero/one-map prototype.
- Solo and 1–4 player online co-op are production targets.
- Full current-version content target: complete wizard roster, all documented realms, spells, elements and combinations, augmentations, scrolls, quests, objectives/variants, enemies/bosses, trials/covenants and meta progression.
- Windows PC first; keyboard/mouse and controller. Console/cross-play is a later gate.
- Production engine direction: Unity 6.3 LTS + URP, pending vertical-slice falsification.
- Original IP and assets: do not copy proprietary source, extracted game data, character designs, original art, animation, fonts, UI expression, writing, music, voice, or recordings. Independently implement gameplay systems and create original content.
- The old requirements "Reginald only", "Verdant Meadows only", "single-player only", and "single offline HTML" are superseded for the full-game branch. They remain historical constraints for the legacy browser prototype only.
- CAOS is a read-only methodological reference. Never modify CAOS code, repo, branches, PRs, files, Skills, plugins, docs, configuration, or data.

## Product engineering loop

Owner intent → current source/version evidence → requirements traceability → L0–L5 root-cause analysis → architecture alternatives/falsifiers → vertical-slice implementation → automated tests → real engine/browser/device integration → human visual/audio/gameplay/network review → independent acceptance → learning and regression guard.

Investigate shared causes before patching symptoms. Compare repair, refactor, redesign, replacement, reuse, and no-change. Record trade-offs, rollback, and uncertainty.

## Architecture invariants

- Gameplay simulation and content definitions must not depend on rendering.
- Networked gameplay-critical state is host/server authoritative; clients send validated intent, not trusted damage, inventory, position, RNG, or win results.
- Randomness is seedable and owned by simulation; rendering/audio must not consume gameplay RNG.
- Spell/element/augmentation behavior is data-driven but each effect has distinct implementation and tests.
- Attack telegraph, collision geometry, active damage, and VFX must derive from one authoritative attack instance.
- UI, audio, VFX and gameplay emit typed events; no hidden cross-system mutation.
- Content counts are not acceptance. Each item needs a behavior card, source confidence, test, and live-play review.
- Every asset needs source files, import settings, license/provenance, and usage manifest.
- Test-only hooks never ship in production builds.

## Test integrity

- Synthetic time jumps, forced boss kills, direct state mutation, mocked storage, screenshots, and a working menu are not full-game acceptance.
- PASS requires exact commit/build ID, reproducible procedure, observed outcome, and evidence.
- Mark unsupported or blocked checks NOT_TESTED.
- Distinguish solo play, 4-player network play, human full-run completion, performance, save/reload, controller input, visual/audio review, and release acceptance.
- The implementation agent cannot self-certify fun, visual quality, or release readiness.

## Branch discipline

- `main`: preserved legacy baseline; never overwrite casually.
- `development`: legacy single-player browser prototype and historical experiments.
- `full-game`: active full-game production.
- Keep prototype code isolated. Reuse only after code review, architecture fit, and tests; do not paste the monolithic HTML into the new runtime.
- Every meaningful change updates project state, handoff, issue register, decision log, and evidence.
- Do not declare READY from CI success, asset count, test count, or document completion.

## Current next action

Create the Unity 6.3 LTS URP production skeleton and a polished, network-capable vertical slice. Validate 1–4 player host-authoritative combat before mass content production. Product status remains NOT_READY.
