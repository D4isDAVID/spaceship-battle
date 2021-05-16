import os
import PyInstaller.__main__


path = os.path.dirname(__file__)


add_data_sep = ';'
if os.path.sep == '/':
    add_data_sep = ':'


PyInstaller.__main__.run([
    f'{path}\\client\\client.py',
    '--onefile',
    f'-p=.\\venv\\Lib\\site-packages',
    '--hidden-import=entity.bullet',
    f'--add-data={path}\\client\\assets{add_data_sep}.\\assets',
])