import os
import PyInstaller.__main__


add_data_sep = ';'
if os.path.sep == '/':
    add_data_sep = ':'


PyInstaller.__main__.run([
    '.\\client\\client.py',
    f'-p=.\\venv\\Lib\\site-packages',
    '--hidden-import=entity.bullet',
    f'--add-data=.\\client\\assets{add_data_sep}.\\assets',
])