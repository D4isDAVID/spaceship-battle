import os
import PyInstaller.__main__


path = os.path.dirname(__file__)


PyInstaller.__main__.run([
    f'{path}\\server\\server.py',
    '--onefile',
    f'-p={path}\\venv\\Lib\\site-packages',
])