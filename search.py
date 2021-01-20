#!/usr/bin/env python3

"""
SQL builder util to help non-programmer people look at data
"""

import argparse
import dateutil.parser
import sqlite3
import os
import sys
import csv

__dir = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(os.path.join(__dir, 'videos.db'))
c = conn.cursor()

parser = argparse.ArgumentParser(description='Search Parler video meta-data')

parser.add_argument('-c', '--city', help='city to search for')
parser.add_argument('-s', '--state', help='state to search for')
parser.add_argument('-u', '--user', help='username to search for')
parser.add_argument('-w', '--with-user', help='Only show records that have user-data', action='store_const', const=True, default=False)
parser.add_argument('-b', '--begin', help='start-time to search for')
parser.add_argument('-e', '--end', dest='end', help='end-time to search for')
parser.add_argument('-f', '--fields', help='The fields you want to include', default='id,latitude,longitude,time,country,state,city,username,displayName')
parser.add_argument('-o', '--or', dest='do_or', help='Use OR instead of AND to combine search-items', action='store_const', const=True, default=False)

args = parser.parse_args()

joiner = ' AND '
if args.do_or:
  joiner = ' OR '

params = []
terms = []

if (args.with_user):
  params.append('username != NULL')

if (args.city):
  params.append("city LIKE ?")
  terms.append(args.city)

if (args.state):
  params.append("state LIKE ?")
  terms.append(args.state)

if (args.user):
  params.append("username LIKE ?")
  terms.append(args.user)

if (args.begin):
  params.append("time >= ?")
  terms.append(dateutil.parser.parse(args.begin).isoformat())

if (args.end):
  params.append("time <= ?")
  terms.append(dateutil.parser.parse(args.end).isoformat())

sql = f"SELECT {args.fields} FROM videos"

if (len(params)):
  sql += " WHERE " + joiner.join(params)

if len(args.fields.split(',')) > 1:
  print (args.fields)

csvout=csv.writer(sys.stdout)
for row in c.execute(sql, terms):
  csvout.writerow(row)

