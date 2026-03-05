"""PyInstaller runtime hook — set Qt plugin paths before anything imports PySide6."""

import os
import sys

if getattr(sys, "frozen", False):
    base = sys._MEIPASS
    # Tell Qt where to find platform plugins (qwindows.dll, etc.)
    plugin_path = os.path.join(base, "PySide6", "plugins")
    if os.path.isdir(plugin_path):
        os.environ["QT_PLUGIN_PATH"] = plugin_path
    # Explicit platform plugin path as fallback
    plat_path = os.path.join(plugin_path, "platforms")
    if os.path.isdir(plat_path):
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plat_path
