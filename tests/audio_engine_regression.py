"""Regression for the offline procedural music and sound engine."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "index.html").read_text(encoding="utf-8")
MARKER = "// Production build: internal debug mutations are test-only and not shipped."
assert SOURCE.count(MARKER) == 1

PROBE = r"""
window.__audioOscillators=0;
const __AudioContext=window.AudioContext||window.webkitAudioContext;
if(__AudioContext){
  const __createOscillator=__AudioContext.prototype.createOscillator;
  __AudioContext.prototype.createOscillator=function(){
    window.__audioOscillators++;
    return __createOscillator.call(this);
  };
}
window.__audioProbe={
  resume:()=>audio?.resume(),
  snapshot:()=>({
    state:audio?.state||'uninitialized',
    oscillators:window.__audioOscillators||0,
    muted:muted,
    musicStep:STUDIO_AUDIO.step
  })
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
        await page.locator("#start").click()
        await page.evaluate("window.__audioProbe.resume()")
        await page.wait_for_timeout(1500)
        state = await page.evaluate("window.__audioProbe.snapshot()")
        report["audio"] = state
        report["checks"]["audio_context_started"] = state["state"] == "running"
        report["checks"]["procedural_music_advances"] = state["musicStep"] >= 2
        report["checks"]["layered_voices_created"] = state["oscillators"] >= 10
        await page.locator("#sound").click()
        muted = await page.evaluate("window.__audioProbe.snapshot()")
        report["checks"]["mute_toggle_works"] = muted["muted"] is True
        report["checks"]["no_runtime_errors"] = not report["page_errors"] and not report["console_errors"]
        report["checks"]["offline_no_external_requests"] = not report["external_requests"]
        report["pass"] = all(report["checks"].values())
        print(report)
        await browser.close()
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
