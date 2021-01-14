#!/usr/bin/env python3

import sys
import csv
from geopy.geocoders import Nominatim

try:
  csvfilename = sys.argv[1]
except IndexError:
  print("Usage %s <CSV_FILE>" % sys.argv[0])
  exit(1)


geolocator = Nominatim(user_agent="parlerviddownloader")

print("longitude,latitude,timestamp,id,zip,country,state,city")

with open(csvfilename, newline='') as csvfile:
  for i, row in enumerate(csv.reader(csvfile)):
      if (i  != 0):
        try:
          location = geolocator.reverse("%s,%s" % (row[1], row[0])).raw['address']
          row.append(location.get('postcode', ''))
          row.append(location.get('country_code', ''))
          row.append(location.get('state', ''))
          row.append(location.get('city', ''))
          print(','.join(row))
        except:
          pass
