#!/usr/bin/env python3

"""
This will geocode the lat/lng positions, and turn a CSV into sqlite database
"""

import sys
import csv
import reverse_geocoder as rg
import sqlite3

try:
  csvfilename = sys.argv[1]
except IndexError:
  print("Usage %s <CSV_FILE>" % sys.argv[0])
  exit(1)

conn = sqlite3.connect('videos.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS videos (longitude FLOAT, latitude FLOAT, time TEXT, id TEXT PRIMARY KEY, country TEXT, state TEXT, city TEXT, username TEXT, displayname TEXT)")

# first pass: build database
with open(csvfilename, newline='') as csvfile:
  for i, row in enumerate(csv.reader(csvfile)):
    if (i!=0):
      c.execute("REPLACE INTO videos (longitude, latitude, time, id) VALUES (?,?,?,?)", row)
      conn.commit()

# second pass: local geocode
rows = [row for row in c.execute("SELECT latitude,longitude,id FROM videos ORDER BY id")]
geos = rg.search([(row[0], row[1]) for row in rows ])

# third pass: save geocoding
for r, row in enumerate(rows):
  g = geos[r]
  if g['admin1'] == 'Washington, D.C.':
    g['admin1'] = "DC"
    g['name'] = "Washington"
  c.execute("UPDATE videos SET country=?, state=?, city=? WHERE id=?", ( g['cc'], g['admin1'], g['name'], row[2] ))
  conn.commit()
  print(g['cc'], g['admin1'], g['name'], row[2])