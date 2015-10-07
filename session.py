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
        end_datetime= datetime(year=date.year, month=date.month, 
                day=date.day, hour=end.hour, 
                minute=end.minute)
        self.start = start_datetime
        self.end = end_datetime
        self.title = row[conf.TITLE_ROW] 
        self.location = row[conf.LOCATION_ROW] 
        self.lecturer = row[conf.LECTURER_ROW] 
        self.kind = row[conf.KIND_ROW] 
