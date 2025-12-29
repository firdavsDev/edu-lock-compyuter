import os
import platform
import shutil
import sys


def enable_autostart(app_name: str):
    system = platform.system()

    # ❌ faqat Windows uchun
    if system != "Windows":
        return

    # PyInstaller bo‘lmagan paytda himoya
    exe_path = sys.executable
    if not exe_path.lower().endswith(".exe"):
        return

    startup_dir = os.path.join(
        os.environ.get("APPDATA", ""),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )

    if not os.path.exists(startup_dir):
        return

    target = os.path.join(startup_dir, f"{app_name}.exe")

    if not os.path.exists(target):
        shutil.copy(exe_path, target)
