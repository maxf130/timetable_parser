#!/usr/bin/python3.4
from csv import reader, writer, QUOTE_MINIMAL
import sys

from utils import parse, make_weeks, session_date
import config


def main(argv):
    weeks = [] 
    sessions = []

    with open('weeks.csv', newline='') as csvfile:
        weeksreader = reader(csvfile, quotechar='"')
        weeks = make_weeks(weeksreader) 

    with open('tt.csv', newline='') as csvfile:
        ttreader = reader(csvfile, quotechar='"')
        errors = []
        sessions = parse(ttreader, config.MODULES, weeks, errors)
        for error in errors:
            print(error)


    calendar = []
    calendar.append(['Subject', 'Start Date', 'End Date', 'Start Time', 'End Time', 'Location'])
    for session in sessions:
        event = ['', '', '', '', '', '']
        event[0] = session.title + '-' + session.kind
        event[1] = session.start.strftime('%Y/%m/%d')
        event[2] = session.end.strftime('%Y/%m/%d')
        event[3] = session.start.strftime('%H:%M')
        event[4] = session.end.strftime('%H:%M')
        event[5] = session.location
        calendar.append(event)

    with open('parsed.csv', 'w', newline='') as csvfile:
        csvwriter = writer(csvfile, delimiter=',', quotechar='"', 
                            quoting=QUOTE_MINIMAL)
        csvwriter.writerows(calendar)

if __name__ == "__main__":
    main(sys.argv[1:])
