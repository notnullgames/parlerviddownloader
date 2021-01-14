#!/usr/bin/env python3

import os
import sys
import csv

try:
  loc = sys.argv[1]
except IndexError:
  print(f'Usage {sys.argv[0]} "<CITY, STATE>"')
  exit(1)

[city, state] = [l.lower().strip() for l in loc.split(',') ]

csvfilename = os.path.join(os.path.dirname(__file__), 'videos.csv')

with open(csvfilename, 'r', newline='') as csvfile:
  for i, row in enumerate(csv.reader(csvfile)):
      if (i  != 0 and row[6].lower() == state and row[7].lower() == city):
        print(row[3])