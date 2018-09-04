# -*- coding: utf-8 -*-.
import xlrd
from CONSTS import *
import pyperclip  # pip install pyperclip
import re
import os
from Levenshtein import distance  # python-Levenshtein
import numpy as np
import matplotlib.pyplot as plt
import shelve
np.set_printoptions(precision=4, threshold=np.nan, linewidth=np.nan, suppress=True)

# with shelve.open('compare_shelve.dmp', writeback=True) as shelve_data:
#     equals_lst, non_equals_lst, known_pairs = shelve_data['vmsh vs vmsha']
# equals_lst = [('01.13', '12а.12а'), ('02.01', '02а.01'), ('02.10', '02а.11'), ('02.11', '02а.10'), ('03.11', '03а.06'), ('03.12', '03а.07'), ('04.07в', '04а.03а'), ('04.07г', '04а.03б'), ('04.07г', '05а.06'), ('04.10', '04а.06'), ('04.11', '04а.07'), ('05.11', '04а.12'), ('06.10', '06а.06'), ('06.11', '06а.09'), ('07.10', '06а.08'), ('08.09а', '07а.07а'), ('08.09б', '07а.07б'), ('09.03', '09а.01'), ('09.06а', '09а.04а'), ('09.06б', '09а.04б'), ('09.06в', '09а.04в'), ('09.08а', '09а.08а'), ('09.08б', '09а.08б'), ('09.09', '08а.08'), ('09.10', '09а.03'), ('09.11', '09а.11'), ('10.02в', '10а.01'), ('10.06', '10а.03'), ('10.09', '10а.09'), ('10.10', '10а.05'), ('11.03', '11а.01'), ('11.05', '11а.04'), ('11.11а', '10а.06а'), ('11.11б', '10а.06б'), ('12.03', '12а.01а'), ('12.06а', '11а.06а'), ('12.08', '11а.09'), ('12.09а', '12а.08а'), ('12.09б', '12а.08б'), ('12.10а', '12а.09а'), ('12.10б', '12а.09б'), ('12.11', '11а.11'), ('13.02', '13а.01'), ('13.04', '13а.03'), ('13.05б', '13а.04'), ('13.06', '12а.07'), ('13.10', '13а.07'), ('13.11', '13а.10'), ('14.02', '14а.01'), ('14.03', '14а.03'), ('14.08', '13а.05'), ('14.09', '13а.09'), ('14.10', '14а.09'), ('14.11', '14а.10'), ('04.12а', '04а.08а'), ('04.12б', '04а.08б'), ('15.03', '15а.01'), ('15.06', '14а.06'), ('15.07', '14а.05'), ('15.09', '15а.05'), ('15.10', '14а.02'), ('15.11', '15а.06'), ('15.12', '15а.09'), ('16.03', '16а.02'), ('16.05', '15а.04'), ('16.06', '16а.03'), ('16.07', '16а.04'), ('16.08', '15а.03'), ('16.09', '16а.06'), ('16.10а', '15а.07а'), ('16.10б', '15а.07б'), ('16.11', '16а.09'), ('16.12', '16а.08'), ('17.01', '17а.01'), ('17.05', '17а.02'), ('17.06', '17а.03'), ('17.10', '17а.06'), ('17.11', '17а.07'), ('17.12', '17а.08'), ('18.02', '18а.01'), ('18.03', '18а.02'), ('18.05', '18а.03'), ('18.06', '18а.05'), ('18.08', '18а.08'), ('18.09а', '18а.06а'), ('18.09б', '18а.06б'), ('18.09в', '18а.06в'), ('18.10', '18а.10'), ('18.11', '18а.04'), ('18.12', '18а.12а'), ('19.03', '19а.01'), ('19.05', '19а.04'), ('19.06а', '19а.02а'), ('19.06б', '19а.02б'), ('19.07', '06а.02'), ('19.09', '18а.07'), ('19.10а', '19а.07а'), ('19.10б', '19а.07б'), ('20.05', '20а.01'), ('20.06', '19а.06'), ('20.08', '20а.02'), ('20.09', '19а.05'), ('20.10', '20а.07'), ('20.11', '20а.06'), ('21.03', '21а.01'), ('21.05а', '21а.02а'), ('21.05б', '21а.02б'), ('21.06', '21а.04'), ('21.08', '21а.05'), ('21.09', '21а.06'), ('22.03', '22а.01'), ('22.04', '22а.03'), ('22.05', '22а.05'), ('22.06а', '22а.06а'), ('22.06б', '22а.06б'), ('22.08', '22а.04'), ('22.09', '22а.08'), ('22.10', '22а.09'), ('23.07', '23а.04'), ('23.09в', '23а.09в'), ('23.10', '23а.08'), ('23.11', '23а.07'), ('23.09а', '23а.09а'), ('23.09б', '23а.09б'), ('24.06а', '24а.06а'), ('24.06б', '24а.06б'), ('24.06в', '24а.06в'), ('24.06д', '24а.06г'), ('24.09а', '24а.03а'), ('24.09б', '24а.03б'), ('24.09в', '24а.03в'), ('24.10а', '24а.08а'), ('24.10б', '24а.08б'), ('25.06а', '25а.02а'), ('25.06б', '25а.02б'), ('25.11', '25а.10'), ('26.01а', '25а.03а'), ('26.01б', '25а.03б'), ('26.01в', '25а.03в'), ('26.01г', '25а.03г'), ('26.01д', '25а.03д'), ('26.04а', '25а.01а'), ('26.04б', '25а.01б'), ('26.05', '26а.07'), ('26.06а', '26а.06а'), ('26.06б', '26а.06б'), ('26.06в', '26а.06в'), ('26.06г', '26а.06г'), ('26.06д', '26а.06д'), ('26.08', '26а.02'), ('26.09а', '26а.08а'), ('26.09б', '26а.08б'), ('26.09в', '26а.08в'), ('26.10', '25а.07'), ('26.11', '26а.04'), ('26.12а', '26а.09а'), ('26.12б', '26а.09б'), ('27.03', '27а.01'), ('27.05', '27а.04'), ('27.08а', '26а.01а'), ('27.08б', '26а.01б'), ('27.08в', '26а.01в'), ('27.09', '26а.05'), ('27.10б', '27а.06'), ('27.11', '27а.07'), ('27.12а', '27а.12а'), ('27.12б', '27а.12б'), ('27.12в', '27а.12в'), ('30.06а', '30а.01а'), ('30.06б', '30а.01б'), ('30.06в', '30а.01в'), ('30.08', '30а.03а'), ('30.09', '30а.04'), ('30.11', '30а.05'), ('31.10', '31а.08'), ('31.11', '31а.03'), ('31.12', '31а.05'), ('25.08', '32а.06а'), ('32.02а', '32а.01а'), ('32.02б', '32а.01б'), ('32.07', '32а.03'), ('32.09', '32а.06б'), ('32.10', '32а.09')]
# with shelve.open('compare_shelve.dmp', writeback=True) as shelve_data:
#     shelve_data['vmsh vs vmsha'] = (equals_lst, non_equals_lst, known_pairs)
# exit()

