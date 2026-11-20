# Art and Audio Bible — Aetherwilds Single-Player

## Visual identity
Original magical frontier with a painterly 2.5D presentation, readable silhouettes, restrained material highlights, atmospheric depth and clear combat telegraphs. The single realm is 翠影荒野 / Verdant Wilds: sunlit grove, broken sanctum, moonfen, mossfall, starwell ruins and the central rift.

## Four wizards
- Aster: cool astral blue, star sigils and a luminous orbiting focus.
- Ember: warm ember red/orange, flame crest and heated staff crystal.
- Briar: moss green, leaf/branch motifs and a living ward.
- Nyx: violet shadow palette, crescent motif and a sharp movement trail.

Each needs distinct selection portrait, gameplay tint/silhouette treatment, cast feedback, active-ability effect and damage reaction. Shared sprite reuse is acceptable only when identity remains immediately readable.

## Realm presentation
One bounded map with named districts, seven landmarks, river, bridges, weathered roads, central rift, foliage, ruins and map boundary. The minimap and world navigation must agree with the actual playable coordinates.

## Audio
Original adaptive procedural music with character motifs, looped forest ambience, wizard-specific cast/ability signatures, elemental impacts, player damage, pickups, objectives, boss arrival/stagger, ghost phase, chest and result cues. Independent persistent music/SFX/ambience/UI levels (0–100%) and master mute are exposed in the audio settings screen. The sound engine is fully synthesized in Web Audio and has no external runtime assets. Owner listening review and loudness balance remain release gates.

## Provenance and budgets
No copied commercial character/creature designs, extracted assets or proprietary recordings. Every external asset needs documented commercial-use rights. Bundle assets or serve from controlled origin; no CDN runtime. Current atlas/procedural art and synthesized audio are prototypes until visually and aurally reviewed by the owner.


## Original wizard identity pass — 2026-11-19 candidate

- Added a bespoke original-IP 4×4 wizard action atlas, 384×384 AVIF with alpha. Each cell is 96×96; rows are Aster, Ember, Briar and Nyx; columns are idle, walk, cast and ability.
- The art was generated for this project rather than extracted from the commercial reference game. The generated checkerboard was removed by edge-connected neutral-background masking; the resulting transparent atlas is embedded into the offline HTML by `scripts/build_game.py`.
- Character selection portraits and in-world player rendering now use the same character-specific source art. Runtime pose selection follows actual movement, cast pulse and ability pulse. Facing, ghost alpha, hurt flash and camera-scale readability remain renderer-controlled.
- Added deterministic character-specific orbiting motes and action rings: Aster star sparks, Ember cinders, Briar leaves and Nyx shadow crescents. Motion derives from the visual clock, not gameplay RNG.
- This closes the shared-base-body implementation gap for the current 2D atlas renderer. It does not constitute a final rig/animation acceptance: sprite silhouette, readability at normal gameplay scale, attack-pose clarity and frame pacing still require browser and owner review.

## Adaptive audio identity pass — 2026-11-19 candidate

- Replaced the shared index-based lead phrase with four character-specific interval motifs while retaining the existing harmonic pad, bass pulse, percussion, boss tension layer and independent volume controls.
- Added sparse, deterministic forest bird-call phrases to the ambience channel. They respect the ambience slider and master mute, and do not advance gameplay RNG.
- Music and ambience remain procedural Web Audio, not recorded production stems. Mix translation, loudness, fatigue, headphones/speakers and owner listening acceptance remain open.


## Environment atmosphere and spell-impact presentation — 2026-11-20 candidate

The 2.5D renderer adds deterministic moving river highlights, world-anchored pollen/fireflies, a three-frame film-grain overlay and layered beam/slash/burst/ring impacts. These effects use render time and coordinate hashes only; they do not consume gameplay RNG or add runtime network assets. The environment visual regression checks visible output, temporal variation, render-path wiring, offline behavior and runtime errors. This is an original atmospheric treatment, not source-game asset parity or owner acceptance.


## Original creature and boss identity pass — 2026-11-20 candidate

- Replaced the shared enemy-atlas body presentation with seven original, cached 2D creature silhouettes: Crawler, Sprout, Ranged Wisp, Buffer, Shield Crab, Gnasher and Crabladon.
- Each archetype has five pre-rendered action poses (idle, two alternating locomotion frames, attack and hurt). State-driven rendering selects the pose; status overlays preserve readable freeze, burn, corruption and elite feedback.
- Rebuilt the three boss silhouettes as distinct original forms: Sol'phish (abyssal leviathan), Krog'wa (armoured amphibian) and Mul'gath (multi-headed void hydra). Mul'gath's visible head count follows the actual boss phase state; Krog'wa's tongue-smash telegraph changes the boss pose.
- Creature shapes are generated locally with Canvas paths and gradients, cached once, and remain offline. Presentation animation is deterministic and does not consume gameplay RNG.
- This is an original 2D art substitute, not a claim of source-game 3D asset or rig parity. Gameplay-scale readability, frame pacing, colour-blind/status contrast, physical-device performance and owner visual acceptance remain open.
