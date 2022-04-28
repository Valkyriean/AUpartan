import os
from mpi4py import MPI
from collections import Counter
import numpy as np
import json
import csv
# only first time
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()


# Divide the twitter file into approximate equal size parts
data_filepath = '../Data/Historic/twitter-melb.json'
i = 0

with open(data_filepath, 'r', encoding = "utf8") as f:

    while (i < 30):
        map_file = f
        line_record = map_file.readline()

        # Decode the json record line
        decoded_line = line_record

        # Preprocess before converting string to dict with json.loads
        new_line = decoded_line.rstrip("]}")
        new_line = new_line.rstrip("\n")
        new_line = new_line.rstrip("\r")
        new_line = new_line.rstrip(",")

        
        try:
            record_dict = json.loads(new_line)
            if (record_dict["doc"]["lang"] == "en"):
                if (record_dict["doc"]["retweeted"]):
                    continue
                else:
                    
                    res = sia.polarity_scores(record_dict["doc"]["text"])
                    print(res)
                    print(record_dict["doc"]["text"])
                    print("\n")
                    i += 1

        except Exception as e:
            pass
