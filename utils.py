from datetime import datetime, timedelta
import re

from session import Session
import config as conf

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
        module_codes = (row[conf.MODULE_CODE_ROW]
                        .replace('"', '').split(','))
        matches = set(modules).intersection(module_codes) 
        if len(matches)==0: 
            continue

        ranges = row[conf.WEEKS_ROW].split(',')
        for span in ranges:
            if '-' in span:
                weeks = re.sub('[Weeks ]', '', span)
                week_start_end = weeks.split('-')
                for week in range(int(week_start_end[0]), 
                        int(week_start_end[1])):
                    date = session_date(defined_weeks, week, 
                                        row[conf.DAY_ROW])
                    sessions.append(Session(row, date))


            else:
                week = re.sub('[Weeks ]', '', span)
                date = session_date(defined_weeks, week, 
                                    row[conf.DAY_ROW])
                sessions.append(Session(row, date))

    return sessions

def session_date(defined_weeks, week, day): 
    matches = [x for x in defined_weeks if int(week)==x[0]]
    if len(matches) != 1:
        raise RuntimeError(week + " is not defined as a week.")

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
