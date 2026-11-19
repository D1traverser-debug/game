"""Browser-rendered identity regression for four distinct wizard silhouettes and seven realm landmarks."""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
MARKER="// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER)==1
PROBE=r"""
window.__wizardArtProbe={
 ready:()=>V2_WIZARD_ATLAS_READY&&V2_WIZARD_PACK.naturalWidth===384&&V2_WIZARD_PACK.naturalHeight===384&&typeof v2wizardSprite==='function'&&typeof v2wizardAura==='function',
 hashCanvas:(canvas)=>{const d=canvas.getContext('2d').getImageData(0,0,canvas.width,canvas.height).data;let h=2166136261;for(let i=0;i<d.length;i+=5)h=Math.imul(h^d[i],16777619);return(h>>>0).toString(16)},
 renderStates:()=>{
  const old=ctx,oldAge=V2.age,off=document.createElement('canvas');off.width=220;off.height=220;ctx=off.getContext('2d');V2.age=3.7;
  const out={};
  for(const ch of CHARACTERS){
   out[ch.id]={};
   for(const [state,lastMove,castPulse,abilityPulse,hurtPulse] of [['idle',0,0,0,0],['walk',1,0,0,0],['cast',0,.24,0,0],['ability',0,0,.65,0],['hurt',0,0,0,.2]]){
    ctx.clearRect(0,0,220,220);
    v2hero({characterId:ch.id,x:110,y:116,lastMove,facing:0,invuln:0,ghost:false,castPulse,abilityPulse,hurtPulse});
    out[ch.id][state]=window.__wizardArtProbe.hashCanvas(off);
   }
  }
  ctx=old;V2.age=oldAge;return out;
 },
 render:(kind)=>{
  const old=ctx,oldAge=V2.age,off=document.createElement('canvas');off.width=220;off.height=220;ctx=off.getContext('2d');V2.age=3.7;
  let out={};
  if(kind==='heroes'){
   for(const ch of CHARACTERS){ctx.clearRect(0,0,220,220);v2hero({characterId:ch.id,x:110,y:116,lastMove:0,facing:0,invuln:0,ghost:false});out[ch.id]=window.__wizardArtProbe.hashCanvas(off)}
  }else if(kind==='portraits'){
   for(const ch of CHARACTERS){const portrait=document.createElement('canvas');portrait.width=160;portrait.height=190;drawCharacterPortrait(portrait,ch);out[ch.id]=window.__wizardArtProbe.hashCanvas(portrait)}
  }else{
   const ids=['sunspire','oathgate','moonfen_temple','mossfall_altar','starwell','eastwatch','westshrine'];
   for(const id of ids){ctx.clearRect(0,0,220,220);v2ruin(110,130,1,0,id);out[id]=window.__wizardArtProbe.hashCanvas(off)}
  }
  ctx=old;V2.age=oldAge;return out;
 },
 renderMotion:()=>{
  const old=ctx,oldAge=V2.age,off=document.createElement('canvas');off.width=220;off.height=220;ctx=off.getContext('2d');
  const out={};
  for(const time of [3.7,4.2]){
   V2.age=time;ctx.clearRect(0,0,220,220);
   v2hero({characterId:'aster',x:110,y:116,lastMove:0,facing:0,invuln:0,ghost:false});
   out[String(time)]=window.__wizardArtProbe.hashCanvas(off);
  }
  ctx=old;V2.age=oldAge;return out;
 }
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
  await page.wait_for_function("window.__wizardArtProbe.ready()",timeout=10000)
  heroes=await page.evaluate("window.__wizardArtProbe.render('heroes')")
  portraits=await page.evaluate("window.__wizardArtProbe.render('portraits')")
  landmarks=await page.evaluate("window.__wizardArtProbe.render('landmarks')")
  report["hero_hashes"]=heroes;report["portrait_hashes"]=portraits;report["landmark_hashes"]=landmarks
  report["checks"]["four_distinct_in_world_wizard_renders"]=len(set(heroes.values()))==4
  report["checks"]["four_distinct_selection_portraits"]=len(set(portraits.values()))==4
  states=await page.evaluate("window.__wizardArtProbe.renderStates()")
  report["wizard_action_states"]=states
  report["checks"]["each_wizard_has_visible_walk_pose"]=all(x["idle"]!=x["walk"] for x in states.values())
  report["checks"]["each_wizard_has_visible_cast_pose"]=all(x["idle"]!=x["cast"] for x in states.values())
  report["checks"]["each_wizard_has_visible_ability_pose"]=all(x["cast"]!=x["ability"] for x in states.values())
  report["checks"]["each_wizard_has_visible_hurt_reaction"]=all(x["idle"]!=x["hurt"] for x in states.values())
  report["checks"]["all_four_action_poses_are_distinct"]=all(len({x["idle"],x["walk"],x["cast"],x["ability"]})==4 for x in states.values())
  motion=await page.evaluate("window.__wizardArtProbe.renderMotion()")
  report["motion_hashes"]=motion
  report["checks"]["orbiting_character_vfx_are_animated"]=motion["3.7"]!=motion["4.2"]
  report["checks"]["seven_distinct_landmark_renders"]=len(set(landmarks.values()))==7
  report["checks"]["original_atlas_embedded_and_pose_renderer_connected"]="V2_WIZARD_PACK.src='data:image/avif;base64," in SOURCE and "function v2wizardPose" in SOURCE and "function v2wizardSprite" in SOURCE
  report["checks"]["character_specific_vfx_renderer_connected"]="function v2wizardAura" in SOURCE and "v2wizardAura(ch,a,cast,ability)" in SOURCE
  report["checks"]["simulation_drives_visual_action_pulses"]="p.castPulse=Math.max" in SOURCE and "p.abilityPulse=.65" in SOURCE and "p.hurtPulse=.2" in SOURCE
  report["checks"]["all_landmarks_use_style_specific_geometry"]=all(x in SOURCE for x in ["'sunspire'","'oathgate'","'moonfen_temple'","'mossfall_altar'","'starwell'","'eastwatch'","'westshrine'"])
  report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
  report["checks"]["offline_no_external_requests"]=not report["external_requests"]
  report["pass"]=all(report["checks"].values());print(json.dumps(report,ensure_ascii=False,indent=2));await browser.close()
 if not report["pass"]:raise SystemExit(1)
if __name__=="__main__":asyncio.run(main())
