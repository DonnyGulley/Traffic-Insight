import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Show Accidents by INITIALIMPACTTYPE and ACCIDENTDATE and Group by year, day, month, hour


# Load the data
df = pd.read_csv('D:\develop\python\\big data project\cleaned.csv', parse_dates=['ACCIDENTDATE'])
print(df)
print(df.info())


# Group by year
yearly_data = df.groupby('ACCIDENT_YEAR').size()

# Group by month
monthly_data = df.groupby('ACCIDENT_MONTH').size()

# Group by day
daily_data = df.groupby(df['ACCIDENTDATE'].dt.day).size()

# Group by hour
hourly_data = df.groupby(df['ACCIDENTDATE'].dt.hour).size()

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