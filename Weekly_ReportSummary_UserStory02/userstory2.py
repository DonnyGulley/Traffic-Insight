import pandas as pd

# Load all GTFS data
calendar_dates = pd.read_csv('calendar_dates.txt')
trips = pd.read_csv('trips.txt')
routes = pd.read_csv('routes.txt')
shapes = pd.read_csv('shapes.txt')
stop_times = pd.read_csv('stop_times.txt')
stops = pd.read_csv('stops.txt')

# Convert the 'date' field in calendar_dates to datetime
calendar_dates['date'] = pd.to_datetime(calendar_dates['date'], errors='coerce')

# Merge calendar_dates and trips to link trips with service dates
calendar_trips = calendar_dates.merge(trips, on='service_id', how='inner')

# Merge with stop_times to get trip details
trip_stop_times = calendar_trips.merge(stop_times, on='trip_id', how='inner')

# Optionally, join with stops and routes for contextual information
trip_details = trip_stop_times.merge(stops, on='stop_id', how='left')
trip_details = trip_details.merge(routes, on='route_id', how='left')

# Count trips by date
trip_counts_by_date = trip_details['date'].value_counts().sort_index()

# Resample to weekly frequency
trip_counts_by_date.index = pd.to_datetime(trip_counts_by_date.index)
weekly_trip_summary = trip_counts_by_date.resample('W').sum()

# Prepare the report
weekly_report = weekly_trip_summary.reset_index()
weekly_report.columns = ['Week', 'Number of Trips']

# Save the report to a CSV file
output_file_path = '/mnt/data/weekly_transit_usage_report.csv'
weekly_report.to_csv(output_file_path, index=False)

print(f"Weekly Transit Usage Report saved successfully at: {output_file_path}")
