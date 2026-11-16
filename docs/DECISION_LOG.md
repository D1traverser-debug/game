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

## D-006 — Architecture not yet frozen (OPEN)
- Canvas 2D, WebGL/Three.js, and hybrid options require a comparative experiment against fidelity, performance, single-file packaging, asset cost, and mobile support.
- Do not prematurely rewrite the whole game before the comparison.
