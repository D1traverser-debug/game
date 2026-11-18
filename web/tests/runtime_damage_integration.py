"""Browser integration test proving real player/enemy damage routes through DamagePipeline."""
import asyncio, base64, json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[2]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
COMBATANT=(ROOT/"web"/"src"/"core"/"combatant.mjs").read_text(encoding="utf-8")
DAMAGE=(ROOT/"web"/"src"/"core"/"damage-pipeline.mjs").read_text(encoding="utf-8")
COMBATANT_IMPORT="import('./web/src/core/combatant.mjs')"
DAMAGE_IMPORT="import('./web/src/core/damage-pipeline.mjs')"
MARKER="// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(COMBATANT_IMPORT)==1
assert SOURCE.count(DAMAGE_IMPORT)==1
assert SOURCE.count(MARKER)==1
def data_url(source):
    return "data:text/javascript;base64,"+base64.b64encode(source.encode("utf-8")).decode("ascii")

combatant_url=data_url(COMBATANT+"\nglobalThis.__AETHER_COMBATANT_MODULE_LOADED=true;\n")
DAMAGE=DAMAGE.replace('from "./combatant.mjs"',f'from "{combatant_url}"')
apply_marker="static apply(source, target, request, policy = new DamagePolicy()) {"
assert DAMAGE.count(apply_marker)==1
DAMAGE=DAMAGE.replace(apply_marker,apply_marker+"\n    globalThis.__AETHER_DAMAGE_PIPELINE_CALLS=(globalThis.__AETHER_DAMAGE_PIPELINE_CALLS||0)+1;")
damage_url=data_url(DAMAGE+"\nglobalThis.__AETHER_DAMAGE_MODULE_LOADED=true;\n")
document=SOURCE.replace(COMBATANT_IMPORT,f"import('{combatant_url}')").replace(DAMAGE_IMPORT,f"import('{damage_url}')")
probe="""window.__damageProbe={
 ready:()=>!!coreDamageApi,
 enemyHit:()=>{const e=game.enemies.find(x=>!x.dead);const before=e.hp;damageEnemy(e,1,'integration_test',null,false);return {before,after:e.hp,calls:globalThis.__AETHER_DAMAGE_PIPELINE_CALLS||0};},
 playerHit:()=>{const p=game.player;p.dodge=0;p.invuln=0;const before=p.hp;damagePlayer(10,'integration_test');return {before,after:p.hp,calls:globalThis.__AETHER_DAMAGE_PIPELINE_CALLS||0};}
};"""
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
        await page.wait_for_function("window.__damageProbe.ready()===true",timeout=5000)
        await page.locator("#start").click()
        enemy=await page.evaluate("window.__damageProbe.enemyHit()")
        player=await page.evaluate("window.__damageProbe.playerHit()")
        report["enemy_damage"]=enemy
        report["player_damage"]=player
        report["checks"]["damage_modules_loaded"]=True
        report["checks"]["enemy_damage_uses_pipeline"]=enemy["after"]<enemy["before"] and enemy["calls"]>=1
        report["checks"]["player_damage_uses_pipeline"]=player["after"]<player["before"] and player["calls"]>=2
        report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
        report["checks"]["no_external_requests"]=not report["external_requests"]
        report["pass"]=all(report["checks"].values())
        print(json.dumps(report,ensure_ascii=False,indent=2))
        await browser.close()
    if not report["pass"]: raise SystemExit(1)

if __name__=="__main__": asyncio.run(main())
