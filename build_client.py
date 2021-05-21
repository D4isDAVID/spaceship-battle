import os
import site
import PyInstaller.__main__


path = os.path.dirname(__file__)
add_data_sep = ':' if os.path.sep == '/' else ';'
PyInstaller.__main__.run([
    os.path.join(path, 'client', 'client.py'),
    '--onefile',
    f'-p={site.getsitepackages()}',
    f'--add-data={os.path.join(path, "client", "assets")}{add_data_sep}assets',
])
