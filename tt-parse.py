#!/usr/bin/python3.4
from csv import reader, writer, QUOTE_MINIMAL
import sys

from utils import parse, make_weeks
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
        for i, error in enumerate(errors):
            if i == len(error) - 1:
                print(error[0] + '\n' + error[1])
            else:
                print(error[0] + '\n' + error[1] + '\n')

    calendar = []
    calendar.append(['Subject', 'Start Date', 'End Date',
                    'Start Time', 'End Time', 'Location'])
    for session in sessions:
        calendar.append([
            session.title + '-' + session.kind,
            session.start.strftime('%Y/%m/%d'),
            session.end.strftime('%Y/%m/%d'),
            session.start.strftime('%H:%M'),
            session.end.strftime('%H:%M'),
            session.location
        ])

    with open('parsed.csv', 'w', newline='') as csvfile:
        csvwriter = writer(csvfile, delimiter=',', quotechar='"',
                           quoting=QUOTE_MINIMAL)
        csvwriter.writerows(calendar)

if __name__ == "__main__":
    main(sys.argv[1:])
