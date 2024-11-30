import matplotlib.pyplot as plt
from Data.Databases.TrafficInsight_ETL import crud
import pandas as pd
import seaborn as sns
class Visualization:

## plotting functions   


    def PlotAccidentsbyCollisionDate(self, data, start_date, end_date):
        if not data:
            print("No data available")
            return

        print(f"Data shape: {len(data)}, {len(data[0]) if data else 0}")
        
        # Convert pyodbc.Row objects to tuples
        data_tuples = [tuple(row) for row in data]
        
        # Print the first few rows of converted data to inspect its structure
        print("First few rows of converted data:")
        for row in data_tuples[:5]:
            print(row)
        
        # Ensure data is a list of tuples
        if isinstance(data_tuples, list) and all(isinstance(row, tuple) for row in data_tuples):
            df = pd.DataFrame(data_tuples, columns=[
                'OBJECTID', 'AccidentNumber', 'AccidentDate', 'AccidentYear', 'AccidentMonth', 'AccidentDay', 
                'AccidentHour', 'AccidentMinute', 'AccidentSecond', 'AccidentWeekday', 'XCoordinate', 'YCoordinate', 
                'Longitude', 'Latitude', 'AccidentLocation', 'InitialDirectionOfTravelOne', 'InitialDirectionOfTravelTwo', 
                'InitialImpactType', 'IntTrafficControl', 'LightID', 'LightForReport', 'RoadJurisdiction', 'TrafficControlID', 
                'TrafficControlCondition', 'ThruLaneNo', 'NorthboundDisobeyCount', 'SouthboundDisobeyCount', 
                'PedestrianInvolved', 'CyclistInvolved', 'MotorcyclistInvolved', 'EnvironmentCondition1', 'SelfReported', 
                'XmlImportNotes', 'LastEditedDate', 'CollisionType', 'ImpactLocation', 'Light', 'ClassificationofAccident'
            ])
            print(df.head())  # Print the first few rows of the DataFrame for verification
        else:
            print("Data is not in the expected format.")
            return

        # Convert 'AccidentDate' to datetime
        df['AccidentDate'] = pd.to_datetime(df['AccidentDate'])
        
        # Filter data by date range
        filtered_df = df[(df['AccidentDate'] >= start_date) & (df['AccidentDate'] <= end_date)]

        if filtered_df.empty:
            print("No data available for the specified date range")
            return

        # Plot accidents by date
        accident_dates = filtered_df['AccidentDate'].tolist()
        date_counts = {date: accident_dates.count(date) for date in set(accident_dates)}
      
        # Create subplots
        fig, axs = plt.subplots(3, 2, figsize=(15, 15))

        # Plot accidents by date
        accident_dates = filtered_df['AccidentDate'].tolist()
        date_counts = {date: accident_dates.count(date) for date in set(accident_dates)}
        axs[0, 0].plot(date_counts.keys(), date_counts.values(), marker='o')
        axs[0, 0].set_xlabel('Date')
        axs[0, 0].set_ylabel('Number of Accidents')
        axs[0, 0].set_title(f'Accidents by Date from {start_date} to {end_date}')
        axs[0, 0].tick_params(axis='x', rotation=45)

        # Plot accidents by weekday
        weekday_counts = df['AccidentWeekday'].value_counts()
        weekday_counts.plot(kind='bar', ax=axs[0, 1])
        axs[0, 1].set_xlabel('Weekday')
        axs[0, 1].set_ylabel('Number of Accidents')
        axs[0, 1].set_title('Accidents by Weekday')
        axs[0, 1].tick_params(axis='x', rotation=45)

        # Plot accidents by hour
        df['AccidentHour'].plot(kind='hist', bins=24, ax=axs[1, 0])
        axs[1, 0].set_xlabel('Hour of the Day')
        axs[1, 0].set_ylabel('Number of Accidents')
        axs[1, 0].set_title('Accidents by Hour of the Day')
       

        # Plot accidents involving different participants
        participant_counts = df[['PedestrianInvolved', 'CyclistInvolved', 'MotorcyclistInvolved']].sum()
        participant_counts.plot(kind='pie', autopct='%1.1f%%', ax=axs[2, 0])
        axs[2, 0].set_title('Accidents Involving Different Participants')

        # Hide the empty subplot
        axs[2, 1].axis('off')

        plt.tight_layout()
        plt.show()


    def PlotAccidentsbyImpactType(self, data, impact_type, impact_type_name):
        if not data:
            print("No data available")
            return

        print(f"Data shape: {len(data)}, {len(data[0]) if data else 0}")
        
        # Convert pyodbc.Row objects to tuples
        data_tuples = [tuple(row) for row in data]
        
        # Print the first few rows of converted data to inspect its structure
        print("First few rows of converted data:")
        for row in data_tuples[:5]:
            print(row)
        
        # Ensure data is a list of tuples
        if isinstance(data_tuples, list) and all(isinstance(row, tuple) for row in data_tuples):
            df = pd.DataFrame(data_tuples, columns=[
                'OBJECTID', 'AccidentNumber', 'AccidentDate', 'AccidentYear', 'AccidentMonth', 'AccidentDay', 
                'AccidentHour', 'AccidentMinute', 'AccidentSecond', 'AccidentWeekday', 'XCoordinate', 'YCoordinate', 
                'Longitude', 'Latitude', 'AccidentLocation', 'InitialDirectionOfTravelOne', 'InitialDirectionOfTravelTwo', 
                'InitialImpactType', 'IntTrafficControl', 'LightID', 'LightForReport', 'RoadJurisdiction', 'TrafficControlID', 
                'TrafficControlCondition', 'ThruLaneNo', 'NorthboundDisobeyCount', 'SouthboundDisobeyCount', 
                'PedestrianInvolved', 'CyclistInvolved', 'MotorcyclistInvolved', 'EnvironmentCondition1', 'SelfReported', 
                'XmlImportNotes', 'LastEditedDate', 'CollisionType', 'ImpactLocation', 'Light', 'ClassificationofAccident', 'ImpactLocationID'
            ])
            print(df.head())  # Print the first few rows of the DataFrame for verification
        else:
            print("Data is not in the expected format.")
            return

        # Convert impact_type to integer
        try:
            impact_type = int(impact_type)
        except ValueError:
            print(f"Invalid impact type: {impact_type}")
            return

        # Debugging: Print unique values in ImpactLocationID column
        print("Unique ImpactLocationID values:", df['ImpactLocationID'].unique())

        # Debugging: Print the value of impact_type
        print("Filtering by ImpactLocationID:", impact_type)

        # Filter data by ImpactLocationID
        filtered_df = df[df['ImpactLocationID'] == impact_type]

        # Debugging: Print the shape of the filtered DataFrame
        print("Filtered data shape:", filtered_df.shape)

        if filtered_df.empty:
            print(f"No data available for impact type: {impact_type}")
            return

        # Create subplots
        fig, axs = plt.subplots(3, 2, figsize=(20, 15))

        # Plot accidents by date for the specified impact type
        accident_dates = filtered_df['AccidentDate'].tolist()
        date_counts = {date: accident_dates.count(date) for date in set(accident_dates)}
        axs[0, 0].plot(date_counts.keys(), date_counts.values(), marker='o')
        axs[0, 0].set_xlabel('Date')
        axs[0, 0].set_ylabel('Number of Accidents')
        axs[0, 0].set_title(f'Accidents by Date for Impact Type: {impact_type_name}')
        axs[0, 0].tick_params(axis='x', rotation=45)

        # Plot accidents by impact type
        impact_counts = filtered_df['ImpactLocationID'].value_counts()
        impact_counts.plot(kind='bar', ax=axs[0, 1])
        axs[0, 1].set_xlabel('Impact Type')
        axs[0, 1].set_ylabel('Number of Accidents')
        axs[0, 1].set_title(f'Accidents by Impact Type: {impact_type_name}')
        axs[0, 1].tick_params(axis='x', rotation=45)

        # Plot accidents by collision type
        collision_counts = filtered_df['CollisionType'].value_counts()
        collision_counts.plot(kind='bar', ax=axs[1, 0])
        axs[1, 0].set_xlabel('Collision Type')
        axs[1, 0].set_ylabel('Number of Accidents')
        axs[1, 0].set_title(f'Accidents by Collision Type for Impact Type: {impact_type_name}')
        axs[1, 0].tick_params(axis='x', rotation=45)

        # Plot accidents involving different participants
        participant_counts = filtered_df[['PedestrianInvolved', 'CyclistInvolved', 'MotorcyclistInvolved']].sum()
        participant_counts.plot(kind='pie', autopct='%1.1f%%', ax=axs[1, 1])
        axs[1, 1].set_title(f'Accidents Involving Different Participants for Impact Type: {impact_type_name}')

        # Heatmap of accident locations
        sns.heatmap(filtered_df.pivot_table(index='YCoordinate', columns='XCoordinate', aggfunc='size', fill_value=0), cmap='viridis', ax=axs[2, 0])
        axs[2, 0].set_xlabel('X Coordinate')
        axs[2, 0].set_ylabel('Y Coordinate')
        axs[2, 0].set_title(f'Heatmap of Accident Locations for Impact Type: {impact_type_name}')

        # Box plot of accident severity by impact type
        sns.boxplot(x='ImpactLocationID', y='ClassificationofAccident', data=filtered_df, ax=axs[2, 1])
        axs[2, 1].set_xlabel('Impact Type')
        axs[2, 1].set_ylabel('Accident Severity')
        axs[2, 1].set_title(f'Accident Severity by Impact Type: {impact_type_name}')

        plt.tight_layout()
        plt.show()



    def PlotAccidentsbyRoadJurisdiction(self, data):
        if not data:
            print("No data available")
            return

        print(f"Data shape: {len(data)}, {len(data[0]) if data else 0}")
        
        # Convert pyodbc.Row objects to tuples
        data_tuples = [tuple(row) for row in data]
        
        # Print the first few rows of converted data to inspect its structure
        print("First few rows of converted data:")
        for row in data_tuples[:5]:
            print(row)
        
        # Ensure data is a list of tuples
        if isinstance(data_tuples, list) and all(isinstance(row, tuple) for row in data_tuples):
            df = pd.DataFrame(data_tuples, columns=[
                'OBJECTID', 'AccidentNumber', 'AccidentDate', 'AccidentYear', 'AccidentMonth', 'AccidentDay', 
                'AccidentHour', 'AccidentMinute', 'AccidentSecond', 'AccidentWeekday', 'XCoordinate', 'YCoordinate', 
                'Longitude', 'Latitude', 'AccidentLocation', 'InitialDirectionOfTravelOne', 'InitialDirectionOfTravelTwo', 
                'InitialImpactType', 'IntTrafficControl', 'LightID', 'LightForReport', 'RoadJurisdiction', 'TrafficControlID', 
                'TrafficControlCondition', 'ThruLaneNo', 'NorthboundDisobeyCount', 'SouthboundDisobeyCount', 
                'PedestrianInvolved', 'CyclistInvolved', 'MotorcyclistInvolved', 'EnvironmentCondition1', 'SelfReported', 
                'XmlImportNotes', 'LastEditedDate', 'CollisionType', 'ImpactLocation', 'Light', 'ClassificationofAccident', 'ImpactLocationID'
            ])
            print(df.head())  # Print the first few rows of the DataFrame for verification
        else:
            print("Data is not in the expected format.")
            return

        # Create subplots
        fig, axs = plt.subplots(3, 2, figsize=(20, 15))

        # Bar Plot of Accidents by Road Jurisdiction
        road_jurisdiction_counts = df['RoadJurisdiction'].value_counts()
        road_jurisdiction_counts.plot(kind='bar', ax=axs[0, 0])
        axs[0, 0].set_xlabel('Road Jurisdiction')
        axs[0, 0].set_ylabel('Number of Accidents')
        axs[0, 0].set_title('Accidents by Road Jurisdiction')
        axs[0, 0].tick_params(axis='x', rotation=45)

        # Pie Chart of Accidents by Road Jurisdiction
        road_jurisdiction_counts.plot(kind='pie', autopct='%1.1f%%', ax=axs[0, 1])
        axs[0, 1].set_title('Accidents by Road Jurisdiction')

        # Heatmap of Accident Locations by Road Jurisdiction
        sns.heatmap(df.pivot_table(index='YCoordinate', columns='XCoordinate', aggfunc='size', fill_value=0), cmap='viridis', ax=axs[1, 0])
        axs[1, 0].set_xlabel('X Coordinate')
        axs[1, 0].set_ylabel('Y Coordinate')
        axs[1, 0].set_title('Heatmap of Accident Locations by Road Jurisdiction')

        # Box Plot of Accident Severity by Road Jurisdiction
        if 'ClassificationofAccident' in df.columns:
            sns.boxplot(x='RoadJurisdiction', y='ClassificationofAccident', data=df, ax=axs[1, 1])
            axs[1, 1].set_xlabel('Road Jurisdiction')
            axs[1, 1].set_ylabel('ClassificationofAccident')
            axs[1, 1].set_title('Accident Severity by Road Jurisdiction')
        else:
            axs[1, 1].text(0.5, 0.5, 'AccidentSeverity column not found', horizontalalignment='center', verticalalignment='center', transform=axs[1, 1].transAxes)
            axs[1, 1].set_title('Accident Severity by Road Jurisdiction')

        # Line Plot of Accidents Over Time by Road Jurisdiction
        df.set_index('AccidentDate').groupby('RoadJurisdiction').resample('M').size().unstack().plot(ax=axs[2, 0])
        axs[2, 0].set_xlabel('Date')
        axs[2, 0].set_ylabel('Number of Accidents')
        axs[2, 0].set_title('Accidents Over Time by Road Jurisdiction')

        # Hide the empty subplot
        axs[2, 1].axis('off')

        plt.tight_layout()
        plt.show()


    def PlotAccidentsbyTrafficControlCondition(self, data):
        if not data:
            print("No data available")
            return

        print(f"Data shape: {len(data)}, {len(data[0]) if data else 0}")
        
        # Convert pyodbc.Row objects to tuples
        data_tuples = [tuple(row) for row in data]
        
        # Print the first few rows of converted data to inspect its structure
        print("First few rows of converted data:")
        for row in data_tuples[:5]:
            print(row)
        
        # Ensure data is a list of tuples
        if isinstance(data_tuples, list) and all(isinstance(row, tuple) for row in data_tuples):
            df = pd.DataFrame(data_tuples, columns=[
                'OBJECTID', 'AccidentNumber', 'AccidentDate', 'AccidentYear', 'AccidentMonth', 'AccidentDay', 
                'AccidentHour', 'AccidentMinute', 'AccidentSecond', 'AccidentWeekday', 'XCoordinate', 'YCoordinate', 
                'Longitude', 'Latitude', 'AccidentLocation', 'InitialDirectionOfTravelOne', 'InitialDirectionOfTravelTwo', 
                'InitialImpactType', 'IntTrafficControl', 'LightID', 'LightForReport', 'RoadJurisdiction', 'TrafficControlID', 
                'TrafficControlCondition', 'ThruLaneNo', 'NorthboundDisobeyCount', 'SouthboundDisobeyCount', 
                'PedestrianInvolved', 'CyclistInvolved', 'MotorcyclistInvolved', 'EnvironmentCondition1', 'SelfReported', 
                'XmlImportNotes', 'LastEditedDate', 'CollisionType', 'ImpactLocation', 'Light', 'ClassificationofAccident', 'ImpactLocationID'
            ])
            print(df.head())  # Print the first few rows of the DataFrame for verification
        else:
            print("Data is not in the expected format.")
            return

        # Create subplots
        fig, axs = plt.subplots(3, 2, figsize=(20, 15))

        # Bar Plot of Accidents by Traffic Control Condition
        traffic_control_counts = df['TrafficControlCondition'].value_counts()
        traffic_control_counts.plot(kind='bar', ax=axs[0, 0])
        axs[0, 0].set_xlabel('Traffic Control Condition')
        axs[0, 0].set_ylabel('Number of Accidents')
        axs[0, 0].set_title('Accidents by Traffic Control Condition')
        axs[0, 0].tick_params(axis='x', rotation=45)

        # Pie Chart of Accidents by Traffic Control Condition
        traffic_control_counts.plot(kind='pie', autopct='%1.1f%%', ax=axs[0, 1])
        axs[0, 1].set_title('Accidents by Traffic Control Condition')

        # Heatmap of Accident Locations by Traffic Control Condition
        sns.heatmap(df.pivot_table(index='YCoordinate', columns='XCoordinate', aggfunc='size', fill_value=0), cmap='viridis', ax=axs[1, 0])
        axs[1, 0].set_xlabel('X Coordinate')
        axs[1, 0].set_ylabel('Y Coordinate')
        axs[1, 0].set_title('Heatmap of Accident Locations by Traffic Control Condition')

        # Box Plot of Accident Severity by Traffic Control Condition
        if 'ClassificationofAccident' in df.columns:
            sns.boxplot(x='TrafficControlCondition', y='ClassificationofAccident', data=df, ax=axs[1, 1])
            axs[1, 1].set_xlabel('Traffic Control Condition')
            axs[1, 1].set_ylabel('ClassificationofAccident')
            axs[1, 1].set_title('Accident Severity by Traffic Control Condition')
        else:
            axs[1, 1].text(0.5, 0.5, 'AccidentSeverity column not found', horizontalalignment='center', verticalalignment='center', transform=axs[1, 1].transAxes)
            axs[1, 1].set_title('Accident Severity by Traffic Control Condition')

        # Line Plot of Accidents Over Time by Traffic Control Condition
        df.set_index('AccidentDate').groupby('TrafficControlCondition').resample('M').size().unstack().plot(ax=axs[2, 0])
        axs[2, 0].set_xlabel('Date')
        axs[2, 0].set_ylabel('Number of Accidents')
        axs[2, 0].set_title('Accidents Over Time by Traffic Control Condition')

        # Hide the empty subplot
        axs[2, 1].axis('off')

        plt.tight_layout()
        plt.show()
