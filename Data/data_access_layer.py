from Data.TrafficData.TrafficInsight_ETL_CRUD import TrafficInsight_ETL_CRUD
from Data.Databases.feedback import Feedback
import pyodbc
import json
import os

crudETL = TrafficInsight_ETL_CRUD


CACHE_FILE_PATH = os.path.join(os.path.dirname(__file__), "cached_accidents.json")
# Data layer - database - fields - services
class DataAccessLayer:

    # def __init__(self, server, database):
    def __init__(self, server="OBIORA\\INSTANCE_ONE_SQL", database="TrafficInsight_ETL"):
        self.server = server
        self.database = database
        self.connection = None
        
        try:
            # Assuming there's an ETL system that uses the same connection details, this would 
            self.etl = crudETL.TrafficInsightETL(self.server, self.database)
            self.etl.connect()
        except Exception as e:
            print(f"ETL connection failed: {e}")
        
    def connect(self):
        """
        Establish a database connection.
        """
        try:
            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                "Trusted_Connection=yes;"
            )
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
    
    
    def __del__(self):
        """
        Safely clean up connections when the object is destroyed.
        """
        try:
            if hasattr(self, 'connection') and self.connection:
                self.close_connection()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def get_connection(self):
        """
        Return the active database connection.
        """
        if not self.connection:
            self.connect()  # Reconnect if connection is not established
        return self.connection

    def get_accident_data(self):
        """
        Fetch accident data from the AccidentDetails table.
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM AccidentDetails")
            return cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error fetching accident data: {e}")
            return []
        finally:
            cursor.close()

    def log_activity(self, action, details):
        """
        Logs an activity to the ActivityLogs table.
        """
        query = """
        INSERT INTO ActivityLogs (Action, Details) VALUES (?, ?)
        """
        connection = self.etl.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, (action, details))
            connection.commit()
        except Exception as e:
            print(f"Error logging activity: {e}")
        finally:
            cursor.close()
    
    def get_activity_logs(self):
        """
        Fetches recent activity logs from the AccidentDetails table.
        """
        query = """
        SELECT TOP 10
            AccidentNumber AS Action, 
            AccidentDate AS Timestamp, 
            AccidentLocation AS Details
        FROM AccidentDetails
        ORDER BY AccidentDate DESC
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            logs = cursor.fetchall()
            
            # Format the logs in an orderly manner with good spacing
            formatted_logs = ["{:<20} {:<25} {}".format("Action", "Timestamp", "Details")]
            formatted_logs.append("-" * 70)
            for row in logs:
                formatted_logs.append("{:<20} {:<25} {}".format(str(row[0]), str(row[1]), str(row[2])))
            return formatted_logs
        except pyodbc.Error as e:
            print(f"Error fetching activity logs: {e}")
            return ["No activity logs available."]
        finally:
            cursor.close()
    
    def get_notifications_by_location(self, location):
        """
        Retrieves the latest 5 notifications based on a specific location.
        For example, traffic incidents, accident reports, or any other related alerts.
        """
        query = """
        SELECT TOP 3
            AccidentLocation, 
            CONCAT('Accident: ', AccidentLocation) AS IncidentDescription, 
            AccidentDate 
        FROM AccidentDetails
        WHERE AccidentLocation LIKE ?
        ORDER BY AccidentDate DESC
        """
        
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, (f"%{location}%",))
            results = cursor.fetchall()
            
            notifications = []
            if results:
                for row in results:
                    notifications.append({
                        "location": row[0],
                        "description": row[1],
                        "date": row[2].strftime('%Y-%m-%d %H:%M:%S')  # Formatting the date
                    })
            # Format the notifications into a more readable format
            if notifications:
                formatted_notifications = ["{:<25} {:<40} {:<20}".format("Location", "Description", "Date")]
                formatted_notifications.append("-" * 85)
                
                for notification in notifications:
                    formatted_notifications.append(
                        "{:<25} {:<40} {:<20}".format(
                            notification["location"],
                            notification["description"],
                            notification["date"]
                        ) + "\n"
                    )
                return formatted_notifications
            else:
                return ["No notifications found for this location."]
        
        except pyodbc.Error as e:
            print(f"Error fetching notifications: {e}")
            return []
        finally:
            cursor.close()
            
    def get_user_locations(self):
        """
        Retrieves a list of unique accident locations from the AccidentDetails table.
        """
        query = "SELECT DISTINCT AccidentLocation FROM AccidentDetails WHERE AccidentLocation IS NOT NULL"
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            locations = [row[0] for row in cursor.fetchall()]
            if not locations:
                print("No accident locations found in the database.")
            return locations
        except pyodbc.Error as e:
            print(f"Error fetching accident locations: {e}")
            return []
        finally:
            cursor.close()
    
    def get_user_notifications(self):
        """
        Fetches notifications for each user based on their location.
        """
        user_locations = self.get_user_locations()
        all_notifications = {}

        for location in user_locations:
            notifications = self.get_notifications_by_location(location)
            if notifications:
                all_notifications[location] = notifications

        return all_notifications

    def search_by_location(self, location):
        """
        Search accidents by location using a raw SQL query and include XmlImportNotes in the output.
        """
        query = """
        SELECT TOP 3
            AccidentLocation, 
            AccidentNumber, 
            AccidentDate, 
            XmlImportNotes
        FROM AccidentDetails 
        WHERE AccidentLocation LIKE ?
        ORDER BY AccidentDate DESC
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, (f"%{location}%",))
            accidents = cursor.fetchall()
            if accidents:
                # Format the results to include XmlImportNotes
                return [
                    f"Accident Number: {row[1]}, Date: {row[2]}, Location: {row[0]}, Notes: {row[3]}"
                    for row in accidents
                ]
            else:
                return ["No accidents found at this location."]
        except Exception as e:
            print(f"Error searching accidents by location: {e}")
            return ["An error occurred while searching accidents."]
        finally:
            cursor.close()


    def cache_accident_data(self):
        """
        Cache accident data into a local JSON file directly from the database.
        """
        query = """
        SELECT TOP 10
        AccidentNumber, AccidentDate, AccidentLocation, XmlImportNotes
        FROM AccidentDetails
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            accidents = cursor.fetchall()
            if accidents:
                accident_data = [
                    {
                        "AccidentNumber": row[0],
                        "Date": str(row[1]),
                        "Location": row[2],
                        "Notes": row[3] if row[3] else "No notes available"
                    }
                    for row in accidents
                ]
                with open(CACHE_FILE_PATH, "w") as cache_file:
                    json.dump(accident_data, cache_file)
                return f"\nAccident data cached successfully at {CACHE_FILE_PATH}."
            else:
                return "No accident data found in the database."
        except Exception as e:
            print(f"Error caching accident data: {e}")
            return "Failed to cache accident data."
        finally:
            cursor.close()


    def offline_search(self, location):
        """
        Search cached accident data for a given location offline.
        """
        try:
            with open(CACHE_FILE_PATH, "r") as cache_file:
                accident_data = json.load(cache_file)
            
            # Filter results by location with headings
            results = [
                f"\n--- Accident Details ---\n"
                f"Accident Number: {accident['AccidentNumber']}\n"
                f"Date: {accident['Date']}\n"
                f"Location: {accident['Location']}\n"
                f"Notes: {accident['Notes']}\n"
                for accident in accident_data
                if location.lower() in accident["Location"].lower()
            ]
            
            return results if results else ["No accidents found at this location in the cached data."]
        except FileNotFoundError:
            return ["Cache file not found. Please sync data while online."]
        except json.JSONDecodeError:
            return ["Cache file is corrupted. Please refresh the cache."]
        except Exception as e:
            print(f"Error during offline search: {e}")
            return ["An error occurred while performing offline search."]


    def add_feedback(self, user_id, content, db_session):
        """
        Add feedback to the database using SQLAlchemy session.
        """
        feedback = Feedback(user_id=user_id, content=content)
        try:
            db_session.add(feedback)
            db_session.commit()
            return "Feedback added successfully."
        except Exception as e:
            db_session.rollback()
            print(f"Error adding feedback: {e}")
            return "Failed to add feedback."
    
    
    def update_feedback(self, feedback_id, new_content, db_session):
        """
        Update feedback content in the database.
        """
        try:
            feedback = db_session.query(Feedback).filter(Feedback.id == feedback_id).first()
            if feedback:
                feedback.content = new_content
                db_session.commit()
                return "Feedback updated successfully."
            return "Feedback not found."
        except Exception as e:
            db_session.rollback()
            print(f"Error updating feedback: {e}")
            return "Failed to update feedback."
    
    
    def search_feedback(self, user_id, db_session):
        """
        Search feedback by user ID.
        """
        try:
            feedbacks = db_session.query(Feedback).filter(Feedback.user_id == user_id).all()
            return feedbacks if feedbacks else ["No feedback found."]
        except Exception as e:
            print(f"Error searching feedback: {e}")
            return ["Failed to search feedback."]
        
