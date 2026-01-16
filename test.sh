#!/usr/bin/bash

set -o pipefail

if [ ! -f data/kkbox-music-recommendation-challenge/songs.csv ] ; then
    echo "No data found, generate the test dataset..." 1>&2
    echo "| Install data from archive" 1>&2
    ./install_data.sh
    echo "| Subset 100 songs" 1>&2
    head -n 100 data/kkbox-music-recommendation-challenge/songs.csv > data/kkbox-music-recommendation-challenge/songs_100.csv
    echo "| Generate the train dataset" 1>&2
    uv run ./create_wsdm-kkbox-music-kg.sh subset data/kkbox-music-recommendation-challenge/songs_100.csv
    echo "OK" 1>&2
fi

echo "Data OK, ontoweave them..." 1>&2
if=$(uv run ./create_wsdm-kkbox-music-kg.sh ontoweave data/kkbox-music-recommendation-challenge/songs_100_train_subset.csv 2> ontoweave.log)

err="$?"
if [ $err -eq 0 ] ; then
    echo "OK, logs are in: ontoweave.log" 1>&2
else
    echo "NOK, logs:" 1>&2
    cat ontoweave.log 1>&2
    exit $err
fi

echo "Found labels:" 1>&2
cat $(dirname $if)/*-part*.csv 2>/dev/null | head | cut -d";" -f4 | sort | uniq

