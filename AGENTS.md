# Agent Instructions — Aetherwilds Single-Player Game

The canonical project is this repository, branch full-game. Read docs/PROJECT_STATE.json and HANDOFF.md before acting.

Owner scope: finish one complete, offline-capable browser single-player action roguelite. One authored realm (翠影荒野 / Verdant Wilds), four playable wizards, one complete run loop, existing enemy/objective/boss systems, progression and persistent camp. Desktop browser first with mobile controls. Do not implement online multiplayer, lobbies, room servers, Unity/native builds, or additional realms/rosters unless the owner changes scope.

Engineering loop: intent → inspect exact runtime and evidence → identify root cause → compare refactor/reuse/rebuild → implement → deterministic tests → real browser integration → visual/gameplay review → acceptance. Avoid local symptom patches.

Invariants: simulation independent of DOM/render/audio; fixed-step simulation; presentation does not consume gameplay RNG; no production debug hooks; offline runtime with no CDN dependency; stable content IDs; save migration preserves existing currency, upgrades and progression.

The one realm must have a bounded world, named districts, recognizable landmarks, navigation/minimap and playable traversal. Each wizard must have a unique starter spell, passive, active ability, base-stat profile and readable in-world visual identity. The run must include character selection, combat, objectives, upgrades, boss encounter, victory/defeat, results, camp and replay.

Automated checks prove only their listed behavior. Synthetic component probes are not owner acceptance. Do not call READY until the owner has played and accepted the exact build.

CAOS repositories and configuration remain read-only.
