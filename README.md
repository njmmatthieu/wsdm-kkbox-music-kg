# WSDM - KKBox's Music Recommendation Challenge data into SKG

## Overview

This repository the scripts to run OntoWeaver and BioCypher for the creation of knowledge graphs from the data provided for the WSDM - KKBox Music Recommendation challenge. 

## Data

	1. Download the data at this link: https://www.kaggle.com/competitions/kkbox-music-recommendation-challenge/data
	2. Unzip them with py7zr package
	3. Structure of the data in the folder: data > kkbox-music-recommendation-challenge/

The columns of the tabular data are described at this link: https://www.kaggle.com/competitions/kkbox-music-recommendation-challenge/data

We will be using only three of these datasets: train.csv, members.csv and songs.csv. 
You need first to  unzip those three files with py7zr python package. 
The downloaded folder called *kkbox-music-recommendation-chalenge* data should be located in a folder called *data* at the root of this directory. 

bash ./create_wsdm-kkbox-music-kg.sh

## Run the SKG creation pipeline with different options

The script `create_wsdm-kkbox-music-kg.sh` supports four main modes:

### 1. full
Runs the full pipeline: creates a subset of songs with targets, then runs Ontoweave and genre-artist statistics on the subset.

**Example:**
```
bash ./create_wsdm-kkbox-music-kg.sh full data/kkbox-music-recommendation-challenge/songs.csv
```

### 2. subset
Creates a subset of songs with targets in train.csv from the input song file.

**Example:**
```
bash ./create_wsdm-kkbox-music-kg.sh subset data/kkbox-music-recommendation-challenge/songs.csv
```

### 3. ontoweave
Runs Ontoweave on the provided song file (can be a subset or full songs file).

**Example:**
```
bash ./create_wsdm-kkbox-music-kg.sh ontoweave data/kkbox-music-recommendation-challenge/songs_subset_train.csv
```

### 4. genre_artists_stats
Runs genre-artist statistics on the provided song file.

**Example:**
```
bash ./create_wsdm-kkbox-music-kg.sh genre_artists_stats data/kkbox-music-recommendation-challenge/songs_subset_train.csv
```
