from collections import namedtuple
import os
import subprocess
import logging
import xlrd
import pickle
from string import ascii_uppercase
from collections import defaultdict
from functools import lru_cache

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('ВМШ')
from BIN_PATH import *
from CREDENTIALS import *

try:
    START_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
except NameError:
    pass
os.chdir(START_PATH)

# Текущее занятие
cur_les = 1
prev_les = cur_les - 1

# FIRST_TIME_FLOOR, FIRST_TIME_AUD = 'второй этаж', '201'
FIRST_TIME_FLOOR, FIRST_TIME_AUD = None, None  # Пока не печатаем
# Печатать ли на обратной стороне условий инструкцию по регистрации?
ADD_REG_INFO_TO_PRT_PDFS = False

PORTRAIT_ORIENTATION = True
PICT_DIR = r'pictures'

# Разные пути
DUMMY_FOLDER_PATH = r"яdummy_files/"
XLS_CONDUIT_PATH = 'Кондуиты/'
PRINT_PDFS_PATH = 'Текущая печать/'

XLS_CONDUIT_NAME_TEMPLATE = os.path.join(XLS_CONDUIT_PATH, f'Кондуит {cur_les:02}.xlsm')  # Маска имени кондуита
XLS_PREV_CONDUIT_NAME_TEMPLATE = os.path.join(XLS_CONDUIT_PATH, f'Кондуит {prev_les:02}.xlsm')  # Маска имени кондуита
XLS_CONDUIT_SHEET = 'Итог'
CRT_COUNDUIT_COMMAND = '\СделатьКондуитИз{4.4mm}{6mm}'

# Настройки excel'я с кондуитами
FIRST_ROW = 6


def ltr2ind(c): return ascii_uppercase.index(c)


COLUMNS = {'Фамилия': ltr2ind("A"),
           'Имя': ltr2ind("B"),
           'ID': ltr2ind("C"),
           'Клс': ltr2ind("D"),
           'Скрыть': ltr2ind("F"),
           'Уровень': ltr2ind("G"),
           'Аудитория': ltr2ind("O"),
           'Ср3': ltr2ind("M")}

# Настройки префиксов-суффиксов
bas = {'tex_name_template': 'usl-{cur_les:02}-n.tex',
       'prev_tex_name_template': 'usl-{prev_les:02}-n.tex',
       'sol_tex_name_template': 'usl-{cur_les:02}-n-sol.tex',
       'dummy_tex_lesson_template': '{cur_les:02}-lesson-n.tex',
       'dummy_tex_conduit_template': '{cur_les:02}-conduit-n.tex',
       'dummy_tex_prev_conduit_template': '{cur_les:02}-prev_conduit-n.tex',
       'dummy_tex_teacher_template': '{cur_les:02}-teacher-n.tex',
       'prt_pdf_prefix': 'Баз_',
       'prt_en_pdf_prefix': 'n',
       'htmls_path': r'Сайт/Сайт_Баз',
       'htmls_pdfs_template': r'{cur_les:02}-n-lesson.pdf',
       'htmls_htmls_template': r'{cur_les:02}-n-lesson.html',
       'ftp_path': "/",  # /shashkovs.ru/htdocs/www/vmsh/ настроено у пользователя
       'ftp_credentials': FTP_BAS_CRED,
       'excel_level_const': 'н',
       'excel_column_shift': 0,
       'other_excel_level_const': 'нхНХ',
       'spisok_name_template': 'spisok-n-{aud}.tex',
       'pred_spisok_name_template': 'pred_spisok-n-{aud}.tex',
       'main_problems_copies_per_aud': 22,
       'addit_problems_copies_per_aud': 20,
       'teacher_conduit_copies_per_aud': 6,
       'short_eng_level': 'n',
       'json_db_api_url': 'https://www.shashkovs.ru/vmsh/conduit/ajax/ParseJSON.php',
       'json_db_credentials': JSON_DB_BAS_CRED,
       }

