# -*- coding: utf-8 -*-.
from CONSTS import *
from z_helpers import *
from shutil import copyfile
import re

# work = (bas,)
# work = (pro, )


for cur_les in range(1, cur_les+1):
    pass


def upd_num_add_parts_stats(wrk, data):
    lvl = wrk['excel_level_const']
    stats = read_stats()
    data = data.replace('\\\\', '').replace(r'\%', '')
    data = re.sub(r'\n\s*%.*$', r'', data, flags=re.MULTILINE)  # Удаляем комментарии
    data = re.sub(r'\s*%.*$', r'', data, flags=re.MULTILINE)  # Удаляем комментарии
    data = re.sub(r'\\end\{document\}.*$', r'\\end\{document\}', data, flags=re.DOTALL)  # Удаляем всё после конца документа
    if PORTRAIT_ORIENTATION:
        stats[cur_les][lvl]['кол-во копий доп.задач'] = 4
    else:
        ncopies = re.findall(r'\\np?copy\{\d\}', data, )
        if len(ncopies) != 2:
            lg.error('Не удалось определить кол-во копий допзадач')
            stats[cur_les][lvl]['кол-во копий доп.задач'] = None
        else:
            ncopies = int(ncopies[-1][-2])
            stats[cur_les][lvl]['кол-во копий доп.задач'] = ncopies
    # Ок, теперь нужно определить кол-во столбцов в будущем кондуите
    data1, dummy, data2 = data.partition(r'\допраздел')
    problems = re.findall(r'(\\[а-я]{0,2}задача)|(\\[а-я]{0,2}пункт)', data1) + ['|'] + re.findall(r'(\\[а-я]{0,2}задача)|(\\[а-я]{0,2}пункт)', data2)
    for i, prb in enumerate(problems):
        prb = ''.join(prb)
        if prb == '|':
            continue
        elif prb == '\кзадача':
            problems[i] = 'к'
        elif prb.endswith('задача'):
            problems[i] = 'з'
        elif prb.endswith('пункт'):
            problems[i] = 'п'
        else:
            lg.fatal('Хрень какая-то с этими вашими задачами...')
            problems[i] = ''
    problems = ''.join(problems)
    stats[cur_les][lvl]['структура'] = problems
    problems = problems.replace('зп', 'п')
    problems = problems.replace('к', '').replace('|', '')
    stats[cur_les][lvl]['кол-во задач/пунктов'] = len(problems)
    update_stats(stats)


