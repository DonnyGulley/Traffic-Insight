# main.py
from  TrafficInsightAPI import TrafficCollisionsAPI
from TrafficInsightDatabase import TrafficDataLoader
from datetime import datetime
# Importing the config.py file
import config  

data_file = "Data\TrafficData\\files\incomming.csv"

# Fetch the database connection string from config.py
db_connection_string = config.DB_CONNECTION_STRING_CollisionETL
#db_connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_ETL;Trusted_Connection=yes;'

if __name__ == "__main__":
    use_api = True  # Set to False to use a file on disk
    if use_api:
        url = "https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Traffic_Collisions/FeatureServer/0/query"


        # Example accident date
        accident_date = datetime(2022, 7, 1)

        # Format the date as a string in the format 'YYYY-MM-DD'
        accident_date_str = accident_date.strftime('%Y-%m-%d')

        params = {
            "outFields": "*",
            "where": f"AccidentDate >= '{accident_date_str}'",  # Filter to fetch rows with AccidentDate greater than or equal to the specified date
            "f": "json"
        }

        # params = {
        #     "outFields": "*",
        #     "where": "1=1",  # This is a universal query to fetch all rows
        #     "f": "json"
        # }
       
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
