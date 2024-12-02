import time
from utils import clear_screen
from db_connection import validate_user
from forgot_password import forgot_password_screen
from register import register_screen
from user_functions import admin_welcome, user_welcome
import os


def main_menu():
    """Display the main menu with options."""
    clear_screen()
    print("=" * 50)
    print(" " * 15 + "TrafficInsight Main Menu")
    print("=" * 50)
    print("\n1. Login")
    print("2. Forgot Password")
    print("3. Register")
    print("4. Exit")
    print("=" * 50)

def welcome_screen(username, user_id, is_admin):
    """Display the welcome screen after successful login."""
    clear_screen()
    if is_admin:
        return admin_welcome(username)
    else:
        return user_welcome(user_id, username)

def login_screen():
    """Display the login screen."""
    clear_screen()
    print("=" * 50)
    print(" " * 15 + "Login Screen")
    print("=" * 50)
    print("\n")

def login():
    while True:
        main_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":  # Login
            while True:
                login_screen()
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
                        clear_screen()  # Clear screen after 2 seconds
                        break
                

        elif choice == "2":  # Forgot Password
            while True:
                forgot_password_screen()
                break
            
        elif choice == "3":  # Register
            while True:
                register_screen()
                break

        elif choice == "4":  # Exit
            print("\nExiting the program...")
            time.sleep(2)
            clear_screen()
            break  # Exit the program

        else:
            print("Invalid choice. Please try again.")
            time.sleep(2)

if __name__ == "__main__":
    login()
