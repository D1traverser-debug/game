"""Shared solo spell catalogue, save migration and quest regression.

Diagnostics are injected into an in-memory document only; no test hooks ship.
"""
import asyncio
import re
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")

EXPECTED_STARTERS = {"astral", "loadedDice", "tinyTremors", "wickedBuzzsaw"}
EXPECTED_QUEST_UNLOCKS = {
    "missile", "solar", "moon", "sword", "beam", "stars", "blades",
    "runes", "rocky", "wings", "bell", "sprout", "talon", "imp",
}
EXPECTED_SOLO_CATALOGUE = EXPECTED_STARTERS | EXPECTED_QUEST_UNLOCKS
UNSUPPORTED_LEGACY_SIGNATURES = {
    "hex", "necro", "spear", "sickle", "orbital", "seismic", "mesh",
}
EXPECTED_RUNTIME_DEFINITIONS = EXPECTED_SOLO_CATALOGUE | UNSUPPORTED_LEGACY_SIGNATURES
EXPECTED_SIZE_UPGRADE_SPELLS = {
    "sword", "solar", "bell", "blades", "rocky", "sprout", "talon",
}
EXPECTED_RESEARCH_NAMES = [
    "魔法飞弹", "太阳脉冲", "月牙回旋", "奥术巨剑", "以太光束", "坠星",
    "幻影刀刃", "基数符文", "碎岩之路", "极光之翼", "钟鸣行军",
    "复仇萌芽", "鹰爪斩", "小恶魔骚乱",
    "命运骰子", "微型地震", "邪刃锯轮",
]
UNSUPPORTED_RESEARCH_NAMES = [
    "Hex Bomb", "Necro Whirl", "Spear Barrage", "Swirl Sickle",
    "Scepter Mesh", "Seismic Slam", "六角诅咒弹", "亡灵旋刃",
    "长矛齐射", "旋风镰刀", "权杖网阵", "地脉震击",
]


def instrument(source: str) -> str:
    marker = "// Production build: internal debug mutations are test-only and not shipped."
    assert source.count(marker) == 1
    assert len(re.findall(r"function\s+v2enemy\s*\(", source)) == 1
    probe = r"""
window.__catalogProbe={
 snapshot:()=>({
  ids:[...SOLO_SPELL_CATALOG_IDS],
  definitionIds:[...SPELL_ID_SET],
  unlocks:[...save.unlocks],
  trial:save.trialSpellId,
  questFlags:[...save.questFlags],
  starterIds:CHARACTERS.map(x=>x.starterSpell),
  sizeUpgradeIds:[...SIZE_UPGRADE_SPELLS],
  atlas:{loaded:V2_ATLAS.complete,w:V2_ATLAS.naturalWidth,h:V2_ATLAS.naturalHeight},
  screen
 }),
 migrate:()=>{
  save.schemaVersion=3;
  save.unlocks=['astral','loadedDice','tinyTremors','wickedBuzzsaw','hex','necro','spear','sickle','orbital','seismic','mesh','solar'];
  save.questFlags=['solar','seismic','beam'];
  save.trialSpellId='hex';
  normalizeSave();
  return window.__catalogProbe.snapshot()
 },
 grant:(id)=>({result:grantSpellQuest(id),unlocks:[...save.unlocks],flags:[...save.questFlags]})
};
"""
    return source.replace(marker, probe + "\n" + marker)


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
        initial = await page.evaluate("__catalogProbe.snapshot()")
        out["initial"] = initial
        definitions = set(initial["definitionIds"])
        catalogue = set(initial["ids"])
        starters = set(initial["starterIds"])
        out["checks"]["exactly_25_runtime_spell_definitions"] = len(definitions) == 25 and definitions == EXPECTED_RUNTIME_DEFINITIONS
        out["checks"]["exactly_18_shared_solo_spells"] = len(catalogue) == 18 and catalogue == EXPECTED_SOLO_CATALOGUE
        out["checks"]["exactly_14_shared_quest_unlocks"] = catalogue - starters == EXPECTED_QUEST_UNLOCKS
        out["checks"]["four_unique_wizard_starters"] = starters == EXPECTED_STARTERS and len(initial["starterIds"]) == 4
        out["checks"]["initial_save_contains_only_four_starters"] = set(initial["unlocks"]) == EXPECTED_STARTERS
        out["checks"]["no_out_of_scope_legacy_signatures"] = not (UNSUPPORTED_LEGACY_SIGNATURES & catalogue)
        out["checks"]["size_upgrade_pool_is_playable"] = set(initial["sizeUpgradeIds"]) == EXPECTED_SIZE_UPGRADE_SPELLS and set(initial["sizeUpgradeIds"]) <= catalogue
        await page.locator("#camp").click()
        research_text = await page.locator("#questGrid").inner_text()
        out["checks"]["research_ui_hides_unsupported_legacy_signatures"] = not any(x in research_text for x in UNSUPPORTED_RESEARCH_NAMES)
        out["checks"]["research_ui_lists_all_14_quest_spells_and_3_other_starters"] = all(x in research_text for x in EXPECTED_RESEARCH_NAMES)
        migrated = await page.evaluate("__catalogProbe.migrate()")
        out["migrated"] = migrated
        out["checks"]["migration_filters_unsupported_unlocks"] = set(migrated["unlocks"]) == (EXPECTED_STARTERS | {"solar", "beam"})
        out["checks"]["migration_filters_unsupported_trial"] = migrated["trial"] is None
        out["checks"]["migration_retains_valid_quest_flags"] = set(migrated["questFlags"]) == {"solar", "beam"}
        rejected = await page.evaluate('__catalogProbe.grant("seismic")')
        accepted = await page.evaluate('__catalogProbe.grant("missile")')
        out["checks"]["unsupported_legacy_quest_rejected"] = rejected["result"] is False and "seismic" not in rejected["unlocks"]
        out["checks"]["valid_shared_spell_quest_granted"] = accepted["result"] is True and "missile" in accepted["unlocks"] and "missile" in accepted["flags"]
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
