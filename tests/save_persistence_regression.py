"""Real-origin offline startup and persistent wizard-selection regression."""
import asyncio
import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]


async def main():
    report = {"checks": {}, "page_errors": [], "console_errors": [], "external_requests": []}
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            page = await browser.new_page(viewport={"width": 1440, "height": 900})
            page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
            page.on("console", lambda m: report["console_errors"].append(m.text) if m.type == "error" else None)
            page.on("request", lambda r: report["external_requests"].append(r.url) if not r.url.startswith(base) else None)
            await page.goto(base + "/index.html", wait_until="load")
            await page.wait_for_timeout(250)
            report["checks"]["real_origin_launch"] = await page.locator("#start").is_visible()
            await page.locator("#selectCharacter").click()
            await page.locator('[data-character="nyx"]').click()
            stored = await page.evaluate("JSON.parse(localStorage.getItem('spellbrigade_solo_v1'))")
            report["save_before_reload"] = {"schemaVersion": stored.get("schemaVersion"), "selectedCharacterId": stored.get("selectedCharacterId")}
            report["checks"]["selection_written_to_real_storage"] = stored.get("schemaVersion") == 4 and stored.get("selectedCharacterId") == "nyx"
            await page.reload(wait_until="load")
            await page.wait_for_timeout(250)
            await page.locator("#selectCharacter").click()
            classes = await page.locator('[data-character="nyx"]').get_attribute("class")
            report["checks"]["selection_survives_reload"] = "selected" in classes
            await page.locator("#characterStart").click()
            await page.wait_for_timeout(250)
            report["run"] = {
                "hero": await page.locator("#heroName").inner_text(),
                "ability": await page.locator("#abilityIcon").inner_text(),
                "hud": await page.locator("#hud").is_visible()
            }
            report["checks"]["selected_wizard_starts_after_reload"] = report["run"]["hero"] == "Nyx" and report["run"]["ability"] == "☾" and report["run"]["hud"]
            # Corrupt the primary record; the previous valid backup must restore the selected wizard.
            await page.evaluate("localStorage.setItem('spellbrigade_solo_v1','{broken-json')")
            await page.reload(wait_until="load")
            await page.wait_for_timeout(200)
            recovered = await page.evaluate("JSON.parse(localStorage.getItem('spellbrigade_solo_v1'))")
            recovery_archive = await page.evaluate("localStorage.getItem('spellbrigade_solo_v1_recovery')")
            report["save_recovery"] = {"selectedCharacterId": recovered.get("selectedCharacterId"), "archive": recovery_archive}
            report["checks"]["corrupt_primary_recovers_from_backup"] = recovered.get("selectedCharacterId") == "nyx" and bool(recovery_archive)
            # If both copies are corrupt, preserve both raw records and create a valid fresh save.
            await page.evaluate("localStorage.setItem('spellbrigade_solo_v1','not-json');localStorage.setItem('spellbrigade_solo_v1_backup','also-not-json')")
            await page.reload(wait_until="load")
            reset = await page.evaluate("JSON.parse(localStorage.getItem('spellbrigade_solo_v1'))")
            archived = await page.evaluate("JSON.parse(localStorage.getItem('spellbrigade_solo_v1_recovery'))")
            report["checks"]["double_corruption_recovers_to_defaults"] = reset.get("selectedCharacterId") == "aster" and reset.get("schemaVersion") == 4 and archived.get("source") == "primary_and_backup_corrupt"
            report["checks"]["no_runtime_errors"] = not report["page_errors"] and not report["console_errors"]
            report["checks"]["no_external_runtime_requests"] = not report["external_requests"]
            report["pass"] = all(report["checks"].values())
            print(json.dumps(report, ensure_ascii=False, indent=2))
            await browser.close()
    finally:
        server.shutdown()
        server.server_close()
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
