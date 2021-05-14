import PyInstaller.__main__


PyInstaller.__main__.run([
    '.\\server\\server.py',
    f'-p=.\\venv\\Lib\\site-packages',
    '--onefile',
])