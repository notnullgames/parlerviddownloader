#!/usr/bin/env python3

"""
Use this after you have ran geocode.py, to add usernames
"""

import sys
import csv
import sqlite3

try:
  csvfilename = sys.argv[1]
except IndexError:
  print("Usage %s <CSV_FILE>" % sys.argv[0])
  exit(1)

conn = sqlite3.connect('videos.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS videos (longitude FLOAT, latitude FLOAT, time TEXT, id TEXT PRIMARY KEY, country TEXT, state TEXT, city TEXT, username TEXT, displayname TEXT)")

with open(csvfilename, newline='') as csvfile:
  for i, row in enumerate(csv.reader(csvfile)):
    if (i!=0):
      for vid in [r.split('/')[-1].replace('.mp4', '').replace('_small', '') for r in row[2:]]:
        for data in c.execute("SELECT id, COUNT(id) from videos WHERE id=?", [vid]):
          print(data[0], data[1])

      # print(ids)
      # c.execute(f"UPDATE videos SET displayname=?, username=? WHERE id IN ({','.join('?'*len(ids))})", [row[0], row[1], *ids])
      # conn.commit()
