# Network Architecture — 1–4 Player Co-op

Status: design baseline; implementation NOT_STARTED.

## 1. Target

Support solo and 2–4 player online co-op. The game is a high-entity-count action roguelite with friendly fire, revives, shared objectives and frequent spell/element events. Network correctness must be designed into simulation from the first vertical slice.

## 2. Authority model

- Host-authoritative session for the first release.
- Host owns run clock, RNG stream, enemy AI, objective state, boss state, collision/damage, drops, shared world events and authoritative progression results.
- Clients send input intent and validated player actions. They do not authoritatively set position, HP, damage, cooldown, inventory, unlocks, RNG or victory.
- Clients predict local movement where useful and reconcile against host snapshots.
- Remote players/enemies use interpolation; latency-sensitive feedback may be predicted cosmetically but must be corrected by authority.
- Rendering, camera shake, particles and audio never consume the gameplay RNG stream.

## 3. Replication strategy

The engine-independent core now defines a host-side player-command envelope validator and an immutable, monotonic simulation event buffer. The validator checks player membership, sequence order, tick window, finite bounded movement and known input bits. Transport adapters must still authenticate the session member and serialize/deserialize safely; the core validator does not replace transport security.

Replicate compact events for discrete changes (spell cast, projectile spawn, hit, status application, objective progress, revive, boss phase) and snapshots/deltas for continuous state. Pool networked entities and use interest/visibility rules only where they preserve gameplay correctness. Measure bandwidth before choosing update rates.

## 4. Session and transport

- First spike: compare Unity Netcode for GameObjects with Unity Lobby/Relay and a Steam-oriented transport option.
- Hide provider-specific APIs behind `ISessionService` / `INetworkTransport` abstractions.
- Session requirements: create/join/invite, ready state, character selection, load synchronization, start, disconnect, reconnect, host departure, end-of-run results.
- No public matchmaking commitment until private invite sessions are reliable.

## 5. Gameplay edge cases

- Friendly fire: define owner attribution, self-damage, teammate damage, status transfer, kill credit and damage recap.
- Revive: authoritative timer, interruption rules, invulnerability/respawn semantics and reconnect behavior.
- Level-up/upgrade: decide pause or slow-time semantics for all players; no client may independently roll a different authoritative option pool.
- Objectives: define shared vs per-player progress, simultaneous interactions and disconnect mid-objective.
- Bosses: host owns phase, telegraph, hitbox, stagger and vulnerability; all clients render the same attack instance/geometry.
- Player death/leave: define whether a dead/left player can return and how run rewards are allocated.
- Pause: online pause is a session vote or host-controlled rule, not a local freeze of only one client.

## 6. Required test matrix

- 1, 2, 3 and 4 clients on LAN and internet/relay.
- 0/50/100/150/250 ms latency; packet loss and jitter profiles.
- Host and client death, revive, disconnect, reconnect and quit at every run phase.
- Simultaneous level-up, objective completion, chest opening and boss phase transition.
- Friendly-fire damage, kill attribution, status stacking and projectile ownership.
- Host loss and migration policy.
- Deterministic replay or authoritative event log for desync diagnosis.

## 7. Security and integrity

Treat all client payloads as untrusted. Validate input rates, movement envelopes, action cooldowns, IDs, ownership and session membership. Never accept client-supplied final damage, loot, quest completion or victory state.