pro = {'tex_name_template': 'usl-{cur_les:02}-p.tex',
       'prev_tex_name_template': 'usl-{prev_les:02}-p.tex',
       'sol_tex_name_template': 'usl-{cur_les:02}-p-sol.tex',
       'dummy_tex_lesson_template': '{cur_les:02}-lesson-p.tex',
       'dummy_tex_conduit_template': '{cur_les:02}-conduit-p.tex',
       'dummy_tex_prev_conduit_template': '{cur_les:02}-prev_conduit-p.tex',
       'dummy_tex_teacher_template': '{cur_les:02}-teacher-p.tex',
       'prt_pdf_prefix': 'Про_',
       'prt_en_pdf_prefix': 'p',
       'htmls_path': r'Сайт/Сайт_Про',
       'htmls_pdfs_template': r'{cur_les:02}-p-lesson.pdf',
       'htmls_htmls_template': r'{cur_les:02}-p-lesson.html',
       'ftp_path': "/",  # /shashkovs.ru/htdocs/www/vmsh-a/ настроено у пользователя
       'ftp_credentials': FTP_PRO_CRED,
       'excel_level_const': 'п',
       'excel_column_shift': 31,
       'other_excel_level_const': 'пП',
       'spisok_name_template': 'spisok-p-{aud}.tex',
       'pred_spisok_name_template': 'pred_spisok-p-{aud}.tex',
       'main_problems_copies_per_aud': 14,
       'addit_problems_copies_per_aud': 12,
       'teacher_conduit_copies_per_aud': 4,
       'short_eng_level': 'p',
       'json_db_api_url': 'https://www.shashkovs.ru/vmsh/conduit/ajax/ParseJSON.php',
       'json_db_credentials': JSON_DB_PRO_CRED,
       }
levels = {'н': bas, 'п': pro}
work = (bas, pro)
ADVANCED_LEVEL_CONST = pro['excel_level_const']
PUNCTS = 'абвгдежзиклмнопрст'


@lru_cache()
def def_real_level(xls_level):
    level_search = [wrk['excel_level_const'] for wrk in work if xls_level in wrk['other_excel_level_const']]
    if len(level_search) != 1:
        lg.fatal('Что-то совсем не так с настройками уровня в CONST и xls: ' + xls_level)
        return None
    return level_search[0]


