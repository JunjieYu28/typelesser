# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Typelesser — produces a single .exe.

Usage (run on Windows):
    pip install -r requirements.txt
    pyinstaller build.spec
"""

import os
import sys
import importlib

block_cipher = None
project_root = SPECPATH  # SPECPATH is already the directory containing the .spec file

# ── Collect sounddevice's bundled PortAudio DLLs ──────────────────────
sd_datas = []
try:
    import sounddevice
    sd_dir = os.path.dirname(sounddevice.__file__)
    sd_datas = [(os.path.join(sd_dir, "_sounddevice_data"), "_sounddevice_data")]
except ImportError:
    pass

a = Analysis(
    [os.path.join(project_root, "main.py")],
    pathex=[project_root],
    binaries=[],
    datas=[
        (os.path.join(project_root, "assets"), "assets"),
    ] + sd_datas,
    hiddenimports=[
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtSvg",
        "keyboard",
        "sounddevice",
        "numpy",
        "httpx",
        "httpx._transports",
        "httpx._transports.default",
        "httpcore",
        "httpcore._backends",
        "httpcore._backends.sync",
        "anyio",
        "anyio._backends",
        "anyio._backends._asyncio",
        "certifi",
        "h11",
        "sniffio",
        "src",
        "src.app",
        "src.config",
        "src.constants",
        "src.core",
        "src.core.hotkey_manager",
        "src.core.audio_recorder",
        "src.core.transcriber",
        "src.core.polisher",
        "src.core.text_injector",
        "src.core.pipeline",
        "src.core.dictionary_engine",
        "src.data",
        "src.data.database",
        "src.data.models",
        "src.data.repositories",
        "src.ui",
        "src.ui.main_window",
        "src.ui.system_tray",
        "src.ui.floating_status",
        "src.ui.components",
        "src.ui.components.sidebar",
        "src.ui.components.nav_item",
        "src.ui.components.stat_card",
        "src.ui.components.info_card",
        "src.ui.components.history_entry",
        "src.ui.components.dictionary_entry",
        "src.ui.components.tab_bar",
        "src.ui.pages",
        "src.ui.pages.home_page",
        "src.ui.pages.history_page",
        "src.ui.pages.dictionary_page",
        "src.ui.pages.settings_dialog",
        "src.utils",
        "src.utils.audio_utils",
        "src.utils.win32_helpers",
        "src.utils.single_instance",
        "src.utils.logger",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib",
        "tkinter",
        "unittest",
        "test",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="Typelesser",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,              # windowed app, no console
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon=os.path.join(project_root, "assets", "icons", "app.ico"),
    uac_admin=True,             # keyboard library needs admin on Windows
)
