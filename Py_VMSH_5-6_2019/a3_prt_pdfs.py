# old code
# -*- coding: utf-8 -*-.
from z_CONSTS import *
from z_helpers import *
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
from copy import copy
from multiprocessing import Pool

#work = (bas,)
# work = (pro, )


if PORTRAIT_ORIENTATION:
    # Нам нужна пустая страница, чтобы на неё "клеить" листы А5 и А6
    blank_page = PdfFileReader(open(os.path.join(PRINT_PDFS_PATH, 'Разное', "blank_page.pdf"), "rb")).getPage(0)




def remove_old_pdfs(wrk):
    lg.info(wrk["short_eng_level"] + 'Удаляем старые pdf...')
    for name in os.listdir(PRINT_PDFS_PATH):
        if name.startswith(wrk['prt_pdf_prefix']) and name.lower().endswith('.pdf'):
            os.remove(os.path.join(PRINT_PDFS_PATH, name))
        if name == '_all_all_all.pdf':
            try:
                os.remove(os.path.join(PRINT_PDFS_PATH, name))
            except FileNotFoundError:
                pass


def crt_big_counduits(wrk, r_in_pdf_conduit, r_prev_name_conduit):
    # Кондуиты в аудитории
    # Берём со второго по предпоследний лист из cur_name_conduit,
    # каждой второй страницей берём последний лист prev_name_conduit
    filename = os.path.join(PRINT_PDFS_PATH, wrk['prt_pdf_prefix'] + "3_aud_conds_" + ("(2side!)" if r_prev_name_conduit else "") + '.pdf')
    lg.info(wrk["short_eng_level"] + filename + '...')
    lg.info(wrk["short_eng_level"] + filename + '...')
    output = PdfFileWriter()
    if r_prev_name_conduit:
        old_cond = r_prev_name_conduit.getPage(r_prev_name_conduit.getNumPages()-1)
        old_cond.scaleBy(0.85)
    for i in range(1, r_in_pdf_conduit.getNumPages() - 1):
        output.addPage(r_in_pdf_conduit.getPage(i))
        if r_prev_name_conduit:
            output.addPage(old_cond)
    with open(filename, "wb") as f:
        output.write(f)


def crt_big_counduits_new(wrk, r_in_pdf_conduit, r_prev_in_pdf_conduit):
    # Кондуиты в аудитории
    # Берём со второго по предпоследний лист из cur_name_conduit,
    # каждой второй страницей берём последний лист prev_name_conduit
    filename = os.path.join(PRINT_PDFS_PATH, wrk['prt_pdf_prefix'] + "3_aud_conds_" + ("(2side!)" if r_prev_name_conduit else "") + '.pdf')
    lg.info(wrk["short_eng_level"] + filename + '...')
    lg.info(wrk["short_eng_level"] + filename + '...')
    output = PdfFileWriter()
    for i in range(1, r_in_pdf_conduit.getNumPages() - 1):
        output.addPage(r_in_pdf_conduit.getPage(i))
        output.addPage(r_prev_in_pdf_conduit.getPage(i))
    with open(filename, "wb") as f:
        output.write(f)


def crt_teacher_texts_ans_counduits(wrk, r_in_pdf_conduit, r_in_pdf_teacher):
    filename = os.path.join(PRINT_PDFS_PATH, wrk['prt_pdf_prefix'] + "4_teacher_task_and_cond_(2side!)_("
                                             + str(wrk['teacher_conduit_copies_per_aud'])
                                             + ' copies).pdf')
    lg.info(wrk["short_eng_level"] + filename + '...')
    output = PdfFileWriter()
    page0 = r_in_pdf_teacher.getPage(0)
    for i in range(1, r_in_pdf_conduit.getNumPages() - 1):
        lg.info(wrk["short_eng_level"] + '  аудитория ' + str(i))
        if not PORTRAIT_ORIENTATION:
            output.addPage(page0)
        else:
            page1 = copy(page0)
            page1.rotateClockwise(90)
            page2 = copy(page1)
            page1.mergeTranslatedPage(page2, page2.mediaBox[2], 0, expand=True)
            output.addPage(page1)
        page1 = r_in_pdf_conduit.getPage(i)
        page1.scaleBy(0.7071067811865475)
        page1.rotateClockwise(90)
        page2 = copy(page1)
        page1.mergeTranslatedPage(page2, page2.mediaBox[2], 0, expand=True)
        output.addPage(page1)
    with open(filename, "wb") as f:
        output.write(f)



