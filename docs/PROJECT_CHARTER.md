# Project Charter — Full-Game Production

## Product

Create a complete, independently branded, premium-quality 3D co-op survivors-like roguelite. The Spell Brigade is the gameplay reference, not the shipped IP. The target is a credible substitute in moment-to-moment gameplay depth and content breadth, with original characters, world, art, audio, writing, UI expression, and identity.

## Owner directive (2026-11-18)

The previous one-wizard / one-realm / single-player / single-HTML restrictions are superseded on the `full-game` branch. They remain applicable only to the archived browser prototype.

## Product target

- Modes: solo and 1–4 player online co-op.
- Platform: Windows PC first; keyboard/mouse and controller. Steam is a distribution target. Additional platforms and cross-play are post-PC gates.
- Content: complete current-version roster and systems, with the exact count/version pinned before each content batch.
- Gameplay reference inventory (provisional): 15 wizards, four realms, five primary elements plus fifteen advanced infusion candidates (disputed against a seven-identity/ten-combo community summary), spells/augmentations, scrolls, objectives/variants, enemies/bosses, quests, trials/covenants, enchantments/masteries, achievements and meta progression. These figures are research targets, not source-verified acceptance facts.
- Engine direction: Unity 6.3 LTS + URP, subject to vertical-slice validation.

## Gameplay fidelity

Reproduce the observable mechanics and interaction rules independently: automatic spell casting, targeting, movement, XP/level-up, spell slots and levels, elemental infusion and combinations, augmentation/scroll choices, friendly fire, objectives, enemy behaviors, boss phases, revives, co-op synergies, difficulty, trials/covenants, and persistent progression. Source version and confidence must be recorded per mechanic. Where the original's exact numbers or behavior are unknown, label the implementation an adaptation rather than presenting it as fact.

## Original-IP boundary

- May independently implement gameplay mechanics, rules, and high-level design patterns.
- Must not copy proprietary source code, extracted game data/assets, original character/creature designs, models, textures, animation, fonts, logos, UI art/layout expression, dialogue, lore text, music, voice, or sound recordings.
- Create an original title, world, cast, visual language, soundtrack, sound library, UI and narrative.
- Third-party assets/tools require documented commercial-use license, attribution obligations, provenance and source-file retention. No unlicensed scraped assets.
- Do not use the original game's title/logo in the shipped product. Reference names may appear in internal research documents only.

## Quality intent

A premium stylized 3D presentation: authored character silhouettes and rigs, responsive animation, detailed biome kits, layered lighting/materials, readable spell VFX, boss telegraphs, high-quality UI, responsive camera, and a coherent original audio identity. "Top-studio quality" is an acceptance target to be demonstrated by a polished vertical slice, not a claim based on generated asset quantity.

## Definition of Done

1. All P0/P1 requirements are source-qualified and accepted.
2. Solo and 1–4 player online co-op complete the core run loop.
3. Full current-version content scope is implemented or explicitly version-scoped.
4. Every spell, element, augmentation, enemy, objective, boss, realm and wizard has a content card, tests, audiovisual review and live-play evidence.
5. Real full-run victories and defeats are player-driven, not forced.
6. Network sessions survive join/leave, latency, reconnect, revive, pause/level-up and host disconnect cases within the documented design.
7. Save/load, migrations, corruption recovery and unlock progression pass real builds.
8. Performance targets pass on frozen reference PCs under representative peak load.
9. Art, animation, VFX, UI and audio pass independent quality review.
10. Asset provenance and licenses are audited.
11. Owner and independent playtests have no blocking issues.
12. Exact native release builds are reproducible, versioned, hashed, and rollbackable.
