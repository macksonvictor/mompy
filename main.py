"""Mompy Python entry point.

Phase 10.2 keeps the existing web frontend and prepares the backend Python
layer. Phase 10.3 can expose ``MompyAPI`` to the frontend through pywebview.
"""

from __future__ import annotations

import argparse
import http.server
import socketserver
from pathlib import Path

from backend.api import MompyAPI


ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"


def serve_frontend(port: int = 8770) -> None:
    handler = http.server.SimpleHTTPRequestHandler

    class FrontendHandler(handler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    with socketserver.TCPServer(("127.0.0.1", port), FrontendHandler) as server:
        print(f"Mompy frontend running at http://127.0.0.1:{port}/")
        server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Mompy backend utilities")
    parser.add_argument("--serve", action="store_true", help="serve the frontend locally")
    parser.add_argument("--port", type=int, default=8770, help="local frontend port")
    args = parser.parse_args()

    if args.serve:
        serve_frontend(args.port)
        return

    api = MompyAPI()
    progress = api.get_progress()
    current = api.get_current_mission()
    print("Mompy backend ready.")
    print(f"Current mission: {current['id']} - {current['title']}")
    print(f"Level: {progress['level_info']['label']}")


if __name__ == "__main__":
    main()
