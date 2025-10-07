#1/usr/bin/env python3
import argparse
import os.path
import pandas as pd


if __name__== "__main__":
    usage = f"Create a subset of the songs.csv data table only for songs with a target in the train.csv data table."
    parser = argparse.ArgumentParser(
        description=usage
    )

    parser.add_argument("-d", "--data_directory", metavar="TXT", help="Data directory")

    parser.add_argument("-s", "--subset_file_full_path", metavar="TXT", help="Subset file full path")

    args, unknown = parser.parse_known_args()
    if unknown:
        raise ValueError(f"Unknown args: {unknown}")
    
    songs_filename = str(args.data_directory) + f"/songs.csv"
    train_filename = str(args.data_directory) + f"/train.csv"

    if os.path.isfile(songs_filename):
        
        print("Songs file exists.")
        songs = pd.read_csv(songs_filename)

        if os.path.isfile(train_filename):
            
            print("Train file exists.")
            train = pd.read_csv(train_filename)

            song_subset_train = songs[songs.song_id.isin(train.song_id)]
            song_subset_train.to_csv(args.subset_file_full_path, index=False)