from datetime import time, datetime

class Session():
    def __init__(self, row, date):
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
