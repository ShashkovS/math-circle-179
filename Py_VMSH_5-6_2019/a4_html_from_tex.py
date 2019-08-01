# -*- coding: utf-8 -*-.
from multiprocessing import Pool
from datetime import datetime
from z_CONSTS import *
from z_helpers import *
from shutil import copyfile
import re
import ftplib

# work = (bas, pro)
# work = (pro,)
# cur_les = 10
NON_BREAKING_SPACE = '\u00A0'
NARROW_NO_BREAK_SPACE = '\u202F'
_max_used_bracket_number = 0


# if cur_les in (7, 8, 9):
#     print('Нет, нельзя! Эти условия правились прямо на сайте!')
#     exit()


def pair_curly_brackets(data):
    global _max_used_bracket_number
    data = list(data)
    brackets_stack = []
    for i, c in enumerate(data):
        if c == '{':
            _max_used_bracket_number += 1
            brackets_stack.append(_max_used_bracket_number)
            data[i] = f'❴{_max_used_bracket_number}❴'
        elif c == '}':
            data[i] = f'❵{brackets_stack.pop()}❵'
    return ''.join(data)


def uppair_curly_brackets(data):
    data = re.sub(r'❴\d+❴', r'{', data)
    data = re.sub(r'❵\d+❵', r'}', data)
    return data


def repl_spec_chars(data):
    data = data \
        .replace('\\\\', 'DOUBLE_SLASH_W4MCFkw6VF') \
        .replace(r'\%', 'PERSENT_W4MCFkw6VF') \
        .replace(r'\$', 'DOLLAR_W4MCFkw6VF') \
        .replace(r'\{', 'OPEN_CURLY_BRACKET_W4MCFkw6VF') \
        .replace(r'\}', 'CLOSE_CURLY_BRACKET_W4MCFkw6VF')
    return data


def remove_comments_spaces_text_after_end_doc(data):
    data = re.sub(r'%.*$', r'', data, flags=re.MULTILINE)
    data = re.sub(r'\\end\{document\}.*$', r'', data, flags=re.DOTALL)
    data = re.sub(r'^\n', r'', data, flags=re.MULTILINE)
    # Теперь удаляем разный треш
    data = re.sub(r'\\hbox\{(.*?)\}', r'\1', data)
    data = data.replace(r'\ВосстановитьГраницы', '')
    data = data.replace('\\hfill', '')
    data = data.replace('\\break', '')
    data = re.sub(r'\\УстановитьГраницы.*', '', data)
    data = re.sub(r'\\hangindent\s*-?\w+\\hangafter\s*-?\w+', '', data)
    data = re.sub(r'\\parshape(.*)\n', r'', data)
    data = re.sub(r'\\phantom\{.*?\}', '', data)
    data = re.sub(r'\\[vh]space\{.*?\}', '', data)
    data = data.replace(r'\mbox', '')
    return data


def cur_tikz_pictures(data, tex_file):
    pos = []
    tikz_pictures_texts = []
    tikz_pictures_names = []
    for match in re.finditer(r'\s*\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}\s*', data, flags=re.DOTALL):
        tikz_pictures_texts.append(match.group(0).strip())
        tikz_pictures_names.append('{}_i{:02}'.format(os.path.split(tex_file)[1].replace('.tex', ''), len(tikz_pictures_texts)))
        pos.append((match.start(0), match.end(0)))
    for name, (st, en) in zip(reversed(tikz_pictures_names), reversed(pos)):
        data = data[:st] + name + data[en:]
    return data, tikz_pictures_texts, tikz_pictures_names


