#!/bin/bash


# Configuration variables
DATA_DIR="data/kkbox-music-recommendation-challenge"

# Functions
run_subset() {
    local song_file="$1"
    echo "Running genre artist stats on $song_file"
    echo "Executing Python script to create subset file."
    python3 create_songs_subset_train.py -d "$DATA_DIR" -sf "$song_file"
    if [ $? -eq 0 ]; then
        echo "Python script executed successfully"
        base_filename="${song_file%.*}"
        local subset_output_file="${base_filename}_train_subset.csv"
        echo "Subset output file will be: $subset_output_file."
        if [ -f "$subset_output_file" ]; then
            echo "File $(basename "$subset_output_file") has been created successfully"
        else
            echo "Warning: Python script completed but file was not found"
        fi
    else
        echo "Error: Python script failed to execute"
        exit 1
    fi

}

run_genre_artist_stats() {
    local song_file="$1"
    echo "Running genre artist stats on $song_file"
    python3 genre_artist_stats.py -d "$DATA_DIR" -sf "$song_file"
    if [ $? -eq 0 ]; then
        echo "Python script executed successfully"
        base_filename="${song_file%.*}"
        local stats_output_file="${base_filename}_genre_artist_stats.csv"
        echo "Stats output file will be: $stats_output_file."
        if [ -f "$stats_output_file" ]; then
            echo "File $stats_output_file has been created successfully"
        else
            echo "Warning: Python script completed but file was not found"
        fi
    else
        echo "Error: Python script failed to execute"
        exit 1
    fi
}

run_ontoweave() {
    local song_file="$1"
    python3 weave.py \
    -sf "$song_file" \
    -t "$DATA_DIR/train.csv" \
    -m "$DATA_DIR/members.csv" \
    -i
}

# Main argument handling
MODE="$1"
SONG_FILE="$2"

case "$MODE" in
    subset)
        if [ -z "$SONG_FILE" ]; then
            echo "Error: Please provide the input song file as the second argument."
            exit 1
        fi
        run_subset "$SONG_FILE"
        ;;
    genre_artist_stats)
        if [ -z "$SONG_FILE" ]; then
            echo "Error: Please provide the input song file as the second argument."
            exit 1
        fi
        run_genre_artist_stats "$SONG_FILE"
        ;;
    ontoweave)
        if [ -z "$SONG_FILE" ]; then
            echo "Error: Please provide the input song file as the second argument."
            exit 1
        fi
        python3 weave.py \
        -sf "$SONG_FILE" \
        -m "$DATA_DIR/members.csv" \
        -t "$DATA_DIR/train.csv" \
        -i
        ;;
    full)
        if [ -z "$SONG_FILE" ]; then
            echo "Error: Please provide the input song file as the second argument."
            exit 1
        fi
        run_subset "$SONG_FILE"
        run_genre_artist_stats "$SONG_FILE"
        base_filename="${SONG_FILE%.*}"
        local subset_output_file="$DATA_DIR/${base_filename}_train_subset.csv"
        python3 weave.py \
        -sf "$SONG_FILE" \
        -t "$DATA_DIR/train.csv" \
        -m "$DATA_DIR/members.csv" \
        -i
        ;;
    *)
        echo "Usage: $0 {full|subset|ontoweave|genre_artist_stats} [song_file]"
        exit 1
        ;;
esac