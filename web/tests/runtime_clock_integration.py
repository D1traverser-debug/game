"""Browser integration test proving the packaged fixed-step module drives the real game loop."""
import asyncio, base64, json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[2]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
MODULE=(ROOT/"web"/"src"/"core"/"fixed-step-clock.mjs").read_text(encoding="utf-8")
IMPORT="import('./web/src/core/fixed-step-clock.mjs')"
MARKER="// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(IMPORT)==1, "production HTML must have exactly one fixed-step module import"
assert SOURCE.count(MARKER)==1, "test probe insertion marker must remain unique"

# Use exact production module bytes through a data URL so set_content works
# without localhost/file navigation in the CI sandbox.
instrumented=MODULE+"\nglobalThis.__AETHER_CLOCK_MODULE_LOADED=true;\n"
data_url="data:text/javascript;base64,"+base64.b64encode(instrumented.encode("utf-8")).decode("ascii")
document=SOURCE.replace(IMPORT,f"import('{data_url}')")
probe="""window.__clockProbe=()=>({screen,time:game?.time??0,clockTick:coreClock?.tick??-1,pending:coreClock?.pendingSeconds??-1});"""
document=document.replace(MARKER,probe+"\n"+MARKER)

async def main():
    report={"checks":{},"page_errors":[],"console_errors":[],"external_requests":[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
        page=await browser.new_page(viewport={"width":1280,"height":800})
        page.on("pageerror",lambda e:report["page_errors"].append(str(e)))
        page.on("console",lambda m:report["console_errors"].append(m.text) if m.type=="error" else None)
        page.on("request",lambda r:report["external_requests"].append(r.url) if r.url.startswith(("http://","https://")) else None)
        await page.set_content(document,wait_until="load")
        await page.wait_for_function("window.__AETHER_CLOCK_MODULE_LOADED===true",timeout=5000)
        await page.locator("#start").click()
        await page.wait_for_timeout(350)
        state=await page.evaluate("window.__clockProbe()")
        report["state"]=state
        report["checks"]["module_loaded"]=True
        report["checks"]["core_clock_instantiated"]=state["clockTick"]>0
        report["checks"]["game_loop_advanced"]=state["screen"]=="playing" and state["time"]>0
        report["checks"]["fixed_step_tick_matches_game_progress"]=state["clockTick"]>=int(state["time"]*29)
        report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
        report["checks"]["no_external_requests"]=not report["external_requests"]
        report["pass"]=all(report["checks"].values())
        print(json.dumps(report,ensure_ascii=False,indent=2))
        await browser.close()
    if not report["pass"]: raise SystemExit(1)

if __name__=="__main__": asyncio.run(main())
