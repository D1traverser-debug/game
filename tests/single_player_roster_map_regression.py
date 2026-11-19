"""Single-player roster, one-realm navigation and character ability integration."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/"index.html").read_text(encoding="utf-8")
MARKER="// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER)==1
PROBE=r"""
window.__soloProbe={
 roster:()=>CHARACTERS.map(c=>({id:c.id,starter:c.starterSpell,passive:c.passive,ability:c.abilityName,hp:c.hp,move:c.move})),
 selectedCharacter:()=>save.selectedCharacterId,
 layout:()=>{
  const modal=document.querySelector('#characterScreen .character-modal'),grid=document.querySelector('#characterCards'),card=grid?.querySelector('.character-card'),portrait=card?.querySelector('canvas'),map=document.querySelector('#mapPreview'),start=document.querySelector('#characterStart');
  const rect=x=>{const r=x.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom,right:r.right}};
  const inside=(a,b)=>a.x>=b.x-1&&a.y>=b.y-1&&a.right<=b.right+1&&a.bottom<=b.bottom+1;
  return{modal:rect(modal),grid:rect(grid),card:rect(card),portrait:rect(portrait),map:rect(map),start:rect(start),
   portraitPosition:getComputedStyle(portrait).position,mapPosition:getComputedStyle(map).position,
   portraitInsideCard:inside(rect(portrait),rect(card)),mapInsideModal:inside(rect(map),rect(modal)),
   startInsideModal:inside(rect(start),rect(modal)),gridLeftOfMap:rect(grid).right<=rect(map).x+1,
   modalScrollGap:modal.scrollHeight-modal.clientHeight};
 },
 runSnapshot:()=>({characterId:game?.player?.characterId,starter:game?.player?.spells?.[0]?.id,screen}),
 map:()=>({id:WORLD_MAP.id,bounds:WORLD_MAP.bounds,regions:WORLD_MAP.regions.map(x=>x.id),landmarks:WORLD_MAP.landmarks.map(x=>x.id),region:worldRegionAt(-850,-570).id}),
 terrain:()=>({land:worldTerrainAt(0,0).id,stream:worldTerrainAt(800,550).id,bridge:worldTerrainAt(-360,346).id,streamSpeed:worldTerrainAt(800,550).speed}),
 collision:()=>{
  const l=WORLD_MAP.landmarks[0],radius=17,edge=l.solidRadius+radius,actor={x:l.x-edge-4,y:l.y};
  const blockedAtCenter=worldPointBlocked(l.x,l.y,radius);
  worldMoveEntity(actor,20,0,radius);const horizontalBlocked=actor.x<=l.x-edge+0.01;
  const beforeY=actor.y;worldMoveEntity(actor,0,25,radius);const canSlide=actor.y>beforeY;
  const open=worldFindOpenPoint(l.x,l.y,radius,320);
  return{blockedAtCenter,horizontalBlocked,canSlide,relocatedClear:!worldPointBlocked(open.x,open.y,radius),relocatedDistance:Math.hypot(open.x-l.x,open.y-l.y)};
 },
 decorCollision:()=>{
  const prop=game.decor.find(x=>['tree','stone','bush'].includes(x.type));
  if(!prop)return{found:false,colliders:WORLD_DECOR_COLLIDERS.length};
  const collider=WORLD_DECOR_COLLIDERS.find(x=>x.x===prop.x&&x.y===prop.y);
  if(!collider)return{found:false,colliders:WORLD_DECOR_COLLIDERS.length};
  const radius=17,actor={x:prop.x-collider.r-radius-5,y:prop.y},before=actor.x;
  worldMoveEntity(actor,12,0,radius);const blocked=Math.abs(actor.x-before)<.001;
  const yBefore=actor.y;worldMoveEntity(actor,0,20,radius);const wallSlide=actor.y>yBefore;
  const open=worldFindOpenPoint(prop.x,prop.y,radius,220);
  return{found:true,colliders:WORLD_DECOR_COLLIDERS.length,blocked,wallSlide,spawnClear:!worldPointBlocked(open.x,open.y,radius),relocated:Math.hypot(open.x-prop.x,open.y-prop.y)>0};
 },
 ability:(id)=>{
  const ch=CHARACTER_BY_ID[id],p=makePlayer();p.characterId=id;p.x=0;p.y=0;p.hp=Math.max(30,p.maxHp*.35);p.facing=0;p.abilityCd=0;
  const e={id:'test-'+id,type:'crawler',x:155,y:0,r:18,hp:20000,max:20000,dead:false,state:'chase',slow:0,burn:0,acid:0,corrupt:0,freeze:0,hitFlash:0};
  game={player:p,enemies:[e],fx:[],damageNumbers:[],shots:[],hazards:[],plants:[],chests:[],orbs:[],decor:[],ghostImps:[],boss:null,objective:null,damageStates:new WeakMap(),nextCombatantId:1,damageSource:{}};
  const old=coreDamageApi,oldDecor=WORLD_DECOR_COLLIDERS;coreDamageApi=null;WORLD_DECOR_COLLIDERS=[];screen='playing';const before={hp:e.hp,playerHp:p.hp,x:p.x};
  const used=useCharacterAbility();const after={hp:e.hp,playerHp:p.hp,x:p.x,cd:p.abilityCd,burn:e.burn||0,slow:e.slow||0};coreDamageApi=old;WORLD_DECOR_COLLIDERS=oldDecor;
  return {used,before,after,ability:ch.abilityName};
 }
};
"""
DOC=SOURCE.replace(MARKER,PROBE+"\n"+MARKER)
async def main():
 report={"checks":{},"page_errors":[],"console_errors":[],"external_requests":[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  page=await browser.new_page(viewport={"width":1440,"height":900})
  page.on("pageerror",lambda e:report["page_errors"].append(str(e)))
  page.on("console",lambda m:report["console_errors"].append(m.text) if m.type=="error" else None)
  page.on("request",lambda r:report["external_requests"].append(r.url) if r.url.startswith(("http://","https://")) else None)
  await page.set_content(DOC,wait_until="load");await page.wait_for_timeout(450)
  await page.locator("#selectCharacter").click()
  await page.locator("#characterScreen.active").wait_for(state="visible")
  await page.wait_for_function("document.querySelectorAll('#characterCards .character-card').length===4")
  desktopLayout=await page.evaluate("window.__soloProbe.layout()")
  report["character_layout"]=desktopLayout
  report["checks"]["portrait_canvas_stays_inside_card"]=desktopLayout["portraitPosition"]=="static" and desktopLayout["portraitInsideCard"]
  report["checks"]["map_preview_stays_inside_modal"]=desktopLayout["mapPosition"]=="static" and desktopLayout["mapInsideModal"]
  report["checks"]["character_grid_and_map_do_not_overlap"]=desktopLayout["gridLeftOfMap"]
  report["checks"]["primary_start_action_fits_desktop_modal"]=desktopLayout["startInsideModal"]
  report["checks"]["character_screen_opens"]=await page.locator("#characterScreen").is_visible()
  report["checks"]["four_character_cards"]=await page.locator(".character-card").count()==4
  await page.locator('[data-character="ember"]').click()
  report["checks"]["selection_persists"]=await page.evaluate("window.__soloProbe.selectedCharacter()==='ember'")
  report["checks"]["map_preview"]=await page.locator("#mapPreview").evaluate("(c)=>c.width===420&&c.height===315")
  await page.locator("#characterStart").click()
  report["checks"]["selected_character_starts"]=await page.evaluate("(()=>{const x=window.__soloProbe.runSnapshot();return x.characterId==='ember'&&x.starter==='loadedDice'&&x.screen==='playing'})()")
  roster=await page.evaluate("window.__soloProbe.roster()");report["roster"]=roster
  report["checks"]["distinct_starters"]=len({x["starter"] for x in roster})==4
  report["checks"]["distinct_passives"]=len({x["passive"] for x in roster})==4
  report["checks"]["distinct_abilities"]=len({x["ability"] for x in roster})==4
  m=await page.evaluate("window.__soloProbe.map()");report["map"]=m
  report["checks"]["one_bounded_realm"]=m["id"]=="verdant_wilds" and m["bounds"]["width"]==2400 and m["bounds"]["height"]==1800
  report["checks"]["six_districts"]=len(m["regions"])==6
  report["checks"]["seven_landmarks"]=len(m["landmarks"])==7
  terrain=await page.evaluate("window.__soloProbe.terrain()");report["terrain"]=terrain
  report["checks"]["river_slowdown"]=terrain["stream"]=="stream" and abs(terrain["streamSpeed"]-.72)<.001
  report["checks"]["bridge_passage"]=terrain["bridge"]=="bridge"
  report["checks"]["dry_ground"]=terrain["land"]=="ground"
  collision=await page.evaluate("window.__soloProbe.collision()");report["collision"]=collision
  report["checks"]["landmark_blocks_player"]=collision["blockedAtCenter"] and collision["horizontalBlocked"]
  report["checks"]["player_slides_along_landmark"]=collision["canSlide"]
  report["checks"]["spawn_points_avoid_landmarks"]=collision["relocatedClear"] and collision["relocatedDistance"]>0
  decor=await page.evaluate("window.__soloProbe.decorCollision()");report["decor_collision"]=decor
  report["checks"]["decorative_trees_stones_bushes_are_solid"]=decor["found"] and decor["colliders"]>=20 and decor["blocked"]
  report["checks"]["decor_collision_allows_wall_sliding"]=decor["wallSlide"]
  report["checks"]["decor_spawn_relocation"]=decor["spawnClear"] and decor["relocated"]
  report["checks"]["live_minimap"]=await page.locator("#minimap").is_visible()
  abilities={cid:await page.evaluate("(id)=>window.__soloProbe.ability(id)",cid) for cid in ["aster","ember","briar","nyx"]}
  report["abilities"]=abilities
  report["checks"]["aster_nova"]=abilities["aster"]["used"] and abilities["aster"]["after"]["hp"]<abilities["aster"]["before"]["hp"]
  report["checks"]["ember_burn"]=abilities["ember"]["used"] and abilities["ember"]["after"]["hp"]<abilities["ember"]["before"]["hp"] and abilities["ember"]["after"]["burn"]>0
  report["checks"]["briar_heal"]=abilities["briar"]["used"] and abilities["briar"]["after"]["playerHp"]>abilities["briar"]["before"]["playerHp"]
  report["checks"]["nyx_dash"]=abilities["nyx"]["used"] and abilities["nyx"]["after"]["x"]>abilities["nyx"]["before"]["x"] and abilities["nyx"]["after"]["hp"]<abilities["nyx"]["before"]["hp"]
  # A separate narrow viewport verifies the responsive modal and a real start action.
  mobile=await browser.new_page(viewport={"width":390,"height":844},device_scale_factor=1,is_mobile=True,has_touch=True)
  mobile_errors=[];mobile_console=[]
  mobile.on("pageerror",lambda e:mobile_errors.append(str(e)))
  mobile.on("console",lambda m:mobile_console.append(m.text) if m.type=="error" else None)
  await mobile.set_content(DOC,wait_until="load")
  await mobile.locator("#selectCharacter").click()
  await mobile.locator("#characterScreen.active").wait_for(state="visible")
  await mobile.wait_for_function("document.querySelectorAll('#characterCards .character-card').length===4")
  mobile_layout=await mobile.evaluate("window.__soloProbe.layout()")
  report["mobile_character_layout"]=mobile_layout
  report["checks"]["mobile_portraits_and_map_are_in_flow"]=mobile_layout["portraitPosition"]=="static" and mobile_layout["mapPosition"]=="static" and mobile_layout["portraitInsideCard"] and mobile_layout["mapInsideModal"]
  await mobile.locator("#characterStart").scroll_into_view_if_needed()
  await mobile.locator("#characterStart").click()
  report["checks"]["mobile_character_start_reaches_gameplay"]=await mobile.evaluate("window.__soloProbe.runSnapshot().screen==='playing'")
  report["checks"]["mobile_character_select_no_runtime_errors"]=not mobile_errors and not mobile_console
  await mobile.close()
  report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
  report["checks"]["offline"]=not report["external_requests"]
  report["pass"]=all(report["checks"].values());print(json.dumps(report,ensure_ascii=False,indent=2));await browser.close()
 if not report["pass"]:raise SystemExit(1)
if __name__=="__main__":asyncio.run(main())
