# main.py
from  TrafficInsightAPI import TrafficCollisionsAPI
from TrafficInsightDatabase import TrafficDataLoader
from datetime import datetime

data_file = "Data\TrafficData\\files\incomming.csv"
db_connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_ETL;Trusted_Connection=yes;'

if __name__ == "__main__":
    use_api = True  # Set to False to use a file on disk
    if use_api:
        url = "https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Traffic_Collisions/FeatureServer/0/query"

        params = {
            "outFields": "*",
            "where": "1=1",  # This is a universal query to fetch all rows
            "f": "json"
        }
       
        traffic_data_api = TrafficCollisionsAPI(url=url, params=params)
        traffic_data_api.fetch_data()
        csv_path = traffic_data_api.save_to_csv(data_file)
        traffic_data_sql = TrafficDataLoader(csv_path, db_connection_string)
        traffic_data_sql.load_data()
    else:
        #use file
        traffic_data_sql = TrafficDataLoader(data_file, db_connection_string)
        traffic_data_sql.load_data()

    traffic_data_sql.transform_data()
    traffic_data_sql.load_to_sql()
    print("All done!")
