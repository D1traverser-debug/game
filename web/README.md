# Browser-native simulation core

These dependency-free ES modules are tested with Node's built-in test runner and packaged with the static browser game.

Current modules: fixed-step clock, PCG RNG, combatant/damage pipeline, event buffer, input validator, projectile simulation and spell casting.

**Integration status:** the live browser runtime imports the fixed-step clock and routes final player/enemy health application through the modular damage pipeline. The canonical PCG-XSH-RR module is embedded into the offline HTML by `scripts/build_game.py`; per-run RNG now owns objective selection/generation, while static collision-bearing world decoration uses a separate fixed, versioned world-layout stream. Render camera shake and procedural audio remain isolated from the per-run stream. Enemy director, combat, loot, spell, chest and boss random call sites remain on legacy randomness until separately migrated. Projectile, spell, event-buffer and input-validation modules remain standalone contracts. The legacy HTML game remains the canonical playable runtime.
