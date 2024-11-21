# # Save the updated DataFrame back to a CSV file
# df.to_csv('your_file_with_count.csv', index=False)

INITIALIMPACTTYPE = {
    'Angle': 0,
    'Approaching': 1,
    'Other': 2,
    'Rear end': 3,
    'Sideswipe': 4,
    'SMV other': 5,
    'SMV unattended vehicle': 6,
    'Turning movement': 7
}


 # Add a new column 'Count' with row numbers
# df['c'] = range(1, len(df) + 1)

# df['INITIALIMPACTTYPE'] = df['INITIALIMPACTTYPE'].map(INITIALIMPACTTYPE)

# # Convert ACCIDENTDATE to datetime
# df['ACCIDENTDATE'] = pd.to_datetime(df['ACCIDENTDATE'])
intersection_data = pd.read_csv("Traffic_Collisions_-3169257883124904994 - Copy (2).csv", header=0, sep=",")

#intersection_data['ACCIDENTDATE'] = pd.to_datetime(intersection_data['ACCIDENTDATE']).dt.strftime('%d/%m/%Y %H:%M:%S')
weekday_map = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}
#intersection_data['ACCIDENT_WEEKDAY'] = intersection_data['ACCIDENT_WEEKDAY'].map(weekday_map)

ENVIRONMENTCONDITION1 = {
    'Clear': 0,
    'Drifting Snow': 1,
    'Fog, mist, smoke, dust': 2,
    'Freezing Rain': 3,
    'Other': 4,
    'Rain': 5,
    'Snow': 6,
    'Strong wind': 7
}
intersection_data['ENVIRONMENTCONDITION1'] = intersection_data['ENVIRONMENTCONDITION1'].map(ENVIRONMENTCONDITION1)

ACCIDENTLOCATION = {
    'At intersection': 0,
    'At railway crossing': 1,
    'At/near private drive': 2,
    'Intersection related': 3,
    'Non intersection': 4,
    'Other': 5,
    'Overpass or bridge': 6,
    'Underpass or tunnel': 7
}
intersection_data['ACCIDENTLOCATION'] = intersection_data['ACCIDENTLOCATION'].map(ACCIDENTLOCATION)


INITIALIMPACTTYPE = {
    'Angle': 0,
    'Approaching': 1,
    'Other': 2,
    'Rear end': 3,
    'Sideswipe': 4,
    'SMV other': 5,
    'SMV unattended vehicle': 6,
    'Turning movement': 7
}
intersection_data['INITIALIMPACTTYPE'] = intersection_data['INITIALIMPACTTYPE'].map(INITIALIMPACTTYPE)

IMPACTLOCATION = {
    'Left shoulder': 0,
    'Left turn lane': 1,
    'Not on roadway - left side': 2,
    'Not on roadway - right side': 3,
    'Off highway': 4,
    'Other': 5,
    'Passing lane': 6,
    'Right shoulder': 7,
    'Right turn channel': 8,
    'Right turn lane': 9,
    'Thru lane': 10,
    'Two-way left turn lane': 11,
    'Within intersection': 12    
}
intersection_data['IMPACTLOCATION'] = intersection_data['IMPACTLOCATION'].map(IMPACTLOCATION)


LIGHT = {
    'Dark': 0,
    'Dark, artificial': 1,
    'Dawn': 2,
    'Dawn, artifical': 3,
    'Daylight': 4,
    'Daylight, artifical': 5,
    'Dusk': 6,
    'Dusk articial': 7,
    'Other': 8,
    'Unknown': 9    
}
intersection_data['LIGHT'] = intersection_data['LIGHT'].map(LIGHT)


print(intersection_data.head())
intersection_data.dropna(axis=0,inplace=True)
intersection_data["ENVIRONMENTCONDITION1"] = intersection_data['ENVIRONMENTCONDITION1'].astype(int)
intersection_data["ACCIDENTLOCATION"] = intersection_data['ACCIDENTLOCATION'].astype(int)
intersection_data["INITIALIMPACTTYPE"] = intersection_data['INITIALIMPACTTYPE'].astype(int)
intersection_data["IMPACTLOCATION"] = intersection_data['IMPACTLOCATION'].astype(int)
intersection_data["LIGHT"] = intersection_data['LIGHT'].astype(int)
