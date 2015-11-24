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

from datetime import datetime, timedelta
import re

from session import Session
import config as conf


def make_weeks(weeksreader):
    weeks = []
    for row in weeksreader:
        weeks.append((int(row[1]), datetime.strptime(row[0], '%Y-%m-%d')))

    return weeks


def parse(ttreader, modules, defined_weeks, errors):
    sessions = []
    for row in ttreader:
        if not ''.join(row).strip():
            continue

        module_codes = (row[conf.MODULE_CODE_ROW]
                .replace('"', '').split(','))
        if not set(modules).intersection(module_codes):
            continue

        try:
            check_syntax(row)
        except ValueError as error:
            errors.append((';'.join(row), str(error)))
            continue

        ranges = row[conf.WEEKS_ROW].split(',')
        for span in ranges:
            if '-' in span:
                weeks = re.sub('[a-zA-Z ]', '', span)
                week_start_end = weeks.split('-')
                for week in range(int(week_start_end[0]),
                        int(week_start_end[1]) + 1):
                    date = session_date(defined_weeks, week,
                            row[conf.DAY_ROW])
                    sessions.append(Session(row, date))

            else:
                week = re.sub('[a-zA-Z ]', '', span)
                date = session_date(defined_weeks, week,
                        row[conf.DAY_ROW])
                sessions.append(Session(row, date))

    return sessions


def session_date(defined_weeks, week, day):
    try:
        matches = [x for x in defined_weeks if int(week) == x[0]]

    except ValueError as error:
        raise RuntimeError(week + " cannot be parsed as an integer.") \
                from error

    if len(matches) != 1:
        raise ValueError(week + " is not defined as a week.")

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


def check_syntax(row):
    if not re.match(r'.+', row[conf.TITLE_ROW]):
        raise ValueError('Row ' + str(conf.TITLE_ROW) +
                ' does not contain a valid title.')

        if not re.match(r'(\w{2}\d{4},?)+', row[conf.MODULE_CODE_ROW]):
            raise ValueError('Row ' + str(conf.MODULE_CODE_ROW) +
                    ' does not contain a valid module code.')

            if not re.match(r'\w{3}', row[conf.DAY_ROW]):
                raise ValueError('Row ' + str(conf.DAY_ROW) +
                        ' does not contain a valid day.')

                if not re.match(r'\d{2}:\d{2}', row[conf.START_ROW]):
                    raise ValueError('Row ' + str(conf.START_ROW) +
                            ' does not contain a valid time.')

                    if not re.match(r'\d{2}:\d{2}', row[conf.END_ROW]):
                        raise ValueError('Row ' + str(conf.END_ROW) +
                                ' does not contain a valid time.')

                        if not re.match(r'.+', row[conf.KIND_ROW]):
                            raise ValueError('Row ' + str(conf.KIND_ROW) +
                                    ' does not contain a valid session type.')

                            if not re.match(r'Week(s)?\s*(\d+(-\d+)?,?)+', row[conf.WEEKS_ROW]):
                                raise ValueError('Row ' + str(conf.WEEKS_ROW) +
                                        ' does not contain a valid week definition.')

                                if not re.match(r'.+', row[conf.LECTURER_ROW]):
                                    raise ValueError('Row ' + str(conf.LECTURER_ROW) +
                                            ' does not contain a valid Lecturer.')

                                    if not re.match(r'.+', row[conf.LOCATION_ROW]):
                                        raise ValueError('Row ' + str(conf.LOCATION_ROW) +
                                                ' does not contain a valid location.')