def replace_single_characters(data):
    data = data \
        .replace(r'<<', '«') \
        .replace(r'>>', '»') \
        .replace(r'<', ' < ') \
        .replace(r'>', ' > ') \
        .replace(r'\,', NARROW_NO_BREAK_SPACE) \
        .replace(r'\ ', ' ') \
        .replace(r'\!', '') \
        .replace(r'\circ', '°') \
        .replace(r'\No', '№') \
        .replace(r'\angle', '∠') \
        .replace(r'\geqslant', ' ≥ ') \
        .replace(r'\leqslant', ' ≤ ') \
        .replace(r'\geq', ' ≥ ') \
        .replace(r'\leq', ' ≤ ') \
        .replace(r'\cdot', ' · ') \
        .replace('---', '—') \
        .replace('\\-', '') \
        .replace('\\"е', 'ё') \
        .replace('\\"Е', 'Ё') \
        .replace('\вСтрочку', '') \
        .replace('~', ' ') \
        .replace(r'\times', ' × ') \
        .replace(r'\ldots', '...') \
        .replace(r'\dots', '...') \
        .replace(r'\hss', '') \
        .replace(r'\noindent', '') \
        .replace(r'\displaystyle', '') \
        .replace(r'\qquad', ' ')
    data = re.sub(r'\\лк\s+', '«', data)
    data = re.sub(r'\\лк(?=\W)', '«', data)
    data = re.sub(r'\\пк(?=\W)', '» ', data)
    return data


def replace_over(data):
    # Пока не доделано
    frac_repl = r'\\frac❴\1❵❴\2❵'
    # data = re.sub(r'([a-z0-9]+)\s*\\over\s*([a-z0-9]+)', frac_repl, data)
    # data = re.sub(r'([a-z0-9]+)\s*\\over\s*(\{)', frac_repl, data)
    data = re.sub(r'\{([^{}]+)\}\s*\\over\s*\{([^{}]+)\}', frac_repl, data)
    data = re.sub(r'([a-z0-9]+)\s*\\over\s*\{([^{}]+)\}', frac_repl, data)
    data = re.sub(r'\{([^{}]+)\}\s*\\over\s*([a-z0-9]+)', frac_repl, data)
    data = re.sub(r'([a-z0-9]+)\s*\\over\s*([a-z0-9]+)', frac_repl, data)
    data = re.sub(r'\{([^{}]+)\}\s*\\over\s*\{([^{}]+)\}', frac_repl, data)
    data = re.sub(r'([a-z0-9]+)\s*\\over\s*\{([^{}]+)\}', frac_repl, data)
    data = re.sub(r'\{([^{}]+)\}\s*\\over\s*([a-z0-9]+)', frac_repl, data)
    data = re.sub(r'([a-z0-9]+)\s*\\over\s*([a-z0-9]+)', frac_repl, data)
    data = re.sub(r'\{([^{}]+)\}\s*\\over\s*\{([^{}]+)\}', frac_repl, data)
    data = re.sub(r'([a-z0-9]+)\s*\\over\s*\{([^{}]+)\}', frac_repl, data)
    data = re.sub(r'\{([^{}]+)\}\s*\\over\s*([a-z0-9]+)', frac_repl, data)
    data = re.sub(r'([a-z0-9]+)\s*\\over\s*([a-z0-9]+)', frac_repl, data)
    data = data.replace('❵', '}').replace('❴', '{')
    return data


def repl_indexes_and_powers(data):
    # Индексы и степени
    data = re.sub(r'_\{(.*?)\}', r'<sub>\1</sub>', data)
    data = re.sub(r'\^\{(.*?)\}', r'<sup>\1</sup>', data)
    data = re.sub(r'_(\d)', r'<sub>\1</sub>', data)
    data = re.sub(r'\^(\d)', r'<sup>\1</sup>', data)
    return data


