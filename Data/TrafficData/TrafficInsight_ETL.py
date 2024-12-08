import sys 
import os
import pymysql # type: ignore
import pyodbc

from TrafficInsightAPI import TrafficCollisionsAPI
from TrafficInsightDatabase import TrafficDataLoader

if __name__ == "__main__":
    # Set to False to use a file on disk    
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
        import config
        data_file = "Data\\TrafficData\\files\\incoming.csv"
        # Fetch the database connection string from config.py
        connection=None
        if config.DB_DRIVER == 'pyodbc':
            db_connection_string = config.DB_CONNECTION_STRING_Collision_MyODBC_ETL
            connection = pyodbc.connect(db_connection_string)

        elif config.DB_DRIVER == 'pymysql':
            db_connection = config.DB_CONNECTION_STRING_Collision_MySQL_ETL
            connection = pymysql.connect(
                host=db_connection['host'],
                user=db_connection['user'],
                password=db_connection['password'],
                database=db_connection['database']
        )
        else:
            raise ValueError("Unsupported database driver")

        traffic_data_sql = TrafficDataLoader(data_file, connection, config.DB_DRIVER)
    
        if config.Use_API:
            url = "https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Traffic_Collisions/FeatureServer/0/query"

            # Fetch the last available accident date from the database
            accident_date = traffic_data_sql.get_last_accident_date()

            # Filter to fetch rows with AccidentDate greater than or equal to the specified date
            params = {
                "outFields": "*",
                "where": f"AccidentDate >= '{accident_date}'",  
                "f": "json"
            }

            traffic_data_api = TrafficCollisionsAPI(url=url, params=params)
            traffic_data_api.fetch_data()
            csv_path = traffic_data_api.save_to_csv(data_file)
            traffic_data_sql = TrafficDataLoader(csv_path, connection, config.DB_DRIVER)
            traffic_data_sql.load_data()
        else:
            # Use file
            traffic_data_sql.load_data()

        traffic_data_sql.transform_data()
        traffic_data_sql.load_to_sql()
        print("All done!")
    finally:        
        connection.close()