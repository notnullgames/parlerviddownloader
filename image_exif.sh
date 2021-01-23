#!/usr/bin/env bash

# collect meta info from images
# sadly no EXIF, but still great other info

# this is where the S3 bucket is mounted
IMAGES_LOCATION="./images"

OUT_LOCATION='./metadata'

while read i; do
  f=$(echo "$i"| awk '{ print $NF }')
  id="${f%.*}"
  echo $id
  exiftool -json -U -u "${IMAGES_LOCATION}/${f}" > "${OUT_LOCATION}/${id}.json"
done < ddosecrets-parler-images-listing.txt

echo "Compressing metadata"
tar -czf metadata-images.tgz "${OUT_LOCATION}"
