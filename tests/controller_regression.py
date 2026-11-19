"""Gamepad controls use standard button mapping and edge-triggered actions."""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
MARKER="// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER)==1
PROBE="""window.__controllerProbe=(()=>{
 const counts={interact:0,ability:0};
 const baseInteract=interact,baseAbility=useCharacterAbility;
 interact=(...args)=>{counts.interact++;return baseInteract(...args)};
 useCharacterAbility=(...args)=>{counts.ability++;return baseAbility(...args)};
 const pad={axes:[0,0],buttons:Array.from({length:16},()=>({pressed:false}))};
 Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[pad]});
 const set=(axes,pressed=[])=>{
  pad.axes=axes;
  pad.buttons.forEach((button,index)=>button.pressed=pressed.includes(index));
  joy.active=false;studioController();
  return {joy:{x:joy.x,y:joy.y},counts:{...counts},screen,abilityCooldown:game?.player?.abilityCd??null};
 };
 return {set,counts:()=>({...counts})};
})();"""
DOCUMENT=SOURCE.replace(MARKER,PROBE+"\n"+MARKER)

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
  await page.wait_for_timeout(100)
  moved=await page.evaluate("window.__controllerProbe.set([0.8,-0.6],[])")
  report["movement"]=moved
  report["checks"]["left_stick_moves_player"] = abs(moved["joy"]["x"]-.8)<.001 and abs(moved["joy"]["y"]+.6)<.001
  deadzone=await page.evaluate("window.__controllerProbe.set([0.08,-0.1],[])")
  report["checks"]["left_stick_deadzone"] = deadzone["joy"]=={"x":0,"y":0}
  firstInteract=await page.evaluate("window.__controllerProbe.set([0,0],[0])")
  heldInteract=await page.evaluate("window.__controllerProbe.set([0,0],[0])")
  report["checks"]["a_button_interacts_once_per_press"] = firstInteract["counts"]["interact"]==1 and heldInteract["counts"]["interact"]==1
  await page.evaluate("window.__controllerProbe.set([0,0],[])")
  secondInteract=await page.evaluate("window.__controllerProbe.set([0,0],[0])")
  report["checks"]["a_button_retriggers_after_release"] = secondInteract["counts"]["interact"]==2
  await page.evaluate("window.__controllerProbe.set([0,0],[])")
  firstAbility=await page.evaluate("window.__controllerProbe.set([0,0],[1])")
  heldAbility=await page.evaluate("window.__controllerProbe.set([0,0],[1])")
  report["ability"]={"first":firstAbility,"held":heldAbility}
  report["checks"]["b_button_uses_character_ability"] = firstAbility["counts"]["ability"]==1 and firstAbility["abilityCooldown"]>0
  report["checks"]["b_button_is_edge_triggered"] = heldAbility["counts"]["ability"]==1
  await page.evaluate("window.__controllerProbe.set([0,0],[])")
  paused=await page.evaluate("window.__controllerProbe.set([0,0],[9])")
  heldPause=await page.evaluate("window.__controllerProbe.set([0,0],[9])")
  report["checks"]["start_button_pauses_once"] = paused["screen"]=="pause" and heldPause["screen"]=="pause"
  await page.evaluate("window.__controllerProbe.set([0,0],[])")
  resumed=await page.evaluate("window.__controllerProbe.set([0,0],[9])")
  report["checks"]["start_button_resumes_after_release"] = resumed["screen"]=="playing"
  report["checks"]["no_runtime_errors"] = not report["page_errors"] and not report["console_errors"]
  report["checks"]["offline_no_external_requests"] = not report["external_requests"]
  report["pass"]=all(report["checks"].values())
  print(json.dumps(report,ensure_ascii=False,indent=2))
  await browser.close()
 if not report["pass"]:raise SystemExit(1)

if __name__=="__main__":asyncio.run(main())
