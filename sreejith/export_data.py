import csv
import os
import time
from db_connection import get_user_data, get_bookmarks, get_user_notifications, get_search_history  # Assuming these functions are implemented
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_csv(user_id, username):
    """Export user data to a CSV file."""
    try:
        # Fetch user data
        user_data = get_user_data(user_id)
        bookmarks = get_bookmarks(user_id)
        notifications = get_user_notifications(user_id)
        search_history = get_search_history(user_id)

        if not user_data:
            print(f"No data found for user {username}.")
            time.sleep(2)
            return
        
        # Prepare the CSV file path
        file_name = f"{username}_data_export.csv"
        file_path = os.path.join(os.getcwd(), file_name)
        
        # Open the CSV file for writing
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header (adjust columns based on your data structure)
            writer.writerow(["UserId", "Username", "Email", "Route", "Bookmark Date", "Notification Message", "Notification Date", "Search History ID"])
            
            # Iterate through each set of data and write it to the CSV
            for bookmark, notification, search in zip(bookmarks, notifications, search_history):
                writer.writerow([user_data[0],  # UserId
                                 user_data[1],  # Username
                                 user_data[2],  # Email
                                 bookmark[0],   # Route
                                 bookmark[1],   # DateAdded
                                 notification[0],  # Message
                                 notification[1],  # DateAdded
                                 search[0]        # SearchHistoryId
                ])
        
        print(f"Data exported successfully to {file_path}")
        time.sleep(2)
    
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")
        time.sleep(2)


def export_to_pdf(user_id, username):
    """Export user data to a PDF file."""
    try:
        # Fetch user data
        user_data = get_user_data(user_id)
        bookmarks = get_bookmarks(user_id)
        notifications = get_user_notifications(user_id)
        search_history = get_search_history(user_id)

        if not user_data:
            print(f"No data found for user {username}.")
            time.sleep(2)
            return
        
        # Prepare the PDF file path
        file_name = f"{username}_data_export.pdf"
        file_path = os.path.join(os.getcwd(), file_name)
        
        # Create a canvas to write the PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        
        # Title for the PDF
        c.setFont("Helvetica", 16)
        c.drawString(100, height - 100, f"Exported Data for {username}")
        
        # Set font for the body
        c.setFont("Helvetica", 12)
        
        # Add user data to the PDF
        y_position = height - 130
        c.drawString(100, y_position, f"User ID: {user_data[0]}")
        c.drawString(100, y_position - 20, f"Username: {user_data[1]}")
        c.drawString(100, y_position - 40, f"Email: {user_data[2]}")
        
        y_position -= 60
        
        # Add Bookmarks, Notifications, and Search History
        for bookmark, notification, search in zip(bookmarks, notifications, search_history):
            c.drawString(100, y_position, f"Route: {bookmark[0]} (Added: {bookmark[1]})")
            c.drawString(100, y_position - 20, f"Notification: {notification[0]} (Added: {notification[1]})")
            c.drawString(100, y_position - 40, f"Search History ID: {search[0]}")
            y_position -= 60
        
        # Save the PDF
        c.save()
        print(f"Data exported successfully to {file_path}")
        time.sleep(2)
    
    except Exception as e:
        print(f"An error occurred while exporting data: {e}")
        time.sleep(2)


def export_data(user_id, username):
    """Prompt user and export data in CSV or PDF format."""
    while True:
        print("\nExporting Data")
        print("1. Export My Data to CSV")
        print("2. Export My Data to PDF")
        print("3. Return to the User Menu")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            export_to_csv(user_id, username)
        elif choice == "2":
            export_to_pdf(user_id, username)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(2)
