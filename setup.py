from setuptools import setup

APP = ['menubar.py']
DATA_FILES = ['icon.icns']
OPTIONS = {
    "argv_emulation": False,    # <-- FIX: turn this off
    "iconfile": "icon.icns",
    "packages": ["rumps", "pynput", "psutil"],
    "plist": {
        "LSUIElement": True,
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
