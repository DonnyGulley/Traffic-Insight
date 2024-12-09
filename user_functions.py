import time
import os
from survey import participate_in_survey, view_survey_responses
from consent import update_consent, get_current_consent
from account_management import account_management_menu, view_all_users, search_user, edit_user, delete_user
from traffic_data import traffic_data
from notification import view_notifications, send_notification_to_all, send_notification_to_user
from export_data import export_data


def clear_screen():
    """Clear the terminal screen to improve readability."""
    # Clears the screen based on the operating system (Windows or UNIX-like)
    os.system('cls' if os.name == 'nt' else 'clear')


def admin_welcome(username):
    """Display the admin welcome menu and handle admin options."""
    while True:
        clear_screen()
        print("=" * 50)
        print(f"Welcome Admin: {username}")  # Displays the admin username
        print("=" * 50)
        # Show available options for the admin
        print("\n1. Manage Users ")
        print("2. View Notifications")
        print("3. Send Notifications")
        print("4. View Survey Responses")
        print("5. Log out")
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
            message = input("Enter the notification message: ").strip()
            if target == 'all':
                # Send notification to all users
                send_notification_to_all(message)
            else:
                # Send notification to a specific user
                send_notification_to_user(target, message)
        elif choice == "4":
            # If the admin chooses to view survey responses
            view_survey_responses()
        elif choice == "5":
            # If the admin chooses to log out
            print("\nLogging out...")
            time.sleep(2)
            return False  # Exits the loop and logs out
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)  # Wait for a moment before showing the menu again


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
