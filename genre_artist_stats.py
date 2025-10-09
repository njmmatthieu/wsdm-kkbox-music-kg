#1/usr/bin/env python3
import argparse
import logging
import os.path
import pandas as pd

logging.basicConfig(level=logging.INFO)

def genre_artist_stats(songs_df):

    # Count songs per genre for each artist
    genre_song_counts = songs_df.groupby(['artist_name', 'genre_ids']).size().reset_index(name='genre_song_count')

    # Count total songs per artist
    artist_song_counts = songs_df.groupby('artist_name').size().reset_index(name='total_song_count')

    # Merge to associate each genre count with the artist's total
    genre_artist_stats_table = genre_song_counts.merge(artist_song_counts, on='artist_name')

    # Calculate percentage of songs in each genre for every artist
    genre_artist_stats_table['genre_percentage'] = (
        genre_artist_stats_table['genre_song_count'] / genre_artist_stats_table['total_song_count'] * 100
    )

    return genre_artist_stats_table

if __name__== "__main__":
    usage = f"Create a table with genre artists statistics from songs table."
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
    stats_filename = os.path.join(args.data_directory, f"{base_filename}_genre_artist_stats.csv")

    logging.info("Stats file exists.")

    songs_filename = str(args.song_file)

    if os.path.isfile(songs_filename):
        
        logging.info("File exists.")
        songs = pd.read_csv(songs_filename)

        stats = genre_artist_stats(songs)
        print(stats.shape)

        stats.to_csv(stats_filename, index=False)



        
    