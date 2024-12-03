import time
import os
from survey import participate_in_survey
from consent import update_consent, get_current_consent
from account_management import account_management_menu
from traffic_data import traffic_data  # Import the traffic_data function
from db_connection import get_user_notifications, send_notification  # Assuming these functions exist
from export_data import export_to_csv, export_to_pdf, export_data


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def admin_welcome(username):
    """Display the admin welcome menu and show notifications."""
    while True:
        clear_screen()
        print("=" * 50)
        print(f"Welcome Admin: {username}")
        print("=" * 50)
        
        # Display any new notifications for the admin
        notifications = get_user_notifications(username)  # Fetch notifications
        if notifications:
            print("\nNew Notifications for Admin:")
            for notification in notifications:
                print(f"- {notification['Message']}")
                time.sleep(2)

        print("\n1. Manage users (in progress...)")
        print("2. Log out")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("Manage Users functionality is in progress...")
            time.sleep(2)  # Simulate the action taking place
        elif choice == "2":
            print("\nLogging out...")
            time.sleep(2)
            return False  # Log out and return to the main menu
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)


def user_welcome(user_id, username):
    """Display the user welcome menu and show notifications."""
    while True:
        clear_screen()
        print("=" * 50)
        print(f"Welcome User: {username}")
        print("=" * 50)
        
        # Display any new notifications for the user
        notifications = get_user_notifications(username)  # Fetch notifications
        if notifications:
            print("\nNew Notifications:")
            for notification in notifications:
                print(f"- {notification['Message']}")
                time.sleep(2)
        
        # Menu options
        print("\n1. Play with Traffic Data")
        print("2. Account Management")
        print("3. Participate in survey (in progress...)")  # Placeholder
        print("4. Export My Data")  # Added the export option here
        print("5. Log out")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            traffic_data()  # Call the traffic_data function
        elif choice == "2":
            account_management_menu(user_id, username)
        elif choice == "3":
            print("Participate in survey is in progress...")  # Placeholder
            time.sleep(2)
        elif choice == "4":
            export_data(user_id,username)
            
        elif choice == "5":
            print("\nLogging out...")
            time.sleep(2)
            return False  # Log out and return to the main menu
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)
