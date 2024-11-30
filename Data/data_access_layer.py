from Data.Databases.TrafficInsight_ETL import crud
crud = crud
# Data layer - database - fields - services
class DataAccessLayer:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.connection = None
        
        # Get the ETL data for plotting
        self.etl = crud.TrafficInsightETL(self.server, self.database)
        self.etl.connect()

    def __del__(self):
        self.etl.close_connection()

    def create_connection(self):
        self.etl.connect()

    def get_accident_data(self):
        return self.etl.get_accident_data()
