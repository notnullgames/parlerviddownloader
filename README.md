# parlerviddownloader

Tools for mirroring parler videos.


You don't really need to do this, because I used this to create [videos.db](https://github.com/notnullgames/parlerviddownloader/releases/download/0.0.0/videos.zip). This will allow you to geocode data (get city/state/country/zip) from a csv file [like this](https://gofile.io/d/7Wg83o). It also has [user-data](https://gofile.io/d/t6M4zx) 


```
python3 geocode.py CSV_FILE
```

## Dependencies

- Download and extract the [videos.db](https://github.com/notnullgames/parlerviddownloader/releases/download/0.0.0/videos.zip) file to the same directory.
- Install "requests": `pip3 install requests`


## Usage


This will split out all the IDs for a named city:


```
python3 getbycity.py "Portland, Oregon"
```

I don't have any abbreviations for states, and some are just weird, so you may have to look in the database to figure out the name format, for example this is Washington DC:

```
python3 getbycity.py "Washington, DC"
```


This will split out all the IDs for a state:


```
python3 getbystate.py Oregon
```

and `downloadvideos.py` will download a list of incoming IDs (from stdin) into "downloads/" so to put it all together, to get Portland:

```
python3 getbycity.py "Portland, Oregon" | python3 downloadvideos.py
```

If you see "Video is gone" it means that it is no longer on S3 (but may have been archived by someone else.)


## new

I am working on some new ideas, which eventually will replace this repo, in new/


### meta2db.py

Turn [video meta-data](magnet:?xt=urn:btih:1723e27bc79186c4574ff056ddb458d771c26e2f&dn=metadata.tar.gz&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2) (1032523 total videos) into initial sqlite db.


### adduser.py

Correlate [user-data](https://gofile.io/d/t6M4zx) to videos




### search.py

Search database, based on a few fields