def crt_current_lesson_pdf(wrk, r_in_pdf):
    lg.info(wrk["short_eng_level"] + 'Текущие условия и дополнительные задачи')
    lvl = wrk['excel_level_const']
    reg_page = None
    both_sides = True
    r_in_pdf_pages = r_in_pdf.getNumPages()
    sizes = [r_in_pdf.getPage(i).mediaBox[2:] for i in range(r_in_pdf_pages)]
    # Здесь лютый хардкод
    types = ['A6' if 200 < y <400 else 'A5' if 400 < y < 700 else 'A4' for x, y in sizes]
    if types.count('A5') > 2:
        lg.error('Почему-то в условиях слишком много листов формата A5')
    both_sides = types.count('A5') > 1

    # if ADD_REG_INFO_TO_PRT_PDFS and r_in_pdf_pages <= 2:  # Если страниц 3, то основное условие на двух sideх
    #     try:
    #         reg_page = PdfFileReader(open(os.path.join(PRINT_PDFS_PATH, 'Разное', "Регистрация_на_кружок.pdf"), "rb")).getPage(0)
    #         both_sides = True
    #     except:
    #         lg.error('Не найден файл с информацией о регистрации Регистрация_на_кружок.pdf')
    #         reg_page = None
    # elif r_in_pdf_pages > 2:
    #     both_sides = True
    # Определяем количество аудиторий данного типа
    try:
        stats = read_stats()  # Статистика добыта в crt1 и crt2
        num_auds = len(stats[cur_les][lvl]['Аудитории'])
        cpy_per_aud = wrk['main_problems_copies_per_aud']
        num_copies = (num_auds * cpy_per_aud + 1) // 2
        copys_string = f'_({num_copies} copies ({cpy_per_aud} per aud.))'
    except:
        copys_string = ''
    filename = os.path.join(PRINT_PDFS_PATH, wrk['prt_pdf_prefix']
                                             + "1_tasks_"
                                             + ("(2side!)" if both_sides else "")
                                             + copys_string
                                             + '.pdf')
    first_page = r_in_pdf.getPage(0)
    second_page = None
    if both_sides:
        second_page = r_in_pdf.getPage(1)
    lg.info(wrk["short_eng_level"] + filename + '...')
    output = PdfFileWriter()
    for _ in range(1):
        if not PORTRAIT_ORIENTATION:
            output.addPage(first_page)
            if second_page:
                output.addPage(second_page)
            else:
                output.addPage(blank_page)
        else:
            page1 = copy(first_page)
            page1.rotateClockwise(90)
            page2 = copy(page1)
            page1.mergeTranslatedPage(page2, page2.mediaBox[2], 0, expand=True)
            output.addPage(page1)
            if second_page:
                page1 = copy(second_page)
                page1.rotateClockwise(90)
                page2 = copy(page1)
                page1.mergeTranslatedPage(page2, page2.mediaBox[2], 0, expand=True)
                output.addPage(page1)
            # else:
            #     output.addPage(blank_page)
        if reg_page:
            output.addPage(reg_page)
    with open(filename, "wb") as f:
        output.write(f)





def crt_addit_lesson_pdf(wrk, r_in_pdf):
    lvl = wrk['excel_level_const']
    both_sides = False
    r_in_pdf_pages = r_in_pdf.getNumPages()
    lg.info(wrk["short_eng_level"] + "pages:" + str(r_in_pdf_pages))

    sizes = [r_in_pdf.getPage(i).mediaBox[2:] for i in range(r_in_pdf_pages)]
    # Здесь лютый хардкод
    types = ['A6' if 200 < y <400 else 'A5' if 400 < y < 700 else 'A4' for x, y in sizes]
    if types.count('A6') > 2:
        lg.error('Почему-то в условиях слишком много листов формата A6')
    a6 = [i for i, t in enumerate(types) if t == 'A6']
    both_sides = len(a6) > 1
    dop_page = r_in_pdf.getPage(a6[0])
    dop_page1 = None
    if both_sides:
        dop_page1 = r_in_pdf.getPage(a6[1])

    # Определяем количество аудиторий данного типа
    try:
        stats = read_stats()  # Статистика добыта в crt1 и crt2
        num_auds = len(stats[cur_les][lvl]['Аудитории'])
        cpy_per_aud = wrk['addit_problems_copies_per_aud']
        copies_per_page = stats[cur_les][lvl]['кол-во копий доп.задач']
        num_copies = (num_auds * cpy_per_aud + copies_per_page - 1) // copies_per_page
        copys_string = f'_({num_copies} copies. ({cpy_per_aud} per aud))'
    except:
        copys_string = ''
    filename = os.path.join(PRINT_PDFS_PATH, wrk['prt_pdf_prefix'] + "2_add_comp_tasks_"
                            + ("(2side!)" if both_sides else "") + copys_string + '.pdf')
    lg.info(wrk["short_eng_level"] + filename + '...')
    output = PdfFileWriter()
    if not PORTRAIT_ORIENTATION:
        output.addPage(dop_page)
        if both_sides:
            output.addPage(dop_page1)
        else:
            output.addPage(blank_page)
    else:
        page1 = copy(dop_page)
        page2 = copy(page1)
        page1.mergeTranslatedPage(page2, page2.mediaBox[2], 0,                 expand=True)
        page2 = copy(page1)
        page1.mergeTranslatedPage(page2, 0, page2.mediaBox[3],                 expand=True)
        output.addPage(page1)
        if both_sides:
            page1 = copy(dop_page1)
            page2 = copy(page1)
            page1.mergeTranslatedPage(page2, page2.mediaBox[2], 0, expand=True)
            page2 = copy(page1)
            page1.mergeTranslatedPage(page2, 0, page2.mediaBox[3], expand=True)
            output.addPage(page1)
        # else:
        #     output.addPage(blank_page)

    with open(filename, "wb") as f:
        output.write(f)




