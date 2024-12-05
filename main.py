import time
from utils import clear_screen
from db_connection import validate_user
from forgot_password import forgot_password_screen
from register import register_screen
from user_functions import admin_welcome, user_welcome
import os


def main_menu():
    """Display the main menu with options."""
    while True:
        clear_screen()
        print("=" * 50)
        print(" " * 15 + "TrafficInsight Main Menu")
        print("=" * 50)
        print("\n1. Login")
        print("2. Forgot Password")
        print("3. Register")
        print("4. Exit")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":  # Login
            login()
        elif choice == "2":  # Forgot Password
            forgot_password_screen()
        elif choice == "3":  # Register
            register_screen()
        elif choice == "4":  # Exit
            print("\nExiting the program...")
            time.sleep(2)
            clear_screen()
            break  # Exit the program
        else:
            print("Invalid choice. Please try again.")
            time.sleep(2)


def login():
    """Handle user login."""
    while True:
        clear_screen()
        print("=" * 50)
        print(" " * 15 + "Login Screen")
        print("=" * 50)
        print("\n")

        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        # Validate user credentials
        user = validate_user(username, password)

        if user:
            user_id = user[0]
            role_type_id = user[4]
            is_admin = role_type_id == 7  # Admin role check
            if welcome_screen(username, user_id, is_admin) is False:
                break  # If logged out, return to main menu
        else:
            print("\nUsername or password is incorrect.")
            print("\n")
            time.sleep(2)
            choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
            if choice == "exit":
                print("Returning to main menu...")
                time.sleep(2)
                clear_screen()
                break


def welcome_screen(username, user_id, is_admin):
    """Display the welcome screen after successful login."""
    clear_screen()
    if is_admin:
        return admin_welcome(username)
    else:
        return user_welcome(user_id, username)


if __name__ == "__main__":
    main_menu()
