import pyodbc
from db_connection import connection_string  # Import the connection string to the database
import time

def view_notifications(username, is_admin):
    """View notifications for a user or admin."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # If the user is an admin, fetch all notifications
        if is_admin:
            cursor.execute("SELECT Message, DateAdded FROM Notifications ORDER BY DateAdded DESC")
        else:
            # If the user is not an admin, fetch notifications specific to their username
            cursor.execute("""
                SELECT Message, DateAdded
                FROM Notifications
                WHERE UserId = (SELECT UserId FROM [User] WHERE username = ?)
                ORDER BY DateAdded DESC
            """, username)

        # Fetch all notifications
        notifications = cursor.fetchall()
        conn.close()

        # Print notifications or indicate that there are none
        print("\nNotifications:")
        print("=" * 50)
        if notifications:
            for notification in notifications:
                print(f"- {notification[0]} (Added on: {notification[1]})")
        else:
            print("No new notifications.")
        
        # Pause and wait for user input before returning to the menu
        input("\nPress Enter to return to the menu...")

    except Exception as e:
        # Handle any errors that occur during the process
        print(f"Error fetching notifications: {e}")


def send_notification_to_all(message):
    """Send a notification to all users."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Insert the notification into the database for all users who are not admins
        cursor.execute("""
            INSERT INTO Notifications (UserId, Message, DateAdded)
            SELECT UserId, ?, GETDATE()
            FROM [User]
            WHERE RoleTypeId = 8  -- Assuming RoleTypeId 8 corresponds to regular users
        """, message)

        # Commit the transaction to save the changes to the database
        conn.commit()
        conn.close()

        print("Notification sent to all users.")
        time.sleep(2)
        input("\nPress Enter to continue...")

    except pyodbc.Error as e:
        # Handle any database-related errors
        print(f"\nDatabase error: {e}")
        time.sleep(2)
    except Exception as e:
        # Handle any other errors
        print(f"\nAn error occurred: {e}")
        time.sleep(2)
        

def send_notification_to_user(userid, message):
    """Send a notification to a specific user identified by their username."""
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Insert the notification for a specific user based on their username
        cursor.execute("""
            INSERT INTO Notifications (UserId, Message, DateAdded)
            VALUES(? , ?, GETDATE())
            
        """, userid, message)

        # Check if any rows were affected to ensure the user exists
        if cursor.rowcount == 0:
            print(f"User '{userid}' not found. Notification not sent.")
            time.sleep(2)
        else:
            print(f"Notification sent to user '{userid}'.")
            time.sleep(2)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        input("\nPress Enter to continue...")


    except pyodbc.Error as e:
        # Handle any database-related errors
        print(f"\nDatabase error: {e}")
        time.sleep(2)
    except Exception as e:
        # Handle any other errors
        print(f"\nAn error occurred: {e}")
        time.sleep(2)