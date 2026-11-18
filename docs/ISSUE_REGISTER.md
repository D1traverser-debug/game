# Issue Register

| ID | Priority | Issue | Evidence | Status | Next action |
|---|---|---|---|---|---|
| WEB-001 | P0 | Only one hero, one realm and solo prototype | Existing HTML baseline | OPEN | Build polished vertical slice, then full roster/realms |
| WEB-002 | P0 | Production 3D renderer not accepted | 2.5D default; raw WebGL2 experimental | OPEN | Same-scene renderer bake-off on real devices |
| WEB-003 | P0 | Online 1–4 player co-op absent | No lobby, WSS authority, reconnect or multi-client tests | OPEN | Implement authoritative rooms and 1/2/3/4-client tests |
| WEB-004 | P0 | Production original art/audio absent | Atlas/procedural visuals and synthesized prototype audio | OPEN | Original character/realm/enemy/animation/VFX/music/SFX pipeline |
| WEB-005 | P0 | Full content inventory unreconciled | Source/community counts conflict | OPEN | Pin source version and content manifest |
| WEB-006 | P1 | Static preview package not CI-verified | Package and artifact job added | CI_PENDING | Verify package hash, manifest and CI artifact |
| WEB-007 | P0 | Browser/device/save acceptance incomplete | Chromium automation only | OPEN | Browser matrix, real-origin persistence, device profiling |
| WEB-008 | P0 | Hosting/operations absent | No deployed frontend/WSS service | OPEN | TLS, monitoring, versioning and rollback |


| WEB-009 | P0 | New modular JS simulation core is not yet integrated | Browser ES modules and 20 contract tests are added alongside the legacy HTML | IN_PROGRESS | Integrate incrementally with behavior-parity tests; retain HTML rollback |
