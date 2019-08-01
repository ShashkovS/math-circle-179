# -*- coding: utf-8 -*-.
from multiprocessing import Pool
from z_helpers import *
from datetime import datetime
import ftplib
import io


# work = (bas, pro)
# work = (pro,)
# cur_les = 10

# if cur_les in (7, 8, 9):
#     print('Нет, нельзя! Эти условия правились прямо на сайте!')
#     exit()


def upload_to_site(wrk):
    ftp_path = wrk['ftp_path']
    htmls_path = wrk['htmls_path']
    lg.info('Шлём условия по ftp в ' + ftp_path)
    pdf_filename = wrk['htmls_pdfs_template'].format(cur_les=cur_les)
    html_filename = wrk['htmls_htmls_template'].format(cur_les=cur_les)
    pdf_full_path = os.path.join(START_PATH, htmls_path, pdf_filename)
    html_full_path = os.path.join(START_PATH, htmls_path, html_filename)
    img_path = os.path.join(START_PATH, htmls_path, 'i')
    img_filenames = [name for name in os.listdir(img_path) if name.startswith('{:02}-'.format(cur_les))]
    # Всё готово, хреначим
    with ftplib.FTP(wrk["ftp_host"], *wrk['ftp_credentials']) as ftp:
        ftp.cwd(ftp_path + 'data')
        ftp.storbinary("STOR " + pdf_filename, open(pdf_full_path, 'rb'))
        lg.info(pdf_filename + ' done')
        ftp.storbinary("STOR " + html_filename, open(html_full_path, 'rb'))
        lg.info(html_filename + ' done')
        ftp.cwd(ftp_path + 'i')
        for img_filename in img_filenames:
            ftp.storbinary("STOR " + img_filename, open(os.path.join(img_path, img_filename), 'rb'))
            lg.info(os.path.join(img_path, img_filename) + ' done')

        lg.info('Шлём объявления и даты по ftp в ' + ftp_path)
        ftp.cwd(ftp_path)
        htmls_notifications_path = wrk['htmls_notifications_path']
        for filename in os.listdir(os.path.join(START_PATH, htmls_notifications_path)):
            full_path = os.path.join(START_PATH, htmls_notifications_path, filename)
            if not os.path.isfile(full_path):
                continue
            if filename == 'dates.inc':
                dates_data = open(full_path, 'r', encoding='utf-8').read()
                dates = {}
                # Парсим даты
                for les_num, year, month, day, hour, minute, second in re.findall(r'^"(\w+)"\s*=>\s*(\d+)\D(\d+)\D(\d+)\D(\d+)\D(\d+)\D(\d+)\s*$',
                                                                                  dates_data, flags=re.MULTILINE):
                    dates[les_num+'-'+wrk['short_eng_level']] = datetime(*map(int, (year, month, day, hour, minute, second)))
                php = '<?php $datesarr = array(\n' + \
                      '\n'.join(f'"{num}" => new DateTime("{dt.strftime("%Y-%m-%dT%H:%M:%SZ")}"),'
                                for num, dt in sorted(dates.items(), key=lambda x: x[1], reverse=True)) + \
                      '\n); ?>'
                fp = io.BytesIO(php.encode('utf-8'))
            else:
                fp = open(full_path, 'rb')
            ftp.storbinary("STOR " + filename, fp)
            lg.info(full_path + ' done')


def do_all_wrk_stuff(wrk):
    # Выргужаем на сайт задание
    upload_to_site(wrk)
    # Ура!
    lg.info('Блин, ну мы сделали это! Сколько говонокода, а?')


if __name__ == '__main__':
    pool = Pool(processes=1)
    # Запускаем по процессу на начинающих и продолжающих
    result = pool.map_async(do_all_wrk_stuff, work)
    result.get(timeout=120)

    lg.info("")
    lg.info("Всё готово!")
