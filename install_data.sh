#!/bin/sh

if [ ! -f kkbox-music-recommendation-challenge.zip ]; then
    echo "KKbox archive not found, download it from https://www.kaggle.com/competitions/kkbox-music-recommendation-challenge/data" >&2
    exit 1
fi

DATA_DIR="data/kkbox-music-recommendation-challenge/"
mkdir -p "$DATA_DIR"

# unzip with overwrite
unzip -o -d "$DATA_DIR"  kkbox-music-recommendation-challenge.zip

cd "$DATA_DIR"
for f in train.csv.7z members.csv.7z songs.csv.7z ; do
    # unzip with overwrite
    7z -aoa e "$f"
done

# Remove useless files
rm -f *.7z

