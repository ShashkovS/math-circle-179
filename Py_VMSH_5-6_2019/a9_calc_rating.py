from z_CONSTS import *
from z_helpers import *
import logging
import re
import numpy as np
import pyperclip
logging.basicConfig(level=logging.DEBUG)



def gen_json_lists(sheet):
    # Сначала читаем заголовок
    probs_in_list = {}
    prb_hdr_matcher = re.compile(r'\s*(\d{1,2}\w?)\.([НнhH]|(?:\d{1,2}\w?))\s*')
    col_hdr_to_colc = {}
    for coln in range(0, sheet.ncols):
        cv = str(sheet.cell(FIRST_ROW - 2, coln).value).strip()
        match = prb_hdr_matcher.fullmatch(cv)
        if match:
            lstn = match.group(1)
            probn = match.group(2)
            if lstn not in probs_in_list:
                probs_in_list[lstn] = [probn]
            else:
                probs_in_list[lstn].append(probn)
            col_hdr_to_colc[cv] = coln
    only_ns_to_colc = {}
    for prob in col_hdr_to_colc.copy():
        match = prb_hdr_matcher.fullmatch(prob)
        lstn = match.group(1)
        probn  = match.group(2)
        if len(probs_in_list[lstn]) == 1:
            del col_hdr_to_colc[prob]
        elif probn in 'НнhH':
            only_ns_to_colc[lstn] = col_hdr_to_colc[prob]
            del col_hdr_to_colc[prob]
    return col_hdr_to_colc, only_ns_to_colc


# Теперь делаем список школьников
def gen_json_pupils(sheet):
    pupils_by_id = {}
    pupil_to_rown = {}
    for rown in range(FIRST_ROW - 1, sheet.nrows):
        surnam, nam, id = (str(sheet.cell(rown, coln).value).strip().replace('.0', '') for coln in \
            [COLUMNS['Фамилия'], COLUMNS['Имя'], COLUMNS['ID']])
        surnam = surnam.title()
        nam = nam.title()
        pupils_by_id[id] = {'Name1': surnam, 'Name2': nam, 'xlsID': id}
        pupil_to_rown[id] = rown
    return pupils_by_id, pupil_to_rown


def gen_json_plus(sheet, pupil_to_rown, col_hdr_to_colc, only_ns_to_colc):

    data = np.empty((len(pupil_to_rown), len(col_hdr_to_colc)))
    data[:, :] = np.nan

    # Итак, у нас есть заголовки всех столбцов.
    # Теперь нужно сделать сложную штуку: если школьник был на занятии, то все несданные задачи должны получить 0,
    # все сданные — 1, а те, что он не решал -- np.nan
    col_to_lstn = np.zeros(len(col_hdr_to_colc), dtype=np.int)
    for i, (pup_id, rown) in enumerate(pupil_to_rown.items()):
        visits = set()
        for col_hdr, coln in only_ns_to_colc.items():
            cv = str(sheet.cell(rown, coln).value).strip().replace('.0', '')
            if cv == '1':
                lstn = col_hdr.split('.')[0]
                visits.add(lstn)
        for j, (col_hdr, coln) in enumerate(col_hdr_to_colc.items()):
            lstn = col_hdr.split('.')[0]
            col_to_lstn[j] = int(lstn.strip('нНhHпПpP'))
            cv = str(sheet.cell(rown, coln).value).strip().replace('.0', '')
            visited = lstn in visits
            if cv == '1' and not visited:
                visits.add(lstn)
                visited = True
            if not visited:
                continue
            data[i, j] = 1 if cv == '1' else 0
    return data, col_to_lstn


