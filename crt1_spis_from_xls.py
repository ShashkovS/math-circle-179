# -*- coding: utf-8 -*-.
from CONSTS import *
from z_helpers import *
from shutil import copyfile
from collections import Counter


def remove_old_spis():
    lg.info('Удаляем старые списки...')
    for name in os.listdir(DUMMY_FOLDER_PATH):
        if name.startswith('spisok') and name != 'spisok_empty.tex':
            os.remove(os.path.join(DUMMY_FOLDER_PATH, name))


def gen_spisok_files(res):
    """Создаём поаудиторные файлы вида spisok..."""
    lg.info('Создаём файлы spisok... для кондуитов')
    head = """\
    %\\downlegendfalse %нумерация задач снизу  будет отсутствовать
    %
    \\пометка={{\\qquad Отметь присутствующих!\\hfill%
     Перемена
     с
     17: 25
     до
     17: 35\\hfill
     \\Huge
     {}\hfill }}
    %
    \\штрихкод={{{}}}
    \\список={{%
    """

    head = '\n'.join(row.strip() for row in head.splitlines())
    line = r"\start{{{}}}%" + '\n'
    dummy_line = '\\phantom{Севастьянова Александра}'
    bottom = """\\hline}"""

    auds = set((x['Аудитория'], x['Уровень']) for x in res)
    for aud, level in auds:
        if level not in levels:
            for __ in range(5): lg.error('!!! Уровень ' + level + ' не настоен в CONST (или кривой в xls)')
            continue
        wrk = levels[level]
        cur_names = sorted(((x['ФИО'], x['Клс'], x['Ср3'], x['IDd']) for x in res if x['Аудитория'] == aud),
                           key=lambda x: x[0].lower().replace('ё', 'е'))
        crt_aud_barcode(aud, [row[-1] for row in cur_names])
        cur_names.append((dummy_line, '', '', ''))
        cur_names += [('', '', '', '')] * (wrk['lines_in_counduit'] - len(cur_names))
        text = head.format(aud, 'barcode_{}.png'.format(aud))
        cur_row = 0
        for i, (name, klass, sr, idd) in enumerate(cur_names):
            if klass != '':
                klass = '\\Ovalbox{' + klass + '}'
            if sr != '':
                sr = '\\Ovalbox{' + str(sr)[:4] + '}'
            text += line.format(name + ' ' + klass)
            cur_row += 1
            if i != len(cur_names) - 1 and cur_row % 9 == 0 and cur_row < 20:
                text += '\\midlegend\n'
            elif i != len(cur_names) - 1 and cur_row % 3 == 0:
                text += '\\hline\n'
        text += bottom
        filename = os.path.join(DUMMY_FOLDER_PATH, wrk['spisok_name_template'].format(aud=aud))
        lg.info('Создаём ' + filename)
        with open(filename, 'w', encoding='windows-1251') as f:
            f.write(text.replace('ё', 'е'))


def gen_aud_lists(res):
    """Создаём поаудиторный список"""
    lg.info('Создаём поаудиторные списки на двери...')
    head = r"""
\documentclass[14pt]{article}
\usepackage[cp1251]{inputenc}
\usepackage[russian]{babel}
\usepackage{graphics}
\usepackage[table]{xcolor}
\usepackage[margin=1truecm]{geometry}
\pagestyle{empty}

\begin{document}
    """

    table_head = r"""
\begin{center}""" + AUD_LIST_TITLE_TEX + r"""
\par
\vspace{1cm}
\fontsize{16}{22}\selectfont
\rowcolors{2}{gray!15}{white}
\begin{tabular}{|c|}\hline
\rowcolor{gray!50}\textbf{\hspace*{2cm}Фамилия и имя\hspace*{2cm}}\\\hline
    """

    table_row = '{} \\\\\\hline\n'

    table_bottom = r"""
\end{tabular}

\vfill
\Huge{Распределение по аудиториям можно найти в~списках при входе на этаж}
\end{center}
    """

    table_short = r"""
\end{tabular}
\end{center}
    """

    bottom = r"""
\end{document}
    """

    auds = set((x['Аудитория']) for x in res)
    text = head
    for aud in sorted(auds):
        cur_names = sorted((x['ФИО'] for x in res if x['Аудитория'] == aud and 'phantom' not in x['ФИО']),
                           key=lambda x: x.lower().replace('ё', 'е'))
        cur_head = table_head.replace('AUD_NUMBER', aud).replace('LES_DATE', LES_DATE)
        if len(cur_names) >= 38:
            cur_head = cur_head.replace(r'\fontsize{16}{22}', r'\fontsize{14}{15}')
        elif len(cur_names) >= 33:
            cur_head = cur_head.replace(r'\fontsize{16}{22}', r'\fontsize{16}{17}')
        elif len(cur_names) >= 30:
            cur_head = cur_head.replace(r'\fontsize{16}{22}', r'\fontsize{16}{19}')
        elif len(cur_names) >= 27:
            cur_head = cur_head.replace(r'\fontsize{16}{22}', r'\fontsize{16}{21}')
        text += cur_head
        for i, name in enumerate(cur_names):
            text += table_row.format(name)
        if len(cur_names) >= 27:
            text += table_short
        else:
            text += table_bottom
        text += '\\newpage'
    text += bottom
    filename = DUMMY_FOLDER_PATH + 'Поаудиторные списки.tex'
    lg.info('Создаём ' + filename)
    with open(filename, 'w', encoding='windows-1251') as f:
        f.write(text)


