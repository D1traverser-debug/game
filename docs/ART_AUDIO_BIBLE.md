# Art & Audio Bible — Original-IP Production Direction

Status: direction baseline for concept development; not final art approval.

## 1. Creative objective

Create a distinctive, premium stylized 3D fantasy world with the readability and spectacle required by a top-down survivors-like game. Do not imitate the reference game's exact models, palette, silhouettes, UI, icons, animations or sound. Build an original identity that remains legible when four players, dozens of spells and large enemy groups occupy the screen.

## 2. Visual pillars

1. **Hand-authored silhouettes:** every hero and enemy reads at gameplay camera distance; signature props and spell poses distinguish characters instantly.
2. **Material richness without visual noise:** stylized PBR surfaces, hand-painted detail, controlled roughness/metalness, selective emissive materials and clear focal hierarchy.
3. **Elemental spectacle with rules:** every primary element and advanced infusion has a unique shape language, motion, color family and sound signature; pair combinations blend both identities rather than merely recoloring a projectile.
4. **Battlefield legibility:** telegraphs, damage zones, ally spells, enemy attacks and pickups remain distinguishable under peak density.
5. **A coherent world:** realm architecture, vegetation, props, lighting, sky, ambient particles and music tell one story.

## 3. Candidate art direction

A distinct "astral frontier / enchanted expedition" identity:
- Heroic silhouettes with tailored expedition robes, layered fabrics, crafted spell instruments and readable accessories.
- Environments with oversized natural forms, ancient magical infrastructure, weathered stone, luminous flora and atmospheric depth.
- Rich but disciplined color grading: grounded world colors; strong, reserved elemental accents; clear enemy-danger contrast.
- Hand-painted stylized PBR, soft stylized shadows, authored highlights, controlled bloom and subtle atmospheric perspective.
- Camera: oblique/orthographic top-down, tuned for readability rather than cinematic occlusion.

This is a candidate direction. The next art review should compare at least three genuinely different moodboards before locking it.

## 4. Character asset standard

Each playable hero requires:
- Original concept sheet: front/side/back, expression, costume/material callouts, palette and silhouette.
- Production mesh with clean topology, UVs, authored materials and sensible LODs.
- Rig with facial/upper-body controls where useful.
- Gameplay animation set: idle, locomotion, turn, cast, hit, knockback, dodge/ability, death, revive and victory.
- Signature spell animation hooks and character-specific VFX/SFX.
- Thumbnail/portrait, selection pose, UI iconography and localization-safe labels.
- Source .blend, exports, textures, rig/animation source and provenance manifest.

## 5. Enemy and boss asset standard

Every archetype needs a distinct silhouette, locomotion, attack anticipation, active attack, recovery, hit reaction, stagger, death, drop/loot response and audio set. Bosses require authored intro/outro, phase transitions, telegraphs aligned to hitboxes, arena interactions and readable vulnerability windows.

## 6. Realm asset standard

Each realm is a modular kit, not a repeated plane with color swaps:
- Terrain materials, paths, cliffs/edges and traversal boundaries.
- Modular rocks, trees, flora, structures, ruins, props and destructibles.
- Unique lighting/sky/fog/ambient VFX and soundscape.
- Unique hazards and traversal interactions.
- Map variants that change routes and combat space while preserving objective reachability.
- Baked/static lighting where useful; dynamic lights reserved for gameplay readability.

## 7. Spell VFX standard

Each spell has a full lifecycle: cast cue → travel/telegraph → impact → damage feedback → status/element interaction → fade/cleanup. Each elemental infusion must be visually distinct and readable at a glance. Pair combinations must communicate both source elements and the resulting gameplay effect.

VFX budgets must be explicit: per-camera particle limits, GPU/CPU particle choice, overdraw limits, transparency discipline, pooling, culling and quality tiers. The four-player peak scene is the acceptance target, not an empty test arena.

## 8. UI standard

- Original visual language and icon system; do not trace the reference UI.
- Strong typography hierarchy and scalable layout for 16:9, ultrawide and controller navigation.
- High-contrast state communication for HP, XP, objective, spell slots, level-up choices, danger and ally damage.
- Clear focus states, keyboard/controller navigation, remapping, subtitles where relevant, scalable text and color-accessible cues.
- Avoid generic unstyled panels and placeholder glyphs in accepted builds.

## 9. Audio identity

Create an original score and sound library:
- Main menu/camp identity.
- A layered exploration/combat score per realm.
- Adaptive intensity layers driven by enemy pressure, objective state, boss phase and player count.
- Dedicated boss encounter and victory/defeat cues.
- Unique cast, travel, impact, loop, status and end-of-life SFX for each spell.
- Elemental status and pair-interaction SFX.
- Enemy locomotion, attack, hit, stagger, death and ambient vocalizations.
- UI navigation, selection, reroll, level-up, objective completion, revive and reward cues.
- Environmental ambiences, weather and realm-specific one-shots.

Mix rules:
- Level-up/important UI events can duck music without cutting gameplay audio.
- Threat cues must remain audible but never become fatiguing.
- Friendly-fire and ally-hit cues must be distinguishable from enemy-hit cues.
- Music, SFX, ambience, UI and voice (if later added) have independent mix controls.
- Setting SFX to zero must produce true silence from the SFX bus.
- Deliver editable masters (WAV, 48 kHz/24-bit target) and runtime-optimized formats with loop metadata and loudness notes.

## 10. Asset provenance

Every asset has: unique ID, source project, author/tool, creation date, license/provenance, allowed platforms, attribution requirements, editable source path, export settings, hash, runtime references and review status. Generated assets also require human review and rights/provenance checks. No ripped, scraped or unlicensed material.

## 11. Acceptance

Art/audio acceptance is performed in motion at normal speed and peak four-player combat density. A static beauty render is insufficient. Review silhouette readability, animation quality, VFX clarity, UI hierarchy, mix balance, performance cost and overall identity.
