# Required Imports
import os
import time
import json
from colorama import Fore, Back, Style, init

# Module Imports
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

# Other Functions and Menus Here...
