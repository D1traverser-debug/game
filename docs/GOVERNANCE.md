# Game Project Governance — CAOS-Informed, Project-Local

**Boundary:** This document applies only to this game repository. CAOS is a read-only parent reference. No CAOS code, files, configuration, Skill, branch, PR, repository, or other asset may be changed.

## 1. Operating principles
- The owner's product goal and explicit exclusions outrank assistant assumptions and implementation convenience.
- Discovery, qualification, diagnosis, solution selection, implementation, and acceptance are separate states.
- Evidence must be traceable to source, version, commit, reproducible test, or observed player outcome.
- A fix must address the highest supported common cause, not only the latest symptom.
- A successful build, test count, commit, or report is not equivalent to a successful game.
- Every important change must include a falsifier, regression coverage, rollback path, and independent review.
- Preserve negative evidence and uncertainty; never convert NOT_TESTED into PASS.

## 2. Ten-stage governance loop
1. **Discovery:** capture symptoms and candidate issues without selecting a fix.
2. **Qualification:** verify reproducibility, severity, confidence, scope, and false-positive risk.
3. **Root-cause elevation:** inspect L0 instance, L1 component, L2 workflow, L3 architecture, L4 governance, and L5 meta-governance. For P0/P1 issues, inspect the current layer and at least two higher layers.
4. **Problem framing:** record evidence, violated invariant, affected paths, hypotheses, constraints, and falsifiers.
5. **Solution search:** compare local fix, workflow redesign, architecture change, governance change, replacement/reuse, and no-change/risk acceptance.
6. **Comparative evaluation:** score causal coverage, fidelity, player impact, regression risk, cost, reversibility, complexity, and bypass likelihood.
7. **Governance review:** verify authority and scope. Owner requirements cannot be silently rewritten by the implementer.
8. **Controlled experiment:** change one coherent mechanism at a time; define expected and disconfirming results before broad adoption.
9. **Independent verification:** reviewer must not merely repeat the implementation path. Use source-grounded tests, deterministic probes, clean browser runs, mutation tests, and owner playtesting. Same-model review is not truly independent; disclose that limitation.
10. **Learning:** convert validated lessons into regression tests, detection rules, design principles, architecture mechanisms, and enforced invariants.

## 3. Root-cause elevation questions
- L0: What exact runtime symptom or player-visible failure occurred?
- L1: Which function/state/entity causes it?
- L2: Which sequence, timing, or state transition permits it?
- L3: Is the system decomposition or shared abstraction wrong?
- L4: Did requirements, review, or release gates allow it?
- L5: Why did the development/verification process fail to detect the defect or accept a false result?

## 4. Knowledge maturity
Observation → Hypothesis → Researched Knowledge → Validated Knowledge → Accepted Principle → Governance Rule → Architecture Mechanism → Enforced Invariant.

Research notes do not become requirements automatically. A principle becomes a gate only after it is validated against the game and has a defined scope. Store rejected hypotheses and counterexamples to prevent negative transfer.

## 5. Evidence and test labels
Allowed statuses: `PASS`, `FAIL`, `BLOCKED`, `NOT_TESTED`, `UNKNOWN_PENDING_READBACK`, `NOT_APPLICABLE`.
Every PASS must state exact artifact SHA/commit, test identity/command, setup/fixture and whether synthetic, expected/observed result, evidence location, reviewer, and independence level.

Test classes: static/source-contract; unit/deterministic simulation; browser integration; real player-driven gameplay; performance/compatibility; visual/audio review; independent product acceptance. These classes are not interchangeable.

## 6. Change transaction
Before a write: record target branch/head, files, expected postconditions, and rollback point. After a write: read back the exact commit and file content. If acknowledgement is lost, classify as UNKNOWN and inspect remote state before retrying. Never blindly replay a non-idempotent write.

## 7. Release authority
The assistant may research, design, implement, test, and prepare a release candidate. It cannot self-certify user satisfaction or claim final acceptance in place of the owner. `READY_FOR_OWNER_PLAYTEST` and `OWNER_ACCEPTED` are distinct statuses.
