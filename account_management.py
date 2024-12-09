import pyodbc  # Import pyodbc for database connection
from forgot_password import forgot_password_screen  # Import the forgot password screen
from db_connection import connection_string  # Import the database connection string
from consent import update_consent, get_current_consent  # Import functions for consent management
from utils import clear_screen  # Import the function to clear the screen
from notification import send_notification_to_user  # Import the function to send notifications


def view_account_details(user_id):
    """Display account details for the logged-in user."""
    try:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT username, email FROM [User] WHERE UserId = ?", user_id)
        user = cursor.fetchone()  # Fetch user details
        conn.close()

        if user:
            # If user is found, display their account details
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
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        print("\nUpdate Your Information:")
        print("=" * 50)
        new_username = input("Enter new username (leave blank to keep unchanged): ").strip()
        new_email = input("Enter new email (leave blank to keep unchanged): ").strip()

        # Update username or email if provided
        if new_username:
            cursor.execute("UPDATE [User] SET username = ? WHERE UserId = ?", (new_username, user_id))
        if new_email:
            cursor.execute("UPDATE [User] SET email = ? WHERE UserId = ?", (new_email, user_id))

        conn.commit()  # Commit the changes
        print("\nYour account information has been updated successfully.")
        conn.close()

        # Send notification to user about the update
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

    # Display current consent status
    print(f"Your current consent is: {'Consented' if consent_status else 'Not Consented'}")
    print("\nWould you like to change your consent?")
    choice = input("Type 'yes' to consent or 'no' to decline: ").strip().lower()
    consent = 1 if choice == "yes" else 0

    if update_consent(user_id, consent):  # Update the consent preference in the database
        print("\nYour consent preference has been updated successfully.")
        send_notification(user_id, "Your consent preference was updated.")
    else:
        print("\nError updating your consent preference. Please try again.")
    
    input("\nPress Enter to return to the menu...")


def delete_account(user_id):
    """Delete the user's account."""
    try:
        # Connect to the database and delete the user account
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
        clear_screen()  # Clear the screen for the account management menu
        print("=" * 50)
        print(f"Account Management - Welcome {username}")
        print("=" * 50)
        print("\n1. View Account Details")  # Option to view account details
        print("2. Update Account Information")  # Option to update account info
        print("3. Change Password")  # Option to change password
        print("4. Change Consent")  # Option to change consent preference
        print("5. Delete Account")  # Option to delete the account
        print("6. Exit")  # Option to exit the menu
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            clear_screen()
            view_account_details(user_id)  # Display account details
            input("\nPress Enter to return to the menu...")
        elif choice == "2":
            clear_screen()
            update_user_info(user_id)  # Update account details
            input("\nPress Enter to return to the menu...")
        elif choice == "3":
            clear_screen()
            forgot_password_screen()  # Open forgot password screen
        elif choice == "4":
            clear_screen()
            change_consent(user_id)  # Change data collection consent
        elif choice == "5":
            clear_screen()
            confirm = input("\nAre you sure you want to delete your account? Type 'yes' to confirm: ").strip().lower()
            if confirm == "yes":
                if delete_account(user_id):  # Delete the account if confirmed
                    print("\nAccount deleted. Exiting to main menu...")
                    break
            else:
                print("\nAccount deletion canceled.")
                input("\nPress Enter to return to the menu...")
        elif choice == "6":
            print("\nExiting Account Management...")
            break  # Exit the account management menu
        else:
            print("\nInvalid choice. Please try again.")  # Handle invalid input
            input("\nPress Enter to continue...")


# Admin User Management Functions

def view_all_users():
    """Display all users in the system."""
    try:
        # Connect to the database and fetch all users
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT UserId, username, email, RoleTypeId, Consent FROM [User]")
        users = cursor.fetchall()
        conn.close()

        print(f"\n{'UserId':<10}{'Username':<20}{'Email':<30}{'RoleType':<10}{'Consent':<10}")
        print("-" * 80)
        for user in users:
            role = "Admin" if user.RoleTypeId == 7 else "User"  # Check role type
            consent = "Yes" if user.Consent == 1 else "No"  # Check consent status
            print(f"{user.UserId:<10}{user.username:<20}{user.email:<30}{role:<10}{consent:<10}")
        input("\nPress Enter to return...")
    except pyodbc.Error as e:
        print(f"\nDatabase error: {e}")
        input("\nPress Enter to return...")


