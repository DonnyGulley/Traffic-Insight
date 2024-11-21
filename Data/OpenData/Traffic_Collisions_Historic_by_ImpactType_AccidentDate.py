import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Traffic Collisions for Kitchener
#Fitered by Date Range and Impact Type
#Uses a cleaned file from open data source
class ImpactType():
    #Show Accidents by INITIALIMPACTTYPE and ACCIDENTDATE and Group by year, day, month, hour
    # Load the data
    df = pd.read_csv('D:\develop\python\\big data project\cleaned.csv', parse_dates=['ACCIDENTDATE'])
    print(df)
    print(df.info())

    # Define the date range for filtering
    input_start_date = input("Enter the start date (YYYY-MM-DD) or leave empty: ('2022-01-01' if ignored): ")
    if input_start_date == '' : input_start_date = '2022-01-01'

    input_end_date=input("Enter the end date (YYYY-MM-DD) or leave empty ('2019-01-01' if ignored): ")
    if input_end_date == '' : input_end_date = '2022-02-01'

    if input_start_date and input_end_date:
        # Filter the DataFrame based on the date range
        df_filtered = df[(df['ACCIDENTDATE'] >= input_start_date) & (df['ACCIDENTDATE'] <= input_end_date)]

    # Input collision type
    collision_type = input("Enter the type of collision to file (e.g. Angle: 0, Approaching: 1, Other: 2, Rear end: 3, Sideswipe: 4, SMV other: 5, SMV unattended vehicle: 6, Turning movement: 7): ")
    if collision_type:
        collision_type = int(collision_type)  # Convert input to integer
        df_filtered = df[df['INITIALIMPACTTYPE'] == collision_type]
    else:
        df_filtered = df
    #print(df_filtered.describe())
    #print(df_filtered)


    # Group by year
    yearly_data = df_filtered.groupby('ACCIDENT_YEAR').size()

    # Group by month
    monthly_data = df_filtered.groupby('ACCIDENT_MONTH').size()

    # Group by day
    daily_data = df_filtered.groupby(df_filtered['ACCIDENTDATE'].dt.date).size()

    # Group by hour
    hourly_data = df_filtered.groupby(df_filtered['ACCIDENTDATE'].dt.hour).size()

    # Example plot: Number of accidents per day
    plt.figure(figsize=(12, 8))

    # Yearly plot
    plt.subplot(2, 2, 1)
    yearly_data.plot(kind='line', marker='o')
    plt.xlabel('Year')
    plt.ylabel('Number of Accidents')
    plt.title('Accidents per Year')
    plt.grid(True)

    # Monthly plot
    plt.subplot(2, 2, 2)
    monthly_data.plot(kind='bar')
    plt.xlabel('Month')
    plt.ylabel('Number of Accidents')
    plt.title('Accidents per Month')
    plt.grid(True)

    # Daily plot
    plt.subplot(2, 2, 3)
    daily_data.plot(kind='line', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Number of Accidents')
    plt.title('Accidents per Day')
    plt.grid(True)

    # Hourly plot
    plt.subplot(2, 2, 4)
    hourly_data.plot(kind='bar')
    plt.xlabel('Hour')
    plt.ylabel('Number of Accidents')
    plt.title('Accidents per Hour')
    plt.grid(True)

    plt.tight_layout()
    plt.show()