import time
from utils import clear_screen  # Import the function to clear the screen
from db_connection import validate_user, get_user_email, get_security_question, validate_security_question  # Import the function to validate user credentials
from forgot_password import forgot_password_screen  # Import the screen for forgotten passwords
from register import register_screen  # Import the screen for user registration
from user_functions import admin_welcome, user_welcome  # Import functions for admin and user welcome screens
import os
from notification import send_notification_to_user

def main_menu():
    """Display the main menu with options."""
    while True:
        clear_screen()  # Clear the screen to display the main menu
        print("=" * 50)  # Print a line separator for visual formatting
        print(" " * 15 + "TrafficInsight Main Menu")  # Title of the main menu
        print("=" * 50)  # Print another line separator
        print("\n1. Login")  # Option for the user to log in
        print("2. Forgot Password")  # Option to reset password
        print("3. Register")  # Option to register a new user
        print("4. Exit")  # Option to exit the program
        print("=" * 50)  # Another line separator

        choice = input("Enter your choice: ").strip()  # Get user input for choice

        # Handle user input for each menu option
        if choice == "1":  # If user selects Login
            login()
        elif choice == "2":  # If user selects Forgot Password
            forgot_password_screen()
        elif choice == "3":  # If user selects Register
            register_screen()
        elif choice == "4":  # If user selects Exit
            print("\nExiting the program...")  # Display exit message
            time.sleep(2)  # Wait for 2 seconds before exiting
            clear_screen()  # Clear the screen before exiting
            break  # Exit the program
        else:  # If the user enters an invalid option
            print("Invalid choice. Please try again.")  # Display error message
            time.sleep(2)  # Wait for 2 seconds before showing the menu again


def login():
    """Handle user login with two-factor authentication (2FA)."""
    while True:
        clear_screen()  # Clear the screen to display the login screen
        print("=" * 50)  # Print a line separator
        print(" " * 15 + "Login Screen")  # Title of the login screen
        print("=" * 50)  # Print another line separator
        print("\n")

        # Prompt the user for login credentials
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        # Validate user credentials by calling the validate_user function
        user = validate_user(username, password)

        # If the user credentials are valid
        if user:
            user_id = user[0]  # Get the user's ID from the validation result
            role_type_id = user[4]  # Get the user's role ID
            is_admin = role_type_id == 1  # Check if the user is an admin (role ID 1)

            # Step 1: Email verification (first factor)
            print("\nStep 1: Email Verification")
            email = input("Enter your registered email address: ").strip()

            # Fetch the stored email for the user from the database
            stored_email = get_user_email(username)
            
            # Compare the entered email with the stored email
            if stored_email != email:
                print("\nError: The email address entered does not match our records.")
                time.sleep(2)
                continue  # Ask the user to retry the email input

            print("Email verified successfully!")

            # Step 2: Security question (second factor)
            print("\nStep 2: Answer the security question")
            
            # Fetch the security question from the database (it should have been stored during registration)
            security_question = get_security_question(username)  # Implement this function to fetch the question
            
            # Ask the user for the answer to the security question
            answer = input(f"Security Question: {security_question}\nYour Answer: ").strip()

            # Validate the security question answer
            if validate_security_question(username, answer):
                print("Authentication successful! You are now logged in.")
                # Call the welcome_screen function to display the appropriate welcome screen
                if welcome_screen(username, user_id, is_admin):
                    break  # If logged out, return to main menu
                break
            else:
                print("Error: The answer to the security question is incorrect.")
                time.sleep(2)  # Wait before allowing the user to try again
                continue  # Ask the user to retry the authentication

        else:
            print("\nUsername or password is incorrect.")  # Show error if invalid credentials
            print("\n")
            time.sleep(2)  # Wait for 2 seconds before allowing user to try again
            # Ask if the user wants to retry or exit
            choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
            if choice == "exit":  # If the user chooses to exit
                print("Returning to main menu...")  # Show return message
                time.sleep(2)  # Wait for 2 seconds before returning
                clear_screen()  # Clear the screen before returning to the main menu
                break  # Exit the login function after completion


def welcome_screen(username, user_id, is_admin):
    """Display the welcome screen after successful login."""
    clear_screen()  # Clear the screen to show the welcome screen
    if is_admin:  # If the user is an admin
        return admin_welcome(username)  # Display admin welcome screen
    else:  # If the user is a regular user
        return user_welcome(user_id, username)  # Display user welcome screen
    

# Entry point of the program: execute the main menu
if __name__ == "__main__":  
    main_menu()  # Call the main_menu function to start the program
