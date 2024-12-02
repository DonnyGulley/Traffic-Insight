import time
import os
from survey import participate_in_survey
from consent import update_consent, get_current_consent

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
        print("3. Manage Consent")
        print("4. Log out")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("Exporting data (in progress...)")
            time.sleep(2)  # Simulate the action taking place
        elif choice == "2":
            participate_in_survey(user_id)   # Call the survey function
            input("\nPress Enter to return to the user menu...")
            time.sleep(2)  # Simulate the action taking place
        elif choice == "3":
            change_consent(user_id)  # Call the consent change function from consent.py
        elif choice == "4":
            print("\nLogging out...")
            time.sleep(2)
            return False  # Log out and return to the main menu
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(2)


def change_consent(user_id):
    """Allow the user to change their data collection consent."""
    print("\nManage Data Collection Consent")
    print("=" * 50)
    print("\nCurrent Preference:")
    consent_status = get_current_consent(user_id)

    if consent_status is None:
        print("Error fetching your consent status. Please try again later.")
        return

    print(f"Your current consent is: {'Consented' if consent_status else 'Not Consented'}")
    print("\nWould you like to change your consent?")
    choice = input("Type 'yes' to consent or 'no' to decline: ").strip().lower()
    consent = 1 if choice == "yes" else 0

    if update_consent(user_id, consent):
        print("\nYour consent preference has been updated successfully.")
    else:
        print("\nError updating your consent preference. Please try again.")
    
    input("\nPress Enter to return to the main menu...")
