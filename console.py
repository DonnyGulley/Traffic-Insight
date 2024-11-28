from Business.business_access_layer import BusinessAccessLayer

bus = BusinessAccessLayer()   

def traffic_data():
    bus.PlotAccidents()

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
