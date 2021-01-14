# parlerviddownloader

Tools for mirroring parler videos.


You don't really need to do this, because I used this to create `videos.db`. This will allow you to geocode data (get city/state/country/zip) from a csv file [like this](https://gofile.io/d/7Wg83o).


```
python3 geocode.py CSV_FILE
```

## Dependencies

- Download and extract the [videos.db]() file to the same directory.
- Install "requests": `pip3 install requests`


## Usage


This will split out all the IDs for a named city:


```
python3 getbycity.py "Portland, Oregon"
```

I don't have any abbreviations for states, so you may have to look in videos.csv to figure out the format, for exmaple this is Washington DC:

```
python3 getbycity.py "Washington, District of Columbia"
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