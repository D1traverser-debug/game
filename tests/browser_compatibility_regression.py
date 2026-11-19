"""Desktop/mobile single-player launch smoke test for Chromium, Firefox and WebKit."""
import asyncio, json, os, threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
BROWSER_NAME=os.environ.get("AETHER_BROWSER","chromium").lower()
async def main():
 report={"browser":BROWSER_NAME,"checks":{},"page_errors":[],"console_errors":[],"external_requests":[]}
 server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 base=f"http://127.0.0.1:{server.server_address[1]}"
 try:
  async with async_playwright() as p:
   browser_type=getattr(p,BROWSER_NAME)
   args=["--no-sandbox","--disable-dev-shm-usage"] if BROWSER_NAME=="chromium" else []
   browser=await browser_type.launch(headless=True,args=args)
   desktop=await browser.new_page(viewport={"width":1440,"height":900})
   desktop.on("pageerror",lambda e:report["page_errors"].append(str(e)))
   desktop.on("console",lambda m:report["console_errors"].append(m.text) if m.type=="error" else None)
   desktop.on("request",lambda r:report["external_requests"].append(r.url) if not r.url.startswith(base) else None)
   await desktop.goto(base+"/index.html",wait_until="load");await desktop.wait_for_timeout(300)
   report["checks"]["desktop_menu_visible"]=await desktop.locator("#start").is_visible()
   report["checks"]["canvas_2d_available"]=await desktop.evaluate("!!document.getElementById('world').getContext('2d')")
   await desktop.locator("#selectCharacter").click()
   report["checks"]["four_wizards_render"]=await desktop.locator("[data-character]").count()==4
   await desktop.locator('[data-character="nyx"]').click()
   report["checks"]["selected_wizard_highlighted"]="selected" in (await desktop.locator('[data-character="nyx"]').get_attribute("class"))
   await desktop.locator("#characterStart").click();await desktop.locator("#hud.active").wait_for(timeout=5000);await desktop.wait_for_timeout(1100)
   report["checks"]["desktop_simulation_advances"]=await desktop.locator("#timer").inner_text()!="00:00"
   await desktop.locator("#pauseBtn").click()
   report["checks"]["pause_overlay_works"]=await desktop.locator("#pause.active").count()==1
   await desktop.locator("#resume").click()
   report["checks"]["resume_restores_hud"]=await desktop.locator("#hud.active").count()==1
   mobile=await browser.new_page(viewport={"width":390,"height":844})
   mobile.on("pageerror",lambda e:report["page_errors"].append("mobile:"+str(e)))
   mobile.on("console",lambda m:report["console_errors"].append("mobile:"+m.text) if m.type=="error" else None)
   mobile.on("request",lambda r:report["external_requests"].append(r.url) if not r.url.startswith(base) else None)
   await mobile.goto(base+"/index.html",wait_until="load");await mobile.locator("#selectCharacter").click()
   await mobile.locator('[data-character="briar"]').click();await mobile.locator("#characterStart").scroll_into_view_if_needed()
   await mobile.locator("#characterStart").click();await mobile.locator("#hud.active").wait_for(timeout=5000)
   report["checks"]["mobile_virtual_joystick_visible"]=await mobile.locator("#joy").is_visible()
   report["checks"]["mobile_interact_button_visible"]=await mobile.locator("#interact").is_visible()
   report["checks"]["mobile_ability_button_visible"]=await mobile.locator("#abilityBtn").is_visible()
   await mobile.wait_for_timeout(900)
   report["checks"]["mobile_simulation_advances"]=await mobile.locator("#timer").inner_text()!="00:00"
   report["checks"]["no_external_runtime_requests"]=not report["external_requests"]
   report["checks"]["no_page_or_console_errors"]=not report["page_errors"] and not report["console_errors"]
   report["pass"]=all(report["checks"].values());print(json.dumps(report,ensure_ascii=False,indent=2))
   await browser.close()
 finally:server.shutdown();server.server_close()
 if not report["pass"]:raise SystemExit(1)
if __name__=="__main__":asyncio.run(main())
