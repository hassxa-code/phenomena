from config import CONFIG
import requests
from datetime import datetime
import pandas as pd
import json
import os
import csv


class Earthquake:

    def __init__(self):
        self.data = None
        self.url = CONFIG["EARTHQUAKE_ENDPOINT"] 
        self.params = {
            "format": "geojson",
            "starttime": datetime.today().strftime("%Y-%m-%d"),
            #"endtime": datetime.today().strftime("%Y-%m-%d"),
            "minmagnitude": 0.0,
            "limit": 20000,        
            "orderby": "time"    
        }

    def connect(self):

        response = requests.get(url=self.url, params=self.params)
        self.data = response.json()

    def save_raw(self):
        
        if not self.connect():
            self.connect()
        
        csv_path = CONFIG["EARTHQUAKE_ROOT_PATH_CSV"]
        file_path = os.path.join(csv_path, "earthquakes.csv")
        column = "raw_data"

        if not os.path.exists(csv_path):
            os.makedirs(csv_path)
            pd.DataFrame(columns=[column]).to_csv(file_path, index=False)

        with open(file=file_path, mode="a", newline="") as f:
            raw_data = json.dumps(self.data)
            writer = csv.writer(f)
            writer.writerow([raw_data])
       