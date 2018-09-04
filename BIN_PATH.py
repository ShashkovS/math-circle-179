import os

START_PATH = r"C:\Users\dirig_000\Dropbox\ВМШ 5-6 2018-2019"
if not os.path.isdir(START_PATH):
    START_PATH = r"C:\Dropbox\ВМШ 5-6 2018-2019\Py_VMSH_2018"

TEXIFY_PATH = r'C:\Users\dirig_000\AppData\Local\Programs\MiKTeX 2.9\miktex\bin\x64\texify.exe'
if not os.path.isfile(TEXIFY_PATH):
    TEXIFY_PATH = r'C:\Full_TeX\texmf\miktex\bin\texify.exe'

GS_PATH = r'C:\Program Files\gs\gs9.22\bin\gswin64c.exe'
if not os.path.isfile(GS_PATH):
    GS_PATH = r'C:\Program Files\gs\gs9.19\bin\gswin64c.exe'