def gen_mega_floor_lists(res):
    # Теперь мега-список

    tex_head = r"""%
\documentclass[14pt]{article}
\usepackage[cp1251]{inputenc}
\usepackage[russian]{babel}
\usepackage{graphics}
\usepackage[table]{xcolor}
\usepackage{multicol}
\usepackage[a3paper,margin=.7truecm]{geometry}
\usepackage{longtable}
\pagestyle{empty}
\newsavebox\ltmcbox
\begin{document}"""
    page_head = r"""%
\begin{center}
\scalebox{1.2}{\Huge{\textbf{CIRCLE_TITLE}}}
\end{center}
\fontsize{12}{13.6}\selectfont
\rowcolors{2}{gray!15}{white}""".replace('CIRCLE_TITLE', CIRCLE_TITLE.replace('LES_DATE', LES_DATE))
    table_head = r"""%
\hfil
\begin{tabular}[t]{|l|c|}\hline
\rowcolor{gray!50}\textbf{Фамилия и имя} & \textbf{Ауд}\\ \hline"""
    table_bottom = r"""%
\end{tabular}\hfil"""
    page_bottom = r"""%
"""
    if FIRST_TIME_FLOOR and FIRST_TIME_AUD:
        first_time_text = r"""
        \begin{center}
        \scalebox{1.0}{\Huge{\textbf{Пришедшие в первый раз приглашаются на FIRST_TIME_FLOOR в FIRST_TIME_AUD ауд.}}}
        \end{center}
        """.replace('FIRST_TIME_AUD', FIRST_TIME_AUD).replace('FIRST_TIME_FLOOR', FIRST_TIME_FLOOR)
    else:
        first_time_text = ""

    tex_bottom = r"""
    \end{document}
    """

    # title_row = r"\rowcolor{gray!50}\textbf{Фамилия и имя} & \textbf{Ауд}\\ \hline" + '\n'
    table_row = '{} & {} \\\\\\hline\n'

    pup_list = sorted([(x['ФИО'] if len(x['ФИО']) <= 20 else x['ФИ.'],
                        x['Аудитория']) for x in res if 'phantom' not in x['ФИО']],
                      key=lambda x: x[0].lower().replace('ё', 'е'))
    # Если фамилий большей 348, то добавляем строчки с буквами (всё равно на одну страницу не лезет)
    if len(pup_list) > 348:
        first_letters = {(x[0][0].upper(), '') for x in pup_list}
        pup_list.extend(first_letters)
        pup_list.sort()

    if len(pup_list) <= 348:
        pages = [pup_list]
    else:  # Пока считаем, что больше 2 страниц не бывает.
        fpl = (len(pup_list) + 2) // 2
        pages = [pup_list[:fpl], [(pup_list[fpl][0][0].upper(), '')] + pup_list[fpl:]]
    # Теперь генерим страницы
    text = tex_head
    for pn, pup_list in enumerate(pages):
        cur_text = (r'\newpage' if pn > 0 else '') + page_head
        # Теперь подгоним масштаб под кол-во школьников
        if len(pup_list) <= 112:
            cur_text = cur_text.replace(r'\fontsize{12}{13.6}', r'\fontsize{13}{15}')
        elif len(pup_list) <= 124:
            cur_text = cur_text.replace(r'\fontsize{12}{13.6}', r'\fontsize{13}{14}')
        elif len(pup_list) <= 252:
            cur_text = cur_text.replace(r'\fontsize{12}{13.6}', r'\fontsize{13}{16}')
        elif len(pup_list) <= 268:
            cur_text = cur_text.replace(r'\fontsize{12}{13.6}', r'\fontsize{13}{15}')
        elif len(pup_list) <= 284:
            cur_text = cur_text.replace(r'\fontsize{12}{13.6}', r'\fontsize{13}{14}')
        elif len(pup_list) <= 300:
            cur_text = cur_text.replace(r'\fontsize{12}{13.6}', r'\fontsize{12}{13.6}')
        elif len(pup_list) <= 320:
            cur_text = cur_text.replace(r'\fontsize{12}{13.6}', r'\fontsize{12}{12.7}')
        elif len(pup_list) <= 348:
            cur_text = cur_text.replace(r'\fontsize{12}{13.6}', r'\fontsize{11}{12.0}')
        cur_text = [cur_text]
        cur_text.append(table_head)
        rows_in_col = ((len(pup_list) + 3) // 4)
        for i, (pup, aud) in enumerate(pup_list):
            if i > 0 and i % rows_in_col == 0:
                cur_text.append(table_bottom)
                cur_text.append(table_head)
            if len(pup) == 1 and aud == '':
                pup = r'\textbf{' + pup + '}'
                aud = pup
            cur_text.append(table_row.format(pup, aud))
        cur_text.append(table_bottom)
        cur_text.append(first_time_text)
        cur_text.append(page_bottom)
        text += ''.join(cur_text)
    text += tex_bottom
    # Если список мал, то печатаем на A4
    if len(pup_list) <= 124:
        text = text.replace(r'\usepackage[a3paper,margin=.7truecm]{geometry}',
                            r'\usepackage[a4paper,margin=.7truecm,landscape]{geometry}')

    filename = DUMMY_FOLDER_PATH + 'Распределение по аудиториям.tex'
    lg.info('Создаём ' + filename)
    with open(filename, 'w', encoding='windows-1251') as f:
        f.write(text)


def compile_and_copy():
    compile_tex('Распределение по аудиториям.tex', DUMMY_FOLDER_PATH)
    compile_tex('Поаудиторные списки.tex', DUMMY_FOLDER_PATH)

    copyfile(os.path.join(DUMMY_FOLDER_PATH, 'Поаудиторные списки.pdf'),
             os.path.join(PRINT_PDFS_PATH, '_Per aud. lists.pdf'))
    copyfile(os.path.join(DUMMY_FOLDER_PATH, 'Распределение по аудиториям.pdf'),
             os.path.join(PRINT_PDFS_PATH, '_Total aud. distribution.pdf'))
    # Удаляем треш
    for path in DUMMY_FOLDER_PATH, START_PATH:
        for name in os.listdir(path):
            if '.' in name and name.lower()[name.rfind('.') + 1:] in ('bak', 'aux', 'bbl', 'blg', 'log', 'synctex'):
                os.remove(os.path.join(path, name))


def upd_stats(pup_lst):
    stats = read_stats()
    lvl_aud_cnt = Counter((def_real_level(pup['Уровень']), pup['Аудитория']) for pup in pup_lst)
    for (lvl, aud), cnt in lvl_aud_cnt.items():
        stats[cur_les][lvl]['Аудитории'][aud] = cnt
    update_stats(stats)


pup_lst = parse_xls_conduit(XLS_CONDUIT_NAME_TEMPLATE)

lg.info("В данном контексте нам не нужны скрытые школьники. А также, у которых нет аудитории. Убираем")
pup_lst = [pup for pup in pup_lst if
           pup['Скрыть'] in (None, 0, '0', '', 0.0, '0.0') and pup['Аудитория'] and pup['Уровень']]
lg.debug(pup_lst)
upd_stats(pup_lst)

remove_old_spis()
gen_spisok_files(pup_lst)
gen_aud_lists(pup_lst)
gen_mega_floor_lists(pup_lst)
compile_and_copy()
