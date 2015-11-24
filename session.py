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

from datetime import time, datetime

import config as conf


class Session():
    def __init__(self, row, date):
        start = time(hour=int(row[conf.START_ROW].split(':')[0]),
                     minute=int(row[conf.START_ROW].split(':')[1]))
        end = time(hour=int(row[conf.END_ROW].split(':')[0]),
                   minute=int(row[conf.END_ROW].split(':')[1]))
        start_datetime = datetime(year=date.year, month=date.month,
                                  day=date.day, hour=start.hour,
                                  minute=start.minute)
        end_datetime = datetime(year=date.year, month=date.month,
                                day=date.day, hour=end.hour,
                                minute=end.minute)
        self.start = start_datetime
        self.end = end_datetime
        self.title = row[conf.TITLE_ROW]
        self.location = row[conf.LOCATION_ROW]
        self.lecturer = row[conf.LECTURER_ROW]
        self.kind = row[conf.KIND_ROW]
