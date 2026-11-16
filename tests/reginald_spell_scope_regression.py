"""Reginald-only spell eligibility, save migration and quest regression.

Diagnostics are injected into an in-memory document only; no test hooks ship.
"""
import asyncio
import re
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")
EXCLUDED = {"hex", "necro", "spear", "sickle", "orbital", "seismic", "mesh"}


def instrument(source: str) -> str:
    marker = "// Production build: internal debug mutations are test-only and not shipped."
    assert source.count(marker) == 1
    assert len(re.findall(r"function\\s+v2enemy\\s*\\(", source)) == 1
    probe = r"""
window.__scopeProbe={
 snapshot:()=>({ids:[...REGINALD_SPELL_IDS],unlocks:[...save.unlocks],trial:save.trialSpellId,questFlags:[...save.questFlags],atlas:{loaded:V2_ATLAS.complete,w:V2_ATLAS.naturalWidth,h:V2_ATLAS.naturalHeight},screen}),
 migrate:()=>{save.schemaVersion=3;save.unlocks=['astral','loadedDice','tinyTremors','wickedBuzzsaw','hex','necro','spear','sickle','orbital','seismic','mesh','solar'];save.questFlags=['solar','seismic','beam'];save.trialSpellId='hex';normalizeSave();return window.__scopeProbe.snapshot()},
 grant:(id)=>({result:grantSpellQuest(id),unlocks:[...save.unlocks],flags:[...save.questFlags]})
};
"""
    return source.replace(marker, probe + "\\n" + marker)


async def main():
    out = {"checks": {}, "errors": [], "console_errors": [], "external_requests": []}
    async with async_playwright() as p:
        opts = {"headless": True, "args": ["--no-sandbox", "--enable-webgl", "--ignore-gpu-blocklist"]}
        if shutil.which("chromium"):
            opts["executable_path"] = shutil.which("chromium")
        browser = await p.chromium.launch(**opts)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("pageerror", lambda e: out["errors"].append(str(e)))
        page.on("console", lambda m: out["console_errors"].append(m.text) if m.type == "error" else None)
        page.on("request", lambda r: out["external_requests"].append(r.url) if r.url.startswith(("http://", "https://")) else None)
        await page.set_content(instrument(SOURCE), wait_until="load")
        await page.wait_for_timeout(1000)
        initial = await page.evaluate("__scopeProbe.snapshot()")
        out["initial"] = initial
        out["checks"]["exactly_18_reginald_spells"] = len(initial["ids"]) == 18
        out["checks"]["no_other_wizard_signature_spells"] = not (EXCLUDED & set(initial["ids"]))
        out["checks"]["four_source_starters_only"] = set(initial["unlocks"]) == {"astral", "loadedDice", "tinyTremors", "wickedBuzzsaw"}
        await page.locator("#camp").click()
        text = await page.locator("#questGrid").inner_text()
        out["checks"]["research_ui_hides_other_hero_spells"] = not any(x in text for x in ["Hex Bomb", "Necro Whirl", "Spear Barrage", "Swirl Sickle", "Scepter Mesh", "Seismic Slam", "六角诅咒弹", "亡灵旋刃", "长矛齐射", "旋风镰刀", "权杖网阵", "地脉震击"])
        out["checks"]["research_ui_has_all_reginald_entries"] = all(x in text for x in ["魔法飞弹", "太阳脉冲", "月牙回旋", "奥术巨剑", "以太光束", "坠星", "命运骰子", "微型地震", "邪刃锯轮"])
        migrated = await page.evaluate("__scopeProbe.migrate()")
        out["migrated"] = migrated
        out["checks"]["legacy_unlocks_filtered"] = not (EXCLUDED & set(migrated["unlocks"]))
        out["checks"]["legacy_trial_filtered"] = migrated["trial"] is None
        out["checks"]["valid_quest_flags_retained"] = set(migrated["questFlags"]) == {"solar", "beam"}
        rejected = await page.evaluate('__scopeProbe.grant("seismic")')
        accepted = await page.evaluate('__scopeProbe.grant("missile")')
        out["checks"]["other_hero_quest_rejected"] = rejected["result"] is False and "seismic" not in rejected["unlocks"]
        out["checks"]["reginald_quest_granted"] = accepted["result"] is True and "missile" in accepted["unlocks"]
        out["checks"]["atlas_loaded"] = initial["atlas"]["loaded"] and initial["atlas"]["w"] == 1024 and initial["atlas"]["h"] == 1024
        out["checks"]["no_runtime_errors"] = not out["errors"] and not out["console_errors"]
        out["checks"]["no_external_requests"] = not out["external_requests"]
        await browser.close()
    out["pass"] = all(out["checks"].values())
    print(out)
    if not out["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
