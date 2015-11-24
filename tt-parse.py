#!/usr/bin/python3.4
# Copyright 2015, Maximilian Friedersdorff

# This file is part of timetable_parser

# timetable_parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# timetable_parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with timetable_parser.  If not, see <http://www.gnu.org/licenses/>.

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