def parse_excel():
    # cur_les = 32
    xls_filename = XLS_CONDUIT_PATH + 'Кондуит {:02}.xlsx'
    print('Читаем файл', xls_filename)
    rb = xlrd.open_workbook(xls_filename.format(cur_les))
    sheet = rb.sheet_by_index(0)

    HEADER_ROW = 2
    FIRST_ROW = 3
    SURNAME_COLUMN = 0
    NAME_COLUMN = 1
    VISIT_POSTFIX = '.Н'
    STAT_CONST = 'СТАТИСТИКА'
    ADVANCED_SUFFIX = 'а'
    PREV_PROB_SUC_SIGN = 'd'
    PREV_PROB_PRICE = 0.5
    problem_regexp = re.compile(r'\d+[aа]?\.\d+[а-я]?')

    visit_cols = []
    visit_heads = []
    cols_to_heads = {}
    heads_to_cols = {}
    for coln in range(sheet.ncols):
        cur_head = sheet.cell(HEADER_ROW, coln).value
        if isinstance(cur_head, str) and cur_head.replace('H', 'Н').endswith(VISIT_POSTFIX):
            visit_cols.append(coln)
            visit_heads.append(cur_head.replace('H', 'Н').replace(VISIT_POSTFIX, '').replace(ADVANCED_SUFFIX, ''))
        elif isinstance(cur_head, str) and problem_regexp.fullmatch(cur_head):
            # это -- заголовок задачи. Отлично!
            cols_to_heads[coln] = cur_head
            heads_to_cols[cur_head] = coln
    assert len(cols_to_heads) == len(heads_to_cols)
    num_problems = len(cols_to_heads)

    # И да, нам нужен список школьников
    pup_row_to_name = {}
    for rown in range(FIRST_ROW, sheet.nrows):
        if sheet.cell(rown, SURNAME_COLUMN).value not in ('', STAT_CONST):
            pup_row_to_name[rown] = sheet.cell(rown, SURNAME_COLUMN).value + ' ' + sheet.cell(rown, NAME_COLUMN).value
    num_pupils = len(pup_row_to_name)
    # Итак, у нас есть заголовки всех столбцов.
    # Теперь нужно сделать сложную штуку: если школьник был на занятии, то все несданные задачи должны получить 0,
    # все сданные — 1, а те, что он не решал -- np.nan
    data = np.empty((num_pupils, num_problems))
    data[:, :] = np.nan
    # Обходим все задачи и всех школьников
    col_head_to_npdata_coln = {}
    for i, rown in enumerate(sorted(pup_row_to_name)):
        for j, coln in enumerate(sorted(cols_to_heads)):
            col_head_to_npdata_coln[cols_to_heads[coln]] = j
            # Определяем, был ли школьник на данном занятии
            cur_cell_val = sheet.cell(rown, coln).value
            if cur_cell_val in (1, 1.0, '1', '1.0'):
                data[i, j] = 1
            elif cur_cell_val in (PREV_PROB_SUC_SIGN, ):
                data[i, j] = PREV_PROB_PRICE
            else:
                vis_col_num = max(x for x in visit_cols if x < coln)  # Ну да, медленно. И хрен с ним
                vis_val = sheet.cell(rown, vis_col_num).value
                if vis_val in (1, 1.0, '1', '1.0'):
                    data[i, j] = 0
                else:
                    data[i, j] = np.nan
    return sheet, visit_cols, visit_heads, cols_to_heads, heads_to_cols, data, col_head_to_npdata_coln

