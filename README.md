# parlerviddownloader

Tools for mirroring parler videos.


You don't really need to do this, because I used this to create `videos.csv`. This will allow you to geocode data (get city/state/country/zip) from a csv file [like this](https://gofile.io/d/7Wg83o). This is the only script that has any dependencies.


```
python3 geocode.py CSV_FILE > BETTER_CSV_FILE
```


This will split out all the IDs for a zipcode:


```
python3 getbyzip.py 97239
```


This will split out all the IDs for a named city:


```
python3 getbycity.py "Portland, Oregon"
```


This will split out all the IDs for a state:


```
python3 getbystate.py Oregon
```

and `downlaodvideos.py` will download a list of incoming IDs (from stdin) into "downloads/" so to put it all together, to get portland:

```
python3 getbycity.py "Portland, Oregon" | python3 downlaodvideos.py
```

It checks the filesystem to see if you already downloaded it, and just downlaods into the current directory.