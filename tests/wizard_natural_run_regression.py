"""Natural 25-minute solo expedition and boss victory for every selectable wizard."""
import asyncio, importlib.util, json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
PILOT_PATH=ROOT/"tests"/"boss_archetype_full_runs.py"
SPEC=importlib.util.spec_from_file_location("aetherwilds_boss_pilot",PILOT_PATH)
PILOT=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PILOT)
CHARACTERS=[("aster",41),("ember",42),("briar",43),("nyx",44)]
MARKER="// Production build: internal debug mutations are test-only and not shipped."
PILOT_ABILITY_ANCHOR="if(!gnasherThreat&&(chestNear||itemNear)){interact();interactions++;}\n    window.__manualTick=true;"
PILOT_ABILITY_PATCH="""if(!gnasherThreat&&(chestNear||itemNear)){interact();interactions++;}
    const hpRatio=p.hp/Math.max(1,p.maxHp),closeThreat=game.enemies.some(e=>!e.dead&&Math.hypot(e.x-p.x,e.y-p.y)<260);
    const abilityReady=p.abilityCd<=0;
    const shouldUseAbility=abilityReady&&(
      (p.characterId==='aster'&&closeThreat)||
      (p.characterId==='ember'&&game.enemies.some(e=>!e.dead&&Math.hypot(e.x-p.x,e.y-p.y)<700))||
      (p.characterId==='briar'&&(hpRatio<.92||closeThreat))||
      (p.characterId==='nyx'&&closeThreat)
    );
    if(shouldUseAbility)useCharacterAbility();
    window.__manualTick=true;"""
DOCUMENT=(PILOT.DOCUMENT
 .replace(MARKER,"window.__setSelectedWizardForTest=(id)=>{save.selectedCharacterId=id;persist();};window.__getSelectedWizardForTest=()=>game?.player?.characterId||save.selectedCharacterId;\\n"+MARKER)
 .replace(PILOT_ABILITY_ANCHOR,PILOT_ABILITY_PATCH))
assert DOCUMENT!=PILOT.DOCUMENT and DOCUMENT.count("window.__setSelectedWizardForTest")==1
assert "if(shouldUseAbility)useCharacterAbility();" in DOCUMENT
assert DOCUMENT!=PILOT.DOCUMENT and DOCUMENT.count("window.__setSelectedWizardForTest")==1

async def main():
 report={"runs":[],"checks":{}}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  for character,seed in CHARACTERS:
   context=await browser.new_context(viewport={"width":1280,"height":800})
   page=await context.new_page()
   errors=[];console=[];requests=[]
   page.on("pageerror",lambda e:errors.append(str(e)))
   page.on("console",lambda m:console.append(m.text) if m.type=="error" else None)
   page.on("request",lambda r:requests.append(r.url) if r.url.startswith(("http://","https://")) else None)
   page.set_default_timeout(180000)
   await page.set_content(DOCUMENT,wait_until="load")
   await page.evaluate("(id)=>window.__setSelectedWizardForTest(id)",character)
   await page.evaluate("(seed)=>window.__setRunSeed(seed)",seed)
   await page.locator("#start").click()
   selected=await page.evaluate("window.__getSelectedWizardForTest()")
   state=await asyncio.wait_for(page.evaluate("window.__fullRun(1500,false)"),timeout=180)
   natural_win=bool(state["bossDead"] and state["ended"] and state["screen"]=="result" and state["wins"]>=1)
   row={
    "character":character,"seed":seed,"selected":selected,"natural_win":natural_win,
    "screen":state["screen"],"ended":state["ended"],"gameTime":round(state["gameTime"],1),
    "bossSpawned":state["bossSpawned"],"bossId":state["bossId"],"bossDead":state["bossDead"],
    "wins":state["wins"],"hp":round(state["hp"],1),"maxHp":state["maxHp"],
    "level":state["level"],"kills":state["kills"],"objectives":state["objectives"],
    "armor":state["armor"],"regen":state["regen"],"enemyCount":state["enemyCount"],
    "position":state["position"],"trace":state["trace"][-8:],
    "pageErrors":errors,"consoleErrors":console,"externalRequests":requests,
    "simulationHarness":state["simulationHarness"],"renderRandomCalls":state["renderRandomCalls"]
   }
   report["runs"].append(row)
   await context.close()
  await browser.close()
 report["checks"]["all_four_selected"] = all(x["selected"]==x["character"] for x in report["runs"])
 report["checks"]["all_four_natural_boss_wins"] = all(x["natural_win"] for x in report["runs"])
 report["checks"]["no_runtime_or_network_errors"] = all(not x["pageErrors"] and not x["consoleErrors"] and not x["externalRequests"] for x in report["runs"])
 report["pass"]=all(report["checks"].values())
 print(json.dumps(report,ensure_ascii=False,indent=2))
 if not report["pass"]: raise SystemExit(1)

if __name__=="__main__": asyncio.run(main())