def search_user():
    """Search for a specific user."""
    search_term = input("Enter username or email to search: ").strip()
    try:
        # Search for a user by username or email
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT UserId, username, email, RoleTypeId, Consent 
            FROM [User] 
            WHERE username LIKE ? OR email LIKE ?
        """, f"%{search_term}%", f"%{search_term}%")
        users = cursor.fetchall()
        conn.close()

        if users:
            # Display the found users
            print(f"\n{'UserId':<10}{'Username':<20}{'Email':<30}{'RoleType':<10}{'Consent':<10}")
            print("-" * 80)
            for user in users:
                role = "Admin" if user.RoleTypeId == 7 else "User"
                consent = "Yes" if user.Consent == 1 else "No"
                print(f"{user.UserId:<10}{user.username:<20}{user.email:<30}{role:<10}{consent:<10}")
        else:
            print("\nNo users found.")  # Display message if no users are found
        input("\nPress Enter to return...")
    except pyodbc.Error as e:
        print(f"\nDatabase error: {e}")
        input("\nPress Enter to return...")


def edit_user():
    """Edit details of a specific user."""
    user_id = input("Enter UserId of the user to edit: ").strip()
    try:
        # Connect to the database and fetch user details to edit
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Check if the user exists in the database
        cursor.execute("SELECT UserId FROM [User] WHERE UserId = ?", user_id)
        user = cursor.fetchone()

        # If the user is not found, raise an error
        if not user:
            print(f"\nError: User with UserId {user_id} not found.")
            input("\nPress Enter to return...")
            conn.close()
            return

        print("\nLeave fields blank to keep current values.")
        new_username = input("Enter new username: ").strip()
        new_email = input("Enter new email: ").strip()
        new_role = input("Enter new role type (7 for Admin, 8 for User): ").strip()
        new_consent = input("Enter consent (1 for Yes, 0 for No): ").strip()

        # Validate RoleTypeId
        if new_role and new_role not in ['7', '8']:
            print("\nError: Invalid role type. Role type must be '7' for Admin or '8' for User.")
            input("\nPress Enter to return...")
            conn.close()
            return

        # Update fields if new values are provided
        if new_username:
            cursor.execute("UPDATE [User] SET username = ? WHERE UserId = ?", new_username, user_id)
        if new_email:
            cursor.execute("UPDATE [User] SET email = ? WHERE UserId = ?", new_email, user_id)
        if new_role:
            cursor.execute("UPDATE [User] SET RoleTypeId = ? WHERE UserId = ?", new_role, user_id)
        if new_consent:
            cursor.execute("UPDATE [User] SET Consent = ? WHERE UserId = ?", new_consent, user_id)

        conn.commit()
        conn.close()
        print("\nUser details updated successfully.")
        input("\nPress Enter to return...")
    except pyodbc.Error as e:
        print(f"\nDatabase error: {e}")
        input("\nPress Enter to return...")


def delete_user():
    """Delete a specific user."""
    user_id = input("Enter UserId of the user to delete: ").strip()

    try:
        # Connect to the database and check if the user is an admin
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT UserId, RoleTypeId FROM [User] WHERE UserId = ?", user_id)
        user = cursor.fetchone()

        # If user not found, raise an error
        if not user:
            print(f"\nError: User with UserId {user_id} not found.")
            input("\nPress Enter to return...")
            conn.close()
            return
        
        # Check if the user is an admin (RoleTypeId == 7)
        if user[1] == 7:  # 7 is for Admin
            print("\nError: Admin users cannot delete their own account.")
            input("\nPress Enter to return...")
            conn.close()
            return

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete user {user_id}? Type 'yes' to confirm: ").strip().lower()
        if confirm != "yes":
            print("\nDeletion canceled.")
            input("\nPress Enter to return...")
            conn.close()
            return

        # Proceed with deletion
        cursor.execute("DELETE FROM [User] WHERE UserId = ?", user_id)
        conn.commit()
        conn.close()

        print("\nUser deleted successfully.")
        input("\nPress Enter to return...")

    except pyodbc.Error as e:
        print(f"\nDatabase error: {e}")
        input("\nPress Enter to return...")
