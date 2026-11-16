import asyncio, json, time
from pathlib import Path
from playwright.async_api import async_playwright

HTML = Path("experiments/webgl-slice.html").read_text(encoding="utf-8")

async def main():
    report = {"webgl2": False, "page_errors": [], "console_errors": [], "external_requests": []}
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--no-sandbox", "--enable-webgl", "--ignore-gpu-blocklist",
                "--use-gl=angle", "--use-angle=swiftshader-webgl",
                "--enable-unsafe-swiftshader"
            ]
        )
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
        page.on("console", lambda m: report["console_errors"].append(m.text) if m.type == "error" else None)
        page.on("request", lambda q: report["external_requests"].append(q.url))
        await page.set_content(HTML, wait_until="domcontentloaded")
        report["webgl2"] = await page.evaluate("!!document.querySelector('canvas').getContext('webgl2')")
        await page.locator("#start").click()
        await page.wait_for_timeout(1500)
        report["baseline"] = await page.evaluate("window.__sliceDebug()")
        report["stress_spawned"] = await page.evaluate("window.__sliceSetEnemies(200)")
        t0 = time.monotonic()
        await page.wait_for_timeout(5000)
        report["stress_wall_seconds"] = time.monotonic() - t0
        report["stress"] = await page.evaluate("window.__sliceDebug()")
        await browser.close()
    report["technical_smoke_pass"] = (
        report["webgl2"] and not report["page_errors"] and
        not report["console_errors"] and not report["external_requests"] and
        report["stress"]["glError"] == 0 and report["stress"]["state"] == "playing"
    )
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
