"""Regression for the offline procedural music and sound engine."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")
MARKER = "// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER) == 1

PROBE = r"""
window.__audioOscillators=0;window.__audioNoiseHits=0;
const __AudioContext=window.AudioContext||window.webkitAudioContext;
if(__AudioContext){
  const __createOscillator=__AudioContext.prototype.createOscillator;
  __AudioContext.prototype.createOscillator=function(){
    window.__audioOscillators++;
    return __createOscillator.call(this);
  };
}
const __baseNoiseHit=studioNoiseHit;
studioNoiseHit=function(...args){window.__audioNoiseHits++;return __baseNoiseHit(...args)};
window.__audioProbe={
  resume:()=>audio?.resume(),
  snapshot:()=>({
    state:audio?.state||'uninitialized',
    oscillators:window.__audioOscillators||0,
    muted:muted,
    musicStep:STUDIO_AUDIO.step,
    noiseBufferReady:!!STUDIO_AUDIO.noiseBuffer,
    layers:STUDIO_AUDIO.lastLayers,
    motif:STUDIO_AUDIO.motif
  }),
  bossMix:()=>{
    const oldBoss=game.boss,oldHp=game.player.hp;
    game.boss={dead:false,phaseIndex:2};game.player.hp=game.player.maxHp*.2;
    STUDIO_AUDIO.next=0;STUDIO_AUDIO.step=2;
    const before=window.__audioNoiseHits;studioMusicTick();
    const result={layers:STUDIO_AUDIO.lastLayers,noiseHits:window.__audioNoiseHits-before,motif:STUDIO_AUDIO.motif};
    game.boss=oldBoss;game.player.hp=oldHp;return result;
  }
};
"""
DOCUMENT = SOURCE.replace(MARKER, PROBE + "\n" + MARKER)


async def main():
    report = {"checks": {}, "page_errors": [], "console_errors": [], "external_requests": []}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
        page.on("console", lambda m: report["console_errors"].append(m.text) if m.type == "error" else None)
        page.on("request", lambda r: report["external_requests"].append(r.url) if r.url.startswith(("http://", "https://")) else None)
        await page.set_content(DOCUMENT, wait_until="load")
        # Verify the real button while the menu is unobstructed. During play an
        # upgrade modal correctly takes pointer focus, so the top-bar button is
        # not expected to receive clicks through that modal.
        await page.locator("#sound").click()
        muted_on = await page.evaluate("window.__audioProbe.snapshot()")
        await page.locator("#sound").click()
        muted_off = await page.evaluate("window.__audioProbe.snapshot()")
        report["checks"]["mute_toggle_works"] = muted_on["muted"] is True and muted_off["muted"] is False
        await page.locator("#start").click()
        await page.evaluate("window.__audioProbe.resume()")
        await page.wait_for_timeout(1500)
        state = await page.evaluate("window.__audioProbe.snapshot()")
        report["audio"] = state
        report["checks"]["audio_context_started"] = state["state"] == "running"
        report["checks"]["procedural_music_advances"] = state["musicStep"] >= 2
        report["checks"]["layered_voices_created"] = state["oscillators"] >= 10
        report["checks"]["deterministic_noise_percussion_created"] = state["noiseBufferReady"] is True
        report["checks"]["character_motif_selected"] = state["motif"] in ("aster", "ember", "briar", "nyx")
        mix = await page.evaluate("window.__audioProbe.bossMix()")
        report["boss_mix"] = mix
        report["checks"]["boss_adaptive_layer_activates"] = mix["layers"]["boss"] is True
        report["checks"]["low_health_tension_layer_activates"] = mix["layers"]["tension"] is True
        report["checks"]["boss_mix_uses_character_motif"] = mix["motif"] == "aster"
        report["checks"]["percussion_and_boss_noise_are_scheduled"] = mix["noiseHits"] >= 1 and mix["layers"]["percussion"] is True
        report["checks"]["no_runtime_errors"] = not report["page_errors"] and not report["console_errors"]
        report["checks"]["offline_no_external_requests"] = not report["external_requests"]
        report["pass"] = all(report["checks"].values())
        print(report)
        await browser.close()
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
