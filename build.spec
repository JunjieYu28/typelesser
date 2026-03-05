# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Typelesser — produces a single .exe.

Usage (run on Windows):
    pip install -r requirements.txt
    python -m PyInstaller build.spec --clean --noconfirm
"""

import os
import sys

block_cipher = None
project_root = SPECPATH

# ── Collect PySide6 plugins (platforms/qwindows.dll etc.) ─────────────
pyside6_datas = []
pyside6_binaries = []
try:
    import PySide6
    pyside6_dir = os.path.dirname(PySide6.__file__)

    # plugins/ directory (contains platforms/, styles/, imageformats/ …)
    plugins_src = os.path.join(pyside6_dir, "plugins")
    if os.path.isdir(plugins_src):
        pyside6_datas.append((plugins_src, os.path.join("PySide6", "plugins")))

    # Collect all .dll / .pyd next to PySide6 package (Qt6Core.dll etc.)
    for f in os.listdir(pyside6_dir):
        full = os.path.join(pyside6_dir, f)
        if os.path.isfile(full) and f.lower().endswith((".dll", ".pyd")):
            pyside6_binaries.append((full, "PySide6"))
except Exception:
    pass

# ── Collect sounddevice's bundled PortAudio DLLs ──────────────────────
sd_datas = []
try:
    import sounddevice
    sd_dir = os.path.dirname(sounddevice.__file__)
    sd_data_dir = os.path.join(sd_dir, "_sounddevice_data")
    if os.path.isdir(sd_data_dir):
        sd_datas.append((sd_data_dir, "_sounddevice_data"))
except ImportError:
    pass

a = Analysis(
    [os.path.join(project_root, "main.py")],
    pathex=[project_root],
    binaries=pyside6_binaries,
    datas=[
        (os.path.join(project_root, "assets"), "assets"),
    ] + pyside6_datas + sd_datas,
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
    runtime_hooks=[os.path.join(project_root, "runtime_hook_qt.py")],
    excludes=[
        # ── Conflicting Qt binding ────────────────────────────
        "PyQt5",
        "PyQt6",
        # ── Heavy packages not needed at runtime ──────────────
        "matplotlib",
        "tkinter",
        "unittest",
        "test",
        "sphinx",
        "sphinxcontrib",
        "docutils",
        "jedi",
        "parso",
        "IPython",
        "jupyter",
        "jupyter_client",
        "jupyter_core",
        "nbformat",
        "nbconvert",
        "black",
        "blib2to3",
        "yapf",
        "yapf_third_party",
        "pygments",
        "PIL",
        "Pillow",
        "zmq",
        "tornado",
        "babel",
        "lib2to3",
        "setuptools",
        "pkg_resources",
        "psutil",
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
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon=os.path.join(project_root, "assets", "icons", "app.ico"),
    uac_admin=True,
)
