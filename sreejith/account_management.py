import pyodbc
from forgot_password import forgot_password_screen
from db_connection import connection_string
from consent import update_consent, get_current_consent
from utils import clear_screen
from notification import send_notification


def view_account_details(user_id):
    """Display account details for the logged-in user."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT username, email FROM [User] WHERE UserId = ?", user_id)
        user = cursor.fetchone()
        conn.close()

        if user:
            print("\nYour Account Details:")
            print("=" * 50)
            print(f"Username: {user[0]}")
            print(f"Email: {user[1]}")
            print("=" * 50)
        else:
            print("\nError: User not found.")
    except pyodbc.Error as e:
        print(f"\nDatabase error: {e}")


def update_user_info(user_id):
    """Update account details for the logged-in user."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        print("\nUpdate Your Information:")
        print("=" * 50)
        new_username = input("Enter new username (leave blank to keep unchanged): ").strip()
        new_email = input("Enter new email (leave blank to keep unchanged): ").strip()

        if new_username:
            cursor.execute("UPDATE [User] SET username = ? WHERE UserId = ?", (new_username, user_id))
        if new_email:
            cursor.execute("UPDATE [User] SET email = ? WHERE UserId = ?", (new_email, user_id))

        conn.commit()
        print("\nYour account information has been updated successfully.")
        conn.close()

        # Notify the user
        send_notification(user_id, "Your account information was updated.")
    except pyodbc.Error as e:
        print(f"\nDatabase error: {e}")


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
        send_notification(user_id, "Your consent preference was updated.")
    else:
        print("\nError updating your consent preference. Please try again.")
    
    input("\nPress Enter to return to the menu...")



def delete_account(user_id):
    """Delete the user's account."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM [User] WHERE UserId = ?", user_id)
        conn.commit()
        conn.close()

        print("\nYour account has been deleted successfully.")
        return True
    except pyodbc.Error as e:
        print(f"\nDatabase error: {e}")
        return False


def account_management_menu(user_id, username):
    """Display the account management menu."""
    while True:
        clear_screen()
        print("=" * 50)
        print(f"Account Management - Welcome {username}")
        print("=" * 50)
        print("\n1. View Account Details")
        print("2. Update Account Information")
        print("3. Change Password")
        print("4. Change Consent")  # Added Change Consent option
        print("5. Delete Account")
        print("6. Exit")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            clear_screen()
            view_account_details(user_id)
            input("\nPress Enter to return to the menu...")
        elif choice == "2":
            clear_screen()
            update_user_info(user_id)
            input("\nPress Enter to return to the menu...")
        elif choice == "3":
            clear_screen()
            forgot_password_screen()
        elif choice == "4":  # Change Consent
            clear_screen()
            change_consent(user_id)
        elif choice == "5":
            clear_screen()
            confirm = input("\nAre you sure you want to delete your account? Type 'yes' to confirm: ").strip().lower()
            if confirm == "yes":
                if delete_account(user_id):
                    print("\nAccount deleted. Exiting to main menu...")
                    break
            else:
                print("\nAccount deletion canceled.")
                input("\nPress Enter to return to the menu...")
        elif choice == "6":
            print("\nExiting Account Management...")
            break
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")
