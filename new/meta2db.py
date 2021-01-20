#!/usr/bin/env python3

"""
Turn video meta-data into initial sqlite db.
"""

import sys
import csv
import sqlite3
import tarfile

conn = sqlite3.connect('videos.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS videos (longitude FLOAT, latitude FLOAT, time TEXT, id TEXT PRIMARY KEY, country TEXT, state TEXT, city TEXT, username TEXT, displayname TEXT)")