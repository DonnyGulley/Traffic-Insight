import pyodbc

# Database connection details
server = r'ROCKSHORE\RSQL'
database = r'TrafficInsight'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def validate_user(username, password):
    """Validate user login credentials."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT UserId, username, password, email, RoleTypeId FROM [User] WHERE username = ?", username)
        user = cursor.fetchone()

        if user:
            # Compare stored password with user input (assuming it's stored in a specific format)
            stored_password = user[2].decode('utf-8').rstrip('\x00')  # Decode and strip any null bytes
            if stored_password == password:
                return user  # Return the user data if the passwords match
            else:
                return None  # Password doesn't match
        else:
            return None  # Username not found

    except Exception as e:
        print(f"Database error occured: {e}")
        return None
    finally:
        conn.close()

#insert new user into database
def register_user(username, password, email, consent):
    """Register a new user in the database."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO [User] (username, password, email, Consent, RoleTypeId) VALUES (?, ?, ?, ?, ?)",
                       (username, password.encode('utf-8'), email, consent, 8))

        conn.commit()
        conn.close()

        return True
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return False

def reset_password(username, new_password):
    """Reset the user's password in the database."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("UPDATE [User] SET password = ? WHERE username = ?", (new_password.encode('utf-8'), username))

        conn.commit()
        conn.close()

        return True
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return False


def get_user_notifications(username):
    """Fetch the user's notifications from the database."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Query to fetch the UserId based on username
        cursor.execute("SELECT UserId FROM [User] WHERE username = ?", username)
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            
            # Fetch notifications for the specific user
            cursor.execute("SELECT Message FROM Notifications WHERE UserId = ? ORDER BY DateAdded DESC", user_id)
            notifications = cursor.fetchall()
            
            # Return a list of notification messages
            return [{"Message": notification[0]} for notification in notifications]
            

        else:
            print("Error: User not found.")
            return []

    except Exception as e:
        print(f"Error fetching notifications: {e}")
        return []
    finally:
        conn.close()



def send_notification(user_id, message):
    """Send a notification to the user about a profile or password change."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Insert the new notification into the Notifications table
        cursor.execute("INSERT INTO Notifications (UserId, Message, DateAdded) VALUES (?, ?, GETDATE())",
                       (user_id, message))

        conn.commit()
        print(f"Notification sent to user {user_id}: {message}")

    except Exception as e:
        print(f"Error sending notification: {e}")
    finally:
        conn.close()


def get_user_data(user_id):
    """Retrieve the user's basic information (UserId, username, email)."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch user data based on UserId
        cursor.execute("SELECT UserId, username, email FROM [User] WHERE UserId = ?", (user_id,))
        user_data = cursor.fetchone()  # Fetch the user data
        
        conn.close()

        # If no data is found, return None
        if user_data:
            return user_data  # Returns a tuple (UserId, username, email)
        else:
            return None  # No data found for the user
    
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return None


def get_bookmarks(user_id):
    """Retrieve the user's bookmarks from the database."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch user bookmarks based on UserId
        cursor.execute("SELECT Route, DateAdded FROM Bookmarks WHERE UserId = ?", (user_id,))
        bookmarks = cursor.fetchall()  # Fetch all bookmark records for the user
        
        conn.close()

        # If no bookmarks are found, return an empty list
        return bookmarks  # Returns a list of tuples, each with (Route, DateAdded)
    
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return []  # Return an empty list in case of error


def get_search_history(user_id):
    """Retrieve the user's search history from the database."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch search history based on UserId
        cursor.execute("SELECT SearchHistoryId FROM SearchHistory WHERE UserId = ?", (user_id,))
        search_history = cursor.fetchall()  # Fetch all search history records for the user
        
        conn.close()

        # If no search history is found, return an empty list
        return search_history  # Returns a list of tuples, each with (SearchHistoryId)
    
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return []  # Return an empty list in case of error

