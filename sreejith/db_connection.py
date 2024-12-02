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
