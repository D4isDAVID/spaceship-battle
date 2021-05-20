import os
import site
import PyInstaller.__main__


path = os.path.dirname(__file__)
add_data_sep = ':' if os.path.sep == '/' else ';'


settings = [
    os.path.join(path, 'client', 'client.py'),
    '--onefile',
    f'-p={site.getsitepackages()}',
    '--hidden-import=entity.bullet',
    f'--add-data={os.path.join(path, "client", "assets")}{add_data_sep}assets',
]


PyInstaller.__main__.run(settings)
