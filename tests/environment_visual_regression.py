"""Deterministic atmosphere, river shimmer, film grain and spell-impact VFX regression."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")
MARKER = "// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER) == 1

PROBE = r"""
window.__environmentProbe = {
 ready: () => [typeof v2riverShimmer,typeof v2ambientWorld,typeof v2filmGrain,typeof v2spellImpact].every(t => t === 'function'),
 render: (kind, time) => {
  const oldCtx=ctx, oldAge=V2.age, off=document.createElement('canvas');
  off.width=640;off.height=480;ctx=off.getContext('2d');V2.age=time;
  if(kind==='ambient')v2ambientWorld(0,0,1200,900);
  else if(kind==='river')v2riverShimmer();
  else if(kind==='grain')v2filmGrain(640,480);
  else if(kind==='beam')v2spellImpact({type:'beam',x:-90,y:-24,tx:110,ty:42,life:.2,max:.4,color:'#8fe5ef'},.42);
  else if(kind==='burst')v2spellImpact({type:'burst',x:0,y:0,r:70,life:.3,max:.6,color:'#e9bd78'},.42);
  else if(kind==='ring')v2spellImpact({type:'ring',x:0,y:0,r:54,life:.3,max:.6,color:'#bd9af0'},.42);
  else if(kind==='slash')v2spellImpact({type:'slash',x:0,y:0,r:60,life:.3,max:.6,color:'#a4e6d5'},.42);
  const data=off.getContext('2d').getImageData(0,0,off.width,off.height).data;
  let hash=2166136261,nonTransparent=0;
  for(let i=0;i<data.length;i+=4){hash=Math.imul(hash^data[i],16777619);hash=Math.imul(hash^data[i+1],16777619);hash=Math.imul(hash^data[i+2],16777619);if(data[i+3]>0)nonTransparent++}
  const out={hash:(hash>>>0).toString(16),nonTransparent};
  ctx=oldCtx;V2.age=oldAge;return out;
 },
 grain: () => ({count:Array.isArray(V2.grain)?V2.grain.length:0,width:V2.grain?.[0]?.width||0,height:V2.grain?.[0]?.height||0}),
 sourceChecks: () => ({
  no_random_calls:[String(v2riverShimmer),String(v2ambientWorld),String(v2filmGrain),String(v2spellImpact)].every(src=>!src.includes('Math.random')&&!src.includes('worldRandom')),
  ambient_connected:String(drawWorld).includes('v2ambientWorld(cx,cy,rw,rh)'),
  film_grain_connected:String(drawWorld).includes('v2filmGrain(w,h)'),
  river_connected:String(drawMapEnvironment).includes('v2riverShimmer()'),
  spell_vfx_connected:String(drawWorld).includes('v2spellImpact(f,')
 })
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
  await page.wait_for_function("window.__environmentProbe.ready()",timeout=10000)
  for kind in ("ambient","river","grain","beam","burst","ring","slash"):
   a=await page.evaluate("(k)=>window.__environmentProbe.render(k,1.13)",kind)
   b=await page.evaluate("(k)=>window.__environmentProbe.render(k,2.71)",kind)
   report.setdefault("renders",{})[kind]={"early":a,"late":b}
   report["checks"][kind+"_renders_visible_pixels"]=a["nonTransparent"]>0 and b["nonTransparent"]>0
   report["checks"][kind+"_animates_deterministically"]=a["hash"]!=b["hash"]
  grain=await page.evaluate("window.__environmentProbe.grain()")
  report["grain"]=grain
  report["checks"]["three_prebaked_grain_frames"]=grain=={"count":3,"width":192,"height":192}
  report["checks"].update(await page.evaluate("window.__environmentProbe.sourceChecks()"))
  report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
  report["checks"]["offline_no_external_requests"]=not report["external_requests"]
  report["pass"]=all(report["checks"].values())
  print(report)
  await browser.close()
 if not report["pass"]:raise SystemExit(1)

if __name__=="__main__":asyncio.run(main())
