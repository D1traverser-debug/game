# PROGRESSION-002 — Unlock Integrity and Spell-Slot Integration

Date: 2026-11-16
Artifact: development/index.html
Implementation commit: 656881540ec26c5d60a580baa2ac42ac21128595
Artifact SHA-256: a4fe8215c491d2139f8345a8f331482cf9d399a9a5d59742b348a08d32f85095
Artifact bytes: 121294
Product verdict: NOT_READY

## Owner outcome being advanced
Recreate The Spell Brigade in a standalone HTML browser game with Reginald and Verdant Meadow only. Progression and unlocking must match the original, rather than a random-card imitation.

## Confirmed source facts
- Official 1.1 update: third spell slot at player level 13, fourth at level 20; when acquiring a new spell the player may immediately choose an Upgrade; new 3rd/4th spells immediately begin at spell levels 3/4. https://steamdb.info/patchnotes/25079940/
- Official 1.2 patch 1.2.0.20127: Loaded Dice, Tiny Tremors, Wicked Buzzsaw are available from the start. https://steamcommunity.com/app/2904000/announcements/
- The original quest page describes spell-specific achievements. A cumulative kill-count threshold is not a valid replacement. https://thespellbrigade.wiki.gg/wiki/Quests

## Changes in this development candidate
1. Replaced unconditional full-spell unlock assignment with explicit versioned save normalization. Initial unlocked spells: Astral Orbs, Loaded Dice, Tiny Tremors, Wicked Buzzsaw.
2. Old version 1 saves that were previously contaminated by blanket unlocks reset the untrusted unlock list to known starters plus explicitly recorded quest flags, while retaining currencies, run counts, statistics, and enchantments.
3. Removed the fabricated progressive kill-count unlock mechanic and its incorrect UI claims. The research screen now displays quest-specific descriptions only where source evidence exists; unimplemented event trackers do not falsely unlock content.
4. Added a player-level spell-slot gate: maximum 2 before level 13, 3 at 13, and 4 at 20; the second-slot threshold remains a documented temporary level-2 assumption, **NOT** a verified original-game fact.
5. Offered a new spell reliably once a slot is available instead of rolling a 27% chance at every level.
6. New third/fourth spells start at spell levels 3/4 and invoke a dedicated immediate upgrade choice.
7. Added the three 1.2 spells with distinct baseline attack loops: a face-scaled delayed Dice explosion, four sequential mini-quakes, and a tracking buzzsaw projectile. These are rough behavior scaffolds, not faithful full implementations or verified source numbers.
8. Preserved the original single-file HTML delivery.

## Verification
- JavaScript extracted from this exact candidate: node --check => PASS.
- Chromium 144 with Playwright set_content and temporarily injected probe (not added to shipped artifact) => 17/17 targeted regression checks PASS.
- Checks: starter unlocks; schema migration; initial hero; slot level boundaries; no 3rd at 12; 3rd at 13; free upgrade; no 4th at 19; 4th at 20; free upgrade; Dice/Tremors/Buzzsaw attack scaffolds; legacy save migration under mock; no page errors.
- Additional browser smoke: menu, start, keyboard, pause/resume, mobile menu, mobile HUD, touch joystick visible and no horizontal overflow => PASS; no page exceptions.
- Browser sandbox blocks URL navigation including localhost. Thus the browser tests use set_content and explicitly mocked localStorage for migration. **Actual file:// open and real close/reopen persistence are NOT_TESTED.**

## Outstanding critical fidelity gaps
- Second spell-slot timing not source verified.
- The three new spells' exact numbers, VFX, sound and all four individual augmentations each are not complete.
- Existing quest-specific unlock challenges lack event trackers and cannot yet be earned.
- Source-derived infusion pairing, augmentation pools, enemy AI, objectives, boss roster and full solo metagame remain incomplete.
- Full player-driven 19-minute victory and boss mechanics remain unverified.
- 3D renderer remains a separate experiment; active gameplay is still on the Canvas 2D baseline.
- The production HTML still contains a query-gated test API; must be stripped from release build.
- Visual quality, audio quality, performance, device testing, player acceptance and public deployment are not accepted.

## Risk / rollback
Main remains at c7980a12e582cf3c265b8bbdaf1e7f16eecfcd6b as the previous playable baseline. This candidate is on development only; do not merge until a verified core-loop and current-version content acceptance path is established.

## Next goal-causal action
Build the versioned spell quest/event contract and all three new spells' exact augmentations; run negative mutations against unlock and slot gates. In parallel, continue the 3D WebGL renderer quality/performance work. Do not substitute tests/docs for the complete playable game.
