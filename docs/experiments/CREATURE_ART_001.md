# Creature Art Integration 001

Date: 2026-11-20
Base: work/production-environment-vfx-001 at 4ac13f24a116f6fa64e389c8da3309e4a838fa3a
Candidate: work/production-creature-art-001
Status: automated CI PASS on 2026-11-20; owner visual/gameplay acceptance pending.

## Problem

The 2.5D renderer used atlas IDs for all seven ordinary enemy archetypes and all three bosses. The player/wizard identity pass had become bespoke, but enemy and boss silhouettes still depended on the shared atlas illustration. This left a material presentation gap at the normal gameplay camera distance.

## Implementation

- Seven original Canvas-drawn enemy designs: crawler, sprout, ranged, buffer, shield, gnasher and crabladon.
- Five cached poses per archetype: idle, alternating walk A/B, attack and hurt.
- State-driven selection for chase, attack, leap, burrow and hit feedback; freeze, burn, corruption and elite overlays remain separate.
- Three original boss designs: Sol'phish abyssal leviathan, Krog'wa armoured amphibian and Mul'gath multi-headed void hydra.
- Mul'gath's head count is bound to the existing phase/headCount state. Krog'wa's tongue-smash pose is bound to the existing attack ID/stage.
- The sprite cache is built once and reused; visual animation uses render time and deterministic coordinate phase only.

## Invariants

- No enemy HP, damage, speed, spawn timing, archetype selection, boss phase, attack telegraph or objective behavior was intentionally changed.
- No gameplay RNG call sites were added or consumed by rendering.
- No external runtime requests or new runtime dependencies.
- The existing atlas remains available for non-creature props and other legacy art.
- Product remains NOT_READY. The vector renderers are an original 2D substitute, not a claim of source-game 3D model/rig parity.

## Verification

tests/creature_art_regression.py is added to the required browser-content-visual CI matrix. It checks all seven enemy silhouettes, five action poses, animated frame variation, all three boss silhouettes, Mul'gath phase/head growth, Krog'wa tongue-smash telegraph, no runtime errors and offline operation. tests/art_renderer_regression.py additionally checks that the live game builds and draws the seven-archetype cache.


## Initial CI failure and test-harness correction

CI run `44652465370` reached the game successfully but failed two visual jobs. The creature-art test attempted to call module-scoped `v2buildCreatureCache` from the page's global evaluation scope; the function was available only inside the injected module closure. The live renderer test still required `v2sprite` calls for enemies, although the new bespoke renderer intentionally uses cached creature canvases. These were test-oracle mismatches, not evidence of a runtime renderer failure.

The probe now builds the cache through `window.__creatureProbe.cache()`. The live renderer test instruments the actual cached creature `ctx.drawImage(sprite, ...)` call and no longer requires obsolete generic-atlas draws. Production gameplay, RNG and balance code were not changed.

## CI result

GitHub Actions run `44653857044`, commit `df507720bfb678993a9f54f7e0cb1697a8f81e0f`: **27/27 jobs passed**. The exact reproducible offline HTML is 857515 UTF-8 bytes, SHA-256 `ee959e218fc95cdeb65274c3ac953ddcae7b10a8f10bbb5f6fc734ca0ad33e23`. The creature visual regression passed all seven archetypes, five cached poses each, three distinct bosses, Mul'gath phase/head growth, Krog'wa tongue-smash, no runtime errors and offline operation. The four-wizard natural-run gate passed 4/4.

This is automated CI evidence only. Normal-scale readability, human playtesting, owner visual acceptance, physical-device performance, full source-game 3D parity and full source-version fidelity remain open. Product remains `NOT_READY`.
