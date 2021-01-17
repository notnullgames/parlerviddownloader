#!/usr/bin/env python3

"""
Use this to create a mapbox CSV layer file
"""

import sys
import csv
import sqlite3

conn = sqlite3.connect('videos.db')
c = conn.cursor()

print('longitude,latitude,time,id,username,displayname')

for row in c.execute('SELECT longitude, latitude, time, id, username, displayname FROM videos'):
  print(f'{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}')