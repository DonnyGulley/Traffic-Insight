import requests
import pandas as pd
import pyodbc
import os
from datetime import datetime

class TrafficCollisionsAPI:
    def __init__(self, url, params):
        self.url = url
        self.params = params
        self.df = None
        print("Initialized TrafficCollisionsAPI with URL and parameters.")

    def fetch_data(self):
        """Fetch data from the API and convert to DataFrame."""
        print("Fetching data from the ArcGIS REST service...")
        response = requests.get(self.url, params=self.params)
        response.raise_for_status()  # Check for request errors
        print("Data fetched successfully.")
        data = response.json()
        features = data['features']
        records = [feature['attributes'] for feature in features]
        self.df = pd.DataFrame(records)
        print("Data processed into DataFrame.")
        print("Columns in DataFrame:", self.df.columns)

    def save_to_csv(self, folder):
        """Save data as CSV with a timestamp."""
        if not os.path.exists(folder):
            os.makedirs(folder)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"traffic_collisions_{current_datetime}.csv"
        filepath = os.path.join(folder, filename)
        print(f"Saving data to {filepath}...")
        self.df.to_csv(filepath, index=False)
        print(f"Data has been saved to {filepath}")
        return filepath


class TrafficDataLoader:
    def __init__(self, file_path, connection_string):
        self.file_path = file_path
        self.connection_string = connection_string
        self.df = None

    def load_data(self):
        """Load data from CSV file."""
        print(f"Loading data from file: {self.file_path}")
        self.df = pd.read_csv(self.file_path)
        print("Data loaded into DataFrame.")
        print("Columns in DataFrame:", self.df.columns)

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

    def transform_data(self):
        """Transform data into correct format."""
        print("Transforming data...")

        # Get column mapping and rename columns
        column_mapping = self.column_mapping()
        self.df = self.df.rename(columns=column_mapping)

        # Remove unused date columns 
        
        # Convert date columns to datetime
        date_columns = ['AccidentDate', 'LastEditedDate']
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')

        # Example of additional transformations (e.g., converting numeric columns)
        if 'NumVehicles' in self.df.columns:
            self.df['NumVehicles'] = pd.to_numeric(self.df['NumVehicles'], errors='coerce')

        if 'COLLISIONTYPE' in self.df.columns:
            self.df['COLLISIONTYPE'] = self.df['COLLISIONTYPE'].astype(str)

        self.df.drop(['ENVIRONMENTCONDITION2', 'CREATE_BY', 'CREATE_DATE'], axis=1, inplace=True)

        print("Data transformation complete.")

    def insert_data_to_sql(self, dataframe, table_name, unique_column):
        #"""Insert data into SQL while checking for duplicates."""
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

                        
            
           

    def load_to_sql(self):
        """Load transformed data into SQL tables."""
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

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

        connection.close()
        print("SQL Server connection is closed")

    def map_foreign_keys(self, accident_details):
        """Map foreign keys to the AccidentDetails table."""
        # Use previously inserted data to map the corresponding foreign key IDs
        collision_type_map = self.get_id_map('CollisionTypes', 'COLLISIONTYPE')
        classification_map = self.get_id_map('ClassificationofAccident', 'ClassificationofAccident')
        impact_location_map = self.get_id_map('ImpactLocations', 'ImpactLocation')
        light_condition_map = self.get_id_map('LightConditions', 'LightCondition')
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
        accident_details['LightConditionID'] = accident_details['LIGHT'].map(light_condition_map)
        accident_details['TrafficControlID'] = accident_details['TRAFFICCONTROL'].map(traffic_control_map)

        # Check for null values after mapping
        print("Null values in CollisionTypeID:", accident_details['CollisionTypeID'].isnull().sum())
        print("Null values in ClassificationID:", accident_details['ClassificationofAccidentID'].isnull().sum())
        print("Null values in ImpactLocationID:", accident_details['ImpactLocationID'].isnull().sum())
        print("Null values in LightConditionID:", accident_details['LightConditionID'].isnull().sum())
        print("Null values in TrafficControlID:", accident_details['TrafficControlID'].isnull().sum())
        
        # Drop original columns
        return accident_details.drop(columns=['COLLISIONTYPE', 'CLASSIFICATIONOFACCIDENT', 
                                              'IMPACTLOCATION', 'LIGHT', 'TRAFFICCONTROL'])

    def get_id_map(self, table_name, column_name):
        """Get a dictionary of {value: ID} mapping for lookup tables."""
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        columnID = column_name  + "Id"
        cursor.execute(f"SELECT {column_name}, {columnID}   FROM {table_name}")
    
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}


# Usage
file_path = 'D:\develop\python\Traffic-Insights\Traffic-Insight\\files\\traffic_collisions_20241122_083125.csv'
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=lp-windows11\DGSQL;'
    'DATABASE=TrafficInsight_ETL;'
    'Trusted_Connection=yes;'
)

if __name__ == "__main__":
    # For API fetching
    use_api = False  # Set to False to use a file on disk
    if use_api:
        url = "https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Traffic_Collisions/FeatureServer/0/query"
        params = {"outFields": "*", "where": "1=1", "f": "json"}
        traffic_data_api = TrafficCollisionsAPI(url=url, params=params)
        traffic_data_api.fetch_data()
        csv_path = traffic_data_api.save_to_csv("files")
        traffic_data_sql = TrafficDataLoader(csv_path, connection_string)
        traffic_data_sql.load_data()
    else:
        traffic_data_sql = TrafficDataLoader(file_path, connection_string)
        traffic_data_sql.load_data()

    traffic_data_sql.transform_data()
    traffic_data_sql.load_to_sql()
    print("All done!")
