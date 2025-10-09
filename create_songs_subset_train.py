#1/usr/bin/env python3
import argparse
import logging
import os.path
import pandas as pd

logging.basicConfig(level=logging.INFO)

if __name__== "__main__":
    usage = f"Create a subset of the songs.csv data table only for songs with a target in the train.csv data table."
    parser = argparse.ArgumentParser(
        description=usage
    )

    parser.add_argument("-d", "--data_directory", metavar="TXT", help="Data directory")
    parser.add_argument("-sf", "--song_file", metavar="TXT", help="Subset file full path")

    args, unknown = parser.parse_known_args()
    if unknown:
        raise ValueError(f"Unknown args: {unknown}")
    
    # Remove ".csv" from the end and add "_train_subset.csv"
    base_filename = os.path.splitext(os.path.basename(args.song_file))[0]
    subset_filename = os.path.join(args.data_directory, f"{base_filename}_train_subset.csv")

    if "_train_subset" in base_filename or os.path.isfile(subset_filename):
        raise ValueError(f"The subset file already exists.")
    
    songs_filename = str(args.song_file)
    train_filename = str(args.data_directory) + f"/train.csv"

    if os.path.isfile(songs_filename):
        
        logging.info("Songs file exists.")
        songs = pd.read_csv(songs_filename)

        if os.path.isfile(train_filename):
            
            logging.info("Train file exists.")
            train = pd.read_csv(train_filename)

            song_subset_train = songs[songs.song_id.isin(train.song_id)]
            song_subset_train.to_csv(subset_filename, index=False)