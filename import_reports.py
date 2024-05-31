import datetime
from functools import cache
import json
data = {}

with open('tagesberichte_new.csv', 'r', encoding='utf-8') as csv:
    for line in csv.readlines():
        current_line = line.split(';')

        date = current_line[1].split('/')
        date[2] = '2021'

        if date[1] == '01':
            break

        begin_week = ''

        c = datetime.date(int(date[2]), int(date[1]), int(date[0]))

        for date in data:
            date_s = date.split('.')
            cache_c = datetime.date(int(date_s[2]), int(date_s[1]), int(date_s[0]))

            print(c.isocalendar().week)

        print(c.isocalendar())
        data[date[0] + '.' + date[1] + '.' + date[2]] = [
            current_line[2].replace('\n', '')
        ]

with open('tagesberichte.json', 'w', encoding='utf-8') as js:
    json.dump(data, js)
