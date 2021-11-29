import os
import site
import PyInstaller.__main__


# TODO: python 3.10 compatibility
path = os.path.dirname(__file__)
PyInstaller.__main__.run([
    os.path.join(path, 'server', 'server.py'),
    '--onefile',
    f'-p={site.getsitepackages()}',
])
