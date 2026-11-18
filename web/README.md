# Browser-native simulation core

These dependency-free ES modules are the first production-runtime extraction. They are tested with Node's built-in test runner and can be imported by the browser application.

Current modules: fixed-step clock, PCG RNG, combatant/damage pipeline, event buffer, input validator, projectile simulation and spell casting.

**Integration status:** not yet connected to the legacy root HTML loop. Do not claim gameplay parity until each module is integrated with regression coverage. The root HTML remains the current playable rollback build.
