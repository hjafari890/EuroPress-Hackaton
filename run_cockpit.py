"""One-click Python launcher for Europress SMART Web Cockpit.
Works from any folder, automatically detects an open port, opens your browser, and starts the server.
"""
import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Always anchor to the repo root regardless of where it is launched from
CURRENT = Path(__file__).resolve().parent
if (CURRENT / "solution").is_dir():
    ROOT_DIR = CURRENT
else:
    ROOT_DIR = CURRENT.parent

os.chdir(ROOT_DIR)
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "solution" / "backend"))


def find_available_port(preferred=8000):
    for port in [preferred, 8001, 8080, 8081, 8888, 5000]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue
    return preferred


def main():
    port = find_available_port(8000)
    url = f"http://127.0.0.1:{port}"

    print("=" * 68)
    print("  EUROPRESS SMART MATERIAL VALUE ENGINE - DEMO COCKPIT ")
    print("=" * 68)
    print(f"\n[+] Local Server starting on {url} ...")
    print(f"[+] Opening your default web browser to {url} ...")
    print("    (Press Ctrl+C in this window at any time to stop the server)\n")

    # Verify bundle exists
    bundle_path = ROOT_DIR / "solution" / "backend" / "data" / "cockpit_bundle.json"
    if not bundle_path.exists():
        print("[*] Generating cockpit data bundle from competition dataset...")
        from solution.engine.export_cockpit_data import build_cockpit_bundle
        build_cockpit_bundle()

    def open_browser():
        time.sleep(1.0)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    from solution.backend.app import app
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")


if __name__ == "__main__":
    main()
