import pandas as pd

# Load GTFS files
trips = pd.read_csv('trips.txt')
calendar_dates = pd.read_csv('calendar_dates.txt')
shapes = pd.read_csv('shapes.txt')
stop_times = pd.read_csv('stop_times.txt')
stops = pd.read_csv('stops.txt')

# Merge trips with stop_times
trip_data = pd.merge(trips, stop_times, on="trip_id")

# Add calendar information
trip_data = pd.merge(trip_data, calendar_dates, on="service_id")

# Filter for the current week (adjust based on your logic)
trip_data['date'] = pd.to_datetime(trip_data['date'])
current_week = trip_data[trip_data['date'].dt.isocalendar().week == pd.Timestamp.now().week]

# Aggregate weekly data
weekly_report = current_week.groupby(['route_id', 'stop_id']).agg(
    total_trips=('trip_id', 'count'),
    avg_stop_time=('arrival_time', 'mean')
).reset_index()


from sqlalchemy import create_engine

# Database connection string
connection_string = "mssql+pyodbc://<username>:<password>@<server>/<database>?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string)

# Save data to SQL Server
weekly_report.to_sql('weekly_transit_usage', engine, if_exists='replace', index=False)
