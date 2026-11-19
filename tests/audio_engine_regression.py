"""Regression for adaptive music, ambience, sound bank and independent mixer."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")
MARKER = "// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER) == 1
PROBE = r"""
window.__audioOscillators=0;window.__audioNoiseHits=0;window.__sfxEvents=[];window.__uiEvents=[];
const __AudioContext=window.AudioContext||window.webkitAudioContext;
if(__AudioContext){const __createOscillator=__AudioContext.prototype.createOscillator;__AudioContext.prototype.createOscillator=function(){window.__audioOscillators++;return __createOscillator.call(this)}}
const __baseNoiseHit=studioNoiseHit;studioNoiseHit=function(...args){window.__audioNoiseHits++;return __baseNoiseHit(...args)};
const __basePlaySfx=playSfx;playSfx=function(...args){window.__sfxEvents.push(args);return __basePlaySfx(...args)};
const __basePlayUiSfx=playUiSfx;playUiSfx=function(...args){window.__uiEvents.push(args);return __basePlayUiSfx(...args)};
window.__audioProbe={
 snapshot:()=>({state:audio?.state||'uninitialized',time:audio?.currentTime||0,oscillators:window.__audioOscillators||0,muted,musicStep:STUDIO_AUDIO.step,noiseBufferReady:!!STUDIO_AUDIO.noiseBuffer,ambientNext:STUDIO_AUDIO.ambientNext,layers:STUDIO_AUDIO.lastLayers,motif:STUDIO_AUDIO.motif,volumes:{music:musicVolume,sfx:sfxVolume,ambience:ambienceVolume,ui:uiVolume},sfxEvents:window.__sfxEvents.slice(),uiEvents:window.__uiEvents.slice()}),
 bossMix:()=>{const oldBoss=game.boss,oldHp=game.player.hp;game.boss={dead:false,phaseIndex:2};game.player.hp=game.player.maxHp*.2;STUDIO_AUDIO.next=0;STUDIO_AUDIO.step=2;const before=window.__audioNoiseHits;studioMusicTick();const result={layers:STUDIO_AUDIO.lastLayers,noiseHits:window.__audioNoiseHits-before,motif:STUDIO_AUDIO.motif};game.boss=oldBoss;game.player.hp=oldHp;return result}
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
  await page.locator("#settings").click()
  report["checks"]["settings_screen_opens"]=await page.locator("#settingsScreen.active").count()==1
  for selector,value in [("musicRange",42),("sfxRange",63),("ambienceRange",27),("uiRange",74)]:
   await page.locator("#"+selector).evaluate("(e,v)=>{e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}))}",value)
  mix=await page.evaluate("window.__audioProbe.snapshot()")
  report["mixer"]=mix["volumes"]
  report["checks"]["four_independent_audio_channels"]=mix["volumes"]=={"music":.42,"sfx":.63,"ambience":.27,"ui":.74}
  await page.locator("#audioPreview").click()
  await page.locator("#sound").click()
  muted_on=await page.evaluate("window.__audioProbe.snapshot()")
  await page.locator("#sound").click()
  muted_off=await page.evaluate("window.__audioProbe.snapshot()")
  report["checks"]["master_mute_toggle_works"]=muted_on["muted"] is True and muted_off["muted"] is False
  await page.locator("#settingsBack").click()
  await page.locator("#start").click()
  await page.wait_for_timeout(1700)
  state=await page.evaluate("window.__audioProbe.snapshot()")
  report["audio"]={k:state[k] for k in ("state","time","oscillators","musicStep","noiseBufferReady","ambientNext","motif","volumes")}
  report["checks"]["audio_context_started"]=state["state"]=="running"
  report["checks"]["procedural_music_advances"]=state["musicStep"]>=2
  report["checks"]["layered_voices_created"]=state["oscillators"]>=10
  report["checks"]["deterministic_noise_buffer_created"]=state["noiseBufferReady"] is True
  report["checks"]["ambient_layer_scheduled"]=state["ambientNext"]>state["time"]
  report["checks"]["character_motif_selected"]=state["motif"] in ("aster","ember","briar","nyx")
  await page.evaluate("playSfx('cast','aster');playSfx('impact','fire');playUiSfx('click')")
  events=await page.evaluate("window.__audioProbe.snapshot()")
  report["checks"]["named_combat_sfx_dispatched"]=any(x[0]=="cast" for x in events["sfxEvents"]) and any(x[0]=="impact" for x in events["sfxEvents"])
  report["checks"]["ui_sfx_dispatched"]=any(x[0]=="click" for x in events["uiEvents"])
  boss=await page.evaluate("window.__audioProbe.bossMix()")
  report["boss_mix"]=boss
  report["checks"]["boss_adaptive_layer_activates"]=boss["layers"]["boss"] is True
  report["checks"]["low_health_tension_layer_activates"]=boss["layers"]["tension"] is True
  report["checks"]["boss_mix_uses_character_motif"]=boss["motif"]=="aster"
  report["checks"]["percussion_and_boss_noise_are_scheduled"]=boss["noiseHits"]>=1 and boss["layers"]["percussion"] is True
  report["checks"]["no_runtime_errors"]=not report["page_errors"] and not report["console_errors"]
  report["checks"]["offline_no_external_requests"]=not report["external_requests"]
  report["pass"]=all(report["checks"].values())
  print(report)
  await browser.close()
 if not report["pass"]:raise SystemExit(1)
if __name__=="__main__":asyncio.run(main())
