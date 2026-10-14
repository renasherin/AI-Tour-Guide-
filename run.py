"""
Unified Single-Localhost Launcher for Incredible Journeys: Discover India with AI.

Starts all services and consolidates everything on a SINGLE localhost:
  http://localhost:3000 (UI, Explorer, AI Guide, API, Swagger Docs)
"""

import sys
import os
import time
import signal
import socket
import urllib.request
import webbrowser
import subprocess
from pathlib import Path

# Ensure UTF-8 output if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def kill_process_on_port(port: int):
    """Gracefully terminate any lingering process holding the specified port on Windows."""
    if os.name != "nt":
        return
    try:
        cmd = f"powershell -Command \"Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess\""
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        pids = set()
        for pid_str in output.splitlines():
            pid_str = pid_str.strip()
            if pid_str and pid_str != "0":
                pids.add(int(pid_str))
        for pid in pids:
            print(f"[!] Freeing port {port} (Terminating PID {pid})...")
            subprocess.run(f"powershell -Command \"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue\"", shell=True)
            time.sleep(1)
    except Exception:
        pass

def wait_for_endpoint(url: str, timeout: int = 40) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(1)
    return False

def main():
    print("=" * 70)
    print("   INCREDIBLE JOURNEYS -- DISCOVER INDIA WITH AI")
    print("   Unified Single-Localhost Production Environment")
    print("=" * 70)

    # 1. Free ports if necessary
    print("\n[*] Initializing runtime ports...")
    kill_process_on_port(8000)
    kill_process_on_port(3000)

    # 2. Start Python FastAPI backend service silently on 127.0.0.1:8000
    print("[1/2] Launching AI & Knowledge RAG Service on 127.0.0.1:8000...")
    backend_env = os.environ.copy()
    backend_env["PYTHONUNBUFFERED"] = "1"
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=str(ROOT_DIR),
        env=backend_env
    )

    # Wait for backend health
    print("      Waiting for AI Vector DB and 639 destinations to mount...")
    wait_for_endpoint("http://127.0.0.1:8000/api/health", timeout=25)

    # 3. Start Next.js frontend unified server on port 3000
    print("[2/2] Launching Unified Editorial Web App on port 3000...")
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    if not (FRONTEND_DIR / "node_modules").exists():
        print("      node_modules not found. Automatically running npm install...")
        subprocess.run([npm_cmd, "install"], cwd=str(FRONTEND_DIR), shell=(os.name == "nt"))

    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=str(FRONTEND_DIR),
        env=os.environ.copy()
    )

    # Wait for unified endpoint
    print("      Connecting reverse proxies on http://localhost:3000...")
    wait_for_endpoint("http://localhost:3000", timeout=35)

    print("\n" + "=" * 70)
    print("   ALL SERVICES UNIFIED ON A SINGLE LOCALHOST:")
    print("   -> Website & Interactive Atlas:   http://localhost:3000")
    print("   -> Destination Explorer:          http://localhost:3000/explore")
    print("   -> AI Tour Guide (RAG):           http://localhost:3000/guide")
    print("   -> Unified Open API:              http://localhost:3000/api/destinations")
    print("   -> Interactive Swagger Docs:      http://localhost:3000/docs")
    print("=" * 70)
    print("\nPress Ctrl+C to terminate the application.\n")

    # Automatically open browser
    try:
        webbrowser.open("http://localhost:3000")
    except Exception:
        pass

    def cleanup():
        print("\n[*] Gracefully stopping Incredible Journeys...")
        try:
            backend_proc.terminate()
        except Exception:
            pass
        try:
            frontend_proc.terminate()
        except Exception:
            pass
        print("[OK] Done. Ports closed cleanly.")
        sys.exit(0)

    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("[!] Backend stopped unexpectedly.")
                cleanup()
            if frontend_proc.poll() is not None:
                print("[!] Frontend stopped unexpectedly.")
                cleanup()
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
