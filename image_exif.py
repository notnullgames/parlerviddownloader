#!/usr/bin/env python3

# save exif data from all images in a sqlite database
# put ddosecrets-parler-images-listing.txt in same dir from https://parler.ddosecrets.com/static/ddosecrets-parler-images-listing.txt.gz

# this is where your images are located
IMAGE_DIR='images'

import os
import sqlite3
from exif import Image
import reverse_geocoder as rg
import dateutil.parser
import mimetypes

__dir = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(os.path.join(__dir, 'images.db'))
c = conn.cursor()

c.execute('''
  CREATE TABLE IF NOT EXISTS images (
    id TEXT PRIMARY KEY,
    longitude FLOAT,
    latitude FLOAT,
    time TEXT,
    country TEXT,
    state TEXT,
    city TEXT,
    mime TEXT,
    width INT,
    height INT
  )
''')
c.execute('PRAGMA synchronous = EXTRA')
c.execute('PRAGMA journal_mode = WAL')

# convert geo location from dms to dd
def dms_to_dd(d, m, s):
  return float(d) + float(m)/60 + float(s)/3600

# insert a record into database
def insert(record, table='images'):
  values = []
  keys =[]
  qs = []
  for k, v in record.items():
    if v != None:
      keys.append(k)
      values.append(v)
      qs.append('?')
  return c.executemany(f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join(qs)})", [values])


for line in open(os.path.join(__dir, 'ddosecrets-parler-images-listing.txt')):
  fname = line.strip().split(' ')[-1]
  with open(os.path.join(IMAGE_DIR, fname), 'rb') as image_file:
    image = Image(image_file)
    id = fname.split('.')[0]
    print(id)
    record = {
      'id': id,
      'mime': mimetypes.guess_type(fname)[0]
    }
    if (image.has_exif):
      lat = image.get('gps_latitude', None)
      lng = image.get('gps_longitude', None)
      if (lat and lng):
        record['latitude'] = dms_to_dd(lat[0], lat[1], lat[2])
        record['longitude'] = dms_to_dd(lng[0], lng[1], lng[2])

      time = image.get('datetime', None)
      if time:
        record['time'] = dateutil.parser.parse(time).isoformat()
      record['width'] = image['pixel_x_dimension']
      record['height'] = image['pixel_y_dimension']
    print(record)
    insert(record)
    conn.commit()

print("adding geocoding info")
rows = [row for row in c.execute("SELECT latitude,longitude,id FROM images WHERE latitude!=0 ORDER BY id")]
for row in rows:
  try:
    geos = rg.search([(row[0], row[1]) for row in rows ])
    values = []
    for r, row in enumerate(rows):
      g = geos[r]
      if g['admin1'] == 'Washington, D.C.':
        g['admin1'] = "DC"
        g['name'] = "Washington"
      values.append(( g['cc'], g['admin1'], g['name'], row[2] ))
    c.executemany("UPDATE images SET country=?, state=?, city=? WHERE id=?", values)
    conn.commit()
  except IndexError:
    pass
