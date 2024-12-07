import time
from db_connection import register_user
from utils import clear_screen


def register_screen():
    """Handle user registration."""
    clear_screen()
    print("=" * 50)
    print(" " * 10 + "Register New Account")
    print("=" * 50)

    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    email = input("Enter your email: ").strip()
    
    print("\nDo you consent to the collection and processing of your data?")
    consent_choice = input("Type 'yes' to consent or 'no' to decline: ").strip().lower()

    
    # Check if consent is given
    if consent_choice == 'y':
        consent = 1
    else:
        consent = 0    
        # Default to regular user

    if register_user(username, password, email,consent):
        print(f"\nUser {username} has been successfully registered!")

    else:
        print(f"\nError: Could not register {username}. Please try again.")

        time.sleep(2)
        clear_screen()
    
       
    choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
    if choice == "exit":
        print("Returning to main menu...")
        time.sleep(2)
        clear_screen()  # Clear screen after 2 seconds
        return
        
        
   
   
    
    

