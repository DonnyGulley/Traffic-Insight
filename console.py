from Business.business_access_layer import BusinessAccessLayer

bus = BusinessAccessLayer()   

def traffic_data():
     
     #user must be logged in and have proper access 


     while True:
        print('\nTraffic Collision Data ')    
        print('1. By Date')
        print('2. By Collision Type')
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
 

        elif choice == '5': 
            break
        else:
            print('Invalid choice. Please try again.')   

def login():
    pass

def admin():
    pass

def register():
    pass

# console = presentation layer      
def main_menu():
    while True:
        print('\nTransportation System ')
        print('1. Login')
        print('2.  User Registration')  # Add functionality or remove if not needed
        print('3.  Play with some Traffic data')  # Add functionality or remove if not needed
        print('4.  Admin')
        print('5. Exit')
        choice = input('Enter your choice: ')

        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '3':
            traffic_data()
        elif choice == '4':
            admin()
        elif choice == '5':  # Corrected to match the menu option
            break
        else:
            print('Invalid choice. Please try again.')

if __name__ == '__main__':
    main_menu()
