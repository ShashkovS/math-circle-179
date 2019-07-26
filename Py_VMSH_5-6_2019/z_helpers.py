import subprocess
import xlrd
import pickle
from collections import defaultdict
from functools import lru_cache
from z_CONSTS import *
from z_BIN_PATH import *
import logging
import re
import sys
import zlib

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('ВМШ')

os.chdir(START_PATH)


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
    output, err = p.communicate(timeout=20)

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
    lg.info('Конвертим ' + filename + ' в ' + filename.replace('pdf', 'png'))
    p = subprocess.Popen(' '.join([gs_path, *swithches, pdf_file_path]),
                         cwd=os.path.join(START_PATH, add_path),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE
                         )
    output, err = p.communicate()
    for row in output.splitlines():
        if b'Page' in row:
            lg.info(row.decode('utf-8'))
    for row in err.splitlines():
        lg.error(row.decode('utf-8'))


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


def check_ids_unique(res):
    lg.info('Проверяем уникальность ID')
    ids = {}
    error_found = False
    for i, row in enumerate(res):
        orig_id = str(row['ID'])
        dig_id = re.sub(r'[^0-9]', '', orig_id)[-4:].lstrip('0')
        if not dig_id:
            lg.error(
                'В строке {} находится ID школьника `{}`, в котором нет ненулевых цифр. Они нужны!'.format(i + FIRST_ROW,
                                                                                                         orig_id))
            error_found = True
        if dig_id in ids:
            lg.error('В строках {} и {} находятся «одинаковые» ID `{}` и `{}`. Правые 4 цифры должны быть уникальны'.format(
                ids[dig_id] + FIRST_ROW, i + FIRST_ROW, res[ids[dig_id]]['ID'], orig_id))
            error_found = True
        ids[dig_id] = i
        res[i]['IDd'] = dig_id.zfill(4)
    return error_found


def check_no_level_intersection(res):
    aud_types = {}
    error_found = False
    for i, row in enumerate(res):
        if not row['Фамилия'] or row['Скрыть'] not in (None, 0, '0', '', 0.0, '0.0'):
            continue
        id, level, aud = row['ID'], row['Уровень'], row['Аудитория']
        level_name = levels[level]['name']
        if aud not in aud_types:
            aud_types[aud] = (i, id, level)
        else:
            old_i, old_id, old_level = aud_types[aud]
            if old_level != level:
                lg.error('В строках {} и {} находятся школьники с разным уровнем, но в одной и той же аудитории {}. '
                         'ID школьников {} и {}'.format(old_i + FIRST_ROW, i + FIRST_ROW, aud, old_id, id))
                error_found = True
    return error_found


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
    err1 = check_ids_unique(res)
    err2 = check_no_level_intersection(res)
    if err1 or err2:
        lg.error('')
        lg.error('В кондуите есть критические ошибки. Введите "отстрелим-ноги", чтобы продолжить\n')
        choice = input()
        if choice.strip().lower() != 'отстрелим-ноги':
            sys.exit()
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


def crt_aud_barcode(aud, ids):
    from pdf417gen import encode, render_image
    ELEM_LEN = 4
    assert ELEM_LEN == 4  # Иначе переделывать нужно
    HASH_CONST = [197, 3, 150, 172]
    data_d = [id.zfill(ELEM_LEN)[-ELEM_LEN:] for id in ids]
    to_save_s = str(aud).zfill(ELEM_LEN) + ''.join(data_d)
    to_save_b = to_save_s.encode()
    control_summ_b = bytes([sum([x * HASH_CONST[i] % 256 for x in to_save_b[i::4]]) % 256 for i in range(4)])
    to_save_b += control_summ_b
    to_save_z = zlib.compress(to_save_b)
    codes = encode(to_save_z, columns=28, security_level=5)
    image = render_image(codes, scale=1, padding=0)
    image.save(os.path.join(DUMMY_FOLDER_PATH, BARCODES, 'barcode_{}.png'.format(aud)))


def parse_tex_template(path):
    block_finder = re.compile(r'(?sm)^%block (\w+)[^\n]*\n(.*)?^%block \1[^\n]*\n')
    with open(path, 'r', encoding='windows-1251') as f:
        tex = f.read()
    tex = tex.replace('{', '{{').replace('}', '}}')
    tex = re.sub(r'<<(\w+)>>', r'{\1}', tex)
    return dict(block_finder.findall(tex))