# Traffic-Insight-Manager


# Traffic-Insight-ETL (Kitchener Open Data)
Traffic Collisions ETL Pipeline
Overview
This ETL pipeline extracts traffic collision data, transforms it, and loads it into a SQL Server database. The data can be fetched from an ArcGIS API or loaded from a CSV file, and it is transformed (column renaming, date formatting, etc.) before being inserted into the database.
* The data only goes up to 2022.
* All data is not returned at once; multiple calls are needed to retrieve the latest set.
* The system does not repeatedly try but pulls the latest accident date and uses it to filter the call.

Requirements
Python 3.x
Required libraries:
pip install requirement.txt

SQL Server for loading data
Install the required libraries:


Setup
1. Configure Database
Ensure the following tables exist in your SQL Server database:

CollisionTypes
ClassificationofAccident
ImpactLocations
LightConditions
TrafficControls
AccidentDetails

2. Configure Script
Set the connection_string server or database name in the config.py located in the root of the traffic insight project
choose whether to use the API or a local CSV file :

python
Copy code from repo https://github.com/DonnyGulley/Traffic-Insight.git

use_api is False for tesing in conjunction with file_path = 'path_to_your_file.csv'  testing /without api call

connection_string = set the config.py refer to this DB_CONNECTION_STRING_CollisionETL and set the server correctly 

3. Running the Script
Run the script to extract, transform, and load the data:
python traffic_etl.py
it should report All done! when complete

4. Data Transformation
Renames columns to a standardized format.
Converts date columns to a uniform format.
Cleans up unnecessary columns and handles missing data.

5. Saving Data to CSV for backup
If using the API, the data is saved to a timestamped CSV file in the specified folder.

6. Other 
Customizing Queries
Modify the API parameters in the script to adjust the data range. For example, to fetch data after Jan 1, 2023:

python
API Parameters
params = {"outFields": "*", "where": "ACCIDENTDATE > last_accident_date_from_database", "f": "json"}

Error Handling
Errors during data insertion into SQL Server are logged with details on the row causing the issue.

Conclusion
This ETL pipeline automates the process of extracting, transforming, and loading traffic collision data into SQL Server. It can be customized by adjusting API parameters or connection settings.

# Traffic-Insight Twitter
Traffic Twitter X ETL Pipeline
Overview
The TwitterTraffic component is designed to fetch and store traffic-related tweets for specified cities. It leverages the TwitterXAPI for fetching tweets and TwitterDatabase for storing them in a database. Below is a detailed explanation of its functionality and usage.
* The bearer token is only  good for 100 hits per month for free
* The system can be scheduled to run on a schedule for free Twitter requires time span between calls or else other issue could arise.
* In addition first calls to the api could be put in a queue , the system responds to some api responses and waits the time assigned

Dependencies
Ensure you have the following dependencies installed:


TwitterAPI
Step 1: Create a Twitter Developer Account
Go to the Twitter Developer Platform.

Sign in with your Twitter account. * be aware twitter only allows for 100 twitter unique pulls per month for free

Apply for a developer account by providing the necessary details about your intended use of the Twitter API.

Step 2: Create a Project and App
Once your developer account is approved, go to the Developer Dashboard.

Click on "Create Project" and follow the prompts to set up your project.

After creating the project, create an app within the project. This app will provide you with the necessary API keys and tokens.

Step 3: Generate API Keys and Tokens
In the app settings, navigate to the "Keys and Tokens" tab.

Generate the following keys and tokens:

Bearer Token

Copy the generated token

Step 4: Place your token in the Twitter_ETL.py
or Replace the bearer token key.

Database
1. Configure Database
Ensure the following tables exist in your SQL Server database:
the Database script can be found in the TwitterXAPI/data folder, look for the file db.sql

Hashtags
Tweets

TwitterXAPI ETL
2. Configure Script
Set the connection_string server or database name in the config.py located in the root of the traffic insight project
choose whether to use the API or a local CSV file

python
Copy code from repo https://github.com/DonnyGulley/Traffic-Insight.git

use_api is False for tesing in conjunction with file_path = 'path_to_your_file.csv'  testing /without api call

connection_string = set the config.py refer to this DB_CONNECTION_STRING_TWITTERXETL and set the server or database correctly 

3. Running the Script
Run the script to extract, transform, and load the data:
python Twitter_ETL.py
it should report All done! when complete

4. Saving Data to CSV for backup
If using the API, the data is saved to a timestamped CSV file in the specified folder.

5. Default admin created.
   username : admin 
   email: admin@example.com 
   password: password 
   Security Question : Adminkey 
   Answer: 1234