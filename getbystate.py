#!/usr/bin/env python3

"""
Search by state, spits out IDs for download.py
"""

import os
import sys
import sqlite3

try:
  state = sys.argv[1]
except IndexError:
  print(f'Usage {sys.argv[0]} "<STATE>"')
  exit(1)

state = state.lower().strip()

conn = sqlite3.connect('videos.db')
c = conn.cursor()

for row in c.execute("SELECT id FROM videos WHERE LOWER(state)=? ORDER BY id", [state]):
  print(row[0])
