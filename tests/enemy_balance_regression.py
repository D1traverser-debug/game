"""Production enemy damage curve and Gnasher warning regression."""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
MARKER="// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER)==1

PROBE=r"""
window.__enemyBalanceProbe=()=>{
 const time=1200,base=86,scale=enemyDamageScale(time),sample={dmg:base*scale,weakness:0,speed:100};
 const formulas={scale,spawnDamage:sample.dmg,leap:gnasherLeapDamage(sample),contact:enemyContactDamage(sample),burrowSpeed:gnasherBurrowSpeed(sample)};
 const p=game.player;
 game.time=600;game.spawn=99999;game.nextObj=4;game.nextChest=99999;
 game.boss=null;game.bossPending=null;game.objective=null;game.carriedCore=null;
 game.enemies=[];game.shots=[];game.orbs=[];game.plants=[];game.hazards=[];game.fx=[];game.damageNumbers=[];game.chests=[];
 p.x=0;p.y=0;p.hp=p.maxHp=1000;p.invuln=0;p.ghost=false;p.dodge=0;p.thick=false;
 const e={id:"balance-gnasher",type:"gnasher",x:140,y:0,r:24,hp:160,max:160,speed:100,dmg:100,state:"burrow",stateT:.01,attack:0,slow:0,freeze:0,acid:0,weakness:0,burn:0,hitFlash:0,dead:false,elite:false};
 game.enemies=[e];
 update(1/30);
 const warning=game.hazards.find(h=>h.gnasherWarning);
 p.maxHp=100;p.hp=100;p.armor=36;p.invuln=0;
 const beforeLeap=p.hp,lateGnasher={dmg:86*enemyDamageScale(385),weakness:0,speed:70};
 damagePlayer(gnasherLeapDamage(lateGnasher),'gnasher');
 const leapPlayerLoss=beforeLeap-p.hp;
 p.maxHp=100;p.hp=100;p.armor=68;p.invuln=0;
 const beforeContact=p.hp,lateCrab={dmg:175*enemyDamageScale(800),weakness:0};
 damagePlayer(enemyContactDamage(lateCrab),'contact');
 const contactPlayerLoss=beforeContact-p.hp;
 return {formulas,playerDamage:{leap:leapPlayerLoss,contact:contactPlayerLoss},enemyState:e.state,leapTarget:{x:e.leapX,y:e.leapY},warning:warning?{kind:warning.kind,x:warning.x,y:warning.y,r:warning.r,timer:warning.timer,life:warning.life,dmg:warning.dmg}:null};
};
"""
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
  result=await page.evaluate("window.__enemyBalanceProbe()")
  report["result"]=result
  f=result["formulas"]
  report["checks"]["damage_scale_is_bounded"]=1.66<f["scale"]<1.68
  report["checks"]["gnasher_leap_is_bounded"]=0<f["leap"]/f["spawnDamage"]<=.33
  report["checks"]["enemy_contact_is_bounded"]=0<f["contact"]/f["spawnDamage"]<=.05
  report["checks"]["gnasher_leap_after_armor_is_nonlethal"]=0<result["playerDamage"]["leap"]<30
  report["checks"]["crabladon_contact_after_armor_is_sustainable"]=0<result["playerDamage"]["contact"]<10
  report["checks"]["burrow_remains_faster_than_player_but_dodgeable"]=200<f["burrowSpeed"]<260
  report["checks"]["leap_has_visible_landing_warning"]=result["enemyState"]=="leap" and result["warning"] is not None and result["warning"]["kind"]=="warning" and result["warning"]["r"]==62 and result["warning"]["dmg"]==0
  report["checks"]["warning_is_placed_at_committed_landing_point"]=result["warning"] is not None and abs(result["warning"]["x"]-result["leapTarget"]["x"])<.001 and abs(result["warning"]["y"]-result["leapTarget"]["y"])<.001
  report["checks"]["warning_uses_distinct_purple_telegraph_color"]="h.gnasherWarning?[.76,.40,.90,.42]" in SOURCE
  report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
  report["checks"]["offline_no_external_requests"]=not report["external_requests"]
  report["pass"]=all(report["checks"].values())
  print(json.dumps(report,ensure_ascii=False,indent=2))
  await browser.close()
 if not report["pass"]:raise SystemExit(1)

if __name__=="__main__":asyncio.run(main())
