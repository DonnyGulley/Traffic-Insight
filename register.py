import time
from db_connection import register_user
from utils import clear_screen


def register_screen():
    """Handle user registration."""
    clear_screen()
    print("=" * 50)
    print(" " * 10 + "Register New Account")
    print("=" * 50)

    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    email = input("Enter your email: ").strip()

    # Option to allow the user to create a custom security question
    print("\nDo you want to choose a predefined security question or create your own?")
    choice = input("Type 'predefined' for predefined questions or 'custom' to create your own: ").strip().lower()

    if choice == "predefined":
        # Provide a list of predefined security questions
        print("\nPlease choose a security question:")
        security_questions = [
            "What was the name of your first pet?",
            "What is the name of your favorite book?",
            "What is the name of the street you grew up on?",
            "What is your mother's maiden name?",
            "What was the name of your elementary school?",
            "What is your favorite color?",
            "In what city were you born?",
            "What was the name of your childhood friend?",
            "What is the name of your favorite movie?",
            "What was the make and model of your first car?"
        ]

        for idx, question in enumerate(security_questions, 1):
            print(f"{idx}. {question}")

        question_choice = input("\nEnter the number of your chosen security question: ").strip()
        try:
            question_index = int(question_choice) - 1
            if 0 <= question_index < len(security_questions):
                selected_question = security_questions[question_index]
                security_answer = input(f"Answer the security question: {selected_question} ").strip()
            else:
                print("Invalid selection. Please try again.")
                return
        except ValueError:
            print("Invalid input. Please try again.")
            return

    elif choice == "custom":
        selected_question = input("\nEnter your custom security question: ").strip()
        security_answer = input(f"Answer the security question: {selected_question} ").strip()
    else:
        print("Invalid choice. Please try again.")
        return

    print("\nDo you consent to the collection and processing of your data?")
    consent_choice = input("Type 'yes' to consent or 'no' to decline: ").strip().lower()

    consent = 1 if consent_choice == 'yes' else 0

    if register_user(username, password, email, consent, selected_question, security_answer):
        print(f"\nUser {username} has been successfully registered!")
    else:
        print(f"\nError: Could not register {username}. Please try again.")

        time.sleep(2)
        clear_screen()

    choice = input("Press Enter to try again or type 'exit' to quit: ").strip().lower()
    if choice == "exit":
        print("Returning to main menu...")
        time.sleep(2)
        clear_screen()  # Clear screen after 2 seconds
        return
