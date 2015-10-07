#!/usr/bin/python3.4
from csv import reader
import sys

from utils import parse, make_weeks, session_date


def main(argv):
    modules = ['CO7105', 'CO7206', 'CO7210', 'CO7219']
    weeks = [] 
    sessions = []

    with open('weeks.csv', newline='') as csvfile:
        weeksreader = reader(csvfile, quotechar='"')
        weeks = make_weeks(weeksreader) 

    with open('tt.csv', newline='') as csvfile:
        ttreader = reader(csvfile, quotechar='"')
        sessions = parse(ttreader, modules, weeks)

if __name__ == "__main__":
    main(sys.argv[1:])
