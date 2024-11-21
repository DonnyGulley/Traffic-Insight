from doctest import REPORT_CDIFF
import pandas as pd
import matplotlib.pyplot as plt
import numpy as numpy
import seaborn as sns

# Traffic Collision for Kitchener

import pandas as pd

# Corrected file path and function
intersection_data = pd.read_csv(r'D:\develop\python\big data project\files\Traffic_Collisions_-3169257883124904994.csv')

# Display the first few rows of the dataframe to verify
print(intersection_data.head())


def AccidentTotals(dataframe,fieldName):
    # Example: Bar plot for ACCIDENT_WEEKDAY
    accident_weekday_counts = dataframe[fieldName].value_counts()

    plt.figure(figsize=(10, 6))
    accident_weekday_counts.plot(kind='bar', color='skyblue')
    plt.xlabel(f'Accident {fieldName}')
    plt.ylabel(f'Number of {fieldName}')
    plt.title(f'Number of Accidents by {fieldName}')
    plt.show()

def HeatMap(dataframe):
    plt.figure(figsize=(10, 8))
    sns.kdeplot(x=dataframe['LONGITUDE'], y=dataframe['LATITUDE'], cmap='Reds', fill=True, bw_adjust=0.5)
    plt.title('Density of Accidents')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

def Pie(dataframe, X='', Y='ENVIRONMENTCONDITION1'):
    plt.figure(figsize=(8, 8))
    plt.pie(X, labels=Y, autopct='%1.1f%%', startangle=140)
    plt.title('Proportion of Accidents Under Different Environmental Conditions')
    plt.show()

def PairPlot(dataframe):
    sns.pairplot(intersection_data[['ACCIDENT_YEAR',   'IMPACTLOCATION', 'INITIALIMPACTTYPE', 'LIGHT', 'ENVIRONMENTCONDITION1']])
    plt.suptitle('Pair Plot of Accident Data', y=1.02)
    plt.show()

def BoxPlot(dataframe, X, Y):
    plt.figure(figsize=(10, 6))
    intersection_data.boxplot(column=X, by=Y)
    plt.xlabel(X)
    plt.ylabel(Y)
    plt.title(f'Impact Location Distribution by {X}')
    plt.suptitle('')  # Suppress the default title
    plt.show()

def StackedBar(intersection_data):
    # Example: Stacked bar plot for COLLISIONTYPE and IMPACTLOCATION
    collision_impact_counts = intersection_data.groupby(['ACCIDENT_YEAR', 'INITIALIMPACTTYPE', "LIGHT"]).size().unstack()

    collision_impact_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.xlabel('ACCIDENT_YEAR Type')
    plt.ylabel('Number of INITIALIMPACTTYPE')
    plt.title('Stacked Bar Plot of ACCIDENT_YEAR and INITIALIMPACTTYPE')
    plt.show()

def Pivot(intersection_data):
# Create a pivot table
    
    # Aggregating data to handle duplicates
    df_aggregated = intersection_data.groupby(['LATITUDE', 'LONGITUDE'])['INITIALIMPACTTYPE'].first().reset_index()

    # Creating pivot table
    pivot_table = df_aggregated.pivot(index='LATITUDE', columns='LONGITUDE', values='INITIALIMPACTTYPE')

    # Create a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_table, annot=True, cmap='YlOrRd', linewidths=.5)
    plt.title('Density of Accidents in Different Locations')
    plt.show()
    
#(intersection_data,'ACCIDENT_YEAR','INITIALIMPACTTYPE')
#AccidentTotals(intersection_data,'ENVIRONMENTCONDITION1')
#


selected_report = input("what kind of report do you want?  Pair, Stacked, BoxPlot, Scatter, Heat - ") 
match selected_report:
    case "Pivot":
        Pivot(intersection_data)    
    case "Heat":
        HeatMap(intersection_data)   
    case _:
         print("Reporty type not found!  Good bye.")
        