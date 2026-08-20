"""
Resolves the correct directories for the app, whether it's
running as a normal Python script or as a frozen PyInstaller exe.

- RESOURCE_DIR: where bundled, read-only files live (config,
  templates, assets). Uses sys._MEIPASS when frozen, which
  correctly points to wherever PyInstaller actually placed
  bundled data (handles the "_internal" folder used by newer
  PyInstaller versions automatically).

- BASE_DIR: where the app should read/write its own runtime
  output (generated posters, prompt history). Always the folder
  the real .exe lives in, so output persists next to it.
"""

import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESOURCE_DIR = BASE_DIR