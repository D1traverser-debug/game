"""Source-grounded progression regression for the single-file dev artifact.

Runs Chromium with Playwright set_content. Browser navigation is blocked in some
sandboxes, so localStorage is mocked; this is NOT a file:// persistence test.
"""
import asyncio, json, pathlib, re, shutil
from playwright.async_api import async_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]
RAW=(ROOT/'index.html').read_text(encoding='utf8')
assert RAW.count('<script>') in (1,2)
assert RAW.count('// Input\naddEventListener')==1
PROBE='''
window.__TEST={
 dump:()=>({level:game?.player.level,slots:game?.player.spells.length,spells:game?.player.spells.map(s=>({id:s.id,level:s.level})),opts:game?.pending?.opts?.map(o=>o.kind),reason:game?.pending?.reason}),
 put:(level,ids)=>{let p=game.player;p.level=level;p.spells=ids.map(id=>({...spells.find(s=>s.id===id),level:1,cdNow:0,infusions:[],augments:[]}));game.pending=null;game.pendingSpellBonus=null;game.pendingLevels=0;document.querySelectorAll('.screen').forEach(e=>e.classList.remove('active'));$('hud').classList.add('active');screen='playing'},
 offers:()=>{offerUpgrade('level');return window.__TEST.dump()},
 cap:l=>allowedSpellSlots(l),
 cast:id=>{let p=game.player,s={...spells.find(t=>t.id===id),level:1,cdNow:0,infusions:[],augments:[]};let e=game.enemies.find(x=>!x.dead);e.x=p.x+140;e.y=p.y;e.hp=e.max=99999;game.shots=[];game.hazards=[];fireSpell(s);return {shots:game.shots.length,hazards:game.hazards.length,faces:game.hazards.map(h=>h.face),timers:game.hazards.map(h=>h.timer)}}
};
'''
MOCK="<script>window.__memoryStore=window.__memoryStore||{};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>window.__memoryStore[k]??null,setItem:(k,v)=>window.__memoryStore[k]=String(v)}});</script>"
DOCUMENT=RAW.replace('<script>',MOCK+'<script>',1).replace('// Input\naddEventListener',PROBE+'// Input\naddEventListener',1)

async def run():
 checks={};errors=[]
 async with async_playwright() as pw:
  opts={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
  binary=shutil.which('chromium') or shutil.which('chromium-browser')
  if binary:opts['executable_path']=binary
  browser=await pw.chromium.launch(**opts)
  page=await browser.new_page(viewport={'width':1280,'height':720})
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.set_content(DOCUMENT,wait_until='domcontentloaded')
  save=await page.evaluate("JSON.parse(localStorage.getItem('spellbrigade_solo_v1'))")
  checks['starter_unlocks']=set(save['unlocks'])=={'astral','loadedDice','tinyTremors','wickedBuzzsaw'}
  checks['schema_v2']=save['schemaVersion']==2
  await page.locator('#start').click()
  checks['only_reginald_starter']=await page.evaluate("window.__TEST.dump().spells[0].id==='astral'&&window.__TEST.dump().slots===1")
  b=[[1,1],[2,2],[12,2],[13,3],[19,3],[20,4]]
  checks['level_caps']=True
  for v in b: checks['level_caps'] &= await page.evaluate('(x)=>window.__TEST.cap(x[0])===x[1]',v)
  await page.evaluate('window.__TEST.put(12,["astral","loadedDice"])')
  checks['level12_no_third']=not any(k=='newSpell' for k in (await page.evaluate('window.__TEST.offers()'))['opts'])
  await page.evaluate('window.__TEST.put(13,["astral","loadedDice"])')
  checks['level13_third']=(await page.evaluate('window.__TEST.offers()'))['opts'][0]=='newSpell'
  await page.locator('#upCards .card').first.click()
  d=await page.evaluate('window.__TEST.dump()')
  checks['third_initial_lv3_and_bonus']=d['slots']==3 and d['spells'][-1]['level']==3 and d['reason']=='newSpellBonus'
  await page.locator('#upCards .card').first.click()
  checks['third_bonus_applied']=(await page.evaluate('window.__TEST.dump()'))['spells'][-1]['level']==4
  await page.evaluate('window.__TEST.put(19,["astral","loadedDice","tinyTremors"])')
  checks['level19_no_fourth']=not any(k=='newSpell' for k in (await page.evaluate('window.__TEST.offers()'))['opts'])
  await page.evaluate('window.__TEST.put(20,["astral","loadedDice","tinyTremors"])')
  checks['level20_fourth']=(await page.evaluate('window.__TEST.offers()'))['opts'][0]=='newSpell'
  await page.locator('#upCards .card').first.click()
  d=await page.evaluate('window.__TEST.dump()')
  checks['fourth_initial_lv4_and_bonus']=d['slots']==4 and d['spells'][-1]['level']==4 and d['reason']=='newSpellBonus'
  await page.evaluate('window.__TEST.put(20,["astral"])')
  dice=await page.evaluate('window.__TEST.cast("loadedDice")')
  tremor=await page.evaluate('window.__TEST.cast("tinyTremors")')
  saw=await page.evaluate('window.__TEST.cast("wickedBuzzsaw")')
  checks['dice_attack']=dice['hazards']==1 and 1<=dice['faces'][0]<=6
  checks['tremor_attack']=tremor['hazards']==4 and len(set(tremor['timers']))==4
  checks['buzzsaw_attack']=saw['shots']==1
  await page.evaluate("localStorage.setItem('spellbrigade_solo_v1',JSON.stringify({schemaVersion:1,gold:173,runs:4,stats:{kills:999999},unlocks:['astral','missile','solar']}))")
  await page.set_content(DOCUMENT,wait_until='domcontentloaded')
  old=await page.evaluate("JSON.parse(localStorage.getItem('spellbrigade_solo_v1'))")
  checks['legacy_unlock_migrated_mock']=set(old['unlocks'])=={'astral','loadedDice','tinyTremors','wickedBuzzsaw'}
  checks['legacy_gold_stats_preserved_mock']=old['gold']==173 and old['runs']==4 and old['stats']['kills']==999999
  checks['no_browser_errors']=not errors
  await browser.close()
 print(json.dumps({'checks':checks,'passed':sum(checks.values()),'total':len(checks),'all_pass':all(checks.values()),'errors':errors,'limitations':['localStorage is mocked; actual file:// close/reopen NOT_TESTED','level 2 for second slot is unverified temporary assumption','tests are component/integration, not full player-driven run']},ensure_ascii=False,indent=2))
 if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':asyncio.run(run())
