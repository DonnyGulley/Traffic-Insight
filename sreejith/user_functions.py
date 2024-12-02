import time
import os
from survey import participate_in_survey
from consent import update_consent, get_current_consent
from account_management import account_management_menu

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def admin_welcome(username):
    """Display the admin welcome menu."""
    while True:
        clear_screen()
        print("=" * 50)
        print(f"Welcome Admin: {username}")
        print("=" * 50)
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
    """Display the user welcome menu."""
    while True:
        clear_screen()
        print("=" * 50)
        print(f"Welcome User: {username}")
        print("=" * 50)
        print("\n1. Export my data (in progress...)")
        print("2. Participate in survey (in progress...)")
        print("3. Account Management")  # Only Account Management option now
        print("4. Log out")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("Exporting data (in progress...)")
            time.sleep(2)
        elif choice == "2":
            participate_in_survey(user_id)
            input("\nPress Enter to return to the user menu...")
        elif choice == "3":  # Route to Account Management, including consent
            account_management_menu(user_id, username)
        elif choice == "4":
            print("\nLogging out...")
            time.sleep(2)
            return False  # Log out and return to main menu
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)