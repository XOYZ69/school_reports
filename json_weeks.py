import json
import datetime

data = {}

weeks = {}

day     = 1
month   = 8
year    = 2021

def fill(number):
    n = str(number)
    if len(n) < 2:
        return '0' + n
    else:
        return n

for m in range(month, 13):
    for d in range(32):
        try:
            new_date = datetime.date(year, m, d)

            if new_date.weekday() < 5:

                if str(new_date.isocalendar().week) not in weeks:
                    weeks[str(new_date.isocalendar().week)] = []
            
                weeks[str(new_date.isocalendar().week)].append(fill(d) + '.' + fill(m) + '.' + '2021')
        except ValueError:
            pass

print(weeks)

for week in weeks:
    data[weeks[week][0] + ' - ' + weeks[week][-1]] = {
        weeks[week][0]: [],
        weeks[week][1]: [],
        weeks[week][2]: [],
        weeks[week][3]: [],
        weeks[week][4]: []
    }

open('tb.json', 'w', encoding='utf-8').write(json.dumps(data))
