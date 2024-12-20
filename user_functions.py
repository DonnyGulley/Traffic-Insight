# Required Imports
import os
import time
import json
from colorama import Fore, Back, Style, init

# Module Imports
from survey import participate_in_survey, view_survey_responses
from consent import update_consent, get_current_consent
from account_management import account_management_menu, view_all_users, search_user, edit_user, delete_user
from traffic_data import traffic_data
from notification import view_notifications, send_notification_to_all, send_notification_to_user
from export_data import export_data
from Business.business_access_layer import BusinessAccessLayer
from Data.data_access_layer import DataAccessLayer
from Data.Databases.Scripts.db_intialize import get_db
from threading import Thread
from time import sleep

# Initialize Components
init(autoreset=True)
bus = BusinessAccessLayer()
dal = DataAccessLayer()

# Theme Configurations
LIGHT_MODE = {
    "background": Back.WHITE,
    "text": Fore.BLACK,
}

DARK_MODE = {
    "background": Back.BLACK,
    "text": Fore.WHITE,
}

# Theme Functions
def save_theme_preference(theme_name):
    with open("theme_preference.json", "w") as file:
        json.dump({"theme": theme_name}, file)

def load_theme_preference():
    try:
        with open("theme_preference.json", "r") as file:
            return json.load(file)["theme"]
    except FileNotFoundError:
        return "light"  # Default theme

def display_message(theme):
    print(theme["background"] + theme["text"] + "Welcome to Traffic Insight!")
    print(theme["background"] + theme["text"] + "Here are your weekly transit reports.")
    print(Style.RESET_ALL)  # Reset styling after output

def color_mode():
    print("Select Theme:")
    print("1. Light Mode")
    print("2. Dark Mode")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        theme = LIGHT_MODE
        save_theme_preference("light")
    elif choice == "2":
        theme = DARK_MODE
        save_theme_preference("dark")
    else:
        print("Invalid choice. Defaulting to Light Mode.")
        theme = LIGHT_MODE
        save_theme_preference("light")
    
    display_message(theme)

# Utility Function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Admin Menu
def admin_welcome(username):
    while True:
        clear_screen()
        print("=" * 50)
        print(f"Welcome Admin: {username}")
        print("=" * 50)
        print("\n1. Manage Users (in progress...)")
        print("2. View Notifications")
        print("3. Send Notifications")
        print("4. View Activity Logs")
        print("5. View Survey Responses")
        print("6. Log out")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # If the admin chooses to manage users, call the manage_users function
            manage_users()
            time.sleep(2)
        elif choice == "2":
            # If the admin chooses to view notifications, call the function
            view_notifications(username, is_admin=True)
        elif choice == "3":
        # If the admin chooses to send notifications, ask for target and message
            target = input("Enter 'all' to notify all users or a specific username: ").strip().lower()
            if not target:  # Check if target is empty
                print("\nError: Notification target cannot be empty. Please try again.")
                time.sleep(2)
                continue

            message = input("Enter the notification message: ").strip()
            
            if not message:  # Check if message is empty
                print("\nError: Notification message cannot be empty. Please try again.")
                time.sleep(2)
                continue

            # Validate message length
            if len(message) > 500:
                print("\nError: Message exceeds the maximum allowed length of 500 characters. Please try again.")
                time.sleep(2)
                continue

            # Validate unsupported characters (example: emojis or invalid symbols)
            if any(ord(char) > 127 for char in message):
                print("\nError: Message contains unsupported characters. Please use plain text.")
                time.sleep(2)
                continue

            if target == 'all':
                # Send notification to all users
                if send_notification_to_all(message):
                    print("\nNotification sent to all users successfully.")
                else:
                    print("\nError: Unable to send notification to all users. Please try again later.")
            else:
                try:
                    # Check if target is a valid username
                    if not target.isalnum():
                        raise ValueError("Invalid username format. Only alphanumeric characters are allowed.")

                    # Attempt to send notification to a specific user
                    if send_notification_to_user(int(target), message):
                        print(f"\nNotification sent to user '{target}' successfully.")
                    else:
                        print(f"\nError: User '{target}' not found. Notification not sent.")
                except ValueError as e:
                    print(f"\nError: {e}")
                except Exception as e:
                    print(f"\nAn unexpected error occurred: {e}")
            
            input("\nPress Enter to return to the menu...")
        elif choice == "4":
            print("\nViewing Activity Logs...")
            admin()
        elif choice == "5":
            # If the admin chooses to view survey responses
            view_survey_responses()
        elif choice == "6":
            # If the admin chooses to log out
            print("\nLogging out...")
            time.sleep(2)
            return False  # Exits the loop and logs out
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)  # Wait for a moment before showing the menu again

def admin():
    logs = bus.get_activity_logs()
    print("\nActivity Logs:")
    for log in logs:
        print(log.strip())
    time.sleep(5)

def user_welcome(user_id, username):
    """Display the user welcome menu and handle user options."""
    while True:
        clear_screen()
        print("=" * 50)
        print(f"Welcome User: {username}")  # Displays the user username
        print("=" * 50)
        # Show available options for the user
        print("\n1. Play with Traffic Data")
        print("2. View Notifications")
        print("3. Account Management")
        print("4. Export My Data")
        print("5. Participate in Survey for System Improvement")  # New option for survey participation
        print("6. Log out")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # If the user chooses to work with traffic data, call the function
            traffic_data()
        elif choice == "2":
            # If the user chooses to view notifications
            view_notifications(username,is_admin=False)
        elif choice == "3":
            # If the user chooses to manage their account
            account_management_menu(user_id, username)
        elif choice == "4":
            # If the user chooses to export their data
            export_data(user_id, username)
        elif choice == "5":
            # If the user chooses to participate in the survey
            participate_in_survey(user_id)  # Call the function for survey participation
        elif choice == "6":
            # If the user chooses to log out
            print("\nLogging out...")
            time.sleep(2)
            return False  # Exits the loop and logs out
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)  # Wait before retrying

def manage_users():
    """Allow the admin to manage users by viewing, searching, editing, or deleting."""
    while True:
        clear_screen()
        print("=" * 50)
        print("User Management")  # Displays the user management section
        print("=" * 50)
        # Show options for managing users
        print("\n1. View All Users")
        print("2. Search for a User")
        print("3. Edit a User")
        print("4. Delete a User")
        print("5. Return to Admin Menu")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # If the admin chooses to view all users
            clear_screen()
            view_all_users()
        elif choice == "2":
            # If the admin chooses to search for a user
            clear_screen()
            search_user()
        elif choice == "3":
            # If the admin chooses to edit a user
            clear_screen()
            edit_user()
        elif choice == "4":
            # If the admin chooses to delete a user
            clear_screen()
            delete_user()
        elif choice == "5":
            # If the admin chooses to return to the main admin menu
            print("\nReturning to Admin Menu...")
            break  # Exits the loop and returns to the admin menu
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")  # Wait for input before retrying

