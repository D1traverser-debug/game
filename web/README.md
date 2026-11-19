# Browser-native simulation core

These dependency-free ES modules are tested with Node's built-in test runner and packaged with the static browser game.

Current modules: fixed-step clock, PCG RNG, combatant/damage pipeline, event buffer, input validator, projectile simulation and spell casting.

**Integration status:** the live browser runtime imports the fixed-step clock and routes final player/enemy health application through the modular damage pipeline. RNG, projectile, spell, event-buffer and input-validation modules remain standalone contracts until they are integrated with behavior-parity tests. The legacy HTML game remains the canonical playable runtime.
