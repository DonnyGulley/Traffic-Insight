# forgot_password.py
import time
from db_connection import validate_user, reset_password
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import clear_screen  # Import clear_screen from utils.py

def send_email(to_email, subject, body):
    """Send email for forgot password."""
    from_email = "your_email@example.com"  # Your email
    from_password = "your_email_password"  # Your email password

    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()  # Secure the connection
        server.login(from_email, from_password)

        # Send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()

        print(f"Verification email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def forgot_password_screen():
    """Handle the forgot password functionality."""
    clear_screen()  # Clear the screen at the beginning
    print("=" * 50)
    print(" " * 10 + "Forgot Password")
    print("=" * 50)

    username = input("Enter your username: ").strip()
    email = input("Enter your email: ").strip()
    password = input("Enter your old password: ").strip()
    # Check if user exists and email matches
    user = validate_user(username,password)
    while True:
        if user[1] == username and user[2].decode('utf-8').rstrip('\x00')== password and user[3] == email:
            new_password = input("Enter your new password: ").strip()
            temp_password = input("Enter your new password again: ").strip()
        
            if new_password == temp_password:
                # Update password in the database
                if reset_password(username, new_password):
                    print(f"\nPassword for {username} has been updated successfully!")
                    time.sleep(2)
                    subject = "Password Reset Notification"
                    body = f"Hello {username},\n\nYour password has been reset successfully."
                    send_email(email, subject, body)  # Send email notification
                    break
                else:
                    print(f"\nError: Could not update password for {username}.")
                    time.sleep(2)
                    break

            break   
        else:
            print("\nError: User not found.")
            choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
            if choice == "exit":
                print("Returning to main menu...")
                time.sleep(2)
                clear_screen()  # Clear screen after 2 seconds
                return  
