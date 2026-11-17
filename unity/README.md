# Unity Production Project

**Editor:** Unity 6.3 LTS, minimum pinned patch `6000.3.27f2`  
**Render pipeline:** URP 17.3.0  
**Core package:** local UPM package `com.d1traverser.game-core` from `../src/core`  
**Target:** Windows PC first.

The project skeleton and package manifest are committed. The Editor has not yet been launched against this checkout, so package resolution, generated URP assets, scene import and Windows player build remain NOT_TESTED.

## Open

1. Install Unity Hub and Unity Editor `6000.3.27f2` or a later security-patched 6000.3 LTS patch.
2. Add this repository's `unity/` folder as an existing project.
3. Allow Package Manager to resolve URP and the local Game Core package.
4. Confirm URP 17.3.0 appears in Package Manager. Create a URP Pipeline Asset with Universal Renderer and assign it under Project Settings > Graphics and Quality. Commit the generated pipeline/renderer assets and settings.
5. Install Windows Build Support (IL2CPP) through Unity Hub.
6. Do not add placeholder primitive scenes as finished content. The first scene is part of the production vertical slice and must follow the art bible.

## Structure

- `Assets/Art`: original character, enemy, realm and prop source/imports.
- `Assets/Audio`: original music, SFX, ambience and mix assets.
- `Assets/Scenes`: authored production scenes.
- `Assets/Settings`: URP, quality, input and volume settings.
- `Assets/Prefabs`: production prefabs.
- `Assets/Editor`: validated project tooling.
- `Packages/manifest.json`: pinned dependencies.
- `ProjectSettings/ProjectVersion.txt`: pinned Editor version.

The legacy browser prototype remains outside this project. Do not copy its monolithic script into Unity.
