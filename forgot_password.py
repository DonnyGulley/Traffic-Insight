import time
import re
from db_connection import validate_user, reset_password
from utils import clear_screen
from getpass import getpass
from notification import send_notification_to_user  # Importing the function to send notifications

def forgot_password_screen():
    """Handle the forgot password functionality."""
    while True:
        clear_screen()  # Clears the screen for a clean display
        print("=" * 50)
        print(" " * 10 + "Forgot Password")  # Displays the header for the forgot password screen
        print("=" * 50)

        # Get username and email from the user
        username = input("Enter your username: ").strip()
        email = input("Enter your email: ").strip()

        # Validate the email format using regular expression
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("\nError: Invalid email format. Please try again.")
            time.sleep(2)  # Pause for 2 seconds before continuing
            continue

        # Get the old password from the user
        password = getpass("Enter your old password: ").strip()

        try:
            # Validate the user by checking the username and password
            user = validate_user(username, password)
            # If user exists and their email matches, proceed to password reset
            if user and user[1] == username and user[3] == email:
                # Get and confirm the new password
                new_password = getpass("Enter your new password: ").strip()
                temp_password = getpass("Re-enter your new password: ").strip()

                # Ensure both entered new passwords match
                if new_password != temp_password:
                    print("\nError: The new passwords do not match. Please try again.")
                    time.sleep(2)
                    continue

                # Check if the new password is at least 8 characters long
                if len(new_password) < 8:
                    print("\nError: Password must be at least 8 characters long.")
                    time.sleep(2)
                    continue

                # Attempt to reset the password in the database
                if reset_password(username, new_password):
                    # Send a notification that the password was updated successfully
                    send_notification_to_user(user[0], "Your password has been updated successfully.")
                    print(f"\nPassword for {username} has been updated successfully!")
                    time.sleep(2)
                    break  # Exit the loop after successful password reset
                else:
                    print(f"\nError: Could not update password for {username}. Please try again.")
                    time.sleep(2)
                    break  # Exit the loop after failure
            else:
                # If the username, email, or password are incorrect
                print("\nError: Invalid username, email, or password.")
                choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
                if choice == "exit":
                    print("Returning to main menu...")
                    time.sleep(2)
                    return  # Exit the function and return to the main menu

        except Exception as e:
            # Catch any unexpected errors and display the message
            print(f"\nError: {str(e)}")
            choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
            if choice == "exit":
                print("Returning to main menu...")
                time.sleep(2)
                return  # Exit the function and return to the main menu
