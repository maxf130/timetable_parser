#!/usr/bin/python3.4
from csv import reader
import sys
from datetime import datetime, timedelta, time

modules = ['CO7105', 'CO7206', 'CO7210', 'CO7219']
weeks = [] 
sessions = []


def main(argv):
    with open('weeks.csv', newline='') as csvfile:
        weeksreader = reader(csvfile, quotechar='\'')
        weeks = make_weeks(weeksreader) 

    with open('tt.csv', newline='') as csvfile:
        ttreader = reader(csvfile, quotechar='\'')
        parse(ttreader)

def make_weeks(weeksreader):
    weeks = []
    for row in weeksreader:
        week = datetime.strptime(row[0], '%Y-%m-%d')
        week_tuple = (int(row[1]), week)
        weeks.append(week_tuple)

    return weeks

def parse(ttreader):
    for row in ttreader:
        module_codes = row[0].replace('"', '').split(',')
        matches = set(modules).intersection(module_codes) 
        if len(matches)==0: 
            continue

        if '-' in row[7]:
            weeks = row[7]
            weeks = weeks.replace('Weeks', '')
            weeks = weeks.replace(' ', '')
            week_start_end = weeks.split('-')
            for week in range(int(week_start_end[0]), 
                    int(week_start_end[1])):
                sessions.append(Session(row, week))

        else:
            week = row[7].replace('Week ', '')
            print(','.join(row))
            sessions.append(Session(row, week))

def session_date(week, day): 
    matches = [x for x in weeks if week==x[0]]
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
    

class Session():
    def __init__(self, row, week):
        date = session_date(week, row[2])

        start = time(hour=int(row[3].split(':')[0]),
                     minute=int(row[3].split(':')[1]))
        end = time(hour=int(row[4].split(':')[0]),
                   minute=int(row[4].split(':')[1]))
        start_datetime = datetime(year=date.year, month=date.month, 
                                  day=date.day, hour=start.hour, 
                                  minute=start.minute)
        end_datetime= datetime(year=date.year, month=date.month, 
                               day=date.day, hour=end.hour, 
                               minute=end.minute)
        self.start = start_datetime
        self.end = end_datetime
        self.title = row[1] 
        self.location = row[8] 
        self.lecturer = row[7] 
        self.kind = row[5] 
        print("Made a session!")


if __name__ == "__main__":
        main(sys.argv[1:])
