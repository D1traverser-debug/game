"""Regression for the canonical atlas-backed 2.5D enemy renderer.

The test injects diagnostics into an in-memory copy only. No debug API ships.
"""
import asyncio
import re
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")


def instrument(source: str) -> str:
    marker = "// Production build: internal debug mutations are test-only and not shipped."
    assert source.count(marker) == 1
    assert len(re.findall(r"function\s+v2enemy\s*\(", source)) == 1
    assert "function v2buildSprite" not in source
    assert "const V2_SPRITES" not in source
    assert source.count("function buildDecorCache(decor)") == 1
    assert "buildDecorCache(game.decor)" in source
    old = "function v2enemy(e){"
    assert source.count(old) == 1
    source = source.replace(old, "function v2enemy(e){window.__enemySpriteRenders=(window.__enemySpriteRenders||0)+1;window.__creatureSpriteDraws=(window.__creatureSpriteDraws||0)+1;", 1)
    probe = r"""
window.__atlasSpriteDraws=0;
const __originalV2Sprite=v2sprite;
v2sprite=function(...args){window.__atlasSpriteDraws++;return __originalV2Sprite(...args)};
window.__wizardSpriteDraws=0;
const __originalWizardSprite=v2wizardSprite;
v2wizardSprite=function(...args){window.__wizardSpriteDraws++;return __originalWizardSprite(...args)};
window.__artProbe={snapshot:()=>({screen,atlasComplete:V2_ATLAS.complete,atlasWidth:V2_ATLAS.naturalWidth,atlasHeight:V2_ATLAS.naturalHeight,wizardAtlasReady:V2_WIZARD_ATLAS_READY,wizardAtlasWidth:V2_WIZARD_PACK.naturalWidth,wizardAtlasHeight:V2_WIZARD_PACK.naturalHeight,mode:save.renderMode,enemies:game?.enemies.filter(e=>!e.dead).length||0,enemySpriteRenders:window.__enemySpriteRenders||0,atlasSpriteDraws:window.__atlasSpriteDraws||0,wizardSpriteDraws:window.__wizardSpriteDraws||0,cacheTiles:V2.decorTiles?.length||0,creatureCacheTypes:V2_CREATURE_CACHE?Object.keys(V2_CREATURE_CACHE).length:0,creatureSpriteDraws:window.__creatureSpriteDraws||0})};
"""
    return source.replace(marker, probe + "\n" + marker)


async def main():
    report = {"checks": {}, "page_errors": [], "console_errors": [], "external_requests": []}
    async with async_playwright() as p:
        launch = {"headless": True, "args": ["--no-sandbox", "--enable-webgl", "--ignore-gpu-blocklist"]}
        if shutil.which("chromium"):
            launch["executable_path"] = shutil.which("chromium")
        browser = await p.chromium.launch(**launch)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
        page.on("console", lambda m: report["console_errors"].append(m.text) if m.type == "error" else None)
        page.on("request", lambda r: report["external_requests"].append(r.url) if r.url.startswith(("http://", "https://")) else None)
        await page.set_content(instrument(SOURCE), wait_until="load")
        await page.wait_for_timeout(1000)
        report["checks"]["menu_visible"] = await page.locator("#start").is_visible()
        await page.locator("#start").click()
        await page.wait_for_timeout(2200)
        state = await page.evaluate("__artProbe.snapshot()")
        report["state"] = state
        report["checks"]["entered_play"] = state["screen"] == "playing"
        report["checks"]["atlas_loaded"] = state["atlasComplete"] and state["atlasWidth"] == 1024 and state["atlasHeight"] == 1024
        report["checks"]["enemies_spawned"] = state["enemies"] >= 8
        report["checks"]["creature_renderer_called"] = state["enemySpriteRenders"] > 0
        report["checks"]["atlas_sprite_draws_occurred"] = state["atlasSpriteDraws"] > 0
        report["checks"]["seven_archetype_creature_cache_ready"] = state["creatureCacheTypes"] == 7
        report["checks"]["creature_sprite_draws_occurred"] = state["creatureSpriteDraws"] > 0
        report["checks"]["original_wizard_atlas_loaded"] = state["wizardAtlasReady"] and state["wizardAtlasWidth"] == 384 and state["wizardAtlasHeight"] == 384
        report["checks"]["original_wizard_sprites_rendered"] = state["wizardSpriteDraws"] > 0
        report["checks"]["static_meadow_cache_baked"] = state["cacheTiles"] == 24
        report["checks"]["no_runtime_errors"] = not report["page_errors"] and not report["console_errors"]
        report["checks"]["no_external_requests"] = not report["external_requests"]
        await browser.close()
    report["pass"] = all(report["checks"].values())
    print(report)
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
