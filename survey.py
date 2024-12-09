import pyodbc
from db_connection import connection_string
from utils import clear_screen
import time

def participate_in_survey(user_id):
    """Allow the user to participate in a survey."""
    clear_screen()  # Clear the screen before displaying the survey
    print("=" * 50)
    print(" " * 15 + "Survey for System Improvement")  # Survey title
    print("=" * 50)

    # List of survey questions
    questions = [
        "How satisfied are you with the system? (1-5)",  # Numeric response expected
        "What features would you like to see in the future?",
        "Any additional comments or suggestions?"
    ]
    
    # List to store user responses
    responses = []

    try:
        # Establish connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Loop through each question and collect responses
        for question in questions:
            print("\n" + question)
            answer = input("Your answer: ").strip()  # Strip any leading/trailing whitespace
            
            # Validate the answer for the first question (satisfaction)
            if question == "How satisfied are you with the system? (1-5)":
                # Ensure the answer is numeric and within the range of 1 to 5
                while not answer.isdigit() or int(answer) < 1 or int(answer) > 5:
                    print("Invalid input. Please enter a number between 1 and 5 for your satisfaction rating.")
                    answer = input("Your answer: ").strip()
            
            # Check for empty answers in other questions
            if not answer:
                print("Answer cannot be empty. Please provide a response.")
                answer = input("Your answer: ").strip()

            responses.append((user_id, question, answer))  # Append valid response to the list

        # Insert each response into the SurveyResponses table in the database
        for response in responses:
            cursor.execute("""
                INSERT INTO SurveyResponses (UserId, Question, Answer)
                VALUES (?, ?, ?)
            """, response)
        
        # Commit changes to save the responses in the database
        conn.commit()
        print("\nThank you for your feedback! Your responses have been recorded.")
        time.sleep(2)

    except pyodbc.Error as e:
        # Handle any database-related errors
        print(f"Database error: {e}")
        time.sleep(2)
    finally:
        conn.close()  # Ensure the connection is closed after the operation


def view_survey_responses():
    """Allow the admin to view survey responses."""
    clear_screen()  # Clear the screen before displaying responses
    print("=" * 50)
    print(" " * 18 + "Survey Responses")  # Title for admin view
    print("=" * 50)

    try:
        # Establish connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # SQL query to fetch survey responses and join with the [User] table to get usernames
        cursor.execute("""
            SELECT SR.SurveyResponseId, U.username, SR.Question, SR.Answer, SR.DateSubmitted
            FROM SurveyResponses SR
            JOIN [User] U ON SR.UserId = U.UserId
            ORDER BY SR.DateSubmitted DESC
        """)

        # Fetch all responses from the database
        responses = cursor.fetchall()

        # Display the responses if available
        if responses:
            print(f"\n{'Response ID':<12}{'Username':<20}{'Question':<30}{'Answer':<30}{'Date Submitted'}")
            print("-" * 100)
            for response in responses:
                print(f"{response.SurveyResponseId:<12}{response.username:<20}{response.Question:<30}{response.Answer:<30}{response.DateSubmitted}")
        else:
            print("\nNo survey responses found.")
        
        input("\nPress Enter to return to the admin menu...")  # Pause for admin to view responses
    
    except pyodbc.Error as e:
        # Handle any database-related errors
        print(f"Database error: {e}")
        input("\nPress Enter to return to the admin menu...")  # Pause even in case of error
    
    finally:
        conn.close()  # Ensure the connection is closed after the operation
