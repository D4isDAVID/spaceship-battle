import os
import sys
import PyInstaller.__main__


path = os.path.dirname(__file__)
add_data_sep = ':' if os.path.sep == '/' else ';'


settings = [
    os.path.join(path, 'client', 'client.py'),
    '--onefile',
    '--hidden-import=entity.bullet',
    f'--add-data={os.path.join(path, "client", "assets")}{add_data_sep}assets',
]


if sys.prefix != sys.base_prefix:
    settings.append(f'-p={os.path.join(path, "venv", "Lib", "site-packages")}')


PyInstaller.__main__.run(settings)
