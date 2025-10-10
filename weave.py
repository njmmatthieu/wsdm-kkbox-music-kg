import argparse
import csv
import logging
import ontoweaver
import os
import pandas as pd
import subprocess
import sys
import yaml

from biocypher import BioCypher

error_codes = {
    "ParsingError"    :  65, # "data format"
    "RunError"        :  70, # "internal"
    "DataValidationError": 76,  # "protocol"
    "ConfigError"     :  78, # "bad config"
    "CannotAccessFile": 126, # "no perm"
    "FileError"       : 127, # "not found"
    "SubprocessError" : 128, # "bad exit"
    "NetworkXError"   : 129, # probably "type not in the digraph"
    "OntoWeaverError" : 254,
    "Exception"       : 255,
}

# logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    #TODO: change description
    usage = f"Extract nodes and edges from Oncodash' CSV tables from OncoKB and/or CGI and prepare a knowledge graph import script."
    parser = argparse.ArgumentParser(
        description=usage)

    # parser.add_argument("-snv", "--single_nucleotide_variants", metavar="CSV",nargs="+",
    #                     help="Extract from a CSV file with single nucleotide variants (SNV) annotations.")
    
    parser.add_argument("-s",
                        "--songs",
                        metavar="TSV",
                        nargs="+")
    
    parser.add_argument("-t",
                        "--train",
                        metavar="TSV",
                        nargs="+")
    
    parser.add_argument("-m",
                        "--members",
                        metavar="TSV",
                        nargs="+")
    
    parser.add_argument("-gas",
                        "--genre_artist_stats",
                        metavar="TSV",
                        nargs="+")


    parser.add_argument("-i", 
                        "--import-script-run", 
                        action="store_true",
                        help=f"If passed, it will call the import scripts created by Biocypher for you.")

    asked = parser.parse_args()
    bc = BioCypher(
        biocypher_config_path="config/biocypher_config.yaml",
        schema_config_path="config/schema_config.yaml"
    )

    nodes = []
    edges = []

    print(str(asked.songs[0]))

    if asked.songs:

        # Song files require preprocessing. 
        songs_filename = str(asked.songs[0])
        print(songs_filename)
        if os.path.isfile(songs_filename):
            logging.info("Songs file exists.")

        logging.info(f"Weave songs data...")

        songs = pd.read_csv(songs_filename, 
                            quoting=csv.QUOTE_NONE, 
                            on_bad_lines='skip')

        mapping_file = "./wsdm-kkbox-music-kg/adapters/songs.yaml"
        with open(mapping_file) as fd:
            mapping = yaml.full_load(fd)

        adapter = ontoweaver.tabular.extract_table(
            df=songs,
            config=mapping,
            separator=":",
            affix="suffix",
        )

        nodes += adapter.nodes
        edges += adapter.edges

        logging.info(f"Wove songs: {len(nodes)} nodes, {len(edges)} edges.")
    
    # Extract from databases not requiring preprocessing.
    data_mappings = {}

    if asked.train:
        logging.info(f"Weave training data...")
        for file_path in asked.train:
            data_mappings[file_path] =  "./wsdm-kkbox-music-kg/adapters/train.yaml"
    
    if asked.members:
        logging.info(f"Weave members data...")
        for file_path in asked.members:
            data_mappings[file_path] =  "./wsdm-kkbox-music-kg/adapters/members.yaml"

    if asked.genre_artist_stats:
        logging.info(f"Weave genre artist stats...")
        for file_path in asked.genre_artist_stats:
            data_mappings[file_path] =  "./wsdm-kkbox-music-kg/adapters/genre_artist_stats.yaml"
    
    # Write everything.
    n, e = ontoweaver.extract(data_mappings, 
                              sep=",", 
                              affix="suffix")
    nodes += n
    edges += e

    import_file = ontoweaver.reconciliate_write(nodes, 
                                                edges, 
                                                "config/biocypher_config.yaml", 
                                                "config/schema_config.yaml", 
                                                separator=", ")
    
    print(import_file)
    # ontoweaver.check_file(import_file)

    if asked.import_script_run:
        shell = os.environ["SHELL"]
        logging.info(f"Run import scripts with {shell}...")
        try:
            subprocess.run([shell, import_file])
        except Exception as e:
            logging.error(e)
            sys.exit(error_codes["SubprocessError"])

    logging.info("Done")