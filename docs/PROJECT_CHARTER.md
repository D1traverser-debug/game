# Project Charter — Aetherwilds Single-Player

The owner narrowed the project to one complete browser-playable single-player game.

## Product
Original-IP action roguelite with one authored realm, four selectable wizards, automatic spell combat, build crafting, elemental interactions, objectives, escalating enemies, boss encounters and persistent camp progression. Offline-capable static browser delivery. Desktop first; mobile compatibility and touch controls are required.

## Fixed content scope
- Realm: 翠影荒野 / Verdant Wilds. One bounded 2400 × 1800 world, six named districts and seven authored landmarks.
- Playable characters: Aster, Ember, Briar and Nyx. Each has a unique starter spell, passive, active ability, stat profile and in-world appearance.
- Enemies: retain and complete the current seven enemy archetypes and three boss archetypes.
- Gameplay: one complete expedition with objectives, chests, spells, upgrades, boss, victory/defeat, results and camp.
- Persistence: selected character, currency, camp upgrades, unlocks, records and safe migration.

## Explicitly out of scope
Online co-op, WSS rooms, lobbies, invites, multiplayer replication, Unity/native builds, extra realms and expansion rosters. Do not spend implementation time on these unless the owner changes scope.

## Original IP and assets
Keep characters, creatures, environment art, UI, writing, sound and music original. Do not copy proprietary source or extracted commercial assets. Every external asset needs documented commercial-use rights.

## Done means
All four characters are selectable and mechanically distinct; the one realm is bounded, navigable and visually recognizable; the full solo loop works; natural wins and defeats are reproducible; saves survive migration/reload; desktop/mobile browser controls are usable; art/audio are reviewed; and the owner accepts the exact build. CI alone cannot establish READY.
