from z_CREDENTIALS import *
import os

import a0_dates
# Текущее занятие
cur_les = a0_dates.cur_les
prev_les = a0_dates.prev_les
LES_DATE = a0_dates.LES_DATE

# В большом кондуиты аудитории ниже будут заменены
AUD_LIST_REPLACERS = {
    '421': '405',
    '422': '405',
    '423': '405',
    '424': '405',
}
# Эта мега-аудитория будет разбита на несколько поменьше
SPLIT_LARGE_AUD = {
    # '405': [
    #     '421', '422',
    #     # '423', '424'
    # ]
}

CIRCLE_TITLE = "Математический кружок для 5-6 классов, LES_DATE"
CIRCLE_TITLE_SHORT = 'ВМШ 5-6'

# FIRST_TIME_FLOOR, FIRST_TIME_AUD = 'второй этаж', '201'
FIRST_TIME_FLOOR, FIRST_TIME_AUD = None, None  # Пока не печатаем
# Печатать ли на обратной стороне условий инструкцию по регистрации?
ADD_REG_INFO_TO_PRT_PDFS = False

PORTRAIT_ORIENTATION = True
PICT_DIR = r'pictures'
BARCODES = r'barcodes'

# Разные пути
DUMMY_FOLDER_PATH = r"яdummy_files/"
XLS_CONDUIT_PATH = 'Кондуиты/'
PRINT_PDFS_PATH = 'Текущая печать/'

XLS_CONDUIT_NAME = os.path.join(XLS_CONDUIT_PATH, f'Кондуит {cur_les:02}.xlsm')  # Маска имени кондуита
XLS_CONDUIT_SHEET = 'Итог'
CRT_COUNDUIT_COMMAND = '\СделатьКондуитИз{4.4mm}{6mm}'

# Настройки excel'я с кондуитами
FIRST_ROW = 6
COLUMNS = {'Фамилия': "A",
           'Имя': "B",
           'ID': "C",
           'Клс': "D",
           'Скрыть': "F",
           'Уровень': "G",
           'Аудитория': "L",
           'Посещаемость': "H",
           'Ср3': "K"}
COLUMNS = {k: ord(v) - ord('A') for (k, v) in COLUMNS.items()}

# Настройки префиксов-суффиксов
bas = {
    'name': 'Начинающие',
    'main_problems_copies_per_aud': 20,
    'addit_problems_copies_per_aud': 16,
    'teacher_conduit_copies_per_aud': 4,
    'lines_in_conduit': 27,
    'json_db_api_url': 'https://www.shashkovs.ru/vmsh/conduit/ajax/ParseJSON.php',
    'tex_name_template': 'usl-{cur_les:02}-n.tex',
    'prev_tex_name_template': 'usl-{prev_les:02}-n.tex',
    'sol_tex_name_template': 'usl-{cur_les:02}-n-sol.tex',
    'dummy_tex_lesson_template': '{cur_les:02}-lesson-n.tex',
    'dummy_tex_conduit_template': '{cur_les:02}-conduit-n.tex',
    'dummy_tex_prev_conduit_template': '{cur_les:02}-prev_conduit-n.tex',
    'dummy_tex_teacher_template': '{cur_les:02}-teacher-n.tex',
    'prt_pdf_prefix': 'Bas_',
    'prt_en_pdf_prefix': 'n',
    'htmls_path': r'Сайт/Сайт_Баз',
    'htmls_notifications_path': r'Сайт/Объявления, даты, контакты',
    'test_local_html': 'index.bas.html',
    'htmls_pdfs_template': r'{cur_les:02}-n-lesson.pdf',
    'htmls_htmls_template': r'{cur_les:02}-n-lesson.html',
    'ftp_host': "shashkovs.ru",
    'ftp_path': "/",  # /shashkovs.ru/htdocs/www/vmsh/ настроено у пользователя
    'ftp_credentials': FTP_BAS_CRED,
    'excel_level_const': 'н',
    'other_excel_level_const': 'нхНХ',
    'excel_column_shift': 0,
    'spisok_name_template': 'spisok-n-{aud}.tex',
    'pred_spisok_name_template': 'pred_spisok-n-{aud}.tex',
    'short_eng_level': 'n',
    'json_db_credentials': JSON_DB_BAS_CRED,
}

pro = {
    'name': 'Продолжающие',
    'main_problems_copies_per_aud': 20,
    'addit_problems_copies_per_aud': 16,
    'teacher_conduit_copies_per_aud': 4,
    'lines_in_conduit': 27,
    'json_db_api_url': 'https://www.shashkovs.ru/vmsh/conduit/ajax/ParseJSON.php',
    'tex_name_template': 'usl-{cur_les:02}-p.tex',
    'prev_tex_name_template': 'usl-{prev_les:02}-p.tex',
    'sol_tex_name_template': 'usl-{cur_les:02}-p-sol.tex',
    'dummy_tex_lesson_template': '{cur_les:02}-lesson-p.tex',
    'dummy_tex_conduit_template': '{cur_les:02}-conduit-p.tex',
    'dummy_tex_prev_conduit_template': '{cur_les:02}-prev_conduit-p.tex',
    'dummy_tex_teacher_template': '{cur_les:02}-teacher-p.tex',
    'prt_pdf_prefix': 'Pro_',
    'prt_en_pdf_prefix': 'p',
    'htmls_path': r'Сайт/Сайт_Про',
    'htmls_notifications_path': r'Сайт/Объявления, даты, контакты',
    'test_local_html': 'index.pro.html',
    'htmls_pdfs_template': r'{cur_les:02}-p-lesson.pdf',
    'htmls_htmls_template': r'{cur_les:02}-p-lesson.html',
    'ftp_host': "shashkovs.ru",
    'ftp_path': "/",  # /shashkovs.ru/htdocs/www/vmsh-a/ настроено у пользователя
    'ftp_credentials': FTP_PRO_CRED,
    'excel_level_const': 'п',
    'other_excel_level_const': 'пП',
    'excel_column_shift': 31,
    'spisok_name_template': 'spisok-p-{aud}.tex',
    'pred_spisok_name_template': 'pred_spisok-p-{aud}.tex',
    'short_eng_level': 'p',
    'json_db_credentials': JSON_DB_PRO_CRED,
}
levels = {**dict(zip(bas['other_excel_level_const'], [bas] * 100)),
          **dict(zip(pro['other_excel_level_const'], [pro] * 100))}
work = [bas, pro]
# work = [bas]
ADVANCED_LEVEL_CONST = pro['excel_level_const']
PUNCTS = 'абвгдежзиклмнопрст'
