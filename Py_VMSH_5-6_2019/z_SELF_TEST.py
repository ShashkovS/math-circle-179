import logging
import ftplib
import io
import inspect
logging.basicConfig(level=logging.INFO)
lg = logging.getLogger('ВМШ')

lg.info('*'*50)
lg.info('Проверяем наличие пакетов...')
import PIL
import PyPDF2
import PyQt5
import pyzbar
import cv2
import numpy
import pyperclip
import requests
import xlrd
import xlwt
import pdf417gen

lg.info('*'*50)
lg.info('Проверяем пути к texify и gswin64c...')
from z_BIN_PATH import *
lg.info('Необходимые пути найдены:\n  {}\n  {}\n  {}'.format(START_PATH, TEXIFY_PATH, GS_PATH))

lg.info('*'*50)
lg.info('Импортируем настройки...')
from z_CONSTS import *

lg.info('*'*50)
lg.info('Проверяем файл с кондуитом...')
from z_helpers import *
pup_lst = parse_xls_conduit(XLS_CONDUIT_NAME_TEMPLATE.replace(f'{cur_les:02}', '00'))
lg.info('Прочиталось следующее:')
for row in pup_lst:
    lg.info(str(row))

lg.info('*'*50)
lg.info("Проверяем работу LaTeXа и Ghostscript'а...")
tikz = r"""
\begin{tikzpicture}
  \draw (0,0) circle (1);
  \draw (0,0) -- (0:1) -- (-135:1) -- (60:1) -- (-60:1) -- (90:1) -- (110:1) ;
\end{tikzpicture}
"""
from a4_html_from_tex import crt_pgns_from_tikz
try:
    os.remove(os.path.join(START_PATH, PICT_DIR, 'self_test.png'))
except FileNotFoundError:
    pass
crt_pgns_from_tikz([tikz], ['self_test'])
if os.path.isfile(os.path.join(START_PATH, PICT_DIR, 'self_test.png')):
    lg.info('Texify и ghostscript работают!')
else:
    raise ValueError('Ошибки в работе texify или ghostscript, увы :(')

lg.info('*'*50)
lg.info("Проверяем работу FTP...")
for wrk in work:
    ftp_path = wrk['ftp_path']
    with ftplib.FTP(wrk["ftp_host"], *wrk['ftp_credentials']) as ftp:
        lg.info('Грузим по ftp файл dates.inc')
        ftp.cwd(ftp_path)
        buffer = io.BytesIO()
        ftp.retrbinary("RETR dates.inc", buffer.write)
        dates_inc = buffer.getvalue().decode('utf-8')
        lg.info('Скачали dates.inc')
        lg.info('\n' + dates_inc)


lg.info('*'*50)
lg.info("Проверяем работу API по выгрузке кондуита наружу...")
import requests
rqs = {'lists': [], 'pupils': [], 'marks': []}
url = work[0]['json_db_api_url']
response = requests.post(url, json=rqs, auth=work[0]['json_db_credentials'])
if response.status_code != 200:
    raise ValueError('Выгрузка кондуита не работает... :(')


lg.info('*'*50)
lg.info("Проверяем работу распознавателя...")
from a5_conduit_recognition import prc_list_of_files
prc_list_of_files([os.path.join(os.path.realpath(os.path.dirname(os.path.abspath(__file__))), r'plus_reader', 'test_img.png')])




lg.info('*'*50)
lg.info('*'*50)
lg.info('*'*50)
lg.info("Все разумные проверки пройдены!")
