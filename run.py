"""
LunarLander-v3 D3QN Mission Control Deck.
Launches the backend server and opens as a guaranteed full-screen maximized window (no address bar).

Usage:
    python run.py
"""

import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
import uvicorn
from server import app


def wait_for_server(url: str, timeout: float = 8.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1.0) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.3)
    return False


def kill_stale_app_window():
    """Ensure any zombie Chrome window with our temp profile is closed before a new session starts."""
    try:
        subprocess.run(
            'powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like \'*lunarlander_app_profile*\' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"',
            shell=True,
            capture_output=True,
            timeout=3
        )
    except Exception:
        pass

    temp_profile = os.path.join(tempfile.gettempdir(), "lunarlander_app_profile")
    cache_dir = os.path.join(temp_profile, "Default", "Cache")
    if os.path.exists(cache_dir):
        try:
            shutil.rmtree(cache_dir, ignore_errors=True)
        except Exception:
            pass


def launch_app_window(url: str):
    """
    Launches Chrome or Edge in standalone maximized App Mode in a completely detached process.
    Forces Windows /MAX flag and isolated user profile for guaranteed wide maximized window (no address bar).
    """
    kill_stale_app_window()

    if not wait_for_server(url):
        print("[Desktop App] Server wait timeout. Attempting launch anyway...")

    candidates = [
        # Chrome
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        # Edge (Default on Windows 10/11)
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe"),
    ]

    browser_path = None
    for p in candidates:
        if os.path.isfile(p):
            browser_path = p
            break

    temp_profile = os.path.join(tempfile.gettempdir(), "lunarlander_app_profile")
    flags = f'--app={url} --start-maximized --window-size=1536,864 --window-position=0,0 --disable-http-cache --disk-cache-size=1 --user-data-dir="{temp_profile}"'

    if browser_path:
        print(f"[Desktop App] Launching guaranteed maximized standalone app: {browser_path}")
        cmd_str = f'start "" /max "{browser_path}" {flags}'
        subprocess.Popen(cmd_str, shell=True)
    elif shutil.which("chrome"):
        subprocess.Popen(f'start "" /max chrome {flags}', shell=True)
    elif shutil.which("msedge"):
        subprocess.Popen(f'start "" /max msedge {flags}', shell=True)
    else:
        import webbrowser
        print("[Desktop App] Opening default browser...")
        webbrowser.open(url)


if __name__ == "__main__":
    url = "http://127.0.0.1:8000"

    print("=" * 70)
    print("🚀 LUNARLANDER-V3 D3QN // MISSION CONTROL DECK | Hwihwa Lab")
    print("=" * 70)
    print("🌕 Model Checkpoint : models/best_model.pth (Peak Score: +311.16 Pts)")
    print(f"🖥️  Desktop App Mode : Launching standalone window at {url} (No URL Bar)")
    print("🎮 Control Modes    : Training | Turbo | Stylish Demo | Manual Flight (W/A/D)")
    print("=" * 70)
    print("Press Ctrl+C to terminate.")
    print()

    threading.Thread(target=launch_app_window, args=(url,), daemon=True).start()

    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\n[Mission Control] Shutdown cleanly.")
        sys.exit(0)
