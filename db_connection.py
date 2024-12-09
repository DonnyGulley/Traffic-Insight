import pyodbc

# Database connection details
server = r'OBIORA\INSTANCE_ONE_SQL'
database = r'TrafficInsight_ETL'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def validate_user(username, password):
    """Validate user login credentials."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Query the User table to find the user based on the provided username
        cursor.execute("SELECT UserId, username, password, email, RoleTypeId FROM [User] WHERE username = ?", username)
        user = cursor.fetchone()

        if user:
            # Compare stored password with the input password (assumes password is stored as bytes)
            stored_password = user[2].decode('utf-8').rstrip('\x00')  # Decode and remove any null bytes
            if stored_password == password:
                return user  # Return the user data if the passwords match
            else:
                return None  # Password doesn't match
        else:
            return None  # Username not found

    except Exception as e:
        # If an error occurs (e.g., database connection issues)
        print(f"Database error occured: {e}")
        return None
    finally:
        conn.close()  # Close the connection

def register_user(username, password, email, consent, security_question, security_answer):
    """Register a new user in the database."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Insert the user data into the database, including email, consent, and security question
        cursor.execute("""
            INSERT INTO [User] (username, password, email, Consent, RoleTypeId, SecurityQuestion, SecurityAnswer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, password.encode('utf-8'), email, consent, 8, security_question, security_answer))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        return True  # Return True if the registration is successful
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return False  # Return False if there was an error


def reset_password(username, new_password):
    """Reset the user's password in the database."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Update the user's password in the database
        cursor.execute("UPDATE [User] SET password = ? WHERE username = ?", (new_password.encode('utf-8'), username))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        return True  # Return True if password reset is successful
    except pyodbc.Error as e:
        # Handle database-related errors
        print(f"Database error: {e}")
        return False  # Return False if there was an error

def get_user_data(user_id):
    """Retrieve the user's basic information (UserId, username, email)."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch user data based on UserId
        cursor.execute("SELECT UserId, username, email FROM [User] WHERE UserId = ?", (user_id))
        user_data = cursor.fetchone()  # Fetch the user data
        
        conn.close()

        # If no data is found, return None
        if user_data:
            return user_data  # Returns a tuple (UserId, username, email)
        else:
            return None  # No data found for the user
    
    except pyodbc.Error as e:
        # Handle any errors that occur while fetching user data
        print(f"Database error: {e}")
        return None

def get_bookmarks(user_id):
    """Retrieve the user's bookmarks from the database."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch user bookmarks based on UserId
        cursor.execute("SELECT Route, DateAdded FROM Bookmarks WHERE UserId = ?", (user_id))
        bookmarks = cursor.fetchall()  # Fetch all bookmark records for the user
        
        conn.close()

        # Return a list of tuples (Route, DateAdded)
        return bookmarks  # Returns an empty list if no bookmarks are found
    
    except pyodbc.Error as e:
        # Handle any database-related errors
        print(f"Database error: {e}")
        return []  # Return an empty list in case of error

def get_search_history(user_id):
    """Retrieve the user's search history from the database."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch search history based on UserId
        cursor.execute("SELECT SearchHistoryId FROM SearchHistory WHERE UserId = ?", (user_id))
        search_history = cursor.fetchall()  # Fetch all search history records for the user
        
        conn.close()

        # Return a list of tuples (SearchHistoryId)
        return search_history  # Returns an empty list if no search history is found
    
    except pyodbc.Error as e:
        # Handle any database-related errors
        print(f"Database error: {e}")
        return []  # Return an empty list in case of error

def get_notification(user_id):
    """Retrieve notifications for a user based on their UserId."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch notifications based on UserId
        cursor.execute("SELECT Message, DateAdded FROM Notifications WHERE UserId =?", (user_id))
        notifications = cursor.fetchall()  # Fetch all notifications for the user
        
        conn.close()

        # Return the list of notifications (Message, DateAdded)
        return notifications
    
    except pyodbc.Error as e:
        # Handle any database-related errors
        print(f"Database error: {e}")
        return []  # Return an empty list in case of error


def get_user_email(username):
    """Retrieve the user's email address based on their username."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch the user's email based on the username
        cursor.execute("SELECT email FROM [User] WHERE username = ?", (username))
        user = cursor.fetchone()  # Fetch the user's email

        conn.close()

        # If no user is found or email is not found, return None
        if user:
            return user[0]  # Return the email address
        else:
            return None  # No email found for the user
    
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return None  # Return None in case of error


def validate_security_question(username, answer):
    """Validate the answer to the security question for the user."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch the user's security answer based on the username
        cursor.execute("SELECT SecurityAnswer FROM [User] WHERE username = ?", (username))
        user = cursor.fetchone()  # Fetch the user's stored answer

        conn.close()

        # If no user or answer is found, return False
        if user and user[0].lower() == answer.lower():
            return True  # The answer is correct
        else:
            return False  # The answer is incorrect
    
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return False  # Return False in case of error


def get_security_question(username):
    """Fetch the user's security question based on their username."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Query the User table to fetch the security question
        cursor.execute("""
            SELECT SecurityQuestion
            FROM [User]
            WHERE username = ?
        """, username)

        # Fetch the result
        security_question = cursor.fetchone()

        if security_question:
            return security_question[0]  # Return the security question text
        else:
            print("Error: Security question not found.")
            return None

    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()  # Close the database connection
