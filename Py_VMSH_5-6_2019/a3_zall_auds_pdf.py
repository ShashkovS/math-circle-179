# Здесь мы собираем всё, собранное в a3_prt_pdfs.py в части листов формата А4 в один огроооомный pdf
# -*- coding: utf-8 -*-.
from z_CONSTS import *
from z_helpers import *
from pathlib import Path
from PyPDF2 import PdfFileReader
import os

to_print = [
    ('104', 'н', 12),
    ('201', 'н', 18),
    ('202', 'п', 18),
    ('203', 'н', 18),
    ('205', 'н', 18),
    ('207', 'н', 18),
    ('209', 'н', 18),
    ('301', 'п', 18),
    ('302', 'п', 18),
    ('303', 'п', 18),
    ('305', 'н', 18),
    ('307', 'н', 18),
    ('309', 'н', 16),
    ('316', 'н', 18),
    ('405', 'н', 30),
    # ('424', 'н', 1),
]

# Здесь лютый хардкод
ppath = Path(PRINT_PDFS_PATH)
usls = [p.name for p in ppath.glob('*_1_*.pdf')]
dops = [p.name for p in ppath.glob('*_2_*.pdf')]
conds = [p.name for p in ppath.glob('*_3_*.pdf')]
teachs = [p.name for p in ppath.glob('*_4_*.pdf')]

BLANK_PAGE = '"Разное\\blank_page.pdf" 1-1 '


def get_num_pages(filename, cache={}):
    if filename not in cache:
        cache[filename] = PdfFileReader(open(os.path.join('Текущая печать', filename), 'rb')).getNumPages()
    return cache[filename]


def add_blank_if_needed(filename):
    pages = get_num_pages(filename)
    return '' if pages % 2 == 0 else BLANK_PAGE


# Каждая пачка начинается с кондуита аудитории, 1 лист
# Затем кондуиты преподавателей, 2-3 листа
# Затем основные условия, порядка 10 листов
# Затем доп. задачи, порядка 4 листов
# И так для каждой аудитории

level_counter = {lvl: 0 for aud, lvl, pups in to_print}
commands_to_run = []
for aud, lvl, pups in to_print:
    pgs = level_counter[lvl]
    take = 0 if lvl == 'н' else 1
    usl = usls[take]
    dop = dops[take]
    cond = conds[take]
    teach = teachs[take]
    sol = f'..\\usl-{prev_les:02}-{["n", "p"][take]}-sol.pdf'
    cmd_part = f'.\\cpdf.exe '
    cond_part = f'"{cond}" {1 + 2 * pgs}-{2 + 2 * pgs} '
    teacher_parf = f'"{teach}" {1 + 2 * pgs}-{2 + 2 * pgs} ' * (2 + take)
    main_tasks = (f'"{usl}" ' + add_blank_if_needed(usl)) * ((pups + 1) // 2)
    dop_tasks = (f'"{dop}" ' + add_blank_if_needed(dop)) * (((pups - 1) // 4) + (lvl=='п'))
    sol_part = f'"{sol}" ' + add_blank_if_needed(sol)
    tail_part = f'  AND -compress -squeeze -o {aud}.pdf'
    # if aud == '405':
    #     cond_part = f'"{cond}" {1 + 2 * pgs}-{8 + 2 * pgs} '
    #     teacher_parf = f'"{teach}" {1 + 2 * pgs}-{8 + 2 * pgs} '
    #     dop_tasks = f'"{dop}" 1-1 "Разное\\blank_page.pdf" 1-1 ' * ((pups-10) // 4)
    commands_to_run.append(' '.join([cmd_part, cond_part, sol_part, teacher_parf, main_tasks, dop_tasks, tail_part]))
    level_counter[lvl] += 1

commands_to_run.append('.\\cpdf.exe ' + ' '.join(f'{aud}.pdf' for aud, lvl, pups in to_print) + ' AND -compress -squeeze  -o _all_all_all.pdf ')

print('\n'.join(commands_to_run))
pwd = os.getcwd()
try:
    os.chdir(ppath)
    for cmd in commands_to_run:
        print(os.system(cmd))
finally:
    os.chdir(pwd)