sheet, visit_cols, visit_heads, cols_to_heads, heads_to_cols, data, col_head_to_npdata_coln = parse_excel()

# Отлично, теперь в data хороший плюсник
# Но есть проблема, некоторые задачи у начинающих и у продолжающих одинаковые
# Это нужно учесть
def retreive_and_ask_for_equals():
    def parse_list(list_text):
        list_text = list_text.replace(r'\%', ' ')
        list_text = re.sub(r'%.*$', r'', list_text, flags=re.MULTILINE)
        list_text = re.sub(r'^.*\\begin\{document\}', r'', list_text, flags=re.DOTALL)
        list_text = re.sub(r'\\end\{document\}.*$', r'', list_text, flags=re.DOTALL)
        original = list_text

        list_text = re.sub(r'\\putpicts\{.*?\}\{.*?\}\{(.*?)\}(\{.*?\}){0,2}', '', list_text)
        list_text = re.sub(r'\\onlyput\{(.*?)\}\{.*?\}\{(.*?)\}', '', list_text)
        list_text = re.sub(r'\\rightpicture\{(.*?)\}\{.*?\}\{.*?\}\{(.*?)\}', '', list_text)
        list_text = re.sub(r'\\leftpicture\{(.*?)\}\{.*?\}\{.*?\}\{(.*?)\}', '', list_text)
        list_text = re.sub(r'\\righttikzw\{(.*?)\}\{.*?\}\{.*?\}\{(.*?)\}', '', list_text)
        list_text = re.sub(r'\\righttikz\{(.*?)\}\{.*?\}\{(.*?)\}', '', list_text)
        list_text = re.sub(r'\\lefttikzw\{(.*?)\}\{.*?\}\{.*?\}\{(.*?)\}', '', list_text)
        list_text = re.sub(r'\\lefttikz\{(.*?)\}\{.*?\}\{(.*?)\}', '', list_text)
        list_text = re.sub(r'\\includegraphics(\[.*?\])?\{(.*?)\}', '', list_text)

        list_text = list_text.replace(r'\ВосстановитьГраницы', '')
        list_text = list_text.replace(r'\УстановитьГраницы', '')
        list_text = list_text.replace(r'\УстановитьГраницы', '')
        list_text = list_text.replace(r'\пункт', '')
        list_text = list_text.replace('\\"е', 'ё').replace('\\"Е', 'Ё')
        list_text = list_text.lower()
        list_text = list_text.replace('~', ' ')
        list_text = list_text.replace('ё', 'е')
        list_text = list_text.replace(r'\s*\times\s*', ' х ')
        list_text = re.sub(r'\\кзадача', 'КОНЕЦЗАДАЧИ', list_text)
        list_text = re.sub(r'\\[а-я]{0,2}задачан?', 'НАЧАЛОЗАДАЧИ', list_text)
        original = re.sub(r'\s*\\кзадача', 'КОНЕЦЗАДАЧИ', original, flags=re.DOTALL)
        original = re.sub(r'\\[а-я]{0,2}задачан?\s*', 'НАЧАЛОЗАДАЧИ', original, flags=re.DOTALL)
        list_text = re.sub(r'\s+', ' ', list_text)
        list_text = re.sub(r'[^а-яА-Я0-9 ]', ' ', list_text)
        list_text = re.sub(r'\s+', ' ', list_text)
        only_problems = re.findall(r'(?<=НАЧАЛОЗАДАЧИ ).*?(?=КОНЕЦЗАДАЧИ)', list_text, flags=re.DOTALL)
        only_problems_orig = re.findall(r'(?<=НАЧАЛОЗАДАЧИ).*?(?=КОНЕЦЗАДАЧИ)', original, flags=re.DOTALL)
        if len(only_problems) != len(only_problems_orig):
            print('#' * 100)
            print(list_text)
            print('#' * 100)
            print(original)
            print('#' * 100)
            f = 1/0

        return only_problems, only_problems_orig

    print('Вычитываем тексты задача')
    bas_problems = {}
    pro_problems = {}
    bas_orig_problems = {}
    pro_orig_problems = {}
    for list_num in range(1, cur_les + 1):
        for (suffix, destination, dest_orig, key_sfx) in [(bas.dummy_suffix, bas_problems, bas_orig_problems, ''),
                                                          (pro.dummy_suffix, pro_problems, pro_orig_problems, 'а')]:
            res_name = '{:02}{}{}.tex'.format(list_num, suffix, 'lesson')
            with open(os.path.join(DUMMY_FOLDER_PATH, res_name), 'r', encoding='windows-1251') as f:
                list_text = f.read()
            parsed_problems, parsed_orig_problems = parse_list(list_text)
            for prob_num, text in enumerate(parsed_problems):
                destination[('{:02}' + key_sfx + '.{:02}').format(list_num, prob_num + 1)] = text
            for prob_num, text in enumerate(parsed_orig_problems):
                dest_orig[('{:02}' + key_sfx + '.{:02}').format(list_num, prob_num + 1)] = text

    # Ок, теперь у нас есть мега-словать задач
    # Нужно определить, какие задачи общие
    print('Начинаем попарное сравнение задач')
    # Попарно сравниваем каждую старую и каждую новую задачу
    bas_keys = sorted(bas_problems)
    pro_keys = sorted(pro_problems)
    cross = [[0] * len(pro_keys) for _ in range(len(bas_keys))]
    # equals_lst, non_equals_lst, known_pais = [], [], set()
    # with open('bas_pro_equals.dmp', 'wb') as f:
    #     pickle.dump((equals_lst, non_equals_lst, known_pais), f)
    # with open('bas_pro_equals.dmp', 'rb') as f:
    #     (equals_lst, non_equals_lst, known_pairs) = pickle.load(f)
    #     print('База вычитана')
    with shelve.open('compare_shelve.dmp', writeback=True) as shelve_data:
        equals_lst, non_equals_lst, known_pairs = shelve_data['vmsh vs vmsha']
        print('База вычитана')

    equals_lst = [(x, y.replace('a', 'а')) for (x, y) in equals_lst]
    non_equals_lst = [(x, y.replace('a', 'а')) for (x, y) in non_equals_lst]
    known_pairs = {(x, y.replace('a', 'а')) for (x, y) in known_pairs}

    equals = []
    non_equals = []
    for i, bkey in enumerate(bas_keys):
        for j, pkey in enumerate(pro_keys):
            cross[i][j] = distance(bas_problems[bkey], pro_problems[pkey])
            cross[i][j] /= (len(bas_problems[bkey]) + len(pro_problems[pkey])) / 2
            if cross[i][j] < 0.65:
                if (bkey, pkey) not in known_pairs:
                    print('\n' * 2 + '*' * 140)
                    print('*' * 70, '{:.2f}'.format(cross[i][j]), '*' * 70)
                    print(bkey)
                    print(bas_orig_problems[bkey])
                    print('='*50)
                    print(pkey)
                    print(pro_orig_problems[pkey])
                    print('*' * 140)
                    eq_add = input('Ну что, {}={}?'.format(bkey, pkey))
                    if eq_add:
                        if eq_add.lower() in ('д', 'да', 'y', 'yes'):
                            equals.append('{}={}'.format(bkey, pkey))
                        elif '=' in eq_add:
                            equals.append(eq_add)
                    else:
                        non_equals.append('{}={}'.format(bkey, pkey))
                    known_pairs.add((bkey, pkey))
    if equals:
        equals_lst += [tuple(eq.split('=')) for eq in ((';'.join(equals)).replace(' ', '').split(';'))]
    if non_equals:
        non_equals_lst += [tuple(eq.split('=')) for eq in ((';'.join(non_equals)).replace(' ', '').split(';'))]

    with shelve.open('compare_shelve.dmp', writeback=True) as shelve_data:
        shelve_data['vmsh vs vmsha'] = (equals_lst, non_equals_lst, known_pairs)
        print('База обновлена')


    def check_eqs():
        for bkey, pkey in equals_lst:
            x, y = bkey, pkey
            if x[-1].isalpha():
                x = x[:-1]
            if y[-1].isalpha():
                y = y[:-1]
            print('\n' * 2 + '*' * 140)
            print(bkey)
            print(bas_orig_problems[x])
            print('=' * 50)
            print(pkey)
            print(pro_orig_problems[y])
            print('*' * 140)
            x = input()

    return equals_lst

