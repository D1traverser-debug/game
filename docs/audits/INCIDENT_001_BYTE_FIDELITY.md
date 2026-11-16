# INCIDENT-001 — Exact HTML Byte Fidelity Lost During Initial Import

Date: 2026-11-16
Severity: P1 repository provenance / test integrity defect
Status: SOURCE_RESTORED / CI_RECHECK_PENDING

## Observed failure
The initial GitHub Actions checkpoint job failed even as the browser-component job succeeded. The GitHub runner checked out a 119416-byte development HTML (SHA-256 626baac0d1818bfb089fcc87d2b4158561cc1ad9a0f5e1fcf1578fe3f8156e2b), whereas the locally tested candidate and the canonical PROJECT_STATE.json expected 119417 bytes (SHA-256 e97ed8770523034ddc71d590a4a7cc3444e8c87811a44f4298910a65597b5190).

GitHub job evidence: https://github.com/D1traverser-debug/game/actions/runs/43838276612

## Root cause
The previous upload path reconstructed HTML text from a parsed Files read via content.join(''). The parser omitted the final LF byte of the uploaded HTML. The GitHub connector then correctly committed the byte-shorter text, so the code was semantically unchanged but was not byte-identical to the local tested artifact.

L0: hash gate fails.
L1: final LF missing in committed index.html.
L2: tool-mediated parsed content had been treated as exact source bytes.
L3: artifact write path lacked post-commit byte-size/SHA validation.
L4: audit prematurely labeled a normalized text comparison as exact provenance.
L5: the engineering process lacked a negative-control proof that text materialization preserves trailing bytes; CHECKPOINT test exposed the flaw after publication to development.

## Alternatives and decision
- A. Change PROJECT_STATE.json to match the silently truncated remote file: rejected because it would normalize a transport-induced source modification and leave false "exact import" claims.
- B. Restore missing LF in both main baseline and development candidate, preserve hashes from the original local artifacts, read back GitHub files, rerun CI: selected.
- C. Stop storing HTML through GitHub connector: unnecessary; the connector faithfully stores supplied UTF-8 bytes. The defect was the parsed-source reconstruction step.

## Actual writes and readbacks
- Main (original 116721 bytes, SHA-256 c14e0f3210320453b0b81b6d49fbd55ae372cf36cfe99a91902d089b8672ef3a): LF restored in commit eace4cb66f282d35c663f3a13d6e39ff8a15e0b8.
- Development (119417 bytes, SHA-256 e97ed8770523034ddc71d590a4a7cc3444e8c87811a44f4298910a65597b5190): LF restored in commit 44938fb8557a856d794e7a0ceff45ccd71faedeb.
- Both GitHub fetch_file readbacks returned the full reconstructed content, including a trailing newline.

## Learned invariant
No byte-identity claim may be based solely on text-parser line joining, names, character count or Git blob presence. Use the actual runtime bytes, exact SHA-256 and remote readback. Keep a negative test where one byte is added/removed and the checkpoint gate must fail. Preserve source/version provenance after a write.

## Acceptance boundary
The actual CI run after these corrections must be read, not assumed successful. Even if the checkpoint and browser component tests pass, game status stays NOT_READY until player outcome, visual fidelity, performance, save, boss and quality acceptance.
