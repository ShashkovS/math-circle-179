import os

PY_PROJ_DIR_PATH = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
START_PATH = os.path.realpath(os.path.join(PY_PROJ_DIR_PATH, '..'))

texify_path_to_try = [
    os.path.expandvars(r'%LocalAppData%\Programs\MiKTeX 2.9\miktex\bin\x64\texify.exe'),
    os.path.expandvars(r'%LocalAppData%\MiKTeX 2.9\miktex\bin\x64\texify.exe'),
    os.path.expandvars(r'%UserProfile%\MiKTeX 2.9\miktex\bin\x64\texify.exe'),
    os.path.expandvars(r'%ProgramFiles%\MiKTeX 2.9\miktex\bin\x64\texify.exe'),
    os.path.expandvars(r'%ProgramFiles(x86)%\MiKTeX 2.9\miktex\bin\x64\texify.exe'),
    r'C:\Full_TeX\texmf\miktex\bin\texify.exe',
    r'C:\ShashkovTeX\Full_TeX\texmf\miktex\bin\texify.exe',
    r'C:\ShashkovsTeX\Full_TeX\texmf\miktex\bin\texify.exe',
]

ghostscript_path_to_try = [
    *[os.path.expandvars(r'%ProgramFiles%\gs\gs{:0.2f}\\bin\gswin64c.exe'.format(i / 100)) for i in range(910, 1090)],
    *[os.path.expandvars(r'%ProgramFiles(x86)%\gs\gs{:0.2f}\\bin\gswin64c.exe'.format(i / 100)) for i in range(910, 1090)],
    r'C:\Drobpox\Foo\Boo\Zoo\Py_VMSH_5-6_2019',
    r'C:\Full_TeX\gs\gs9.19\bin\gswin64c.exe',
    r'C:\ShashkovTeX\Full_TeX\gs\gs9.19\bin\gswin64c.exe',
    r'C:\ShashkovsTeX\Full_TeX\gs\gs9.19\bin\gswin64c.exe',
    r'C:\Full_TeX\gs\gs9.22\bin\gswin64c.exe',
    r'C:\ShashkovTeX\Full_TeX\gs\gs9.22\bin\gswin64c.exe',
    r'C:\ShashkovsTeX\Full_TeX\gs\gs9.22\bin\gswin64c.exe',
]

for file in texify_path_to_try:
    if os.path.isfile(file):
        TEXIFY_PATH = file
        break
else:
    raise ValueError('Укажите правильный путь в конце списка texify_path_to_try в файле z_BIN_PATH.py')

for file in ghostscript_path_to_try:
    if os.path.isfile(file):
        GS_PATH = file
        break
else:
    raise ValueError('Укажите правильный путь в конце списка ghostscript_path_to_try в файле z_BIN_PATH.py')
