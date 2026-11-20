"""Visual regression for seven original creature archetypes and three bespoke bosses."""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
MARKER="// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER)==1
PROBE=r"""
window.__creatureProbe={
 ready:()=>typeof v2buildCreatureCache==='function'&&typeof v2drawCreature==='function'&&typeof v2drawBoss==='function',
 hash:(c)=>{const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let h=2166136261,n=0;for(let i=0;i<d.length;i+=4){h=Math.imul(h^d[i],16777619);h=Math.imul(h^d[i+1],16777619);h=Math.imul(h^d[i+2],16777619);if(d[i+3]>8)n++}return{hash:(h>>>0).toString(16),pixels:n}},
 enemy:(type,time,pose='walk')=>{const old=ctx,age=V2.age,c=document.createElement('canvas');c.width=180;c.height=160;ctx=c.getContext('2d');V2.age=time;const e={type,x:90,y:92,r:({crawler:18,sprout:16,ranged:16,buffer:17,shield:22,gnasher:24,crabladon:33})[type],hp:70,max:100,state:pose==='burrow'?'burrow':pose==='leap'?'leap':pose==='idle'?'idle':'chase',stateT:.27,attack:pose==='attack'?.08:1.2,hitFlash:pose==='hurt'?.15:0,freeze:0,burn:0,corruptT:0,elite:false};v2enemy(e);const out=window.__creatureProbe.hash(c);ctx=old;V2.age=age;return out},
 boss:(id,time,phase=0,heads=1,attackId='')=>{const old=ctx,age=V2.age,c=document.createElement('canvas');c.width=260;c.height=240;ctx=c.getContext('2d');V2.age=time;v2boss({bossId:id,x:130,y:128,r:id==='krog'?60:id==='sol'?52:56,hp:100,max:100,vulnerable:0,hitFlash:0,phaseIndex:phase,headCount:heads,attackInstance:attackId?{id:attackId,stage:'telegraph'}:null});const out=window.__creatureProbe.hash(c);ctx=old;V2.age=age;return out},
 cache:()=>({types:V2_CREATURE_CACHE?Object.keys(V2_CREATURE_CACHE).length:0,poses:V2_CREATURE_CACHE?Object.values(V2_CREATURE_CACHE).map(x=>Object.keys(x).length):[]}),
 sourceChecks:()=>({seven_types:V2_CREATURE_TYPES.length===7,five_poses:V2_CREATURE_POSES.length===5,three_boss_drawers:typeof v2bossSol==='function'&&typeof v2bossKrog==='function'&&typeof v2bossMul==='function',no_random:[String(v2drawCreature),String(v2drawBoss),String(v2buildCreatureCache)].every(x=>!x.includes('Math.random')&&!x.includes('worldRandom'))})
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
  await page.wait_for_function("window.__creatureProbe.ready()",timeout=10000)
  cache=await page.evaluate("()=>{v2buildCreatureCache();return window.__creatureProbe.cache()}")
  report["checks"]["seven_archetypes_cached"]=cache["types"]==7
  report["checks"]["five_poses_each"]=cache["poses"]==[5]*7
  types=["crawler","sprout","ranged","buffer","shield","gnasher","crabladon"];hashes={};poses={}
  for kind in types:
   a=await page.evaluate("(k)=>window.__creatureProbe.enemy(k,1.05,'walk')",kind)
   b=await page.evaluate("(k)=>window.__creatureProbe.enemy(k,1.18,'walk')",kind)
   hashes[kind]=a["hash"];report["checks"][kind+"_visible"]=a["pixels"]>150;report["checks"][kind+"_animated"]=a["hash"]!=b["hash"]
   poses[kind]={}
   for pose in ["idle","walk","attack","hurt"]:
    out=await page.evaluate("([k,p])=>window.__creatureProbe.enemy(k,1.12,p)",[kind,pose]);poses[kind][pose]=out["hash"]
   report["checks"][kind+"_four_poses_distinct"]=len(set(poses[kind].values()))==4
  report["checks"]["seven_distinct_enemy_silhouettes"]=len(set(hashes.values()))==7
  report["enemy_hashes"]=hashes;report["pose_hashes"]=poses
  bosses=["sol","krog","mul"];bh={}
  for boss in bosses:
   out=await page.evaluate("(b)=>window.__creatureProbe.boss(b,2.2)",boss);bh[boss]=out["hash"];report["checks"][boss+"_boss_visible"]=out["pixels"]>500
  report["boss_hashes"]=bh;report["checks"]["three_distinct_boss_silhouettes"]=len(set(bh.values()))==3
  m1=await page.evaluate("window.__creatureProbe.boss('mul',2.2,0,1)");m3=await page.evaluate("window.__creatureProbe.boss('mul',2.2,2,3)")
  k0=await page.evaluate("window.__creatureProbe.boss('krog',2.2)");k1=await page.evaluate("window.__creatureProbe.boss('krog',2.2,1,1,'tongueSmash')")
  report["checks"]["mul_phase_head_growth_visible"]=m1["hash"]!=m3["hash"];report["checks"]["krog_tongue_pose_visible"]=k0["hash"]!=k1["hash"]
  report["checks"].update(await page.evaluate("window.__creatureProbe.sourceChecks()"))
  report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
  report["checks"]["offline_no_external_requests"]=not report["external_requests"]
  report["pass"]=all(report["checks"].values());print(json.dumps(report,ensure_ascii=False,indent=2));await browser.close()
 if not report["pass"]:raise SystemExit(1)
if __name__=="__main__":asyncio.run(main())
