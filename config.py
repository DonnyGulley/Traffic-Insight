# config.py
import os

# Database configuration
# DB_CONNECTION_STRING_TWITTERX_MyODBC_ETL = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_Tweets;Trusted_Connection=yes;'
# DB_CONNECTION_STRING_Collision_MyODBC_ETL ='DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_ETL;Trusted_Connection=yes;'
# DB_CONNECTION_STRING_TRAFFICINSIGHT = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight;Trusted_Connection=yes;'


# Other configurations can be added here


# Database configuration
DB_CONNECTION_STRING_TWITTERXETL = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=OBIORA\\INSTANCE_ONE_SQL;DATABASE=TrafficInsight_Tweets;Trusted_Connection=yes;'
DB_CONNECTION_STRING_CollisionETL ='DRIVER={ODBC Driver 17 for SQL Server};SERVER=OBIORA\\INSTANCE_ONE_SQL;DATABASE=TrafficInsight_ETL;Trusted_Connection=yes;'
DB_CONNECTION_STRING_TRAFFICINSIGHT = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=OBIORA\\INSTANCE_ONE_SQL;DATABASE=TrafficInsight;Trusted_Connection=yes;'

# # Other configurations can be added here


DB_CONNECTION_STRING_Collision_MySQL_ETL = {
    'host': 'trafficinsight.mysql.pythonanywhere-services.com',
    'user': 'trafficinsight',
    'password': 'Passwords4Passwords2024!',
    'database': 'trafficinsight$TrafficInsight_ETL'
}
DB_CONNECTION_STRING_TwitterX_MySQL_ETL = {
    'host': 'trafficinsight.mysql.pythonanywhere-services.com',
    'user': 'trafficinsight',
    'password': 'Passwords4Passwords2024!',
    'database': 'trafficinsight$TrafficInsight_Tweets'
}

API_Collision_URL = "https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Traffic_Collisions/FeatureServer/0/query"
# Set the database driver based on the environment
DB_DRIVER = 'pyodbc'
#development use only
Use_API = True