def process_images(data, wrk):
    # спасаем картинки
    # В некоторых картинках мы знаем правильную ширину. Используем её
    img_text = r'\\задача<img alt="\2" style="width:100%; max-width:300px;" src="i/{cl:02}-{lv}-IXX.png"/>\\кзадача'.format(cl=cur_les,
                                                                                                                            lv=wrk['short_eng_level'])
    img_text_w = r'\задача<img alt="{alt}" style="width:100%; max-width:{wd}px;" src="i/{cl:02}-{lv}-IXX.png"/>\кзадача'.format(cl=cur_les, wd='{wd}',
                                                                                                                                alt='{alt}', lv=wrk[
            'short_eng_level'])
    img_text_lf_w = r'\задача<img alt="{alt}" style="float:left; width:100%; max-width:{wd}px;" src="i/{cl:02}-{lv}-IXX.png"/>\кзадача'.format(
        cl=cur_les, wd='{wd}', alt='{alt}', lv=wrk['short_eng_level'])
    pos = []
    for match in re.finditer(r'\\rightpicture\{(.*?)\}\{.*?\}\{(.*?)\}\{(.*?)\}', data, flags=re.DOTALL):
        wd = match.group(2).strip().replace('true', '')
        im_w = -1
        if wd.endswith('cm'):
            try:
                im_w = int(round(900 / (20 / int(wd[:-2]))))
            except:
                im_w = -1
        if wd.endswith('mm'):
            try:
                im_w = int(round(900 / (200 / int(wd[:-2]))))
            except:
                im_w = -1
        if im_w > 0:
            pos.append((match.start(0), match.end(0), img_text_w.format(wd=im_w, alt=match.group(3).strip())))
    for match in re.finditer(r'\\leftpicture\{(.*?)\}\{.*?\}\{(.*?)\}\{(.*?)\}', data, flags=re.DOTALL):
        wd = match.group(2).strip().replace('true', '')
        im_w = -1
        if wd.endswith('cm'):
            try:
                im_w = int(round(900 / (20 / int(wd[:-2]))))
            except:
                im_w = -1
        if wd.endswith('mm'):
            try:
                im_w = int(round(900 / (200 / int(wd[:-2]))))
            except:
                im_w = -1
        if im_w > 0:
            pos.append((match.start(0), match.end(0), img_text_lf_w.format(wd=im_w, alt=match.group(3).strip())))
    for st, en, text in sorted(pos, reverse=True):
        data = data[:st] + text + data[en:]
    lg.debug('-' * 100);
    lg.debug(data)

    data = re.sub(r'\\putpicts\{.*?\}\{.*?\}\{(.*?)\}(\{.*?\}){0,2}', img_text, data)
    data = re.sub(r'\\onlyput\{(.*?)\}\{.*?\}\{(.*?)\}', r"\2", data)
    data = re.sub(r'\\rightpicture\{(.*?)\}\{.*?\}\{.*?\}\{(.*?)\}', img_text, data)
    data = re.sub(r'\\leftpicture\{(.*?)\}\{.*?\}\{.*?\}\{(.*?)\}', img_text, data)
    data = re.sub(r'\\righttikzw\{(.*?)\}\{.*?\}\{.*?\}\{(.*?)\}', img_text, data)
    data = re.sub(r'\\righttikz\{(.*?)\}\{.*?\}\{(.*?)\}', img_text, data)
    data = re.sub(r'\\lefttikzw\{(.*?)\}\{.*?\}\{.*?\}\{(.*?)\}', img_text, data)
    data = re.sub(r'\\lefttikz\{(.*?)\}\{.*?\}\{(.*?)\}', img_text, data)
    data = re.sub(r'\\includegraphics(\[.*?\])?\{(.*?)\}', img_text, data)
    data = re.sub(r'\\задача\s*\\задача(<img alt=.*_IXX.png"/>)\\кзадача', r'\\задача\n\1', data)
    lg.debug('-' * 100);
    lg.debug(data)
    return data


def find_tex_parm_group(data, strpos):
    while re.fullmatch(r'\s', data[strpos]): strpos += 1
    # strpos — первый непробельный после frac. Если это не {, то весь числитель — один символ
    endpos = strpos + 1
    if data[strpos] == '{':
        deep = 1
        while deep > 0:
            if data[endpos] == '}':
                deep -= 1
            elif data[endpos] == '{':
                deep += 1
            endpos += 1
    return strpos, endpos