equals_lst = retreive_and_ask_for_equals()


# Так, некоторые задачи дополнительные.
# Будем помечать их нулями (школьник мог решить, но не решил) только если
# а) либо школьник сдал хотя бы одну дополнительную задачу этого листка
# б) либо решил 80% обязательных задач
# Итак, сначала нужно для каждого занятия добыть кол-во обязательных
def rtv_dop_problems_dict():
    def parse_list_for_dops(list_text):
        list_text = list_text.replace(r'\%', ' ')
        list_text = re.sub(r'%.*$', r'', list_text, flags=re.MULTILINE)
        list_text = re.sub(r'^.*\\begin\{document\}', r'', list_text, flags=re.DOTALL)
        list_text = re.sub(r'\\end\{document\}.*$', r'', list_text, flags=re.DOTALL)
        list_text = re.sub(r'Дополнительные задачи', r'\допраздел', list_text, flags=re.DOTALL)
        list_text = re.sub(r'\\допраздел.*$', r'', list_text, flags=re.DOTALL)
        list_text = re.sub(r'\\кзадача', 'КОНЕЦЗАДАЧИ', list_text)
        list_text = re.sub(r'\\[а-я]{0,2}задачан?', 'НАЧАЛОЗАДАЧИ', list_text)
        return list_text.count('НАЧАЛОЗАДАЧИ')

    num_dops = {}
    for list_num in range(1, cur_les + 1):
        for suffix, key_sfx in [(bas.dummy_suffix, ''), (pro.dummy_suffix, 'а')]:
            res_name = '{:02}{}{}.tex'.format(list_num, suffix, 'lesson')
            with open(os.path.join(DUMMY_FOLDER_PATH, res_name), 'r', encoding='windows-1251') as f:
                list_text = f.read()
            dops = parse_list_for_dops(list_text)
            num_dops['{:02}{}'.format(list_num, key_sfx)] = dops
    return num_dops


