import pyodbc
from db_connection import connection_string
from utils import clear_screen


def participate_in_survey(user_id):

    clear_screen()
    """Allow the user to participate in a survey."""
    print("=" * 50)
    print(" " * 15 + "Survey for System Improvement")
    print("=" * 50)

    # Sample survey questions
    questions = [
        "How satisfied are you with the system? (1-5)",
        "What features would you like to see in the future?",
        "Any additional comments or suggestions?"
    ]
    
    responses = []
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        for question in questions:
            print("\n" + question)
            answer = input("Your answer: ").strip()
            responses.append((user_id, question, answer))
        
        # Insert responses into the database
        for response in responses:
            cursor.execute("""
                INSERT INTO SurveyResponses (UserId, Question, Answer)
                VALUES (?, ?, ?)
            """, response)
        
        conn.commit()
        print("\nThank you for your feedback! Your responses have been recorded.")
    
    except pyodbc.Error as e:
        print(f"Database error: {e}")
    
    finally:
        conn.close()
