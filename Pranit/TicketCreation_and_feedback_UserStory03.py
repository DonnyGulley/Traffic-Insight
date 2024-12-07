import uuid
from datetime import datetime

# In-memory database (dictionary to store tickets)
tickets = {}

# Function to create a ticket
def create_ticket(title, description):
    ticket_id = str(uuid.uuid4())  # Generate a unique ticket ID
    tickets[ticket_id] = {
        "title": title,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Open",
        "feedback": []
    }
    return ticket_id

# Function to add feedback to a ticket
def add_feedback(ticket_id, comment):
    if ticket_id in tickets:
        feedback = {
            "comment": comment,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        tickets[ticket_id]["feedback"].append(feedback)
        return f"Feedback added to ticket {ticket_id}"
    else:
        return f"Ticket ID {ticket_id} not found."

# Function to view a ticket
def view_ticket(ticket_id):
    if ticket_id in tickets:
        return tickets[ticket_id]
    else:
        return f"Ticket ID {ticket_id} not found."

# Function to list all tickets
def list_tickets():
    return tickets

# Example usage
if __name__ == "__main__":
    print("Welcome to the Ticket Management System!")

    # Create a ticket
    ticket_id = create_ticket(
        title="Traffic light not working",
        description="The traffic light at Main St & 5th Ave is malfunctioning."
    )
    print(f"Ticket created successfully! Ticket ID: {ticket_id}")

    # Add feedback to the ticket
    response = add_feedback(ticket_id, "Technician has been dispatched to the location.")
    print(response)

    # View the ticket details
    ticket_details = view_ticket(ticket_id)
    print("\nTicket Details:")
    for key, value in ticket_details.items():
        print(f"{key}: {value}")

    # List all tickets
    print("\nAll Tickets:")
    all_tickets = list_tickets()
    for tid, details in all_tickets.items():
        print(f"Ticket ID: {tid}")
        for key, value in details.items():
            print(f"  {key}: {value}")
