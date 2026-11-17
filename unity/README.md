# Unity Production Project

Target editor: Unity 6.3 LTS (exact patch to be pinned after the first editor install). Render pipeline: URP. Language: C#.

This folder will contain the native production project. It is intentionally not populated with unverified placeholder scenes/scripts yet. First create/open the editor project, pin package versions, verify the URP template and build a clean Windows player. Then add runtime modules and assets incrementally.

Required first milestone:
1. Unity project opens without package errors.
2. Clean Windows development build launches.
3. Edit-mode and play-mode tests run in CI.
4. A 4-client network test scene can host/join and exchange authoritative movement/state.
5. Build and test manifests record exact editor/package versions.

The legacy browser game remains in the repository root and on `development`; do not import its monolithic script as the new architecture.
