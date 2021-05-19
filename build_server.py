import os
import sys
import PyInstaller.__main__


path = os.path.dirname(__file__)


settings = [
    os.path.join(path, "server", "server.py"),
    '--onefile',
]


if sys.prefix != sys.base_prefix:
    settings.append(f'-p={os.path.join(path, "venv", "Lib", "site-packages")}')


PyInstaller.__main__.run(settings)