def process_fractions(data):
    data = re.sub(r'\\dfrac(?![a-zA-Z])', r'\\frac', data)
    frac_html = r"""<span style="display: inline-block; vertical-align:middle; padding: 0 5px; text-align: center; white-space: nowrap;">
    <span style="vertical-align: bottom; border-bottom: 1px solid Black; display: block;">{}</span>
    <span style="vertical-align: top;">{}</span>
    </span>""".replace('\n', '')

    frac = re.search(r'\\frac(?![a-zA-Z])', data)
    while frac:
        frs, fre = frac.span()
        ts, te = find_tex_parm_group(data, fre)
        bs, be = find_tex_parm_group(data, te)
        data = data[:frs] + frac_html.format(data[ts:te].strip('{}'), data[bs:be].strip('{}')) + data[be:]
        frac = re.search(r'\\frac(?![a-zA-Z])', data)
    data = re.sub(r'\\over\s+', '/', data)
    return data


def remove_non_problem_text(data):
    only_problems = re.findall(r'\\[а-я]{0,2}задача.*?\\кзадача', data, flags=re.DOTALL)
    data = '\n\n\n'.join(only_problems)
    return data


def fix_dummy_problem_replaces(data):
    data = data.replace('DOUBLE_SLASH_W4MCFkw6VF', '<br/>')
    data = data.replace('PERSENT_W4MCFkw6VF', '%')
    data = data.replace('OPEN_CURLY_BRACKET_W4MCFkw6VF', '{')
    data = data.replace('CLOSE_CURLY_BRACKET_W4MCFkw6VF', '}')
    data = data.replace('\\задачаDOP_PART_W4MCFkw6VF\\кзадача', '<p class="dopproblems">Дополнительные задачи</p>')
    data = data.replace(r'\задача<img', '<img') \
        .replace(r'IXX.png"/>\кзадача', 'IXX.png"/>')
    return data


def cvt_problem_and_puncts(data):
    data = re.sub(r'\\кзадача', '</p>\n\n', data, flags=re.MULTILINE)
    data = re.sub(r'\\[а-я]{0,2}задача[а-я]?', r'<p id="X"> <span class="problem_num"><b>Задача X</b></span>\n', data, flags=re.MULTILINE)
    data = re.sub(r'<b>Задача X</b></span>\s*', r'<b>Задача X</b></span>\n', data)
    data = re.sub(r'\\[а-я]{0,2}пункт[а-я]?', '\n' + r'<br/><span class="punct_num"><b>пункт X</b></span>\n', data, flags=re.MULTILINE)
    data = re.sub(r'\s+<br/><span class="punct_num">', '\n<br/><span class="punct_num">', data, flags=re.MULTILINE)
    # Вставляем нумерацию
    pp = data.find('пункт X')
    while pp >= 0:
        next_z = data.find('Задача X', pp)
        if next_z < 0:
            next_z = 10 ** 6
        j = 0
        while pp >= 0 and pp < next_z:
            data = data.replace('пункт X', '' + PUNCTS[j] + ')', 1)
            j += 1
            pp = data.find('пункт X')
    j = 0
    while data.find('Задача X') >= 0:
        j += 1
        data = data.replace('Задача X', 'Задача ' + str(cur_les) + '.' + str(j) + '.', 1)
    # Проставляем ID-шники задач. Вдруг пригодятся
    j = 0
    while data.find(r'<p id="X">') >= 0:
        j += 1
        data = data.replace(r'<p id="X">', r'<p id="prob_{:02}_{:02}">'.format(cur_les, j), 1)
    # Заменяем двойные пропуски строк
    data = re.sub(r'<br/>\s*<br/>', r'<br/>', data)
    return data


def numerize_images(data):
    j = 0
    while data.find('-IXX.png') >= 0:
        j += 1
        data = data.replace('-IXX.png', '-I{:02}.png'.format(j), 1)
    return data