num_dops = rtv_dop_problems_dict()
# sheet, visit_cols, visit_heads, cols_to_heads, heads_to_cols, data, col_head_to_npdata_coln
def fix_data_for_dop_prob():
    ADDIT_THRESHOLD = 0.6
    for list_num in range(1, cur_les + 1):
        for key_sfx in ['', 'а']:
            key = '{:02}{}'.format(list_num, key_sfx)
            # Найдём множество столбцов с обязательными задачами
            mandat_probs = [coln for head, coln in col_head_to_npdata_coln.items()
                            if head.split('.')[0].lstrip('0') == key.lstrip('0') and
                               int(re.sub(r'\D', '', head.split('.')[1])) <= num_dops[key]]
            addit_probs = [coln for head, coln in col_head_to_npdata_coln.items()
                            if head.split('.')[0].lstrip('0') == key.lstrip('0') and
                               int(re.sub(r'\D', '', head.split('.')[1])) > num_dops[key]]
            no_add_positives = np.sum(data[:, addit_probs], axis=1) == 0
            few_mandatory = np.sum(data[:, mandat_probs], axis=1) < (ADDIT_THRESHOLD * len(mandat_probs))
            rows_to_nan = few_mandatory & no_add_positives
            # print(key, mandat_probs, addit_probs, np.sum(rows_to_nan))
            local_threshold = ADDIT_THRESHOLD * len(mandat_probs)
            for rown in range(data.shape[0]):
                if data[rown, addit_probs].sum() == 0 and data[rown, mandat_probs].sum() < local_threshold:
                    # У школьника в дополнительных задачах стоят все нули
                    # Может быть, он и не мог решать эти задачи?
                    data[rown, addit_probs] = np.nan
