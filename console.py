from Business.business_access_layer import BusinessAccessLayer
from Data.data_access_layer import DataAccessLayer
from Data.Databases.Script.db_intialize import get_db
from threading import Thread
from time import sleep

bus = BusinessAccessLayer()
dal = DataAccessLayer()

def traffic_data():
    #user must be logged in and have proper access 

    while True:
        print('\nTraffic Collision Data ')    
        print('1. By Date')
        print('2. By Collision Type')
        print('3. By Road Jurisdiction')
        print('4. By Traffic Condition')
        print('5. Dashboard')
        print('6. Exit')

        choice = input('Enter your choice: ')

        if choice == '1':
            input_start_date = input("Enter the start date (YYYY-MM-DD) or leave empty: ('2022-01-01' if ignored): ")
            if input_start_date == '' : input_start_date = '2022-01-01'

            input_end_date=input("Enter the end date (YYYY-MM-DD) or leave empty ('2019-01-01' if ignored): ")
            if input_end_date == '' : input_end_date = '2022-02-01'
            
            bus.plot_accidents_by_collisionDate(input_start_date,input_end_date)               
        elif choice=="2":
            # Define a dictionary to map impact type numbers to their corresponding names
            impact_types = {
                0: "Angle",
                1: "Approaching",
                2: "Other",
                3: "Rear end",
                4: "Sideswipe",
                5: "SMV other",
                6: "SMV unattended vehicle",
                7: "Turning movement"
            }

            # Get user input
            user_input = input("Enter the ID of the impact type (e.g. 0 for Angle, 1 for Approaching, 2 for Other, 3 for Rear end, 4 for Sideswipe, 5 for SMV other, 6 for SMV unattended vehicle, 7 for Turning movement): ")

            # Convert the input to an integer
            try:
                impact_type_id = int(user_input)
            except ValueError:
                print(f"Invalid ID: {user_input}")
                exit()

            # Get the corresponding name from the dictionary
            impact_type_name = impact_types.get(impact_type_id)

            if impact_type_name is not None:
                print(f"Collision Type: {impact_type_name}, Number: {impact_type_id}")
                bus.plot_accidents_by_impact_type(impact_type_id, impact_type_name)
            else:
                print(f"Invalid ID: {impact_type_id}")

        elif choice=="3":
            bus.plot_accidents_by_road_jurisdiction()
        
        elif choice=="4":
            bus.plot_accidents_by_traffic_condition()
        elif choice=="5":
            bus.create_dashboard()
        elif choice == '6': 
            break
        else:
            print('Invalid choice. Please try again.')   

def register():
    print("Registration feature coming soon...")
    pass

def login():
    """
    Simulated login functionality to authenticate a user.
    """
    print("\nLogin:")
    user_menu()

def admin():
    print("\nAdmin Menu:")
    print("1. View Activity Logs")
    choice = input("Enter your choice: ")

    if choice == "1":
        logs = bus.get_activity_logs()
        print("\nActivity Logs:")
        for log in logs:
            print(log.strip())
    else:
        print("Invalid choice, please try again ... or ...feature may not be implemented yet.")

def monitor_notifications(dal):
    """
    Monitors notifications for real-time updates in a separate thread.
    """
    def run_monitoring():
        while True:
            user_locations = dal.get_user_locations()
            for location in user_locations:
                notifications = dal.get_notifications_by_location(location)
                if notifications:
                    for note in notifications:
                        print(f"{note}")
                else:
                    print(f"{location}: No incidents nearby.")
            sleep(30)

    notification_thread = Thread(target=run_monitoring, daemon=True)
    notification_thread.start()
    print("\nNotification monitoring started in the background.")


def search_by_location():
    location = input("Enter the location to search for accidents: ")
    try:
        with next(get_db()) as db:
            results = dal.search_by_location(location)
        print("\n".join(results))
    except Exception as e:
        print(f"An error occurred: {e}")

def offline_search_menu():
    """
    Submenu for offline search functionality.
    """
    while True:
        print("\nOffline Search Menu:")
        print("1. Sync Accident Data and Search")
        print("2. Back to Main Menu")
        choice = input("Enter your choice: \n")

        if choice == "1":
            # Sync data and perform the offline search immediately
            sync_and_search()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")
        
        
def sync_and_search():
    """
    Sync accident data from the database and immediately prompt the user for an offline search.
    """
    try:
        # Sync data
        message = dal.cache_accident_data()
        print(message)

        # If successful, prompt for offline search
        if "successfully" in message.lower():
            location = input("Enter the location to search for accidents offline:")
            results = dal.offline_search(location)
            print("\n".join(results))
        else:
            print("Failed to sync data. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")


def offline_search():
    location = input("\nEnter the location to search for accidents offline: ")
    try:
        results = dal.offline_search(location)
        print("\n".join(results))
    except Exception as e:
        print(f"An error occurred: {e}")


def feedback_menu():
    print("\nFeedback Menu:")
    print("1. Add Feedback")
    print("2. Update Feedback")
    print("3. Search Feedback")
    choice = input("Enter your choice: ")

    if choice == "1":
        user_id = int(input("Enter your User ID: "))
        content = input("Enter your feedback: ")
        with next(get_db()) as db:
            message = bus.add_feedback(user_id, content, db)
        print(message)
    elif choice == "2":
        feedback_id = int(input("Enter Feedback ID to update: "))
        new_content = input("Enter the updated feedback: ")
        with next(get_db()) as db:
            message = bus.update_feedback(feedback_id, new_content, db)
        print(message)
    elif choice == "3":
        user_id = int(input("Enter User ID to search feedback for: "))
        with next(get_db()) as db:
            feedbacks = bus.search_feedback(user_id, db)
        if feedbacks:
            for feedback in feedbacks:
                print(f"Feedback ID: {feedback.id}, Content: {feedback.content}")
        else:
            print("No feedback found.")
    else:
        print("Invalid choice.")

def user_menu():
    """
    Displays the menu for logged-in users with appropriate features.
    """
    while True:
        # print(f"\nWelcome, {logged_in_user['username']}!")
        print(f"\nWelcome User!")
        print("1. Search by Location")
        print("2. Offline Search")
        print("3. Notifications")
        print("4. Feedback Menu")
        print("5. Logout")
        choice = input("Enter your choice: \n \n")

        if choice == "1":
            search_by_location()
        elif choice == "2":
            offline_search_menu()
        elif choice == "3":
            monitor_notifications(dal)
        elif choice == "4":
            feedback_menu()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

# console = presentation layer      
def main_menu():
    while True:
        print('\nTransportation System ')
        print('1. User Login')
        print('2. User Registration')  # Add functionality or remove if not needed
        print('3. Play with some Traffic data')  # Add functionality or remove if not needed
        print('4. Admin')
        print('5. User')
        print('6. Exit')
        choice = input('Enter your choice: ')

        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '3':
            traffic_data()
        elif choice == '4':
            admin()
        elif choice == '5':
            user_menu()
        elif choice == '6':  
            break
        else:
            print('Invalid choice. Please try again.')

if __name__ == '__main__':
    main_menu()