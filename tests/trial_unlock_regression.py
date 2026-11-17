"""Browser component regression: solo spell trials and quest unlock event pipeline.

The test injects helpers into a temporary in-memory document. It does NOT
claim actual 19-minute player-play acceptance or real file:// persistence.
"""
import asyncio
import json
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'index.html').read_text(encoding='utf-8')
MARKER = '// Keep the single-player game running without external assets or libraries.'
assert SOURCE.count(MARKER) == 1

PROBE = """
window.__trialProbe={
 snapshot:()=>({trial:save.trialSpellId,unlocks:save.unlocks.slice(),flags:(save.questFlags||[]).slice(),level:game?.player.level,spells:game?.player.spells.map(s=>s.id),screen}),
 offer:(n)=>{game.player.level=n;screen='playing';offerUpgrade('level');return{offers:game.pending?.opts.map(o=>o.spell?.id||'NONE'),screen}},
 acceptFirst:()=>{applyUpgrade(game.pending.opts[0]);return{spells:game.player.spells.map(s=>s.id),screen}},
 grant:(id)=>({newlyGranted:grantSpellQuest(id),isFlagged:save.questFlags.includes(id),isUnlocked:save.unlocks.includes(id)}),
 starEvent:()=>{let s={...spells.find(x=>x.id==='stars'),level:14,infusions:[],augments:[],cdNow:0};
   const already=save.questFlags?.includes('stars')||false;
   game.player.spells.push(s);fireSpell(s);
   return {unlocked:save.unlocks.includes('stars'),preexisting:already};
 },
 restart:()=>{startRun();return{trial:save.trialSpellId,spells:game.player.spells.map(s=>s.id),screen}}
};
"""
TEST_HTML = SOURCE.replace(MARKER, PROBE + '\n' + MARKER)

async def main():
  outcome = {'checks': {}, 'page_errors': [], 'requests': [], 'scope': 'browser components, synthetic QA helpers'}
  async with async_playwright() as p:
    kwargs={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage','--enable-webgl','--ignore-gpu-blocklist','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']}
    chromium=shutil.which('chromium')
    if chromium: kwargs['executable_path']=chromium
    browser=await p.chromium.launch(**kwargs)
    page=await browser.new_page(viewport={'width':1240,'height':780})
    page.on('pageerror',lambda e:outcome['page_errors'].append(str(e)))
    page.on('request',lambda r:outcome['requests'].append(r.url))
    await page.set_content(TEST_HTML)
    await page.locator('#camp').click()
    c=outcome['checks']
    c['research_open']=await page.locator('#questGrid').is_visible()
    c['solar_trial_available']=await page.locator('[data-trial="solar"]').count()==1
    await page.locator('[data-trial="solar"]').click()
    c['trial_selected']=await page.evaluate('__trialProbe.snapshot().trial==="solar"')
    await page.locator('#campBack').click()
    await page.locator('#start').click()
    before=await page.evaluate('__trialProbe.snapshot()')
    c['solar_not_early_unlock']='solar' not in before['unlocks']
    c['trial_consumed_on_start']=before['trial'] is None
    c['trial_spell_equipped_at_start']='solar' in before['spells']
    offer=await page.evaluate('__trialProbe.offer(2)')
    c['trial_offered_at_slot_two']='solar' in offer['offers']
    accepted=await page.evaluate('__trialProbe.acceptFirst()')
    c['trial_equipped']='solar' in accepted['spells']
    granted=await page.evaluate('__trialProbe.grant("solar")')
    c['quest_permanent_unlock']=granted['newlyGranted'] and granted['isFlagged'] and granted['isUnlocked']
    second=await page.evaluate('__trialProbe.grant("solar")')
    c['grant_is_idempotent']=not second['newlyGranted']
    star=await page.evaluate('screen="playing";__trialProbe.starEvent()')
    c['star_cast_event_unlock']=star['unlocked'] and not star['preexisting']
    await page.evaluate('__trialProbe.restart()')
    restarted=await page.evaluate('__trialProbe.snapshot()')
    c['trial_does_not_repeat_next_run']='solar' not in restarted['spells']
    c['no_runtime_exceptions']=not outcome['page_errors']
    c['no_external_requests']=not outcome['requests']
    await browser.close()
  outcome['pass']=all(outcome['checks'].values())
  outcome['count']=len(outcome['checks'])
  print(json.dumps(outcome,ensure_ascii=False,indent=2))
  if not outcome['pass']:raise SystemExit(1)

if __name__=='__main__':
  asyncio.run(main())
