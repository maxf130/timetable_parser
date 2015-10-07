#!/usr/bin/python3.4
from csv import reader
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
        sessions = parse(ttreader, config.MODULES, weeks)

if __name__ == "__main__":
    main(sys.argv[1:])
