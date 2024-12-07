import sys 
import os
import pymysql
import pyodbc

from TrafficInsightAPI import TrafficCollisionsAPI
from TrafficInsightDatabase import TrafficInsightDatabase

if __name__ == "__main__":
   
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
        import config
        
        import os

        # Get the current working directory
        project_root = os.getcwd()

        # Construct the relative path to the directory
        data_directory = os.path.join(project_root, 'Data\\TrafficData\\files')

        print(data_directory)


        data_file = os.path.join(data_directory, "incoming.csv")
        # Fetch the database connection string from config.py based on dev or prd
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

        #create instance of the database class 
        traffic_data_sql = TrafficInsightDatabase(data_file, connection, config.DB_DRIVER)
    
        if config.Use_API:
            url = config.API_Collision_URL

            # Fetch the last available accident date from the database
            accident_date = traffic_data_sql.get_last_accident_date()

            # Filter to fetch rows with AccidentDate greater than or equal to the specified date
            params = {
                "outFields": "*",
                "where": f"AccidentDate >= '{accident_date}'",  
                "f": "json"
            }

            #Create instance of API class
            traffic_data_api = TrafficCollisionsAPI(url=url, params=params)

            traffic_data_api.fetch_data()
            
            #save incoming api data to file for backup
            csv_path = traffic_data_api.save_to_csv(data_directory)
          
            traffic_data_sql.load_data_from_df(traffic_data_api.df)
        else:
            # Use file, create a incoming file from a api datafile backup
            traffic_data_sql.load_data_from_file(data_file)

        traffic_data_sql.transform_data()
        traffic_data_sql.load_to_sql()
        print("All done!")
    finally:        
        connection.close()