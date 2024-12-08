import time
import os
from survey import participate_in_survey
from consent import update_consent, get_current_consent
from account_management import account_management_menu
from traffic_data import traffic_data
from notification import view_notifications, send_notification

from export_data import export_data

from Business.business_access_layer import BusinessAccessLayer
from Data.data_access_layer import DataAccessLayer
from Data.Databases.Scripts.db_intialize import get_db
from threading import Thread
from time import sleep

bus = BusinessAccessLayer()
dal = DataAccessLayer()


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
        print("4. View Activity Logs")
        print("5. Log out")
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
            print("\nViewing Activity Logs...")
            admin()
        elif choice == "5":
            print("\nLogging out...")
            time.sleep(2)
            return False
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)


def admin():
    logs = bus.get_activity_logs()
    print("\nActivity Logs:")
    for log in logs:
        print(log.strip())
    time.sleep(5)


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
        print("5. Other User Menu")
        print("6. Log out")
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
            other_user_menu()            
        elif choice == "6":
            print("\nLogging out...")
            time.sleep(2)
            return False
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)


def other_user_menu():
    """
    Displays the menu for logged-in users with appropriate features.
    """
    while True:
        print("1. Search by Location")
        print("2. Offline Search")
        print("3. Notifications")
        print("4. Feedback Menu")
        print("5. Logout")
        choice = input("Enter your choice: \n \n")

        if choice == "1":
            search_by_location()
        elif choice == "2":
            offline_search_menu()
        elif choice == "3":
            monitor_notifications(dal)
        elif choice == "4":
            feedback_menu()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


def monitor_notifications(dal):
    """
    Monitors notifications for real-time updates in a separate thread.
    """
    def run_monitoring():
        while True:
            user_locations = dal.get_user_locations()
            for location in user_locations:
                notifications = dal.get_notifications_by_location(location)
                if notifications:
                    for note in notifications:
                        print(f"{note}")
                else:
                    print(f"{location}: No incidents nearby.")
            sleep(30)

    notification_thread = Thread(target=run_monitoring, daemon=True)
    notification_thread.start()
    print("\nNotification monitoring started in the background.")


def search_by_location():
    location = input("Enter the location to search for accidents: ")
    try:
        with next(get_db()) as db:
            results = dal.search_by_location(location)
        print("\n".join(results))
    except Exception as e:
        print(f"An error occurred: {e}")

def offline_search_menu():
    """
    Submenu for offline search functionality.
    """
    while True:
        print("\nOffline Search Menu:")
        print("1. Sync Accident Data and Search")
        print("2. Back to Main Menu")
        choice = input("Enter your choice: \n")

        if choice == "1":
            # Sync data and perform the offline search immediately
            sync_and_search()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
        
        
def sync_and_search():
    """
    Sync accident data from the database and immediately prompt the user for an offline search.
    """
    try:
        # Sync data
        message = dal.cache_accident_data()
        print(message)

        # If successful, prompt for offline search
        if "successfully" in message.lower():
            location = input("Enter the location to search for accidents offline:")
            results = dal.offline_search(location)
            print("\n".join(results))
        else:
            print("Failed to sync data. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")


def offline_search():
    location = input("\nEnter the location to search for accidents offline: ")
    try:
        results = dal.offline_search(location)
        print("\n".join(results))
    except Exception as e:
        print(f"An error occurred: {e}")


def feedback_menu():
    print("\nFeedback Menu:")
    print("1. Add Feedback")
    print("2. Update Feedback")
    print("3. Search Feedback")
    choice = input("Enter your choice: ")

    if choice == "1":
        user_id = int(input("Enter your User ID: "))
        content = input("Enter your feedback: ")
        with next(get_db()) as db:
            message = bus.add_feedback(user_id, content, db)
        print(message)
    elif choice == "2":
        feedback_id = int(input("Enter Feedback ID to update: "))
        new_content = input("Enter the updated feedback: ")
        with next(get_db()) as db:
            message = bus.update_feedback(feedback_id, new_content, db)
        print(message)
    elif choice == "3":
        user_id = int(input("Enter User ID to search feedback for: "))
        with next(get_db()) as db:
            feedbacks = bus.search_feedback(user_id, db)
        if feedbacks:
            for feedback in feedbacks:
                print(f"Feedback ID: {feedback.id}, Content: {feedback.content}")
        else:
            print("No feedback found.")
    else:
        print("Invalid choice.")