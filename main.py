"""Mompy Python entry point."""

from __future__ import annotations

import argparse
import http.server
import socketserver
from pathlib import Path

from backend.api import MompyAPI


ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"
FRONTEND_INDEX = FRONTEND_DIR / "index.html"


def serve_frontend(port: int = 8770) -> None:
    handler = http.server.SimpleHTTPRequestHandler

    class FrontendHandler(handler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    with socketserver.TCPServer(("127.0.0.1", port), FrontendHandler) as server:
        print(f"Mompy frontend running at http://127.0.0.1:{port}/")
        server.serve_forever()


def print_backend_status() -> None:
    api = MompyAPI()
    progress = api.get_progress()
    current = api.get_current_mission()
    print("Mompy backend ready.")
    print(f"Current mission: {current['id']} - {current['title']}")
    print(f"Level: {progress['level_info']['label']}")


def require_pywebview():
    try:
        import webview
    except ImportError as error:
        raise SystemExit(
            "pywebview is required for desktop mode. "
            "Install it with: python -m pip install -r requirements.txt"
        ) from error
    return webview


def run_desktop(debug: bool = False) -> None:
    webview = require_pywebview()
    if not FRONTEND_INDEX.exists():
        raise SystemExit(f"Frontend not found: {FRONTEND_INDEX}")

    webview.create_window(
        "Mompy",
        FRONTEND_INDEX.as_uri(),
        js_api=MompyAPI(),
        width=1280,
        height=720,
        min_size=(960, 540),
        background_color="#020403",
    )
    webview.start(debug=debug)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mompy Python app")
    parser.add_argument("--serve", action="store_true", help="serve the frontend locally")
    parser.add_argument("--port", type=int, default=8770, help="local frontend port")
    parser.add_argument("--check", action="store_true", help="print backend status and exit")
    parser.add_argument("--debug", action="store_true", help="enable pywebview debug mode")
    args = parser.parse_args()

    if args.serve:
        serve_frontend(args.port)
        return

    if args.check:
        print_backend_status()
        return

    run_desktop(debug=args.debug)


if __name__ == "__main__":
    main()
