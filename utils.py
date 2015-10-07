from datetime import datetime, timedelta
from session import Session

def make_weeks(weeksreader):
    weeks = []
    for row in weeksreader:
        week = datetime.strptime(row[0], '%Y-%m-%d')
        week_tuple = (int(row[1]), week)
        weeks.append(week_tuple)

    return weeks

def parse(ttreader, modules, defined_weeks):
    sessions = []
    for row in ttreader:
        module_codes = row[0].replace('"', '').split(',')
        matches = set(modules).intersection(module_codes) 
        if len(matches)==0: 
            continue

        ranges = row[6].split(',')
        for span in ranges:
            if '-' in span:
                weeks = span.replace('Weeks ', '')
                weeks = weeks.replace('Week ', '')
                weeks = weeks.replace(' ', '')
                week_start_end = weeks.split('-')
                for week in range(int(week_start_end[0]), 
                        int(week_start_end[1])):
                    date = session_date(defined_weeks, week, row[2])
                    sessions.append(Session(row, date))


            else:
                week = span.replace('Week ', '')
                week = week.replace('Weeks ', '')
                week = week.replace(' ', '')
                date = session_date(defined_weeks, week, row[2])
                sessions.append(Session(row, date))

    return sessions

def session_date(defined_weeks, week, day): 
    matches = [x for x in defined_weeks if int(week)==x[0]]
    if len(matches) != 1:
        raise Exception('Oh crap')

    weekstart = matches[0][1] 
    if 'Mon' in day:
        return weekstart
    if 'Tue' in day:
        return weekstart + timedelta(days=1)
    if 'Wed' in day:
        return weekstart + timedelta(days=2)
    if 'Thu' in day:
        return weekstart + timedelta(days=3)
    if 'Fri' in day:
        return weekstart + timedelta(days=4)