def replace_math(data):
    # Формулы
    data = re.sub(r'\$(.*?)\$', r'<em>\1</em>', data)
    data = re.sub(r'\\hspace\*?\{.*?\}', '', data)
    data = data.replace(r'^', '')
    data = re.sub(r'\\rm\s', '', data)  # Удаляем указания на \rm
    data = re.sub(r'\\overline\{(.*?)\}', r'<span style="text-decoration: overline;">\1</span>', data)
    data = data.replace('{', '').replace('}', '')
    data = re.sub(r'<br/>\s*<br/>', '<br/>', data)
    data = re.sub(r'\s*\+\s*', r' + ', data)
    data = re.sub(r'\$(\d+) *\\times *(\d+)\$', r' \1 × \2 ', data)
    data = re.sub(r'\$(\d+) *\\times *(\d+) *\\times *(\d+)\$', r' \1 × \2 × \3 ', data)
    data = re.sub(r'\\hbox to \d+\w{2,6}\{(.*?)\}', r'\1', data)
    data = re.sub(r'\{\s*\\it (.*?)\}', r'<em>\1</em>', data, flags=re.DOTALL)
    data = re.sub(r'\{\s*\\em (.*?)\}', r'<em>\1</em>', data, flags=re.DOTALL)
    data = re.sub(r'\\underline\{([^{}]+?)\}', r'<u>\1</u>', data, flags=re.DOTALL)
    data = re.sub(r'\{\\tt ([^{}]*?)\}', r'<code>\1</code>', data)
    data = re.sub(r'\$\\tt (.*?)\$', r'<code>\1</code>', data)
    return data


def hide_unknown_commands(data):
    data = re.sub(r'(\\[a-zA-Zа-яА-Я]+)', r'<span class="stat" style="background-color: RGB(255,0,0);">\1</span>', data)
    return data


def crt_pgns_from_tikz(tikz_pictures_texts, tikz_pictures_names):
    # Теперь нужно создать tikz-картинки.
    tikz_sample = r"""
    \documentclass[tikz, border=5pt]{standalone}
    \usetikzlibrary{calc,through,intersections,backgrounds,arrows}
    \usepackage{russ}
    \begin{document}
    TIKZ_CODE
    \end{document}
        """
    for text, texname in zip(tikz_pictures_texts, tikz_pictures_names):
        text = re.sub(r'\n\s*', r'\n', text)
        text = re.sub(r'\n\n+', r'\n', text)
        cur_tex_name = os.path.join(START_PATH, PICT_DIR, texname + '.tex')
        tex_data = tikz_sample.replace('TIKZ_CODE', text).strip()
        with open(cur_tex_name, 'w', encoding='windows-1251') as f:
            f.write(tex_data)
        lg.info(cur_tex_name)
        lg.debug(tex_data)
        compile_tex(texname + '.tex', add_path=PICT_DIR)
        # Теперь конвертим pdf в png
        pdf2png(texname + '.pdf', add_path=PICT_DIR, dest=os.path.join(texname + '.png'))
        # pdf2png(texname + '.pdf', add_path=PICT_DIR, dest=os.path.join('png_picts', texname + '.png'))
    for name in os.listdir(os.path.join(START_PATH, PICT_DIR)):
        if '.' in name and name.lower()[name.rfind('.') + 1:] in ('bak', 'aux', 'bbl', 'blg', 'log', 'synctex'):
            os.remove(os.path.join(START_PATH, PICT_DIR, name))


