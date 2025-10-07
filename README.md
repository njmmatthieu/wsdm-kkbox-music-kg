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

## Create the SKG on a subset of songs with taregts in *train.csv* with Ontoweaver and BioCypher

```
bash ./create_wsdm-kkbox-music-kg.sh
```

## Run Ontoweaver and Biocypher 

```
ontoweave \
    ./data/kkbox-music-recommendation-challenge/train.csv:./wsdm-kkbox-music-kg/adapters/train.yaml \
    ./data/kkbox-music-recommendation-challenge/songs.csv:./wsdm-kkbox-music-kg/adapters/songs.yaml \
    ./data/kkbox-music-recommendation-challenge/members.csv:./wsdm-kkbox-music-kg/adapters/members.yaml \
    --biocypher-config ./config/biocypher_config.yaml \
    --biocypher-schema ./config/schema_config.yaml \
    -a suffix
```
