import time
import re
from db_connection import validate_user, reset_password
from utils import clear_screen
from getpass import getpass
from notification import send_notification  # Importing from notification.py

def forgot_password_screen():
    """Handle the forgot password functionality."""
    while True:
        clear_screen()
        print("=" * 50)
        print(" " * 10 + "Forgot Password")
        print("=" * 50)

        username = input("Enter your username: ").strip()
        email = input("Enter your email: ").strip()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("\nError: Invalid email format. Please try again.")
            time.sleep(2)
            continue

        password = getpass("Enter your old password: ").strip()

        try:
            user = validate_user(username, password)
            if user and user[1] == username and user[3] == email:
                new_password = getpass("Enter your new password: ").strip()
                temp_password = getpass("Re-enter your new password: ").strip()

                if new_password != temp_password:
                    print("\nError: The new passwords do not match. Please try again.")
                    time.sleep(2)
                    continue

                if len(new_password) < 8:
                    print("\nError: Password must be at least 8 characters long.")
                    time.sleep(2)
                    continue

                if reset_password(username, new_password):
                    # Reuse the send_notification function from notification.py
                    send_notification(user[0], "Your password has been updated successfully.")
                    print(f"\nPassword for {username} has been updated successfully!")
                    time.sleep(2)
                    break
                else:
                    print(f"\nError: Could not update password for {username}. Please try again.")
                    time.sleep(2)
                    break
            else:
                print("\nError: Invalid username, email, or password.")
                choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
                if choice == "exit":
                    print("Returning to main menu...")
                    time.sleep(2)
                    return

        except Exception as e:
            print(f"\nError: {str(e)}")
            choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
            if choice == "exit":
                print("Returning to main menu...")
                time.sleep(2)
                return