def refactor_tex(data):
    lg.debug('Было:\n' + ('*'*100 + '\n') * 3)
    lg.debug(data)
    data = data.replace('\\theFullTitleLine', '')
    data = data.replace('\\\\', 'DOUBLE_SLASH_W4MCFkw6VF')
    data = data.replace(r'\%', 'PERSENT_W4MCFkw6VF')
    data = data.replace(r'%[Взято', 'TAKEN_W4MCFkw6VF')
    data = data.replace(r'\$', 'DOLLAR_W4MCFkw6VF')
    # Удаляем комментарии и блок после конца

    if data.count(r'} % \ncopy') == 2:  # Избавляемся от ncopy
        data = re.sub(r'\\ncopy{\d+}{', r'', data)
        data = re.sub(r'\} % \\ncopy от.*', r'', data)
    else:
        data = re.sub(r'\\ncopy{\d+}{', r'{', data)
    if data.count(r'} % \npcopy') == 2:  # Избавляемся от ncopy
        data = re.sub(r'\\npcopy{\d+}{', r'', data)
        data = re.sub(r'\} % \\npcopy от.*', r'', data)
    else:
        data = re.sub(r'\\npcopy{\d+}{', r'{', data)

    if r'\begin{center}%КОММЕНТЫ В КОНЦЕ' in data:
        data = re.sub(r'(\\vfil\s*)?(\\vspace\{.*?\}\s*)?\s*\\begin\{center\}%КОММЕНТЫ В КОНЦЕ.*?\\end\{center\}', '', data, flags=re.DOTALL)

    data = re.sub(r'\n\s*%.*$', r'', data, flags=re.MULTILINE)  # Удаляем комментарии
    data = re.sub(r'\s*%.*$', r'', data, flags=re.MULTILINE)  # Удаляем комментарии
    data = re.sub(r'\\end\{document\}.*$', r'\\end{document}', data, flags=re.DOTALL)  # Удаляем всё после конца документа

    # print(data); exit(1)
    #
    # Теперь сложный кусок. Нужно вырезать блок с "новостями"
    # Возможно, он уже оформлен "хорошо", тогда его легко вырезать (он уже вырезан)
    posl = posr = data.find('логин: vmsh')
    if posl >= 0:
        br_diff_l, br_diff_r = 0, 0
        while posl >= 0 and br_diff_l < 1:
            br_diff_l += 1 if data[posl] == '{' else -1 if data[posl] == '}' else 0
            posl -= 1
        while posr >= 0 and br_diff_r > -1:
            br_diff_r += 1 if data[posr] == '{' else -1 if data[posr] == '}' else 0
            posr += 1
        data = data[:posl] + data[posr+1:   ]
    # Конец сложного куска
    #
    data = re.sub(r'\\renewcommand\{\\spacer\}\{\\vspace\*\{(.*?)\}\}', r'\\renewcommand{\\spacer}{\\vspace*{3.5pt}}', data)
    data = re.sub(r'\s*\n\s*\n\s*', '\n\n', data)
    data = re.sub(r'\\smallskip\s*', r'', data)
    data = re.sub(r'\\medskip\s*', r'', data)
    data = re.sub(r'\\bigskip\s*', r'', data)
    data = re.sub(r'\\noindent\s*', r'', data)
    data = data.replace(r'\УвеличитьВысоту', r'%\УвеличитьВысоту')
    data = data.replace(r'\newpage', '')
    data = data.replace(r'\vfilll', '')
    data = data.replace(r'\vfill', '')
    data = data.replace(r'\vfil', '')
    data = data.replace(r'\newaaaaaalpage', '')
    # data = data.replace(r'\aaaaappage', '')
    data = data.replace('DOUBLE_SLASH_W4MCFkw6VF', '\\\\')
    data = data.replace('PERSENT_W4MCFkw6VF', r'\%')
    data = data.replace('TAKEN_W4MCFkw6VF', r'%[Взято')
    data = data.replace('DOLLAR_W4MCFkw6VF', r'\$')
    data = data.replace(r'\graphicspath{{' + PICT_DIR + '/}}', r'\graphicspath{{../' + PICT_DIR + '/}{' + BARCODES + '/}}')
    lg.debug(('*'*100 + '\n') * 3 + 'Стало:\n' + ('*'*100 + '\n') * 3)
    lg.debug(data)
    return data



def crt_lesson_tex_for_site_pdf(data, res_name, pdf_name):
    # Делаем А4
    data = data.replace(r'\aaaaappage', '')
    data = re.sub(r'mag=\d{3},', r'mag=1000,', data)    # Удаляем newpage
    data = re.sub(r' *\\newpage\s*', '', data)
    data = data.replace(r'\vfilll', '')
    data = data.replace(r'\vfill', '')
    data = data.replace(r'\vfil', '')
    lg.info('Создаём и комплируем ' + res_name)
    with open(os.path.join(DUMMY_FOLDER_PATH, res_name), 'w', encoding='windows-1251') as f:
        f.write(data)
    # Теперь компилим это
    compile_tex(res_name, DUMMY_FOLDER_PATH)
    copyfile(os.path.join(START_PATH, DUMMY_FOLDER_PATH, res_name.replace('.tex', '.pdf')),
             os.path.join(START_PATH, wrk['htmls_path'], pdf_name))


