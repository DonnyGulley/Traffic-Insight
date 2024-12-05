import time
import os
from survey import participate_in_survey
from consent import update_consent, get_current_consent
from account_management import account_management_menu
from traffic_data import traffic_data
from notification import view_notifications, send_notification

from export_data import export_data


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
        print("\n1. Manage Users (in progress...)")
        print("2. View Notifications")
        print("3. Send Notifications")
        print("4. Log out")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("Manage Users functionality is in progress...")
            time.sleep(2)
        elif choice == "2":
            view_notifications(username, is_admin=True)
        elif choice == "3":
            target = input("Enter 'all' to notify all users or a specific username: ").strip()
            message = input("Enter the notification message: ").strip()
            send_notification(target, message)
        elif choice == "4":
            print("\nLogging out...")
            time.sleep(2)
            return False
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
        print("\n1. Play with Traffic Data")
        print("2. View Notifications")
        print("3. Account Management")
        print("4. Export My Data")
        print("5. Log out")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            traffic_data()
        elif choice == "2":
            view_notifications(username)
        elif choice == "3":
            account_management_menu(user_id, username)
        elif choice == "4":
            export_data(user_id, username)
        elif choice == "5":
            print("\nLogging out...")
            time.sleep(2)
            return False
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)
