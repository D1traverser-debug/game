# Online Co-op Architecture — Browser 1–4 Players

Status: design baseline; implementation NOT_STARTED.

Use secure WebSockets and an authoritative room process. The room owns simulation tick, RNG, player state, enemy AI, projectile collision, damage/status, drops, objectives, boss phases, revives and results. Clients send validated movement/action intent only; never authoritative HP, damage, loot or victory.

Flow: short-lived session token → private room/invite code → 1–4 player lobby → protocol/content negotiation → ready check → run → results. Reconnect uses a short-lived token and authoritative snapshot. Host departure does not transfer authority to an untrusted client.

Messages include protocolVersion, roomId, playerId, sequence, clientTick and type. Validate membership, monotonic sequence, tick window, rate, finite bounded movement, allowed buttons, cooldown/action cadence and state transitions.

Tests: 1/2/3/4 clients; 0–250 ms latency/loss; reconnect during lobby/combat/level-up/boss; friendly fire, revive, simultaneous objectives/chests, player leave/death, boss transitions, server restart and mobile network handoff. Treat all client payloads as untrusted.
