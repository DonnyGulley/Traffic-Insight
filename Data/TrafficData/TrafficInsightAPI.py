# traffic_collisions_api.py
import requests
import pandas as pd
import os
from datetime import datetime

class TrafficCollisionsAPI:
    def __init__(self, url, params):
        self.url = url
        self.params = params
        self.df = None
        print("Initialized TrafficCollisionsAPI with URL and parameters.")

    def fetch_data(self):
        """Fetch data from the API and convert to DataFrame."""
        print("Fetching data from the ArcGIS REST service...")
        response = requests.get(self.url, params=self.params)
        
        response.raise_for_status()  # Check for request errors
        
        print("Data fetched successfully.")
        data = response.json()
        features = data['features']
        records = [feature['attributes'] for feature in features]
        self.df = pd.DataFrame(records)
        print("Data processed into DataFrame.")
        print("Columns in DataFrame:", self.df.columns)

    def save_to_csv(self, folder):
        """Save data as CSV with a timestamp."""
        if not os.path.exists(folder):
            os.makedirs(folder)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"traffic_collisions_{current_datetime}.csv"
        filepath = os.path.join(folder, filename)
        print(f"Saving data to {filepath}...")
        self.df.to_csv(filepath, index=False)
        print(f"Data has been saved to {filepath}")
        return filepath
