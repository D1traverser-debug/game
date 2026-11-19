"""Character-upgrade pool and effect regressions."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")
MARKER = "// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER) == 1

PROBE = r"""
window.__characterUpgradeRegression = () => {
  startRun();
  game.player.level=2;
  const random=Math.random;
  let offers;
  try {
    Math.random=()=>.5;
    offerUpgrade('level');
    offers=game.pending.opts.map(x=>({kind:x.kind,k:x.k,rarity:x.rarity,amount:x.amount}));
  } finally { Math.random=random; }
  const offerChecks={
    three_cards:offers.length===3,
    new_spell_slot:offers.some(x=>x.kind==='newSpell'),
    spell_upgrade:offers.some(x=>x.kind==='spellLevel'||x.kind==='infuse'),
    character_upgrade:offers.some(x=>x.kind==='stat'&&Number.isFinite(x.amount)&&x.amount>0),
    survival_option_when_underbuilt:offers.some(x=>x.kind==='stat'&&['maxHp','regen','armor','dodge'].includes(x.k))
  };
  const cases=[
    ['maxHp',100,200],['regen',1,1],['armor',16,16],['dodge',.04,.07],
    ['speed',.08,170*1.08],['damage',.05,1.05],['spellSize',.12,1.25*1.12],
    ['cast',.06,1.06],['crit',.04,.09],['critDmg',.1,1.6],
    ['manaPull',.08,108],['manaGain',.07,1.07],['luck',2,4]
  ];
  const effects={};
  startRun();
  game.player.hp=20;
  applyUpgrade({kind:'stat',k:'maxHp',amount:100,title:'Vitality Forge'});
  const vitalityHealing={hp:game.player.hp,maxHp:game.player.maxHp,pass:game.player.hp===45&&game.player.maxHp===200};

  for(const [key,amount,expected] of cases){
    startRun();
    const p=game.player;
    const before=({maxHp:p.maxHp,regen:p.regen,armor:p.armor,dodge:p.dodge,
      speed:p.move,damage:p.damage,spellSize:p.spellSize,cast:p.cast,crit:p.crit,
      critDmg:p.critDmg,manaPull:p.manaPull,manaGain:p.manaGain,luck:p.luck})[key];
    applyUpgrade({kind:'stat',k:key,amount,title:'test'});
    const after=({maxHp:p.maxHp,regen:p.regen,armor:p.armor,dodge:p.dodge,
      speed:p.move,damage:p.damage,spellSize:p.spellSize,cast:p.cast,crit:p.crit,
      critDmg:p.critDmg,manaPull:p.manaPull,manaGain:p.manaGain,luck:p.luck})[key];
    effects[key]={before,after,expected,pass:Math.abs(after-expected)<.0001};
  }
  return {offers,offerChecks,effects,vitalityHealing};
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
        result=await page.evaluate("window.__characterUpgradeRegression()")
        report["result"]=result
        report["checks"].update(result["offerChecks"])
        report["checks"]["all_13_upgrade_effects"]=all(x["pass"] for x in result["effects"].values())
        report["checks"]["vitality_upgrade_heals_25_percent"]=result["vitalityHealing"]["pass"]
        report["checks"]["no_runtime_or_console_errors"]=not report["page_errors"] and not report["console_errors"]
        report["checks"]["offline_no_external_requests"]=not report["external_requests"]
        report["pass"]=all(report["checks"].values())
        print(json.dumps(report,ensure_ascii=False,indent=2))
        await browser.close()
    if not report["pass"]:
        raise SystemExit(1)

if __name__=="__main__":
    asyncio.run(main())
