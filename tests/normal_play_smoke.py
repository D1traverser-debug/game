"""Normal-play 90-second combat smoke.

Unlike component probes, this test does not inject game-state values, damage
enemies, skip mission time, grant XP, or force a result. It only supplies player
movement and selects offered upgrades through the production upgrade handler.
The simulation clock is advanced in 100 ms steps to keep CI deterministic.
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
window.__normalPlay = async (seconds) => {
  const dt = 0.1;
  let elapsed = 0, ticks = 0, upgrades = 0;
  while (elapsed < seconds && (screen === 'playing' || screen === 'upgrade') && !game.ended) {
    if (screen === 'upgrade') {
      const opts = game.pending?.opts || [];
      if (!opts.length) break;
      // Real player action: choose the first option actually offered by the game.
      applyUpgrade(opts[0]);
      upgrades++;
      continue;
    }
    const p = game.player;
    const orb = game.orbs.filter(o => o.type === 'xp')
      .map(o => ({o,d:Math.hypot(o.x-p.x,o.y-p.y)}))
      .filter(x => x.d < 650)
      .sort((a,b) => a.d-b.d)[0];
    let dx,dy;
    if (orb && orb.d > 24) {
      dx=(orb.o.x-p.x)/orb.d; dy=(orb.o.y-p.y)/orb.d;
    } else {
      const a=Math.floor(elapsed/7)%4*Math.PI/2;
      dx=Math.cos(a); dy=Math.sin(a);
    }
    keys={KeyD:dx>.25,KeyA:dx<-.25,KeyS:dy>.25,KeyW:dy<-.25};
    const chest=game.chests.find(c=>!c.open&&Math.hypot(c.x-p.x,c.y-p.y)<70);
    if(chest) interact();
    update(dt);
    elapsed+=dt;ticks++;
    if(ticks%100===0) await new Promise(r=>setTimeout(r,0));
  }
  keys={};
  return {
    screen,ended:game.ended,time:game.time,kills:game.player.kills,level:game.player.level,
    hp:game.player.hp,maxHp:game.player.maxHp,xp:game.player.xp,nextXp:game.player.nextXp,upgrades,
    objectiveCount:game.player.objectives,enemyCount:game.enemies.filter(e=>!e.dead).length
  };
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
        state=await page.evaluate("window.__normalPlay(90)")
        report["state"]=state
        report["checks"]["natural_time_advanced"]=state["time"]>=89
        report["checks"]["normal_combat_kills"]=state["kills"]>0
        report["checks"]["player_survived_smoke"]=state["hp"]>0 and state["hp"]<=state["maxHp"]
        report["checks"]["real_upgrade_flow_used"]=state["upgrades"]>0 and state["level"]>1
        report["checks"]["no_ended_or_failed_screen"]=state["screen"]=="playing" and not state["ended"]
        report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
        report["checks"]["offline_no_external_requests"]=not report["external_requests"]
        report["pass"]=all(report["checks"].values())
        print(json.dumps(report,ensure_ascii=False,indent=2))
        await browser.close()
    if not report["pass"]:
        raise SystemExit(1)

if __name__=="__main__":
    asyncio.run(main())
