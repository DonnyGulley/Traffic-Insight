# traffic_data_loader.py
import pandas as pd
from datetime import datetime

#class used to communicate with the Traffic Insight Collision Repo 
class TrafficDataLoader:
    def __init__(self, file_path, db_connection, db_driver):
        self.file_path = file_path
        self.db_connection = db_connection
        self.df = None
        self.db_driver = db_driver

    #load data from file - testing
    def load_data(self):        
        print(f"Loading data from file: {self.file_path}")
        
        self.df = pd.read_csv(self.file_path)
        
        print("Data loaded into DataFrame.")
        print("Columns in DataFrame:", self.df.columns)

    #Transforming 
    def column_mapping(self):
        """Define column mapping for renaming."""
        return {
            'ACCIDENTNUM': 'AccidentNumber',
            'ACCIDENTDATE': 'AccidentDate',
            'ACCIDENT_YEAR': 'AccidentYear',
            'ACCIDENT_MONTH': 'AccidentMonth',
            'ACCIDENT_DAY': 'AccidentDay',
            'ACCIDENT_HOUR': 'AccidentHour',
            'ACCIDENT_MINUTE': 'AccidentMinute',
            'ACCIDENT_SECOND': 'AccidentSecond',
            'ACCIDENT_WEEKDAY': 'AccidentWeekday',
            'XCOORD': 'XCoordinate',
            'YCOORD': 'YCoordinate',
            'LONGITUDE': 'Longitude',
            'LATITUDE': 'Latitude',
            'ACCIDENTLOCATION': 'AccidentLocation',
            'COLLISIONTYPE': 'COLLISIONTYPE',
            'CLASSIFICATIONOFACCIDENT': 'CLASSIFICATIONOFACCIDENT',
            'IMPACTLOCATION': 'IMPACTLOCATION',
            'INITIALDIRECTIONOFTRAVELONE': 'InitialDirectionOfTravelOne',
            'INITIALDIRECTIONOFTRAVELTWO': 'InitialDirectionOfTravelTwo',
            'INITIALIMPACTTYPE': 'InitialImpactType',
            'INTTRAFFICCONTROL': 'IntTrafficControl',
            'LIGHT': 'LIGHT',
            'LIGHTFORREPORT': 'LightForReport',
            'ROADJURISDICTION': 'RoadJurisdiction',
            'TRAFFICCONTROL': 'TRAFFICCONTROL',
            'TRAFFICCONTROLCONDITION': 'TrafficControlCondition',
            'THRULANENO': 'ThruLaneNo',
            'NORTHBOUNDDISOBEYCOUNT': 'NorthboundDisobeyCount',
            'SOUTHBOUNDDISOBEYCOUNT': 'SouthboundDisobeyCount',
            'PEDESTRIANINVOLVED': 'PedestrianInvolved',
            'CYCLISTINVOLVED': 'CyclistInvolved',
            'MOTORCYCLISTINVOLVED': 'MotorcyclistInvolved',
            'ENVIRONMENTCONDITION1': 'EnvironmentCondition1',            
            'SELFREPORTED': 'SelfReported',
            'XMLIMPORTNOTES': 'XmlImportNotes',
            'LASTEDITEDDATE': 'LastEditedDate'
            
        }
    
    #Transform data into correct format.
    def transform_data(self):
    
        print("Transforming data...")

        # Get column mapping and rename columns
        column_mapping = self.column_mapping()
        self.df = self.df.rename(columns=column_mapping)

        # Convert date columns to datetime
        self.df['LastEditedDate'] = pd.to_datetime(self.df['LastEditedDate'], errors='coerce')

        self.df['AccidentDate'] = pd.to_datetime(self.df['AccidentDate'], unit='ms', errors='coerce')


        # Example of additional transformations (e.g., converting numeric columns)
        if 'NumVehicles' in self.df.columns:
            self.df['NumVehicles'] = pd.to_numeric(self.df['NumVehicles'], errors='coerce')

        if 'COLLISIONTYPE' in self.df.columns:
            self.df['COLLISIONTYPE'] = self.df['COLLISIONTYPE'].astype(str)

        self.df.drop(['ENVIRONMENTCONDITION2', 'CREATE_BY', 'CREATE_DATE'], axis=1, inplace=True)

        print("Data transformation complete.")
    
    #Helper function for switching between mssql and mysql        
    def format_query( self, query, driver):
        if driver == 'pyodbc':
            return query.replace('%s', '?')
        elif driver == 'pymysql':
            return query
        else:
            raise ValueError("Unsupported database driver")


    def insert_data_to_sql(self, dataframe, table_name, unique_column):
        
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        print(dataframe.columns)

        # Ensure the unique_column exists in the dataframe
        if unique_column not in dataframe.columns:
            print(f"Error: '{unique_column}' not found in the dataframe columns.")
            return

        # Create a query to check if the record already exists
        check_query = f"SELECT COUNT(*) FROM {table_name} WHERE {unique_column} = ?"

        # Prepare the insert query (done once)
        placeholders = ', '.join(['?'] * len(dataframe.columns))
        columns = ', '.join(dataframe.columns)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Iterate over each row in the dataframe
        for _, row in dataframe.iterrows():

            # Check if the value for the unique column is valid (not None or empty)
            unique_value = row[unique_column]
            if unique_value is None or pd.isna(unique_value):
                print(f"Skipping row with invalid unique column value: {unique_value}")
                continue  # Skip this row if the unique column value is invalid

            try:
                # Execute the check query to see if the record already exists
                cursor.execute(check_query, (unique_value,))
                records_exists = cursor.fetchone()[0] > 0
                
                if not records_exists:  # If the record does not exist, insert it
                    cursor.execute(sql, tuple(row))
                    print(f"New record inserted: {row[unique_column]}")

                # Commit the transaction
                connection.commit()

            except Exception as e:
                print(f"Error executing query for row {row[unique_column]}: {e}")                       
            
        
        with self.db_connection.cursor() as cursor:
            print(dataframe.columns)

            # Ensure the unique_column exists in the dataframe
            if unique_column not in dataframe.columns:
                print(f"Error: '{unique_column}' not found in the dataframe columns.")
                return

            # Create a query to check if the record already exists
            check_query = f"SELECT COUNT(*) FROM {table_name} WHERE {unique_column} = %s"
            check_query = self.format_query(check_query, self.db_driver)

            # Prepare the insert query (done once)
            placeholders = ', '.join(['%s'] * len(dataframe.columns))
            columns = ', '.join(dataframe.columns)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            sql = self.format_query(sql, self.db_driver)

            # Iterate over each row in the dataframe
            for _, row in dataframe.iterrows():
                # Check if the value for the unique column is valid (not None or empty)
                unique_value = row[unique_column]
                if unique_value is None or pd.isna(unique_value):
                    print(f"Skipping row with invalid unique column value: {unique_value}")
                    continue  # Skip this row if the unique column value is invalid

                try:
                    # Execute the check query to see if the record already exists
                    cursor.execute(check_query, (unique_value,))
                    records_exists = cursor.fetchone()[0] > 0

                    if not records_exists:  # If the record does not exist, insert it
                        cursor.execute(sql, tuple(row))
                        print(f"New record inserted: {row[unique_column]}")

                except Exception as e:
                    print(f"Error executing query for row {row[unique_column]}: {e}")

            # Commit the transaction
            self.db_connection.commit()            
           
    #Load transformed data into SQL tables."""
    def load_to_sql(self):     

        # Step 1: Insert data into CollisionTypes table
        collision_types = self.df[['COLLISIONTYPE']].drop_duplicates().reset_index(drop=True)
        self.insert_data_to_sql(collision_types, 'CollisionTypes', 'COLLISIONTYPE')

        # Step 2: Insert data into Classifications table
        classifications = self.df[['CLASSIFICATIONOFACCIDENT']].drop_duplicates().reset_index(drop=True)
        self.insert_data_to_sql(classifications, 'ClassificationofAccident', 'CLASSIFICATIONOFACCIDENT')

        # Step 3: Insert data into other lookup tables (ImpactLocations, LightConditions, TrafficControls)
        impact_locations = self.df[['IMPACTLOCATION']].drop_duplicates().reset_index(drop=True)
        self.insert_data_to_sql(impact_locations, 'ImpactLocations', 'IMPACTLOCATION')

        light_conditions = self.df[['LIGHT']].drop_duplicates().reset_index(drop=True)
        self.insert_data_to_sql(light_conditions, 'LightConditions', 'LIGHT')

        traffic_controls = self.df[['TRAFFICCONTROL']].drop_duplicates().reset_index(drop=True)
        self.insert_data_to_sql(traffic_controls, 'TrafficControls', 'TRAFFICCONTROL')

        # Step 4: Prepare AccidentDetails data
        accident_details = self.df  # Example columns
        accident_details = self.map_foreign_keys(accident_details)

        # Step 5: Insert AccidentDetails data
        self.insert_data_to_sql(accident_details, 'AccidentDetails', 'OBJECTID')


    #transforming - Map foreign keys to the AccidentDetails table.
    def map_foreign_keys(self, accident_details):
     
        # Use previously inserted data to map the corresponding foreign key IDs
        collision_type_map = self.get_id_map('CollisionTypes', 'COLLISIONTYPE')
        classification_map = self.get_id_map('ClassificationofAccident', 'ClassificationofAccident')
        impact_location_map = self.get_id_map('ImpactLocations', 'ImpactLocation')
        light_condition_map = self.get_id_map('LightConditions', 'Light')
        traffic_control_map = self.get_id_map('TrafficControls', 'TrafficControl')

        # Debug prints to check mapping dictionaries
        print("Collision Type Map:", collision_type_map)
        print("Classification Map:", classification_map)
        print("Impact Location Map:", impact_location_map)
        print("Light Condition Map:", light_condition_map)
        print("Traffic Control Map:", traffic_control_map)

        accident_details['CollisionTypeID'] = accident_details['COLLISIONTYPE'].map(collision_type_map)
        accident_details['ClassificationofAccidentID'] = accident_details['CLASSIFICATIONOFACCIDENT'].map(classification_map)
        accident_details['ImpactLocationID'] = accident_details['IMPACTLOCATION'].map(impact_location_map)
        accident_details['LightID'] = accident_details['LIGHT'].map(light_condition_map)
        accident_details['TrafficControlID'] = accident_details['TRAFFICCONTROL'].map(traffic_control_map)

        # Check for null values after mapping
        print("Null values in CollisionTypeID:", accident_details['CollisionTypeID'].isnull().sum())
        print("Null values in ClassificationID:", accident_details['ClassificationofAccidentID'].isnull().sum())
        print("Null values in ImpactLocationID:", accident_details['ImpactLocationID'].isnull().sum())
        print("Null values in LightID:", accident_details['LightID'].isnull().sum())
        print("Null values in TrafficControlID:", accident_details['TrafficControlID'].isnull().sum())
        
        # Drop original columns
        return accident_details.drop(columns=['COLLISIONTYPE', 'CLASSIFICATIONOFACCIDENT', 
                                            'IMPACTLOCATION', 'LIGHT', 'TRAFFICCONTROL'])

    #Get a dictionary of {value: ID} mapping for lookup tables."""
    def get_id_map(self, table_name, column_name):   

        with self.db_connection.cursor() as cursor:
            column_id = column_name + "Id"
            query = f"SELECT {column_name}, {column_id} FROM {table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}
    
    # Fetch the accident date from the database
    def get_last_accident_date(self):       
       
        with self.db_connection.cursor() as cursor:          
            cursor.execute("SELECT MAX(AccidentDate) FROM AccidentDetails")
            accident_date = cursor.fetchone()[0]

        # Check if accident_date is None and set to default if necessary
        if accident_date is None:
            accident_date = datetime(2015, 1, 1, 0, 0, 0)

        # Format the date as a string in the format 'YYYY-MM-DD'
        return accident_date.strftime('%Y-%m-%d')
     
    

