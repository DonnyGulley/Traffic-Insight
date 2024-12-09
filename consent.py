import pyodbc
from db_connection import connection_string

def update_consent(user_id, consent):
    """Update the consent preference for data collection."""
    try:
        # Check if user_id is an integer and consent is either 0 or 1
        if not isinstance(user_id, int) or consent not in [0, 1]:
            print("Invalid input: user_id must be an integer and consent must be 0 or 1.")
            return False

        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Update the consent preference in the User table
        cursor.execute("UPDATE [User] SET Consent = ? WHERE UserId = ?", consent, user_id)

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return True

    except pyodbc.Error as e:
        # Print database error message and return False
        print(f"Database error: {e}")
        return False

def get_current_consent(user_id):
    """Fetch the current consent status of a user."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT Consent FROM [User] WHERE UserId = ?", user_id)
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return None
