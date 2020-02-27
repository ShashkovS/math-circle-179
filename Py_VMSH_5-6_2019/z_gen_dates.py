from datetime import datetime, timedelta, date
week = timedelta(days=7)
ignore_dates = {date(2020,1,1), date(2020,1,8),date(2019,11,4),date(2020,1,6),date(2020,2,24),date(2020,3,9),date(2020,5,4),date(2020,5,11)}

start_date = date(2019, 9, 9)
dt_list = []
for i in range(1, 40):
    cur = start_date + (i-1) * week
    if cur in ignore_dates:
        continue
    dt_list.append(f'"{len(dt_list)+1:02}-n" => new DateTime("{cur.strftime("%Y-%m-%dT19:00:00Z") }"),')

for row in reversed(dt_list):
    print(row)

# 2019-04-15T19:00:00Z