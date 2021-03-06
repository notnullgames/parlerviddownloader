#!/usr/bin/env python3

"""
Build sqlite db from meta-data tarball and user-data CSV

You should have metadata.tar.gz and user_to_video.csv extracted here
"""

import os
import sys
import csv
import sqlite3
import json
import re
import datetime
import dateutil.parser
import reverse_geocoder as rg
from os import listdir

__dir = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(os.path.join(__dir, 'videos.db'))
c = conn.cursor()

c.execute('''
  CREATE TABLE IF NOT EXISTS videos (
    id TEXT PRIMARY KEY,
    longitude FLOAT,
    latitude FLOAT,
    altitude FLOAT,
    time TEXT,
    country TEXT,
    state TEXT,
    city TEXT,
    username TEXT,
    displayname TEXT,
    mime TEXT,
    width INT,
    height INT,
    duration INT
  )
''')
c.execute('PRAGMA synchronous = EXTRA')
c.execute('PRAGMA journal_mode = WAL')

# normalize 00:00:00 and 10.2s to seconds float
def time_to_sec(time_str):
  if time_str.find(':') != -1:
    return sum(x * float(t) for x, t in zip([1, 60, 3600], reversed(time_str.split(":"))))
  return 0

# convert geo location from dms to dd
def dms_to_dd(d, m, s):
  return float(d) + float(m)/60 + float(s)/3600

# get a location in decimal array format from text location
def getLocation(location):
  loc = re.findall(r'[\d\.]+', location)
  lat = dms_to_dd(loc[0], loc[1], loc[2])
  lng = dms_to_dd(loc[3], loc[4], loc[5])
  if len(loc) == 7:
    alt = float(loc[6])
  else:
    alt = None
  return [lat, lng, alt]


# insert a record into database
def insert(record, table='videos'):
  values = []
  keys =[]
  qs = []
  for k, v in record.items():
    if v != None:
      keys.append(k)
      values.append(v)
      qs.append('?')
  return c.executemany(f"REPLACE INTO {table} ({','.join(keys)}) VALUES ({','.join(qs)})", [values])
  

# build a video-to-user-mapping
usermap = {}
namemap = {}
def step_user():
  with open('user_to_video.csv', newline='') as csvfile:
    for i, row in enumerate(csv.reader(csvfile)):
      if (i!=0):
        for vid in [r.split('/')[-1].replace('.mp4', '').replace('_small', '') for r in row[2:]]:
          namemap[vid] = row[0]
          usermap[vid] = row[1]

# first pass: create the database with meta-data 
def step_meta():
  for f in listdir(os.path.join(__dir, 'metadata')):
    id = f.replace('meta-', '').replace('.json', '')
    if id[0] == '.':
      continue
    with open(os.path.join(__dir, 'metadata', f)) as d:
      for meta in json.loads(d.read()):
        record = {
          'id': id,
          'username': usermap.get(id, None),
          'displayname': namemap.get(id, None),
          'mime': meta['MIMEType'],
          'width': meta.get('SourceImageWidth', None),
          'height': meta.get('SourceImageHeight', None),
          'duration': time_to_sec(meta.get('Duration', ''))
        }
        t = meta.get('CreateDate', '0000:00:00 00:00:00')
        if t != '0000:00:00 00:00:00':
          try:
            record['time'] = dateutil.parser.parse(t).isoformat()
          except:
            pass
        gps = meta.get('GPSCoordinates', False)
        if gps:
          loc = getLocation(gps)
          record['latitude'] = loc[0]
          record['longitude'] = loc[1]
          record['altitude'] = loc[2]
        insert(record)
        conn.commit()

# get geo info for every record
def step_geocode():
  rows = [row for row in c.execute("SELECT latitude,longitude,id FROM videos WHERE latitude != 0 AND longitude != 0")]
  geos = rg.search([(row[0], row[1]) for row in rows ])
  values = []
  for r, row in enumerate(rows):
    g = geos[r]
    if g['admin1'] == 'Washington, D.C.':
      g['admin1'] = "DC"
      g['name'] = "Washington"
    values.append(( g['cc'], g['admin1'], g['name'], row[2] ))
  c.executemany("UPDATE videos SET country=?, state=?, city=? WHERE id=?", values)
  conn.commit()

if __name__ == '__main__':
  step_user()
  step_meta()
  step_geocode()
