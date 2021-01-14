#!/usr/bin/env python3

import os
import sys
import csv

try:
  zip = sys.argv[1]
except IndexError:
  print("Usage %s <ZIP>" % sys.argv[0])
  exit(1)

csvfilename = os.path.join(os.path.dirname(__file__), 'videos.csv')

with open(csvfilename, 'r', newline='') as csvfile:
  for i, row in enumerate(csv.reader(csvfile)):
      if (i  != 0 and zip in row[4]):
        print(row[3])