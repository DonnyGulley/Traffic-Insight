# config.py
import os

# Database configuration
DB_CONNECTION_STRING_TWITTERXETL = os.getenv('DB_CONNECTION_STRING', 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_Tweets;Trusted_Connection=yes;')
DB_CONNECTION_STRING_CollisionETL = os.getenv('DB_CONNECTION_STRING', 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_ETL;Trusted_Connection=yes;')
DB_CONNECTION_STRING_TRAFFICINSIGHT = os.getenv('DB_CONNECTION_STRING', 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight;Trusted_Connection=yes;')

# Other configurations can be added here
