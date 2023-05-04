#!/bin/sh
if [ -n "$1" ]; then
  printf "\nBucket name is set to:\n"
  printf "\n$1"
else
  printf "\nPlease enter bucket name: "
  read $1
fi

aws s3 cp ./geolocator-bucket-content/ s3://$1 --recursive