fix_data_for_dop_prob()






# Супер-мега божественно: у нас есть список совпадающих задач у начинающих и продолжающих
# Это --- equals_lst.
# Ещё есть словарь номеров задач heads_to_cols
# По этим данным нужно определить, какие столбцы нужно склеить
col_head_to_npdata_coln_bef = col_head_to_npdata_coln
col_head_to_npdata_coln = {}
for key in col_head_to_npdata_coln_bef:
    nkey = re.sub(r'(?<=\D)(\d)(?=\D)', r'0\1', ' ' + key + ' ').strip()
    col_head_to_npdata_coln[nkey] = col_head_to_npdata_coln_bef[key]
equals_lst_np_idxs = []
for bkey, pkey in equals_lst:
    pkey = pkey.replace('a', 'а')
    if bkey not in col_head_to_npdata_coln:
        print('wtf', bkey)
        print(col_head_to_npdata_coln)
    if pkey not in col_head_to_npdata_coln:
        print('wtf', pkey)
        print(col_head_to_npdata_coln)
    # Гуд. Теперь в первом концентрируем данные, а во втором везде пишем np.nan
    bind = col_head_to_npdata_coln[bkey]
    pind = col_head_to_npdata_coln[pkey]
    equals_lst_np_idxs.append((bind, pind))
    for rown in range(data.shape[0]):
        if data[rown, pind] > 0:
            data[rown, bind] = data[rown, pind]
        elif data[rown, bind] is np.nan:
            data[rown, bind] = data[rown, pind]
        data[rown, pind] = np.nan
equals_lst_np_idxs = np.array(equals_lst_np_idxs)
# Ок, ура! Теперь по data можно считать крутизну!
# sheet, visit_cols, visit_heads, cols_to_heads, heads_to_cols, data, col_head_to_npdata_coln








