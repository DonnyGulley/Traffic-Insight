import time
from db_connection import validate_user, reset_password
from utils import clear_screen

def forgot_password_screen():
    """Handle the forgot password functionality."""
    while True:
        clear_screen()  # Clear the screen at the beginning
        print("=" * 50)
        print(" " * 10 + "Forgot Password")
        print("=" * 50)
    
        username = input("Enter your username: ").strip()
        email = input("Enter your email: ").strip()
        password = input("Enter your old password: ").strip()
        
        # Check if user exists and email matches
        try:
            user = validate_user(username, password)
            if user:
                # User exists and password is correct
                if user[1] == username and user[3] == email:
                    new_password = input("Enter your new password: ").strip()
                    temp_password = input("Enter your new password again: ").strip()
                    
                    if new_password == temp_password:
                        # Update password in the database
                        if reset_password(username, new_password):
                            print(f"\nPassword for {username} has been updated successfully!")
                            time.sleep(2)
                            break
                        else:
                            print(f"\nError: Could not update password for {username}. Please try again.")
                            time.sleep(2)
                            break
                    else:
                        print("\nError: The new passwords do not match. Please try again.")
                        time.sleep(2)
                else:
                    print("\nError: Email does not match. Please check your email or username.")
                    choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
                    if choice == "exit":
                        print("Returning to main menu...")
                        time.sleep(2)
                        clear_screen()  # Clear screen after 2 seconds
                        return
            else:
                print("\nError: User not found or incorrect password. Please check your credentials.")
                choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
                if choice == "exit":
                    print("Returning to main menu...")
                    time.sleep(2)
                    clear_screen()  # Clear screen after 2 seconds
                    return

        except Exception as e:
            print(f"\nError: {str(e)}")
            choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
            if choice == "exit":
                print("Returning to main menu...")
                time.sleep(2)
                clear_screen()  # Clear screen after 2 seconds
                break
