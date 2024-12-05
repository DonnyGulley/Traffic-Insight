import pyodbc
from db_connection import connection_string

def update_consent(user_id, consent):
    """Update the consent preference for data collection."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("UPDATE [User] SET Consent = ? WHERE UserId = ?", (consent, user_id))

        conn.commit()
        conn.close()

        return True
    except pyodbc.Error as e:
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
