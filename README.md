# parlerviddownloader

Tools for messing with parler video meta-data


### create.py

You don't really need to use this, because I used this to create [videos.db](https://github.com/notnullgames/parlerviddownloader/releases/download/0.0.0/videos.zip).

- Install deps with `pip3 install -r requirements.txt`.
- Grab [user_to_videos.csv](https://gofile.io/d/7Wg83o)
- Grab [video meta-data](magnet:?xt=urn:btih:1723e27bc79186c4574ff056ddb458d771c26e2f&dn=metadata.tar.gz&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2)
- run `python3 create.py` to generate videos.db


### search.py

Search database, based on a few fields

Download [videos.db](https://github.com/notnullgames/parlerviddownloader/releases/download/0.0.0/videos.zip) and put it in the same dir as search.py.


```
usage: search.py [-h] [-c CITY] [-s STATE] [-u USER] [-w] [-b BEGIN] [-e END] [-f FIELDS] [-o]

Search Parler video meta-data

optional arguments:
  -h, --help            show this help message and exit
  -c CITY, --city CITY  city to search for
  -s STATE, --state STATE
                        state to search for
  -u USER, --user USER  username to search for
  -w, --with-user       Only show records that have user-data
  -b BEGIN, --begin BEGIN
                        start-time to search for
  -e END, --end END     end-time to search for
  -f FIELDS, --fields FIELDS
                        The fields you want to include
  -o, --or              Use OR instead of AND to combine search-items
```

#### Examples:

Use fullname for `state` (no abbreviation) except for `DC`.

- `search.py -c washington -s DC -b "jan 6", -e "jan 7"` - get videos recorded during capital riot
- `search.py -c portland -s oregon` - get videos from Portland, OR.
- `search.py -f id` - output only the ID of all videos