def crt_solutions_tex(sol_data, sol_name):
    lg.info('Обрабатываем ' + sol_name)
    if os.path.isfile(sol_name):
        lg.info(sol_name + ' уже существует. НИЧЕГО НЕ ТРОГАЕМ!')
        return

    # sol_data = re.sub(r'(\\vspace\*?\{.*?\})?\s*?(\\noindent)?\s*?\{\\small([^{}]*?\{[^{}]*?\})*?([^{}]*)?\}', r'', sol_data, flags=re.DOTALL)
    sol_data = re.sub(r'\\a*ppage', r'', sol_data)
    if 'УвеличитьВысоту' in sol_data:
        sol_data = re.sub(r'%\\УвеличитьВысоту\{.*?\}', r'\УвеличитьВысоту{25truemm}', sol_data)
    else:
        sol_data = re.sub(r'(\\usepackage(?:\[[^\[\]]+\])?{newlistok})', r'\1\n\\УвеличитьВысоту{25truemm}', sol_data)
    if 'УвеличитьШирину' in sol_data:
        sol_data = re.sub(r'%\\УвеличитьШирину\{.*?\}', r'\УвеличитьШирину{20truemm}', sol_data)
    else:
        sol_data = re.sub(r'(\\usepackage(?:\[[^\[\]]+\])?{newlistok})', r'\1\n\\УвеличитьШирину{20truemm}', sol_data)
    sol_data = re.sub(r'(\\usepackage(?:\[[^\[\]]+\])?{newlistok})\s*(\\[А-Яа-яёЁ])', r'\1\n\n\2', sol_data)
    END_PROBLEM_MARK = r'\кзадача'
    end_pos = sol_data.rfind(END_PROBLEM_MARK)
    while end_pos >= 0:
        str_pos = sol_data.rfind(r'задача', 0, end_pos)
        if str_pos >= 0 and '\\' in sol_data[str_pos - 2:str_pos]:
            # Итак, задача простирается от str_pos до end_pos
            npuncts = sol_data[str_pos: end_pos].count('\\пункт')
            puncts_list = ['\\textbf{{{}}})'.format('абвгдежзикл'[i]) for i in range(npuncts)]
            addition = """
\\ответ
{}
\\кответ
\\решение
{}
\\крешение
\\spacer\\hrule\\vspace*{{4pt}}
                """.format('; '.join(puncts_list), '\n'.join(puncts_list)) + '\n' * 8
            sol_data = sol_data[:end_pos + len(END_PROBLEM_MARK)] + addition + sol_data[
                                                                               end_pos + len(END_PROBLEM_MARK):]
        end_pos = sol_data.rfind(END_PROBLEM_MARK, 0, end_pos - 1)
    # Текст готов.
    sol_data = sol_data.replace(r'\graphicspath{{../' + PICT_DIR + '/}}', r'\graphicspath{{' + PICT_DIR + '/}}')
    sol_data = sol_data.strip()
    with open(sol_name, 'w', encoding='windows-1251') as f:
        f.write(sol_data)
    lg.info(sol_name + ' done')


def crt_conduit_tex(cond_data, spisok_name_template, res_name, wrk):
    # Ок, для кондуитов нужно только добавить в хвост кусок "\СделатьКондуитИз"
    lg.info('Готовим ' + res_name)
    lvl = wrk['excel_level_const']
    cond_data = cond_data.replace(r'\aaaaappage', '')
    stats = read_stats()
    num_conduit_problems = stats[cur_les][lvl]['кол-во задач/пунктов']
    spisok_name_template = re.sub(r'\{[^{}]+\}', r'(.*)?', spisok_name_template)
    max_pupils_in_coduit = 27
    include = []
    names = []
    for name in os.listdir(DUMMY_FOLDER_PATH):
        if re.match(spisok_name_template, name):
            try:
                data = open(os.path.join(DUMMY_FOLDER_PATH, name), 'r', encoding='windows-1251').read()
                cur_pupils_in_coduit = max(data.count(r'\start'), max_pupils_in_coduit)
            except:
                pass
            names.append((name, cur_pupils_in_coduit))
    for name, cur_pupils_in_coduit in names:
        lg.info(name)
        crt_conduit = CRT_COUNDUIT_COMMAND
        crt_qrconduit = '\CreateQRConduitFrom{4.4mm}{6mm}'
        audname = re.findall("[0-9]+",name)[0]
        if num_conduit_problems:
            # На все столбцы есть 120mm. Каждый столбец "отъедает" 0.5mm на границу
            num_conduit_problems = max(15, num_conduit_problems)
            col_width = f'{(115-num_conduit_problems/2)/num_conduit_problems:0.2f}mm'
            crt_conduit = crt_conduit[:crt_conduit.find('{')+1] + col_width + crt_conduit[crt_conduit.find('}'):]
        # На все строки у нас есть 240mm. Каждая строчка отъедает ".3mm" на границу
        row_height = f'{(225-cur_pupils_in_coduit/3)/cur_pupils_in_coduit:0.2f}mm'
        crt_conduit = crt_conduit[:crt_conduit.rfind('{') + 1] + row_height + crt_conduit[crt_conduit.rfind('}'):]
        include.append(crt_conduit + '{' + name.replace('.tex', '') + '}')
    include.append(CRT_COUNDUIT_COMMAND + '{spis_empty}')
    cond_data = cond_data.replace(r'\begin{document}', '\\usepackage{fancybox}\n\\begin{document}\n\\sbox{\\blok}{\\vbox{')
    cond_data = cond_data.replace(r'\end{document}', '}}\\GenXMLW\n' + '\n'.join(include) + '\n\\end{document}')
    cond_data = re.sub(r'mag=\d{3,4}', r'mag=1000', cond_data)  # Выравниваем масштаб, если он был испорчен
    with open(os.path.join(DUMMY_FOLDER_PATH, res_name), 'w', encoding='windows-1251') as f:
        f.write(cond_data)
    compile_tex(res_name, DUMMY_FOLDER_PATH)

