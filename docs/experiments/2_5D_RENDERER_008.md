# 2.5D Atlas, Static Cache and Reginald Scope — Experiment 008

Date: 2026-11-17
Branch: development
Product commit: 17070bc703b7bd7800b4bb67d6a5c40288a9bfee
Artifact: 717369 bytes
SHA-256: 7c64a2e3b650cfc1b07e314eec6fe07ca1448e791e1ac6198e762cfdfe332cd3
Status: COMPONENT_PASS / NOT_PRODUCT_READY

## Root causes corrected

1. Enemy artwork was not actually active. A later duplicate v2enemy function declaration shadowed the atlas-backed renderer. The 4x4 art atlas existed but gameplay used the older procedural renderer. The shadowing function was removed; only one v2enemy declaration remains.
2. Static scenery was being redrawn every frame. The 480 meadow props and seven ruin landmarks are now rendered once into a 2600x2000 offscreen surface, split into 24 512x512 tiles, and only visible tiles are blitted each frame. Dynamic actors remain depth-sorted.
3. The spell pool violated the one-hero scope. The previous 25-entry array included other wizard Ascension signatures and an unverified placeholder. The active Reginald allowlist is now 18: one signature, three official 1.2 starters, and 14 general spell-quest spells. Research UI, trials, unlock grants, save migration and level-up pool all enforce this set.

## Verification

- Atlas renderer browser regression: 9/9 checks passed, including loaded 1024x1024 atlas, enemy renderer execution, atlas draw calls, 24 cached tiles, no page/console errors and no external requests.
- Reginald scope/save migration browser regression: 13/13 checks passed, including all 18 eligible spell IDs, exclusion of seven non-Reginald entries, exact starter unlocks, UI visibility, legacy save filtering, invalid trial rejection and valid/invalid quest grants.
- Two embedded JavaScript blocks pass node --check.
- Production HTML contains no injected test probe, exactly one v2enemy declaration, no v2buildSprite legacy override and no external runtime assets.
- Normal movement smoke (~14 seconds): 12 kills, XP collected, level 2, upgrade selection visible, HP 100/100, no runtime errors.
- Synthetic stress at 197 active enemies: desktop 1440x900 ~48.7 FPS (p95 frame interval ~33.4 ms); mobile viewport 390x844 ~60 FPS. This is a short headless-browser synthetic benchmark, not a real-device or sustained 19-minute measurement.
- File-origin save persistence could not be tested because the container blocks file:// navigation by administrator policy.

## Open product gates

- Desktop peak-combat performance remains below the 60 FPS target in the synthetic environment.
- No complete 19-minute normal run or natural boss victory has been demonstrated.
- Boss phases, objectives/variants, spell-specific augmentations and all spell effects still need source-by-source acceptance.
- Local file save/reload, real hardware performance, audio quality, art/animation acceptance and owner playtest remain open.
- Product status remains NOT_READY. No merge to main and no release claim.

## Source references

- Official 1.2.0.20127 patch announcement: https://steamcommunity.com/app/2904000/announcements/
- Spell quest catalogue: https://thespellbrigade.wiki.gg/wiki/Quests
- Spell catalogue: https://thespellbrigade.wiki.gg/wiki/Spells
- Reginald: https://thespellbrigade.wiki.gg/wiki/Reginald
- Ascension spell mapping discussion: https://steamcommunity.com/app/2904000/discussions/0/838375062933398814/
