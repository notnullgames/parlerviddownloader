#!/usr/bin/env python3

"""
Search by city, spits out IDs for download.py
"""


import os
import sys
import sqlite3

try:
  loc = sys.argv[1]
except IndexError:
  print(f'Usage {sys.argv[0]} "<CITY, STATE>"')
  exit(1)

[city, state] = [l.lower().strip() for l in loc.split(',') ]

conn = sqlite3.connect('videos.db')
c = conn.cursor()

for row in c.execute("SELECT id FROM videos WHERE LOWER(city)=? AND LOWER(state)=? ORDER BY id", [city, state]):
  print(row[0])