def crt_prev_conduit_tex(cond_data, spisok_name_template, res_name, wrk):
    # Ок, для кондуитов нужно только добавить в хвост кусок "\СделатьКондуитИз"
    lg.info('Готовим ' + res_name)
    lvl = wrk['excel_level_const']
    cond_data = cond_data.replace(r'\aaaaappage', '')
    stats = read_stats()
    num_conduit_problems = stats[prev_les][lvl]['кол-во задач/пунктов']
    spisok_name_template = re.sub(r'\{[^{}]+\}', r'(.*)?', spisok_name_template)
    max_pupils_in_coduit = 27
    include = []
    names = []
    for name in os.listdir(DUMMY_FOLDER_PATH):
        if re.match(spisok_name_template, name):
            try:
                data = open(os.path.join(DUMMY_FOLDER_PATH, name), 'r', encoding='windows-1251').read()
                cur_pupils_in_coduit = max(data.count(r'\start'), max_pupils_in_coduit)
            except:
                pass
            names.append((name, cur_pupils_in_coduit))
    for name, cur_pupils_in_coduit in names:
        lg.info(name)
        crt_conduit = CRT_COUNDUIT_COMMAND
        crt_qrconduit = '\CreateQRConduitFrom{4.4mm}{6mm}'
        audname = re.findall("[0-9]+",name)[0]
        if num_conduit_problems:
            # На все столбцы есть 120mm. Каждый столбец "отъедает" 0.5mm на границу
            num_conduit_problems = max(15, num_conduit_problems)
            col_width = f'{(115-num_conduit_problems/2)/num_conduit_problems:0.2f}mm'
            crt_conduit = crt_conduit[:crt_conduit.find('{')+1] + col_width + crt_conduit[crt_conduit.find('}'):]
        # На все строки у нас есть 240mm. Каждая строчка отъедает ".3mm" на границу
        row_height = f'{(225-cur_pupils_in_coduit/3)/cur_pupils_in_coduit:0.2f}mm'
        crt_conduit = crt_conduit[:crt_conduit.rfind('{') + 1] + row_height + crt_conduit[crt_conduit.rfind('}'):]
        include.append(crt_conduit + '{' + name.replace('.tex', '') + '}')
    include.append(CRT_COUNDUIT_COMMAND + '{spis_empty}')
    cond_data = cond_data.replace(r'\begin{document}', '\\usepackage{fancybox}\n\\begin{document}\n\\sbox{\\blok}{\\vbox{')
    cond_data = cond_data.replace(r'\end{document}', '}}\\GenXMLW\n' + '\n'.join(include) + '\n\\end{document}')
    cond_data = re.sub(r'mag=\d{3,4}', r'mag=1000', cond_data)  # Выравниваем масштаб, если он был испорчен
    with open(os.path.join(DUMMY_FOLDER_PATH, res_name), 'w', encoding='windows-1251') as f:
        f.write(cond_data)
    compile_tex(res_name, DUMMY_FOLDER_PATH)




