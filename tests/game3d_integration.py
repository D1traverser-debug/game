"""Browser integration probes for the new 3D single-file game.

IMPORTANT: these inject a temporary diagnostic into the test-only page. They are
component tests, NOT proof of a real 19-minute player-driven completion.
"""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'index.html').read_text(encoding='utf-8')
MARKER='// Keep the single-player game running without external assets or libraries.'
assert SOURCE.count(MARKER)==1
PROBE=r"""
window.__INTEGRATION={
  gnasher:()=>{
    const e={id:'probe',type:'gnasher',state:'burrow',hp:100,max:100,dead:false,r:20,x:game.player.x+20,y:game.player.y+20};
    game.enemies.push(e); damageEnemy(e,10000,'astral');
    const immune=e.hp===100 && !e.dead;
    e.state='chase';damageEnemy(e,10,'astral');
    return immune && e.hp<100;
  },
  boss:(id)=>{
    game.boss=null;game.enemies=game.enemies.filter(e=>e.type!=='boss');
    const index=BOSS_ARCHETYPES.findIndex(x=>x.id===id);
    if(index<0)return false;
    const original=Math.random;
    Math.random=()=>Math.min(.999,(index+.5)/BOSS_ARCHETYPES.length);
    try{spawnBoss()}finally{Math.random=original}
    for(let i=0;i<12;i++)updateBossEncounter(.05);
    return game.boss?.bossId===id && game.boss?.age>.3;
  },
  objective:(name)=>{
    const types=['fungi','statues','crab','rift','sludge','sacrifice','cores','brazier','beasts'];
    game.seenObjectives=types.filter(x=>x!==name);save.stats.objectives=42;
    const old=Math.random;Math.random=()=>.1;try{startObjective()}finally{Math.random=old}
    const o=game.objective;
    return o?.type===name&&o.target>0&&o.objects.every(x=>Math.abs(x.x)<=1130&&Math.abs(x.y)<=810);
  },
  augments:()=>['loadedDice','tinyTremors','wickedBuzzsaw'].every(id=>SOURCE_AUGMENTS[id]?.length===4)
};
"""
DOCUMENT=SOURCE.replace(MARKER,PROBE+'\n'+MARKER)

async def main():
    result={'checks':{},'errors':[],'external_requests':[]}
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=[
            '--no-sandbox','--disable-dev-shm-usage','--enable-webgl',
            '--ignore-gpu-blocklist','--use-gl=angle',
            '--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader'
        ])
        page=await browser.new_page(viewport={'width':1280,'height':720})
        page.on('pageerror',lambda e:result['errors'].append(str(e)))
        page.on('request',lambda r:result['external_requests'].append(r.url))
        await page.set_content(DOCUMENT,wait_until='domcontentloaded')
        result['checks']['menu']=await page.locator('#menu').is_visible()
        result['checks']['webgl2']=await page.evaluate('window.Game3D?.available===true')
        await page.locator('#start').click()
        result['checks']['playing']=await page.locator('#hud').is_visible()
        result['checks']['gnasher_underground_immunity']=await page.evaluate('window.__INTEGRATION.gnasher()')
        result['checks']['three_1_2_spell_augments']=await page.evaluate('window.__INTEGRATION.augments()')
        for id in ['sol','krog','mul']:
            result['checks']['boss_'+id]=await page.evaluate('(x)=>window.__INTEGRATION.boss(x)',id)
        for id in ['fungi','statues','crab','rift','sludge','sacrifice','cores','brazier','beasts']:
            result['checks']['objective_'+id]=await page.evaluate('(x)=>window.__INTEGRATION.objective(x)',id)
        await page.keyboard.press('Escape')
        result['checks']['pause']=await page.locator('#pause').is_visible()
        await page.keyboard.press('Escape')
        result['checks']['resume']=await page.locator('#hud').is_visible()
        result['checks']['production_debug_absent']=await page.evaluate('typeof window.__QA==="undefined"')
        result['checks']['no_unhandled_errors']=not result['errors']
        result['checks']['offline_requests']=not result['external_requests']
        await browser.close()
    result['all_pass']=all(result['checks'].values())
    result['count']=len(result['checks'])
    result['limitations']=['Test-only state mutation: not a human full-run acceptance.',
       'Shader correctness and artifact topology checked only in software-rendered Chromium.',
       'Offline file:// navigation and persistent browser reload not tested.']
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not result['all_pass']:
        raise SystemExit(1)

if __name__=='__main__':
    asyncio.run(main())
