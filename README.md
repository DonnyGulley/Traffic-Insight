# Traffic-Insight-ETL (Kitchener Open Data)
Traffic Collisions ETL Pipeline
Overview
This ETL pipeline extracts traffic collision data, transforms it, and loads it into a SQL Server database. The data can be fetched from an ArcGIS API or loaded from a CSV file, and it is transformed (column renaming, date formatting, etc.) before being inserted into the database.

Requirements
Python 3.x
Required libraries: requests, pandas, pyodbc
SQL Server for loading data
Install the required libraries:

bash
Copy code
pip install requests pandas pyodbc
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
Set the file_path and connection_string in the script, and choose whether to use the API or a local CSV file:

python
Copy code
file_path = 'path_to_your_file.csv'  # Only if use_api is False
connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_database;Trusted_Connection=yes;'
use_api = False  # Set to True to use the API
3. Running the Script
Run the script to extract, transform, and load the data:

bash
Copy code
python traffic_etl.py
4. Data Transformation
Renames columns to a standardized format.
Converts date columns to a uniform format.
Cleans up unnecessary columns and handles missing data.
5. Saving Data to CSV (If Using API)
If using the API, the data is saved to a timestamped CSV file in the specified folder.

Customizing Queries
Modify the API parameters in the script to adjust the data range. For example, to fetch data after Jan 1, 2023:

python
Copy code
params = {"outFields": "*", "where": "ACCIDENTDATE > 1672531200000", "f": "json"}
Error Handling
Errors during data insertion into SQL Server are logged with details on the row causing the issue.

Conclusion
This ETL pipeline automates the process of extracting, transforming, and loading traffic collision data into SQL Server. It can be customized by adjusting API parameters or connection settings.

# Traffic-Insight Twitter
Step 1: Create a Twitter Developer Account
Go to the Twitter Developer Platform.

Sign in with your Twitter account.

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


Replace the placeholders in your script with the actual keys and tokens.


Database:
the Database script can be found in the TwitterXAPI/data folder, look for the file db.sql