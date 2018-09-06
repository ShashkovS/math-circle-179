from CONSTS import *
from z_helpers import *
import requests
import logging
import re
from collections import Counter
logging.basicConfig(level=logging.DEBUG)

stats = read_stats()

lg.info('Открываем файл (займёт время) ' + XLS_CONDUIT_NAME_TEMPLATE)
rb = xlrd.open_workbook(XLS_CONDUIT_NAME_TEMPLATE)
sheet = rb.sheet_by_index(0)


def rtv_main_part_num_prob(lvl):
    main_part = stats[cur_les][lvl]['структура']
    if main_part:
        main_part = main_part.replace('к', '').index('|')
    if not main_part or main_part <= 0:
        main_part = 1000
    return main_part


def gen_json_lists(sheet):
    json_lists = []
    # Сначала читаем заголовок
    prb_hdr_matcher = re.compile(r'\d{1,2}\w?\.(Н|(\d{1,2}\w\*?))')
    col_hdr_to_colc = {}
    for coln in range(0, sheet.ncols):
        cv = str(sheet.cell(FIRST_ROW - 2, coln).value).strip()
        if not cv.endswith('*') and prb_hdr_matcher.match(cv):
            lstn = int(re.split('\D+', cv)[0])
            if not (cur_les - 3 <= lstn <= cur_les):
                continue
            col_hdr_to_colc[cv] = coln
            print(cv)
    hdr_cnt = Counter(x.split('.')[0] for x in col_hdr_to_colc)
    lsts_to_process = [lst for lst, cnt in hdr_cnt.items() if cnt > 3]
    col_hdr_to_colc = {lst: cnt for lst, cnt in col_hdr_to_colc.items() if lst.split('.')[0] in lsts_to_process}

    for lst in lsts_to_process:
        # Определяем кол-во основных задач в листке
        main_part = rtv_main_part_num_prob(lst[-1])
        cur_lst_problems = [x.split('.')[1] for x in col_hdr_to_colc if x.startswith(lst)]
        cur_lst_problems.sort(key=lambda x: re.sub(r'\D', '', x).zfill(3))
        curr_problems = []
        for n, prb in enumerate(cur_lst_problems):
            if prb in ('Н', 'H'):
                curr_problems.append({'ProblemTypeID': 0, 'Number': n, 'Group': 0, 'Name': 'Н'})
            else:
                curr_problems.append({'ProblemTypeID': (0 if n-1 <= main_part else 1), 'Number': n,
                                      'Group': int(re.sub(r'\D', '', prb)), 'Name': prb})
        lst = lst[:2] + '-' + lst[2:].replace('н', 'n').replace('п', 'p').replace('с', 's')
        lst_dict = {'ListTypeID': 1, 'ClassID': 1, 'Number': lst, 'Description': 'занятие-н',
                    'Date': '', 'problems': curr_problems}
        json_lists.append(lst_dict)
    return json_lists, col_hdr_to_colc


# Теперь делаем список школьников
def gen_json_pupils(sheet):
    json_pupils = []
    pupil_to_rown = {}
    for rown in range(FIRST_ROW - 1, sheet.nrows):
        surnam, nam, id = (str(sheet.cell(rown, coln).value).strip().replace('.0', '') for coln in \
            [COLUMNS['Фамилия'], COLUMNS['Имя'], COLUMNS['ID']])
        surnam = surnam.title()
        nam = nam.title()
        json_pupils.append({'ClassID': 1, 'Name1': surnam, 'Name2': nam, 'xlsID': id})
        pupil_to_rown[id] = rown
    return json_pupils, pupil_to_rown


def gen_json_plus(sheet, pupil_to_rown, col_hdr_to_colc):
    marks = []
    for pup_id, rown in pupil_to_rown.items():
        for col_hdr, coln in col_hdr_to_colc.items():
            lst, prb = col_hdr.split('.')
            lst = lst[:2] + '-' + lst[2:].replace('н', 'n').replace('п', 'p').replace('с', 's')
            cv = str(sheet.cell(rown, coln).value).strip().replace('.0', '')
            if cv in ('1', 'd', 'д'):
                marks.append({'LN': lst, 'PN': prb, 'PI': pup_id})
    return marks


json_lists, col_hdr_to_colc = gen_json_lists(sheet)
json_pupils, pupil_to_rown = gen_json_pupils(sheet)
json_marks = gen_json_plus(sheet, pupil_to_rown, col_hdr_to_colc)


rqs = {'lists': json_lists, 'pupils': json_pupils, 'marks': json_marks}
print(rqs)
url = work[0]['json_db_api_url']
response = requests.post(url, json=rqs, auth=work[0]['json_db_credentials'])
print(response.json())

"""
DELIMITER $$
CREATE DEFINER=`host1000218_vm18`@`localhost` PROCEDURE `PutPlus`(IN `ListNumber` VARCHAR(15) CHARSET utf8, IN `ProblemName` VARCHAR(10) CHARSET utf8, IN `PupilXlsdID` CHAR(7) CHARSET utf8)
    MODIFIES SQL DATA
    COMMENT 'Внести плюс данному школьнику за данную задачу в данном листке'
BEGIN
DECLARE useListID, useProblemID, usePupilID int(6);
SELECT ID into useListID    FROM `PList`    where replace(Number, 'a', 'а') = replace(ListNumber, 'a', 'а');
SELECT ID into useProblemID FROM `PProblem` where Name = ProblemName and ListID = useListID;
SELECT ID into usePupilID   FROM `PPupil`   where xlsID  = PupilXlsdID;
insert into `PResult` (`PupilID`, `ProblemID`, `Mark`, `User`, `TS`) VALUES (usePupilID, useProblemID, '+', 'admin', CURRENT_TIMESTAMP)  ON DUPLICATE KEY UPDATE Mark = '+';
COMMIT;
END$$
DELIMITER ;
"""