def calc_strengths(data):
    num_pupils, num_problems = data.shape
    # Будущие оценки слоности и силы
    prob_compl_for_strong = np.ones(num_problems) / 2
    prob_compl_for_weak = np.ones(num_problems) / 2
    pup_compl_prob_strength = np.ones(num_pupils) / 2
    pup_simple_prob_strength = np.ones(num_pupils) / 2
    SOLVED_THRESHOLD = 1/2

    for i in range(33):
        # Переоцениваем силу школьника
        for curr_pup in range(num_pupils):
            solved_vec = data[curr_pup, :] >= SOLVED_THRESHOLD  # Вектор задач, которые школьник решИл
            tried_vec = data[curr_pup, :] >= 0  # Вектор задач, которые школьник решАл
            # Сила школьника в сложных задачах --- доля сложности, которую он порвал
            # Ясно, что нерешённая сложная задача сильно уменьшает эту долю
            pup_compl_prob_strength[curr_pup] = \
                np.dot(data[curr_pup, solved_vec], prob_compl_for_strong[solved_vec]) * 3 / \
                (2*sum(prob_compl_for_strong[tried_vec]) + sum(prob_compl_for_strong[tried_vec]>0))
            # Сила школьника в простых задачах --- доля (единица минус сложностей) задач, которые он решил
            # Если школьник не решил простую задачу, то он потерял почти единицу в числителе
            pup_simple_prob_strength[curr_pup] = \
                np.dot(data[curr_pup, solved_vec], 1 - prob_compl_for_weak[solved_vec]) * 20 / \
                (19*sum(1 - prob_compl_for_weak[tried_vec]) + 1*sum(prob_compl_for_weak[tried_vec]>0))
        # Переоцениваем сложность задач
        for curr_prob in range(num_problems):
            solved_vec = data[:, curr_prob] >= SOLVED_THRESHOLD  # Вектор школьников, решИвших задачу
            tried_vec = data[:, curr_prob] >= 0  # Вектор школьников, решАвших задачу
            # Сложность задачи для сильных --- доля силы школьников в простых задачах, НЕ решивших задачу
            # Если школьник с большим умением решать простые задачи задачу не решил, то это знак
            prob_compl_for_strong[curr_prob] = 1 - \
                                               np.dot(data[:, curr_prob][solved_vec],
                                                      pup_compl_prob_strength[solved_vec]) * 20/ \
                                               (19*sum(pup_compl_prob_strength[tried_vec]) + 1*sum(pup_compl_prob_strength[tried_vec]>0))
            # Сложность задачи для слабых --- доля (единица минус сила в сложных задачах) школьников, НЕ решивших задачу
            # Если школьник, нефига не умеющий решать сложные задачи, решил задачу, то это знак
            prob_compl_for_weak[curr_prob] = 1 - \
                                             np.dot(data[:, curr_prob][solved_vec],
                                                    1 - pup_simple_prob_strength[solved_vec]) * 20/ \
                                             (19*sum(1 - pup_simple_prob_strength[tried_vec])+1*sum(pup_simple_prob_strength[tried_vec]>0))
    return pup_compl_prob_strength, pup_simple_prob_strength
    # res_pupils = '\n'.join('{:.3}\t{:.3}'.format(*pair).replace('.', ',')
    #                        for pair in zip(pup_compl_prob_strength, pup_simple_prob_strength))
    # res_pupils = res_pupils.replace('nan', '-0,01')
    # print('Pupils:')
    # pyperclip.copy(res_pupils)
    # print(res_pupils)
    # input('Paste puple data and press enter')
    #
    # res_problems = '\t'.join('{:.3}'.format(st) for st in prob_compl_for_strong) + '\n' + \
    #                '\t'.join('{:.3}'.format(st) for st in prob_compl_for_weak)
    # res_problems = res_problems.replace('-1.0', '').replace('.', ',')
    # print('Problems:')
    # pyperclip.copy(res_problems)
    # print(res_problems)
    

lg.info('Открываем файл (займёт время) ' + XLS_CONDUIT_NAME)
rb = xlrd.open_workbook(XLS_CONDUIT_NAME)
sheet = rb.sheet_by_index(0)
col_hdr_to_colc, only_ns_to_colc = gen_json_lists(sheet)
pupils_by_id, pupil_to_rown = gen_json_pupils(sheet)
data, col_to_lstn = gen_json_plus(sheet, pupil_to_rown, col_hdr_to_colc, only_ns_to_colc)

simps = np.zeros((len(pupil_to_rown), cur_les))
compls = np.zeros((len(pupil_to_rown), cur_les))
for i in range(cur_les):
    bef_data = data[:, col_to_lstn<=(i+1)]
    print(bef_data.shape)
    pup_compl_prob_strength, pup_simple_prob_strength = calc_strengths(bef_data)
    simps[:, i] = pup_simple_prob_strength
    compls[:, i] = pup_compl_prob_strength

for row in compls:
    print('\t'.join(map(str, row)))
