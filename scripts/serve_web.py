#!/usr/bin/env python3
"""Serve the offline Aetherwilds browser game on loopback."""
from __future__ import annotations

import argparse
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
WEB_ROOT = DIST if (DIST / "index.html").is_file() else ROOT


class GameHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def log_message(self, fmt, *args):
        print("[game] " + (fmt % args))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--open", action="store_true", help="open the game in the default browser")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    server = None
    selected_port = None
    for port in range(args.port, min(65536, args.port + 20)):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), GameHandler)
            selected_port = port
            break
        except OSError:
            continue
    if server is None:
        raise SystemExit(f"No free loopback port in {args.port}..{min(65535, args.port + 19)}")

    url = f"http://127.0.0.1:{selected_port}/"
    print(f"Aetherwilds is ready: {url}")
    print("This server is local to this computer. Press Ctrl+C in this window to stop it.")
    if args.open:
        webbrowser.open_new_tab(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Aetherwilds local server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
