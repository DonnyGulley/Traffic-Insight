def display_help():
    """
    Function to display help options for the Traffic Insights console application.
    """
    print("\n=== Traffic Insights Help ===")
    print("Welcome to Traffic Insights! Below are the available features:")
    
    # Section: General Features
    print("\nGeneral Features:")
    print("1. View Traffic Data - Explore traffic statistics and trends.")
    print("2. Filter by Weather - Filter traffic data based on weather conditions.")
    print("3. Map Speed Limits - Visualize speed limits on a map.")
    print("4. Weekly Transit Reports - Analyze weekly transit usage trends.")
    print("5. Create Tickets - Report an issue and receive feedback.")

    # Section: User Features
    print("\nUser Features:")
    print("6. Participate in Surveys - Help improve the system by taking surveys.")
    print("7. Enter Location - Input your location for better insights.")
    print("8. Search Users by Location - Find other users based on location.")
    print("9. Login - Securely access your account.")
    print("10. Set Dark Mode - Enable a dark theme for the application.")
    print("11. Export Data - Download your traffic-related data.")
    print("12. Real-Time Notifications - Receive alerts for traffic incidents.")
    print("13. Collision Reporting - Access the Collision Reporting menu and features.")

    # Section: Admin Features
    print("\nAdmin Features:")
    print("14. Register and Login - Admin access to manage the system.")
    print("15. Activity Tracking - Monitor user activity in the system.")

    # Section: Automated Features
    print("\nAutomated Features:")
    print("16. Social Media Data - Collect traffic-related data from X (formerly Twitter).")
    print("17. Daily Collision ETL - Automatically extract, transform, and load collision data.")
    print("18. Dashboard Statistics - Gather and display statistics in a dashboard.")
    
    # Section: Advanced Data Insights
    print("\nAdvanced Data Insights:")
    print("19. Traffic Collision by Impact Type - View collision data by impact type.")
    print("20. Traffic Collision by Jurisdiction - View collision data by road jurisdiction.")
    print("21. Traffic Collision by Traffic Info - Analyze collisions based on traffic-related information.")

    # Section: System Features
    print("\nSystem Features:")
    print("22. Data Encryption - Ensures data security where applicable.")
    print("23. Offline Search - Search for people even without an internet connection.")
    print("24. Consent Management - Manage your consent for data collection and processing.")
    
    print("\nFor further assistance, contact our support at: support@trafficinsights.com")
    print("=============================\n")

# Simulate calling the help option
if __name__ == "__main__":
    while True:
        print("\nTraffic Insights Console")
        print("1. Help")
        print("2. Exit")
        user_input = input("Enter your choice (1/2): ")

        if user_input == "1":
            display_help()
        elif user_input == "2":
            print("Exiting Traffic Insights. Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")
