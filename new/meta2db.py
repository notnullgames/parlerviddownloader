#!/usr/bin/env python3

"""
Turn video meta-data into initial sqlite db.
"""

import sys
import csv
import sqlite3
import tarfile
import json
import reverse_geocoder as rg

conn = sqlite3.connect('videos.db')
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
    audio TEXT,
    width INT,
    height INT,
    rotation INT,
    device TEXT
  )
''')

def save(record, table='videos', additional=''):
  values = []
  keys =[]
  qs = []
  for k,v in record.items:
    keys.append(k)
    values.append(v)
    qs.append('?')
  print(f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join(qs)})", values)
  # return c.execute(f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join(qs)})", values)
  

with tarfile.open('metadata.tar.gz') as metaFile:
  for f in metaFile.getnames():
    id = f.replace('metadata/meta-', '').replace('.json', '')
    d = metaFile.extractfile(f)
    if d:
      meta = json.loads(d.read())
      # geos = rg.search(meta['GPSPosition'])
      save({
        'id': id,
        'longitude': '',
        'latitude': '',
        'altitude': '',
        'time': meta['CreationDate'],
        'country': '',
        'state': '',
        'city': '',
        'username': '',
        'displayname': '',
        'mime': meta['MIMEType'],
        'audio': '',
        'width': meta['SourceImageWidth'],
        'height': meta['SourceImageHeight'],
        'rotation:': meta['Rotation'],
        'device:': f"{meta['Make']} {meta['Model']} {meta['Software']}"
      })