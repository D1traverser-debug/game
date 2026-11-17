# Game.Core

Engine-independent deterministic simulation kernel for the full-game project.

Target: .NET Standard 2.1 so the assembly can be referenced by Unity 6.3 LTS. The core must not reference UnityEngine, rendering, audio, UI, networking providers, wall-clock APIs or global random state.

Initial scope:
- Fixed-step simulation clock with explicit pause semantics and preserved backlog.
- Seeded PCG random stream for gameplay only.
- Central damage gate with configurable friendly-fire/self-damage policy and invulnerability.
- No armor formula or exact damage scaling is frozen until source-version research supports it.

Run tests:
```bash
dotnet build src/core/Game.Core.csproj --configuration Release
dotnet run --project tests/core/Game.Core.Tests.csproj --configuration Release
```

This is foundational code, not a playable game or proof of source fidelity.