def crt_teacher_edition(data, res_name):
    # Добавляем высоты
    data = re.sub(r'\\УвеличитьШирину\{.*?\}', '\\УвеличитьВысоту{27truemm}\n\\УвеличитьШирину{18truemm}', data)
    # Удаляем положительные vspace'ы
    data = re.sub(r'\\vspace\*?\{[^-].*?\}', '', data)
    # Удаляем newpage
    data = re.sub(r' *\\newpage\s*', '', data)
    data = data.replace(r'\vfilll', '')
    data = data.replace(r'\vfill', '')
    data = data.replace(r'\vfil', '')
    # Уменьшаем межзадачные промежутки
    data = re.sub(r'\\renewcommand\{\\spacer\}\{.*?\}', r'\\renewcommand{\\spacer}{\\vspace*{0.035pt}}', data)
    # Не в режиме портрет делаем две копии
    if not PORTRAIT_ORIENTATION:
        data = data.replace(r'\begin{document}', '\\begin{document}\n\\npcopy{2}{')
        data = data.replace(r'\end{document}', '\\vspace*{6truemm}}\\vspace*{-6truemm}\n\\end{document}')
    # Удаляем объявления
    data = re.sub(r'(\\vspace\*?\{.*?\})?\s*?(\\noindent)?\s*?\{\\small([^{}]*?\{[^{}]*?\})*?([^{}]*)?\}', r'', data, flags=re.DOTALL)

    # Теперь бинпоиск оптимального мастаба
    lg.info('Пишем ' + res_name)
    last_good, cur_mag, min_mag, max_mag = 400, 840, 480, 1000
    while True:
        lg.info('Ищем мастштаб в {}, пробуем {} ([{}, {}])'.format(res_name, cur_mag, min_mag, max_mag))
        data = re.sub(r'mag\s*=\s*\d+', r'mag=' + str(cur_mag), data)
        with open(os.path.join(DUMMY_FOLDER_PATH, res_name), 'w', encoding='windows-1251') as f:
            f.write(data)
        res = compile_tex(res_name, DUMMY_FOLDER_PATH)
        if '2 pages' in res:
            max_mag = cur_mag
            cur_mag = (min_mag + cur_mag) // 2
        else:
            min_mag = cur_mag
            last_good = cur_mag
            cur_mag = (max_mag + cur_mag) // 2
        if max_mag - min_mag < 5 and '2 pages' not in res:
            break
        elif max_mag - min_mag < 5:
            cur_mag = last_good
        elif max_mag - min_mag < 2:
            break


def remove_trash():
    for path in (DUMMY_FOLDER_PATH, START_PATH):
        for name in os.listdir(path):
            if '.' in name and name.lower()[name.rfind('.') + 1:] in ('bak', 'aux', 'bbl', 'blg', 'log', 'synctex'):
                os.remove(os.path.join(path, name))


copyfile(os.path.join(START_PATH, 'newlistok.sty'), os.path.join(START_PATH, DUMMY_FOLDER_PATH, 'newlistok.sty'))  # Освежаем стиль на всякий случай

for wrk in work:
    cur_name = os.path.join(START_PATH, wrk['tex_name_template'].format(cur_les=cur_les))
    lg.info('Обрабатываем ' + cur_name)
    with open(cur_name, 'r', encoding='windows-1251') as f:
        data = f.read()
    # Отложим кол-во копий дополнительного задания
    upd_num_add_parts_stats(wrk, data)
    # Делаем основное общее преобразование
    data = refactor_tex(data)
    # Файл, на основе которого готовится pdf на сайт (а также html)
    crt_lesson_tex_for_site_pdf(data, wrk['dummy_tex_lesson_template'].format(cur_les=cur_les), wrk['htmls_pdfs_template'].format(cur_les=cur_les))
    # Файлик, в которое будем писать решения.
    crt_solutions_tex(data, wrk['sol_tex_name_template'].format(cur_les=cur_les))
    # Файлик, для поаудиторных кондуитов
    crt_conduit_tex(data, wrk['spisok_name_template'], wrk['dummy_tex_conduit_template'].format(cur_les=cur_les), wrk)
    # Предыдущее занятие
    try:
        cur_prev_name = os.path.join(START_PATH, wrk['tex_name_template'].format(cur_les=prev_les))
        lg.info('Обрабатываем ' + cur_prev_name)
        with open(cur_prev_name, 'r', encoding='windows-1251') as f:
            prev_data = f.read()
        # Делаем основное общее преобразование
        prev_data = refactor_tex(prev_data)
        crt_prev_conduit_tex(prev_data, wrk['pred_spisok_name_template'], wrk['dummy_tex_prev_conduit_template'].format(cur_les=cur_les), wrk)
    except FileNotFoundError:
        lg.info('Предыдущий кондуит не найден')
    # Так, теперь самое сложное - версия для преподавателей
    crt_teacher_edition(data, wrk['dummy_tex_teacher_template'].format(cur_les=cur_les))
    # Удаляем треш
    remove_trash()
    print('*'*100 + '\nКусок готов\n' + '*'*100)
