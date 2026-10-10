import os
import sys
import tempfile
import urllib.request
import subprocess
import threading

def get_current_executable_path() -> str:
    """Returns absolute path of the currently running .exe or python script."""
    if getattr(sys, "frozen", False):
        return os.path.abspath(sys.executable)
    return os.path.abspath(__file__)

def download_update_binary(download_url: str, progress_callback=None) -> str:
    """
    Downloads the new .exe binary to a temp directory and reports progress percentage.
    """
    temp_dir = tempfile.gettempdir()
    target_path = os.path.join(temp_dir, "AwakePulse_New.exe")

    def report(count, block_size, total_size):
        if total_size > 0 and progress_callback:
            percent = int(count * block_size * 100 / total_size)
            progress_callback(min(percent, 100))

    req = urllib.request.Request(download_url, headers={"User-Agent": "AwakePulse-Updater"})
    with urllib.request.urlopen(req, timeout=30) as response, open(target_path, "wb") as out_file:
        total = int(response.headers.get("Content-Length", 0))
        block_size = 8192
        downloaded = 0
        while True:
            buffer = response.read(block_size)
            if not buffer:
                break
            out_file.write(buffer)
            downloaded += len(buffer)
            if total > 0 and progress_callback:
                pct = int(downloaded * 100 / total)
                progress_callback(min(pct, 100))

    return target_path

def apply_update_and_restart(new_exe_path: str):
    """
    Spawns a tiny helper batch script that waits for current app to exit,
    replaces old .exe with new .exe, and launches the updated app.
    """
    current_exe = get_current_executable_path()
    batch_file = os.path.join(tempfile.gettempdir(), "update_swap.bat")

    batch_content = f"""@echo off
timeout /t 1 /nobreak > nul
:retry
move /y "{new_exe_path}" "{current_exe}" > nul
if errorlevel 1 (
    timeout /t 1 /nobreak > nul
    goto retry
)
start "" "{current_exe}"
del "%~f0"
"""
    with open(batch_file, "w") as f:
        f.write(batch_content)

    # Launch batch script in hidden background and exit current app
    subprocess.Popen(["cmd.exe", "/c", batch_file], creationflags=0x08000000)
    sys.exit(0)
