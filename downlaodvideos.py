#!/usr/bin/env python3

import os
import sys
import requests

try:
  os.mkdir("downloads")
except:
  pass


def download(id):
  savefile = f'downloads/{id}.mp4'
  if (os.path.exists(savefile)):
    print(f'Skipping {savefile}')
  else:
    print(f'Downloading {savefile}') 
    url = f'http://8.240.242.124/{id[0:2]}/{id[2:4]}/{id}'
    r = requests.get(url, headers={
        'Host': 'video.parler.com'
    })
    try:
      if ('<?xml version="1.0" encoding="UTF-8"?>' in r.content.decode("utf-8")):
        print(f'Video is gone: {savefile}')
      else:
        with open(savefile, 'wb') as f:
          f.write(r.content)
    except UnicodeDecodeError:
      with open(savefile, 'wb') as f:
        f.write(r.content)


for id in map(str.strip, sys.stdin):
  download(id)