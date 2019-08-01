from z_CONSTS import *
from z_helpers import *
import os
import numpy as np  # numpy
import xlwt  # xlwt
from time import time
from plus_reader.plus_reader import prc_list_of_files

np.set_printoptions(linewidth=200)
START_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
os.chdir(START_PATH)

VERBOSE = False

res_prefix = '../'
path = '.'
os.chdir(path)


def unmark_useless_cells(filled_cells):
    # Лично у нас первая и последняя строка, а также нулевой и второй столбец отмечать не нужно
    filled_cells[filled_cells[:, 2] == False, :] = False
    filled_cells[:, 0] = False
    filled_cells[0, :] = False
    filled_cells[-1, :] = False
    return filled_cells


def remove_useless_cells(filled_cells):
    # Лично у нас первая и последняя строка, а также первый столбец не нужны
    # Кроме того, вовсе удалим строки, в которых не заполнена фамилия.
    filled_cells = filled_cells[1:-1, 1:]
    filled_cells = filled_cells[filled_cells[:, 1] == True, :]
    filled_cells = np.delete(filled_cells, 1, axis=1)  # Здесь столбец с фамилией
    print('*' * 100)
    print(filled_cells.astype(int))
    print('*' * 100)
    return filled_cells


def gen_hdr(cur_les, lvl, prob_num, punt_num=0):
    return f'{cur_les:02}{lvl}.' + ('Н' if prob_num == 0 else (f'{prob_num:02}' + ('' if not punt_num else PUNCTS[punt_num - 1])))


def fill_xls_header(sheet, stats):
    pass


def join_recognized_and_xlsx(recognized_pages, xlsx_data, stats):
    auds = sorted({x['Аудитория'] for x in xlsx_data if '100' <= x['Аудитория'] <= '999'})
    with open(os.path.join(START_PATH, 'results.csv'), 'w') as f:
        for page, aud in zip(recognized_pages, sorted(auds)):
            f.write('vvvvvvvvvvvvvvv {}\n'.format(aud))
            for row in page:
                f.write('\t'.join(map(str, row.astype(np.int8))).replace('0', ''))
                f.write('\n')
            f.write('^^^^^^^^^^^^^^^ {}\n\n'.format(aud))

    min_row = min(x['Строчка'] for x in xlsx_data) - 1
    max_row = max(x['Строчка'] for x in xlsx_data)
    excel_aud_lists = []
    for aud in auds:
        cur_names = sorted((x for x in xlsx_data if x['Аудитория'] == aud and x['Скрыть'] in (None, 0, '0', '', 0.0, '0.0')),
                           key=lambda x: x['ФИО'].lower().replace('ё', 'е'))
        excel_aud_lists.append(cur_names)
    # Ок, теперь recognized_pages --- список распознанных таблиц, а paper_lists --- список школьников с доп. инфо
    assert (len(recognized_pages) == len(excel_aud_lists))

    for aud, plus_page, excel_aud in zip(auds, recognized_pages, excel_aud_lists):
        for rownum, row in enumerate(plus_page):
            try:
                excel_aud[rownum]['Результат'] = list(row.astype(np.int8))
            except IndexError:
                max_row += 1
                excel_aud.append({'ФИО': '???',
                                  'Аудитория': aud,
                                  'Скрыть': 0,
                                  'Строчка': max_row,
                                  'Уровень': excel_aud[0]['Уровень'],
                                  'Результат': list(row.astype(np.int8))
                                  })
                xlsx_data.append(excel_aud[-1])
    xlsx_data.sort(key=lambda x: (x['Строчка']))
    #
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Results', cell_overwrite_ok=True)
    fill_xls_header(sheet, stats)
    sheet.col(0).width = 5500
    sheet.col(1).width = 1500
    sheet.col(2).width = 1500
    sheet.col(3).width = 1500
    for clmn in range(4, 4 + 31 * 2):
        sheet.col(clmn).width = 600
    sheet.write(min_row, 0, 'ФИО')
    sheet.write(min_row, 1, 'Ауд')
    sheet.write(min_row, 2, 'Скр')
    sheet.write(min_row, 3, 'Уров')
    for coln in range(0, 31):
        sheet.write(min_row, coln + 4, gen_hdr(cur_les, 'н', coln) + ('*' if coln > 0 else ''))
    for coln in range(0, 31):
        sheet.write(min_row, coln + 4 + 31, gen_hdr(cur_les, 'п', coln) + ('*' if coln > 0 else ''))
    # Дозаполняем шапку
    if stats and stats[cur_les]['н']['структура']:  # ХАРДКОД!
        cur_col = 5
        cur_prob = 1
        cur_punct = 0
        for c in stats[cur_les]['н']['структура']:
            if c == 'к' and cur_punct > 0:
                cur_punct = 0
                cur_prob += 1
            elif c == 'к':
                sheet.write(min_row, cur_col, gen_hdr(cur_les, 'н', cur_prob, cur_punct))
                cur_prob += 1
                cur_col += 1
            elif c == 'п':
                cur_punct += 1
                sheet.write(min_row, cur_col, gen_hdr(cur_les, 'н', cur_prob, cur_punct))
                cur_col += 1
    if stats and stats[cur_les]['п']['структура']:  # ХАРДКОД!
        cur_col = 5 + 31
        cur_prob = 1
        cur_punct = 0
        for c in stats[cur_les]['п']['структура']:
            if c == 'к' and cur_punct > 0:
                cur_punct = 0
                cur_prob += 1
            elif c == 'к':
                sheet.write(min_row, cur_col, gen_hdr(cur_les, 'п', cur_prob, cur_punct))
                cur_prob += 1
                cur_col += 1
            elif c == 'п':
                cur_punct += 1
                sheet.write(min_row, cur_col, gen_hdr(cur_les, 'п', cur_prob, cur_punct))
                cur_col += 1

        pass

    for item in xlsx_data:
        rown = item['Строчка']
        sheet.write(rown, 0, item['ФИО'])
        sheet.write(rown, 1, item['Аудитория'])
        sheet.write(rown, 3, item['Уровень'])
        if item['Скрыть'] not in (None, 0, '0', '', 0.0, '0.0'):
            sheet.write(rown, 2, 'x')
        try:
            col_mov = int(levels[item['Уровень']]['excel_column_shift'])  # Вот здесь бы поправить
        except KeyError:
            col_mov = 0
        if 'Результат' in item and item['Результат']:
            # print('foo', item['Результат'])
            for clmn, res in enumerate(item['Результат']):
                if res:
                    sheet.write(rown, clmn + col_mov + 4, 1)
    save_dest = os.path.join(START_PATH, '..', 'Сканы кондуитов', 'results.xls')
    lg.info('Сохраняем результат в ' + save_dest)
    workbook.save(save_dest)


if __name__ == '__main__':
    stt = time()
    PDF_FILENAME = os.path.join('..', 'Сканы кондуитов', 'Scan{:02}.pdf'.format(cur_les))
    recognized_pages = prc_list_of_files(PDF_FILENAME, black_threshold=240,
                                         unmark_useless_cells_func=unmark_useless_cells,
                                         remove_useless_cells_func=remove_useless_cells)
    import pickle
    with open('recognized.pickle', 'wb') as f:
        pickle.dump(recognized_pages, file=f)
    print('Done in ', time() - stt)
    # with open('recognized.pickle', 'rb') as f:
    #     recognized_pages = pickle.load(file=f)

    os.chdir(r"..")
    xlsx_data = parse_xls_conduit(XLS_CONDUIT_NAME)

    stats = read_stats()
    join_recognized_and_xlsx(recognized_pages, xlsx_data, stats)
