import os
import site
import PyInstaller.__main__


path = os.path.dirname(__file__)
PyInstaller.__main__.run([
    os.path.join(path, "server", "server.py"),
    '--onefile',
    f'-p={site.getsitepackages()}',
])
