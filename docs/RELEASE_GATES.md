# Release Gates — Browser Game

Product remains NOT_READY until all gates pass on the exact hosted build.

1. WEB_PACKAGE: reproducible static frontend, byte-identical output, manifest, no CDN runtime.
2. BROWSER_MATRIX: desktop Chromium/Firefox/WebKit and physical mobile Safari/Android Chrome.
3. GAMEPLAY: natural solo victory/defeat and complete core loop; no forced state mutation.
4. CONTENT: complete source-version inventory implemented or explicitly version-scoped.
5. ART_AUDIO: original production-quality characters, environments, animation, VFX, UI, music and SFX with provenance.
6. NETWORK: real 1/2/3/4-client WSS sessions; authority, latency/loss, reconnect, revive and boss tests.
7. PERFORMANCE: frozen desktop 60 FPS and mobile 30 FPS targets under representative peak load.
8. PERSISTENCE: versioned saves, migrations, corruption recovery, backup/export and reload on real origin.
9. OPERATIONS: deployed frontend/room service, TLS, monitoring, versioning and rollback.
10. ACCEPTANCE: owner and independent reviewers accept the exact hosted release candidate.

CI, packaging, screenshots or documentation alone cannot mark READY.
