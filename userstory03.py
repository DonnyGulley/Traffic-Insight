from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory database for demo purposes
# Replace with a real database like SQLite, MongoDB, etc.
tickets = {}

# Create a ticket
@app.route('/create_ticket', methods=['POST'])
def create_ticket():
    data = request.json
    ticket_id = str(uuid.uuid4())
    tickets[ticket_id] = {
        "title": data.get("title"),
        "description": data.get("description"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Open",
        "feedback": []
    }
    return jsonify({"message": "Ticket created successfully!", "ticket_id": ticket_id}), 201

# Add feedback to a ticket
@app.route('/add_feedback/<ticket_id>', methods=['POST'])
def add_feedback(ticket_id):
    if ticket_id not in tickets:
        return jsonify({"error": "Ticket not found"}), 404
    data = request.json
    feedback = {
        "comment": data.get("comment"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tickets[ticket_id]["feedback"].append(feedback)
    return jsonify({"message": "Feedback added successfully!"}), 200

# Get ticket details
@app.route('/get_ticket/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    if ticket_id not in tickets:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify(tickets[ticket_id]), 200

# List all tickets
@app.route('/list_tickets', methods=['GET'])
def list_tickets():
    return jsonify(tickets), 200

if __name__ == "__main__":
    app.run(debug=True)