def compile_tex(filename, add_path=''):
    texify_path = TEXIFY_PATH
    texify_path = '"' + texify_path + '"'
    tex_file_path = os.path.join(START_PATH, add_path, filename)
    tex_file_path = '"' + tex_file_path + '"'
    swithches = ('--pdf', '--src-specials',
                 '--tex-option="--tcx=CP1251 --enable-write18 --shell-escape  --interaction=nonstopmode"')  ###
    lg.info('Компилим ' + tex_file_path)
    p = subprocess.Popen(' '.join([texify_path, *swithches, tex_file_path]),
                         cwd=os.path.join(START_PATH, add_path),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, err = p.communicate(timeout=100)

    if b'failed' in err:
        lg.error('Не удалось скомпилировать ' + filename)
        log = open(os.path.join(START_PATH, add_path, filename).replace('.tex', '.log'), 'r', encoding='utf-8',
                   errors='ignore')
        for row in log:
            if row.startswith('! ') or row.startswith('l.'):
                lg.error(row.strip())
        lg.fatal(err.decode('utf-8', errors='ignore').strip())

        return None

    for row in output.splitlines():
        if b'Output written' in row:
            lg.info(row)
            lg.info(row.decode('utf-8'))

            return row.decode('utf-8')


def pdf2png(filename, add_path='', dest=None):
    gs_path = GS_PATH
    gs_path = '"' + gs_path + '"'
    pdf_file_path = os.path.join(START_PATH, add_path, filename)
    pdf_file_path = '"' + pdf_file_path + '"'
    if dest is None:
        dest = filename + '.png'
    swithches = ('-sDEVICE=png16m', '-dTextAlphaBits=4', '-r300', '-o', dest)
    print('Конвертим', filename)
    p = subprocess.Popen(' '.join([gs_path, *swithches, pdf_file_path]),
                         cwd=os.path.join(START_PATH, add_path),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE
                         )
    output, err = p.communicate()
    for row in output.splitlines():
        if b'Page' in row:
            print(row.decode('utf-8'))
    print(err.decode('utf-8'))


# def pdf2png(filename, add_path='', dest=None):
#     gs_path = GS_PATH
#     if not os.path.isfile(gs_path):
#         gs_path = r'C:\Program Files\gs\gs9.19\bin\gswin64c.exe'
#     gs_path = '"' + gs_path + '"'
#     pdf_file_path = os.path.join(START_PATH, add_path, filename)
#     if dest is None:
#         dest = pdf_file_path.replace('.pdf', '.png')
#     swithches = ('-sDEVICE=png16m', '-dTextAlphaBits=4', '-r300', '-o', '"' + pdf_file_path + '"', '-sOutputFile="' + dest + '"')
#     lg.info('Конвертим ' + filename)
#     full_cmd = ' '.join([gs_path, *swithches])
#     p = subprocess.Popen(full_cmd,
#                          cwd=os.path.join(START_PATH, add_path),
#                          stdout=subprocess.PIPE,
#                          stderr=subprocess.PIPE
#                         )
#     output, err = p.communicate(timeout=5)
#     for row in output.splitlines():
#         if b'Page' in row:
#             lg.info(row.decode('utf-8'))
#     if err:
#         lg.error(err.decode('utf-8'))


def cond_color(val):
    if 0 <= val <= 0.5:
        val *= 2
        return (round((1 - val) * 248 + val * 255),
                round((1 - val) * 105 + val * 235),
                round((1 - val) * 107 + val * 132))
    elif 0.5 <= val <= 1:
        val = 2 * val - 1
        return (round((1 - val) * 255 + val * 99),
                round((1 - val) * 235 + val * 190),
                round((1 - val) * 132 + val * 123))
    else:
        print('АААА! Число больше 1')


def parse_xls_conduit(fn):
    """Вычитывает данные из кондуита. Возвращает список постолцовых словарей"""
    lg.info('Открываем файл (займёт время) ' + fn)
    rb = xlrd.open_workbook(fn)
    sheet = rb.sheet_by_index(0)
    res = []
    lg.info('Вычитываем файл ' + fn)
    for rown in range(FIRST_ROW - 1, sheet.nrows):
        d_row = {key: str(sheet.cell(rown, coln).value).strip().replace('.0', '') for key, coln in COLUMNS.items()}
        lg.debug(d_row)
        #  lg.info(d_row)
        if type(d_row['Фамилия']) == str and d_row['Фамилия'].upper() != d_row['Фамилия']:
            d_row['ФИО'] = d_row['Фамилия'].title() + ' ' + d_row['Имя'].title()
            d_row['ФИ.'] = d_row['Фамилия'].title() + ' ' + d_row['Имя'].title()[0] + '.'
            d_row['Строчка'] = rown
            #    d_row['Класс'] =
            res.append(d_row)
    lg.info('Файл вычитан ' + fn)
    return res


def tree():
    return defaultdict(tree)


def read_stats() -> object:
    pickle_dump_path = os.path.join(DUMMY_FOLDER_PATH, 'zstats.pickle')
    try:
        with open(pickle_dump_path, 'rb') as f:
            stats = pickle.load(file=f)
    except FileNotFoundError:
        dd = tree()
        with open(pickle_dump_path, 'wb') as f:
            pickle.dump(dd, file=f)
        stats = dd
    return stats


def update_stats(stats):
    pickle_dump_path = os.path.join(DUMMY_FOLDER_PATH, 'zstats.pickle')
    with open(pickle_dump_path, 'wb') as f:
        pickle.dump(stats, file=f)
