# import pyodbc

# class TrafficInsightETL:
#     def __init__(self, server, database):
#         self.server = server
#         self.database = database
        
#         self.connection = None

#     def connect(self):
#         try:
#             self.connection = pyodbc.connect(                
#                 f'DRIVER={{ODBC Driver 17 for SQL Server}};
#                 SERVER={self.server};
#                 DATABASE={self.database};
#                 Trusted_Connection=yes;'
#             )
#             print("Connection successful")
#         except Exception as e:
#             print(f"Error connecting to database: {e}")

#     def get_accident_data(self):
#         query = """
#         SELECT 
#             AD.[OBJECTID],
#             AD.[AccidentNumber],
#             AD.[AccidentDate],
#             AD.[AccidentYear],
#             AD.[AccidentMonth],
#             AD.[AccidentDay],
#             AD.[AccidentHour],
#             AD.[AccidentMinute],
#             AD.[AccidentSecond],
#             AD.[AccidentWeekday],
#             AD.[XCoordinate],
#             AD.[YCoordinate],
#             AD.[Longitude],
#             AD.[Latitude],
#             AD.[AccidentLocation],           
#             AD.[InitialDirectionOfTravelOne],
#             AD.[InitialDirectionOfTravelTwo],
#             AD.[InitialImpactType],
#             AD.[IntTrafficControl],
#             AD.[LightID],
#             AD.[LightForReport],
#             AD.[RoadJurisdiction],
#             AD.[TrafficControlID],
#             AD.[TrafficControlCondition],
#             AD.[ThruLaneNo],
#             AD.[NorthboundDisobeyCount],
#             AD.[SouthboundDisobeyCount],
#             AD.[PedestrianInvolved],
#             AD.[CyclistInvolved],
#             AD.[MotorcyclistInvolved],
#             AD.[EnvironmentCondition1],
#             AD.[SelfReported],
#             AD.[XmlImportNotes],
#             AD.[LastEditedDate],
#             CT.[CollisionType],
#             IL.[ImpactLocation],
#             LC.[Light],
#             COA.[ClassificationofAccident],
#             IL.[ImpactLocationID]
#         FROM [TrafficInsight_ETL].[dbo].[AccidentDetails] AD
#         INNER JOIN [dbo].[CollisionTypes] CT ON AD.[CollisionTypeID] = CT.[CollisionTypeID]
#         INNER JOIN [dbo].[ImpactLocations] IL ON AD.[ImpactLocationID] = IL.[ImpactLocationID]
#         INNER JOIN [dbo].[LightConditions] LC ON AD.[LightID] = LC.[LightID]
#         INNER JOIN [dbo].[ClassificationofAccident] COA ON AD.[ClassificationofAccidentID] = COA.[ClassificationofAccidentID]
#         """
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(query)
#             rows = cursor.fetchall()
#             return rows
#         except Exception as e:
#             print(f"Error executing query: {e}")
#             return []

#     def close_connection(self):
#         if self.connection:
#             self.connection.close()
#             print("Connection closed")



import pyodbc

class TrafficInsightETL:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the database.
        """
        try:
            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                "Trusted_Connection=yes;"
            )
            print("Connection successful")
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")
            raise  # Propagate the error for better error handling

    def get_connection(self):
        """
        Returns the current connection. Reconnects if not already connected.
        """
        if not self.connection:
            self.connect()
        return self.connection

    def get_accident_data(self):
        """
        Retrieves accident data with detailed joins.
        """
        query = """
        SELECT 
            AD.[OBJECTID],
            AD.[AccidentNumber],
            AD.[AccidentDate],
            AD.[AccidentYear],
            AD.[AccidentMonth],
            AD.[AccidentDay],
            AD.[AccidentHour],
            AD.[AccidentMinute],
            AD.[AccidentSecond],
            AD.[AccidentWeekday],
            AD.[XCoordinate],
            AD.[YCoordinate],
            AD.[Longitude],
            AD.[Latitude],
            AD.[AccidentLocation],           
            AD.[InitialDirectionOfTravelOne],
            AD.[InitialDirectionOfTravelTwo],
            AD.[InitialImpactType],
            AD.[IntTrafficControl],
            AD.[LightID],
            AD.[LightForReport],
            AD.[RoadJurisdiction],
            AD.[TrafficControlID],
            AD.[TrafficControlCondition],
            AD.[ThruLaneNo],
            AD.[NorthboundDisobeyCount],
            AD.[SouthboundDisobeyCount],
            AD.[PedestrianInvolved],
            AD.[CyclistInvolved],
            AD.[MotorcyclistInvolved],
            AD.[EnvironmentCondition1],
            AD.[SelfReported],
            AD.[XmlImportNotes],
            AD.[LastEditedDate],
            CT.[CollisionType],
            IL.[ImpactLocation],
            LC.[Light],
            COA.[ClassificationofAccident],
            IL.[ImpactLocationID]
        FROM [TrafficInsight_ETL].[dbo].[AccidentDetails] AD
        INNER JOIN [dbo].[CollisionTypes] CT ON AD.[CollisionTypeID] = CT.[CollisionTypeID]
        INNER JOIN [dbo].[ImpactLocations] IL ON AD.[ImpactLocationID] = IL.[ImpactLocationID]
        INNER JOIN [dbo].[LightConditions] LC ON AD.[LightID] = LC.[LightID]
        INNER JOIN [dbo].[ClassificationofAccident] COA ON AD.[ClassificationofAccidentID] = COA.[ClassificationofAccidentID]
        """
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")
            return []
        finally:
            cursor.close()

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Connection closed")

