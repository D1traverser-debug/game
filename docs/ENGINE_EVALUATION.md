# Engine Evaluation — Full-Game Branch

Date: 2026-11-18. Decision D-031 selects Unity 6.3 LTS + URP for a controlled vertical slice, not an irreversible production lock.

## Requirements that changed

The full-game directive now targets 1–4 online co-op, native PC, authored 3D models/rigs/animation, high-density VFX, controller input, adaptive audio and a scalable content pipeline. A single offline HTML file is no longer a viable final delivery contract for this target.

## Options

| Option | Strengths | Risks / costs | Verdict |
|---|---|---|---|
| Keep browser/WebGL prototype | Fast iteration; easy sharing; preserves existing playable artifact | Single-file constraints, network services, high-density 3D asset pipeline and editor workflows become custom engineering; existing renderer has performance limits | Keep as legacy mechanics reference, not production runtime |
| Godot 4.x | Open source; integrated 3D engine; high-level multiplayer API with ENet/WebRTC/WebSocket transports; no engine royalty | Lobby/relay, invites, NAT traversal, production asset tooling and some platform integrations require more custom work; evaluate actual artist workflow | Viable fallback if license/service cost or owner workflow rules out Unity |
| Unity 6.3 LTS + URP | Mature stylized 3D pipeline; Shader Graph/VFX Graph; broad asset and animation ecosystem; native PC/controller pipeline; Unity multiplayer services and NGO | Requires Unity editor/account; package/service versioning and possible service costs; must test real 4-client performance and asset workflow | Selected for vertical-slice validation |
| Unreal Engine | High-end rendering and animation tools; strong PC/console pipeline | Heavier editor/runtime and production overhead for this stylized high-entity-count game; overkill for first slice | Not selected |

## Selected baseline

- Unity 6.3 LTS, URP, C#.
- Use ScriptableObjects for authored content data; keep simulation logic independent from renderer/UI.
- Evaluate Netcode for GameObjects and Unity Lobby/Relay for the first 4-player spike. Keep the transport/session layer abstract so Steam Networking or another provider can be compared without rewriting simulation.
- Use Blender as editable source for original models/rigs; Unity import pipeline for runtime assets.
- Use Unity AudioMixer and event-driven audio initially; add middleware only if a measured requirement justifies it.
- Pin exact editor and package versions only after the first project is opened and package compatibility is verified.

## Vertical-slice falsifiers

Revisit the engine decision if:
1. A four-client session cannot keep host/client state consistent under spell/projectile load.
2. 1080p PC performance cannot meet the agreed target after profiling and reasonable optimization.
3. The artist asset pipeline cannot deliver acceptable character/environment/VFX quality.
4. Build automation or required distribution services are impractical or have unacceptable cost.
5. The owner cannot reasonably install/open/use the editor.

## Current official references

- Unity 6.3 LTS support and support window: https://unity.com/releases/unity-6/support
- Unity 6.3 LTS feature/production notes: https://unity.com/blog/unity-6-3-lts-is-now-available
- Unity Multiplayer services (Lobby, Matchmaker, Relay, Netcode): https://docs.unity.com/en-us/multiplayer
- Netcode for GameObjects compatibility: https://mp-docs.dl.it.unity3d.com/netcode/current/about/
- Godot high-level multiplayer API and ENet/WebRTC/WebSocket: https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html