def crt_prev_lesson_pdf(wrk, r_prev_pdf_teacher):
    lg.info(wrk["short_eng_level"] + 'Условия предыдущего занятия')
    if not r_prev_pdf_teacher:
        lg.error('Предыдущее занятие не найдено')
        return
    filename = os.path.join(PRINT_PDFS_PATH, wrk['prt_pdf_prefix'] + "5_предыдущее_занятие.pdf")
    filename = os.path.join(PRINT_PDFS_PATH, wrk['prt_en_pdf_prefix'] + "uslpred.pdf")
    lg.info(wrk["short_eng_level"] + filename + '...')
    output = PdfFileWriter()
    page0 = r_prev_pdf_teacher.getPage(0)
    if not PORTRAIT_ORIENTATION:
        output.addPage(page0)
    else:
        page1 = copy(page0)
        page1.rotateClockwise(90)
        page2 = copy(page1)
        page1.mergeTranslatedPage(page2, page2.mediaBox[2], 0, expand=True)
        output.addPage(page1)
        output.addPage(blank_page)
    with open(filename, "wb") as f:
        output.write(f)


def do_all_wrk_stuff(wrk):
    cur_name = os.path.join(START_PATH, wrk['tex_name_template'].format(cur_les=cur_les)).replace('.tex', '.pdf')
    cur_name_teacher = os.path.join(DUMMY_FOLDER_PATH, wrk['dummy_tex_teacher_template'].format(cur_les=cur_les).replace('.tex', '.pdf'))
    cur_name_conduit = os.path.join(DUMMY_FOLDER_PATH, wrk['dummy_tex_conduit_template'].format(cur_les=cur_les).replace('.tex', '.pdf'))
    cur_name_prev_conduit = os.path.join(DUMMY_FOLDER_PATH,wrk['dummy_tex_prev_conduit_template'].format(cur_les=cur_les).replace('.tex', '.pdf'))
    prev_name_teacher = os.path.join(DUMMY_FOLDER_PATH, wrk['dummy_tex_teacher_template'].format(cur_les=prev_les).replace('.tex', '.pdf')) ##
    prev_name_conduit = os.path.join(DUMMY_FOLDER_PATH, wrk['dummy_tex_conduit_template'].format(cur_les=prev_les).replace('.tex', '.pdf')) ##
    lg.info(wrk["short_eng_level"] + 'Окучиваем для печати ' + cur_name)

    # Открываем PDF-файлы
    r_in_pdf = PdfFileReader(open(cur_name, "rb"))
    r_in_pdf_teacher = PdfFileReader(open(cur_name_teacher, "rb"))
    r_in_pdf_conduit = PdfFileReader(open(cur_name_conduit, "rb"))
    #r_prev_in_pdf_conduit = PdfFileReader(open(cur_name_prev_conduit, "rb"))
    try:
        r_prev_pdf_teacher = PdfFileReader(open(prev_name_teacher, "rb"))
    except:
        r_prev_pdf_teacher = None
        lg.error('Нет предыдщего занятия для учителей (файл ' + prev_name_teacher)
    try:
        r_prev_name_conduit = PdfFileReader(open(prev_name_conduit, "rb"))
    except:
        r_prev_name_conduit = None
        lg.error('Нет предыдщего файла с кондуитом (файл ' + prev_name_conduit)

    # Теперь генерим все pdf'ы
    remove_old_pdfs(wrk)
    crt_current_lesson_pdf(wrk, r_in_pdf)
    crt_addit_lesson_pdf(wrk, r_in_pdf)
    crt_big_counduits(wrk, r_in_pdf_conduit, r_prev_name_conduit)
   # crt_big_counduits_new(wrk, r_in_pdf_conduit, r_prev_in_pdf_conduit)
    crt_prev_lesson_pdf(wrk, r_prev_pdf_teacher)
    crt_teacher_texts_ans_counduits(wrk, r_in_pdf_conduit, r_in_pdf_teacher)


if __name__ == '__main__':
    pool = Pool(processes=2)
    # Запускаем по процессу на начинающих и продолжающих
    result = pool.map_async(do_all_wrk_stuff, work)
    result.get(timeout=120)

    lg.info("")
    lg.info("Всё готово!")
