#!/usr/bin/env python3

import os
import sys
import csv

try:
  state = sys.argv[1]
except IndexError:
  print(f'Usage {sys.argv[0]} "<STATE>"')
  exit(1)

state = state.lower().strip()

csvfilename = os.path.join(os.path.dirname(__file__), 'videos.csv')

with open(csvfilename, 'r', newline='') as csvfile:
  for i, row in enumerate(csv.reader(csvfile)):
      if (i  != 0 and row[6].lower() == state):
        print(row[3])