def copy_images_to_html_folders(data, wrk):
    lg.info('Теперь копируем все картинки...')
    import shutil
    j = 0
    for match in re.finditer('<img alt="(.*?)"', data):
        filename = match.group(0)[10:-1] + '.png'
        filename = filename.replace('.png.png', '.png')
        if not os.path.isfile(os.path.join(PICT_DIR, filename)) \
                and os.path.isfile(os.path.join(PICT_DIR, filename.replace('.png', '.pdf'))):
            pdf2png(filename.replace('.png', '.pdf'), add_path=PICT_DIR, dest=filename)
            # pdf2png(filename.replace('.png', '.pdf'), add_path=PICT_DIR)
        j += 1
        to_filename = '{:02}-{}-I{:02}.png'.format(cur_les, wrk['short_eng_level'], j)
        try:
            shutil.copy(os.path.join(START_PATH, PICT_DIR, filename),
                        os.path.join(START_PATH, wrk['htmls_path'], 'i', to_filename))
            lg.info('{} -> {}'.format(filename, to_filename))
        except:
            lg.error('Не удалось скопировать {} в {}'.format(filename, to_filename))


def create_local_test_html(wrk):
    htmls_path = wrk['htmls_path']
    htmls_notifications_path = wrk['htmls_notifications_path']
    htmls = {}
    # Вычитываем все файлы
    for filename in os.listdir(os.path.join(START_PATH, htmls_notifications_path)):
        full_path = os.path.join(START_PATH, htmls_notifications_path, filename)
        if not os.path.isfile(full_path):
            continue
        htmls[filename] = open(full_path, 'r', encoding='utf-8').read()
    dates = {}
    # Парсим даты
    for les_num, year, month, day, hour, minute, second in re.findall(r'^"(\w+)"\s*=>\s*(\d+)\D(\d+)\D(\d+)\D(\d+)\D(\d+)\D(\d+)\s*$', htmls['dates.inc'], flags=re.MULTILINE):
        dates[les_num] = datetime(*map(int, (year, month, day, hour, minute, second)))
    dates['∞'] = datetime(9999, 12, 31, 19, 0, 0)
    # Находим ближайшую большую
    next_date = min(dt for dt in dates.values() if dt >= datetime.now())
    days_names = ["", "понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"]
    month_names = ["", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    nearest_date = f'{days_names[next_date.isoweekday()]} {next_date.day}-го {month_names[next_date.month]}'

    # Парсим шаблон
    index_template = parse_html_template(os.path.join(PY_PROJ_DIR_PATH, 'tex_templates', 'index.template.html'))
    result_html = []
    # TODO Вот здесь захардкожено участие ровно двух уровней сложности
    result_html.append(index_template['html_top'].format(other_url=bas['test_local_html'] if wrk!=bas else pro['test_local_html'],
                                                         other_text=bas['name'] if wrk!=bas else pro['name'],
                                                         contact_html='../' + wrk['htmls_notifications_path'] + '/contact.html',
                                                         about_html='../' + wrk['htmls_notifications_path'] + '/about.html',
                                                         nearest_date=nearest_date,
                                                         onTheTopForAll=htmls['onTheTopForAll.html'],
                                                         onTheTopForReg=htmls['onTheTopForReg.html'],
                                                         onTheTopForNoReg=htmls['onTheTopForNoReg.html'],
                                                         onTheTopForProOrBeg=htmls['onTheTopForPro.html'] if wrk!=bas else htmls['onTheTopForBeg.html'],
                                                         ))
    # Теперь добавляем все созданные задания
    for les_html_name in os.listdir(os.path.join(START_PATH, wrk['htmls_path'])):
        if not les_html_name.endswith('.html'): continue
        full_les_html_path = os.path.join(START_PATH, wrk['htmls_path'], les_html_name)
        html_les_num = re.sub('\D', '', les_html_name)  # Здесь немного треш :(
        html_les_data = open(full_les_html_path, 'r', encoding='utf-8').read()
        textdt = dates.get(html_les_num, None)
        if textdt is None:
            textdt = f'Дата занятия {html_les_num} в файле dates.inc не найдена'
        else:
            textdt = f'{textdt.day} {month_names[textdt.month]} {textdt.year} г.'
        result_html.append(index_template['lesson'].format(cur_les=html_les_num,
                                                           textdt=textdt,
                                                           lesson_pdf='../' + wrk['htmls_path'] + '/' + wrk['htmls_pdfs_template'].format(cur_les=int(html_les_num)),
                                                           lesson_html=html_les_data.replace(r'src="i/', r'src="../' + wrk['htmls_path'] + '/i/')))


    result_html.append(index_template['html_footer'].format())
    result_html_path = os.path.join(START_PATH, wrk['htmls_path'], '..', wrk['test_local_html'])
    with open(result_html_path, 'w', encoding='utf-8') as f:
        f.write(''.join(result_html))


def do_all_wrk_stuff(wrk):
    htmls_path = wrk['htmls_path']
    tex_file = os.path.join(START_PATH, wrk['tex_name_template'].format(cur_les=cur_les))
    res_file = os.path.join(START_PATH, htmls_path, wrk['htmls_htmls_template'].format(cur_les=cur_les))

    lesson_pdf_name = os.path.join(START_PATH, DUMMY_FOLDER_PATH, wrk['dummy_tex_lesson_template'].format(cur_les=cur_les).replace('.tex', '.pdf'))
    dst_pdf_name = os.path.join(START_PATH, wrk['htmls_path'], wrk['htmls_pdfs_template'].format(cur_les=cur_les))
    lg.info(f'Копируем {lesson_pdf_name} в {dst_pdf_name}')
    copyfile(lesson_pdf_name, dst_pdf_name)

    data = open(tex_file, 'r', encoding='windows-1251').read()
    lg.info('Открыли ТеХ файл, обрабатываем ' + tex_file)

    # Подменяем спецсимволы
    data = repl_spec_chars(data)
    # Удаляем комментарии и треш
    data = remove_comments_spaces_text_after_end_doc(data)
    # Вырезаем tikz-картинки
    data, tikz_pictures_texts, tikz_pictures_names = cur_tikz_pictures(data, tex_file)
    # Сохраняем допраздел
    data = data.replace(r'допраздел', '\n\n\\задачаDOP_PART_W4MCFkw6VF\\кзадача\n')
    # Заменяем отельные символы и команды
    data = replace_single_characters(data)
    # Удаляем команды text
    data = re.sub(r'\\text\{(.*?)\}', r'\1', data)
    # Заменяем \over на \frac
    data = replace_over(data)
    # Обрабатываем картинки
    data = process_images(data, wrk)
    # Обрабатываем индексы и степени
    data = repl_indexes_and_powers(data)
    # Обрабатываем дроби
    data = process_fractions(data)
    # Выбрасываем всё кроме задач
    data = remove_non_problem_text(data)
    # Возвращаем насильно испорченное
    data = fix_dummy_problem_replaces(data)
    # Подменяем разнообразные мат-формулы
    data = replace_math(data)
    # Проставляем нумерацию задач и пунктов
    data = cvt_problem_and_puncts(data)
    # Проставляем нумерацию изображений
    data = numerize_images(data)
    # Прячем нераспознанные команды
    data = hide_unknown_commands(data)
    # Ок, готово, сохраняем
    with open(res_file, 'w', encoding='utf-8') as f:
        lg.debug(data)
        f.write(data)
    # Конвертим картинки tikz в png
    crt_pgns_from_tikz(tikz_pictures_texts, tikz_pictures_names)
    # Копируем картинки в соответствующую папку (с переименованием)
    copy_images_to_html_folders(data, wrk)
    # Создаём локальную версию со всеми условиями для отладки
    create_local_test_html(wrk)
    # Ура!
    lg.info('Блин, ну мы сделали это! Сколько говонокода, а?')


if __name__ == '__main__':
    pool = Pool(processes=2)
    # Запускаем по процессу на начинающих и продолжающих
    result = pool.map_async(do_all_wrk_stuff, work)
    result.get(timeout=120)

    lg.info("")
    lg.info("Всё готово!")
