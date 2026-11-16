"""Deterministic objective collection regressions.

These component probes place the player on real objective objects and call the
production update/interaction functions. They do not simulate a mission win,
change player combat stats, or count as full-run acceptance.
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")
MARKER = "// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER) == 1

PROBE = r"""
window.__objectiveRegression = () => {
  const results = {};
  const run = (type, variant, object, target=1) => {
    startRun();
    const p = game.player;
    game.objective = {
      type, variant, progress:0, target, time:95,
      x:p.x, y:p.y, done:false, objects:[object]
    };
    if(type==='cores' && variant==='heavy'){
      const picked=objectiveItemInteraction();
      updateObjective(.1);
      return {picked,progress:game.player.objectives,done:game.objective.done,screen,carried:!!game.carriedCore};
    }
    updateObjective(.1);
    return {progress:game.objective.progress,done:game.objective.done,screen,alive:object.alive};
  };
  results.fungi_normal=run('fungi',null,{x:0,y:0,alive:true});
  results.fungi_scared=run('fungi','scared',{x:0,y:0,alive:true,scared:true});
  results.fungi_explosive=run('fungi','explosive',{x:0,y:0,alive:true,explosive:true});
  results.sludge_normal=run('sludge',null,{x:0,y:0,alive:true});
  results.sludge_dark=run('sludge','dark',{x:0,y:0,alive:true});
  results.cores_normal=run('cores',null,{x:0,y:0,alive:true});
  results.cores_heavy=run('cores','heavy',{x:0,y:0,alive:true});
  return results;
};
"""
DOCUMENT = SOURCE.replace(MARKER, PROBE + "\n" + MARKER)

async def main():
    report={"checks":{},"page_errors":[],"console_errors":[],"external_requests":[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
        page=await browser.new_page(viewport={"width":1280,"height":800})
        page.on("pageerror",lambda e:report["page_errors"].append(str(e)))
        page.on("console",lambda m:report["console_errors"].append(m.text) if m.type=="error" else None)
        page.on("request",lambda r:report["external_requests"].append(r.url) if r.url.startswith(("http://","https://")) else None)
        await page.set_content(DOCUMENT,wait_until="load")
        await page.locator("#start").click()
        report["results"]=await page.evaluate("window.__objectiveRegression()")
        r=report["results"]
        for key in ["fungi_normal","fungi_scared","fungi_explosive","sludge_normal","sludge_dark","cores_normal"]:
            report["checks"][key]=r[key]["done"] and r[key]["progress"]>=1 and r[key]["screen"]=="upgrade" and r[key]["alive"] is False
        report["checks"]["cores_heavy"]=r["cores_heavy"]["picked"] and r["cores_heavy"]["done"] and r["cores_heavy"]["progress"]>=1 and r["cores_heavy"]["screen"]=="upgrade" and not r["cores_heavy"]["carried"]
        report["checks"]["no_runtime_or_console_errors"]=not report["page_errors"] and not report["console_errors"]
        report["checks"]["offline_no_external_requests"]=not report["external_requests"]
        report["pass"]=all(report["checks"].values())
        print(json.dumps(report,ensure_ascii=False,indent=2))
        await browser.close()
    if not report["pass"]:
        raise SystemExit(1)

if __name__=="__main__":
    asyncio.run(main())
