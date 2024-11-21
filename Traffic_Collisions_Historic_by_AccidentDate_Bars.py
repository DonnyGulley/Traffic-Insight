from datetime import datetime
from attr import NOTHING
import pandas as pd
import matplotlib.pyplot as plt

#Traffic Collisions for Kitchener
#Multiple Views by Year, Month, Day, Hours
#Filter by Date Range
class AccidentDate():
    
    def Plot():
        
        try:
            file_path = 'cleaned.csv'
            df = pd.read_csv('D:\develop\python\\big data project\cleaned.csv', 
            parse_dates=['ACCIDENTDATE'])
            print("File loaded successfully")
        except FileNotFoundError:
            print("File not found. Please check the file path.")
        except pd.errors.ParserError:
            print("Error parsing file. Please check the file content.")
        except Exception as e:
            print(f"An error occurred: {e}")

        def filter():   
        # Define the date range for filtering
            input_start_date = input("Enter the start date (YYYY-MM-DD) or leave empty: ('2022-01-01' if ignored): ")
            if input_start_date == '' : input_start_date = '2022-01-01'

            input_end_date=input("Enter the end date (YYYY-MM-DD) or leave empty ('2019-01-01' if ignored): ")
            if input_end_date == '' : input_end_date = '2022-02-01'

            if input_start_date and input_end_date:
                # Filter the DataFrame based on the date range
                filtered = df[(df['ACCIDENTDATE'] >= input_start_date) & (df['ACCIDENTDATE'] <= input_end_date)]
        
            # Display the DataFrame
            print(filtered)
            return filtered

        try:
            print(df.head())  # Display the first few rows of the DataFrame

            filtered_df = filter()

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


        except NameError as e:
            print(f"The variable {e.name} is not defined.")
        except Exception as e:
            print(f"An error occurred: {e}")   
