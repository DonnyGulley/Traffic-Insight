# config.py
import os

# Database configuration
DB_CONNECTION_STRING_TWITTERXETL = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_Tweets;Trusted_Connection=yes;'
DB_CONNECTION_STRING_CollisionETL ='DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight_ETL;Trusted_Connection=yes;'
DB_CONNECTION_STRING_TRAFFICINSIGHT = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=lp-windows11\\DGSQL;DATABASE=TrafficInsight;Trusted_Connection=yes;'

# Other configurations can be added here


# # Database configuration
# DB_CONNECTION_STRING_TWITTERXETL = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=OBIORA\\INSTANCE_ONE_SQL;DATABASE=TrafficInsight_Tweets;Trusted_Connection=yes;'
# DB_CONNECTION_STRING_CollisionETL ='DRIVER={ODBC Driver 17 for SQL Server};SERVER=OBIORA\\INSTANCE_ONE_SQL;DATABASE=TrafficInsight_ETL;Trusted_Connection=yes;'
# DB_CONNECTION_STRING_TRAFFICINSIGHT = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=OBIORA\\INSTANCE_ONE_SQL;DATABASE=TrafficInsight;Trusted_Connection=yes;'

# # Other configurations can be added here