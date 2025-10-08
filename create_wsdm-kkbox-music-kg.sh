#!/bin/bash

# Configuration variables
DATA_DIR="data/kkbox-music-recommendation-challenge"
SUBSET_FILENAME="songs_subset_train.csv"
PYTHON_SCRIPT="create_songs_subset_train.py"

# Full path to the song subset file
FILEPATH="${DATA_DIR}/${SUBSET_FILENAME}"

run_subset() {    # Check if the file exists
    if [ -f "$FILEPATH" ]; then
        echo "File ${SUBSET_FILENAME} already exists in ${DATA_DIR}"
    else
        echo "File ${SUBSET_FILENAME} not found in ${DATA_DIR}"
        echo "Executing Python script to create it..."
        
        # Execute create_songs_subset_train.py to subset only songs that have targets in the train data.
        python3 "$PYTHON_SCRIPT" -d "$DATA_DIR" -s "$FILEPATH"

        # Check if the Python script executed successfully
        if [ $? -eq 0 ]; then
            echo "Python script executed successfully"
            
            # Verify the file was created
            if [ -f "$FILEPATH" ]; then
                echo "File ${SUBSET_FILENAME} has been created successfully"
            else
                echo "Warning: Python script completed but file was not found"
            fi
        else
            echo "Error: Python script failed to execute"
            exit 1
        fi
    fi
}

run_ontoweave() {
    ontoweave \
    "${FILEPATH}:./wsdm-kkbox-music-kg/adapters/songs.yaml" \
    "${DATA_DIR}/train.csv:./wsdm-kkbox-music-kg/adapters/train.yaml" \
    "${DATA_DIR}/members.csv:./wsdm-kkbox-music-kg/adapters/members.yaml" \
    --biocypher-config ./config/biocypher_config.yaml \
    --biocypher-schema ./config/schema_config.yaml \
    -a suffix \
    -i
    # -l INFO
}
    
# Main argument handling
case "$1" in
    full)
        run_subset
        run_ontoweave
        ;;
    subset)
        run_subset
        ;;
    ontoweave)
        run_ontoweave
        ;;
    *)
        echo "Usage: $0 {full|subset|ontoweave}"
        exit 1
        ;;
esac