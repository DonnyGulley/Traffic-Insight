import pyodbc
from db_connection import connection_string


def view_notifications(username, is_admin=False):
    """View notifications for a user or admin."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        if is_admin:
            cursor.execute("SELECT Message, DateAdded FROM Notifications ORDER BY DateAdded DESC")
        else:
            cursor.execute("""
                SELECT Message, DateAdded
                FROM Notifications
                WHERE UserId = (SELECT UserId FROM [User] WHERE username = ?)
                ORDER BY DateAdded DESC
            """, username)

        notifications = cursor.fetchall()
        conn.close()

        print("\nNotifications:")
        print("=" * 50)
        if notifications:
            for notification in notifications:
                print(f"- {notification[0]} (Added on: {notification[1]})")
        else:
            print("No new notifications.")
        input("\nPress Enter to return to the menu...")
    except Exception as e:
        print(f"Error fetching notifications: {e}")



def send_notification(target, message):
    """Send a notification to a specific user."""
    try:
        # Establish database connection
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Insert notification for a specific user identified by user_id (target)
        cursor.execute("""
            INSERT INTO Notifications (UserId, Message, DateAdded)
            SELECT UserId, ?, GETDATE()
            FROM [User]
            WHERE UserId = ?
        """, message, target)  # Use the user_id (int) as target

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        # Success message
        print(f"Notification sent to user {target}.")

        # Wait for user input to continue
        input("\nPress Enter to continue...")

    except pyodbc.Error as e:
        # Handle database errors
        print(f"\nDatabase error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"\nAn error occurred: {e}")

        print(f"Error sending notification: {e}")
