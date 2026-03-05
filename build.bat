@echo off
REM ── Typelesser Build Script ──────────────────────────────────────
REM Run this on Windows to produce dist\Typelesser.exe
REM Prerequisites: Python 3.10+ installed and on PATH

echo [1/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause
    exit /b 1
)

echo [2/3] Building Typelesser.exe with PyInstaller...
python -m PyInstaller build.spec --clean --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause
    exit /b 1
)

echo [3/3] Done!
echo.
echo    Output: dist\Typelesser.exe
echo    Double-click to run. The app requires administrator privileges
echo    (for global hotkey support).
echo.
pause