def calc_strengths(data, visit_cols, cols_to_heads, equals_lst_np_idxs):
    num_pupils, num_problems = data.shape
    # Будущие оценки слоности и силы
    prob_сompl_for_strong = np.ones(num_problems) / 2
    prob_сompl_for_weak = np.ones(num_problems) / 2
    pup_compl_prob_strength = np.ones(num_pupils) / 2
    pup_simple_prob_strength = np.ones(num_pupils) / 2
    SOLVED_THRESHOLD = 1/2

    for i in range(33):
        # Переоцениваем силу школьника
        for curr_pup in range(num_pupils):
            solved_vec = data[curr_pup] >= SOLVED_THRESHOLD  # Вектор задач, которые школьник решИл
            tried_vec = data[curr_pup] >= 0  # Вектор задач, которые школьник решАл
            # Сила школьника в сложных задачах --- доля сложности, которую он порвал
            # Ясно, что нерешённая сложная задача сильно уменьшает эту долю
            pup_compl_prob_strength[curr_pup] = \
                np.dot(data[curr_pup, solved_vec], prob_сompl_for_strong[solved_vec]) * 3 / \
                (2*sum(prob_сompl_for_strong[tried_vec]) + sum(prob_сompl_for_strong[tried_vec]>0))
            # Сила школьника в простых задачах --- доля (единица минус сложностей) задач, которые он решил
            # Если школьник не решил простую задачу, то он потерял почти единицу в числителе
            pup_simple_prob_strength[curr_pup] = \
                np.dot(data[curr_pup, solved_vec], 1 - prob_сompl_for_weak[solved_vec]) * 20 / \
                (19*sum(1 - prob_сompl_for_weak[tried_vec]) + 1*sum(prob_сompl_for_weak[tried_vec]>0))
        # Переоцениваем сложность задач
        for curr_prob in range(num_problems):
            solved_vec = data[:, curr_prob] >= SOLVED_THRESHOLD  # Вектор школьников, решИвших задачу
            tried_vec = data[:, curr_prob] >= 0  # Вектор школьников, решАвших задачу
            # Сложность задачи для сильных --- доля силы школьников в простых задачах, НЕ решивших задачу
            # Если школьник с большим умением решать простые задачи задачу не решил, то это знак
            prob_сompl_for_strong[curr_prob] = 1 - \
                                               np.dot(data[:, curr_prob][solved_vec],
                                                      pup_compl_prob_strength[solved_vec]) * 20/ \
                                               (19*sum(pup_compl_prob_strength[tried_vec]) + 1*sum(pup_compl_prob_strength[tried_vec]>0))
            # Сложность задачи для слабых --- доля (единица минус сила в сложных задачах) школьников, НЕ решивших задачу
            # Если школьник, нефига не умеющий решать сложные задачи, решил задачу, то это знак
            prob_сompl_for_weak[curr_prob] = 1 - \
                                             np.dot(data[:, curr_prob][solved_vec],
                                                    1 - pup_simple_prob_strength[solved_vec]) * 20/ \
                                             (19*sum(1 - pup_simple_prob_strength[tried_vec])+1*sum(pup_simple_prob_strength[tried_vec]>0))
    res_pupils = '\n'.join('{:.3}\t{:.3}'.format(*pair).replace('.', ',')
                           for pair in zip(pup_compl_prob_strength, pup_simple_prob_strength))
    print('Pupils:')
    pyperclip.copy(res_pupils)
    print(res_pupils)
    input('Paste puple data and press enter')

    # Теперь нужно в совпадающих задачах скопировать сложность к продолжающим,
    # а также добавить пустые столбцы для столбцов посещаемости
    # visit_cols --- номера столбцов в excel'е с посещаемостью
    # cols_to_heads --- номера столбцов с задачами
    # equals_lst_np_idxs --- пары np-шных склееных индексов
    prob_сompl_for_strong[equals_lst_np_idxs[:, 1]] = prob_сompl_for_strong[equals_lst_np_idxs[:,0]]
    prob_сompl_for_weak[equals_lst_np_idxs[:, 1]] = prob_сompl_for_weak[equals_lst_np_idxs[:,0]]
    prob_idxs = np.array(sorted(cols_to_heads))
    ins_idxs = [len(prob_idxs[prob_idxs < x]) for x in sorted(visit_cols)]
    prob_сompl_for_strong2 = np.insert(prob_сompl_for_strong, ins_idxs, -1)
    prob_сompl_for_weak2 = np.insert(prob_сompl_for_weak, ins_idxs, -1)
    res_problems = '\t'.join('{:.3}'.format(st) for st in prob_сompl_for_strong2) + '\n' + \
                   '\t'.join('{:.3}'.format(st) for st in prob_сompl_for_weak2)
    res_problems = res_problems.replace('-1.0', '').replace('.', ',')
    print('Problems:')
    pyperclip.copy(res_problems)
    print(res_problems)

calc_strengths(data, visit_cols, cols_to_heads, equals_lst_np_idxs)
