# Project Charter — Aetherwilds

The owner selected a complete browser-playable website as the delivery target. Unity/native delivery is superseded.

## Product
Original-IP action roguelite with automatic spell combat, build crafting, elemental interactions, objectives, escalating enemies, boss encounters and co-op. Modes: solo and 1–4 player online co-op. Desktop browsers first; mobile browser compatibility. Keyboard/mouse, controller and touch. Static web frontend plus separate authoritative WSS room service.

## Presentation
Target WebGL2 3D world with DOM UI. Keep the 2.5D fallback until the 3D renderer passes visual and physical-device acceptance. Compare raw WebGL2 and bundled Three.js on the same scene. No CDN runtime.

## Scope
Current browser prototype is one hero, one realm and solo only. Full-game scope includes the complete source-version wizard roster, four realms, spells, elements/infusions, augmentations, enemies, bosses, objectives, scrolls, quests, trials/covenants and meta progression. Inventory counts remain provisional until reconciled against a pinned source version.

## Original IP
Do not ship copied proprietary source, extracted game data/assets, exact character/creature designs, original art/animation, fonts, UI expression, writing, music or recordings. Gameplay patterns may be independently researched and implemented. Every third-party asset needs documented commercial-use rights.

## Done means
Natural solo wins/defeats; real 1/2/3/4-player authority/reconnect/revive tests; complete version-scoped content; reliable saves/migrations; desktop/mobile browser performance; original production art/audio with provenance; hosted deployment/monitoring/rollback; owner and independent acceptance. CI or screenshots alone cannot establish readiness.
