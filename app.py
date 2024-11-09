import os
from flask import Flask, jsonify
import random
import string

app = Flask(__name__)

# In-memory storage for temporary emails (for demonstration only)
temp_emails = {}

def generate_random_email():
    # Generates a random email address with a random username and a .edu domain
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    email = f"{username}@tempmail.edu"
    temp_emails[email] = {"messages": []}
    return email

@app.route('/create_temp_email', methods=['GET'])
def create_temp_email():
    email = generate_random_email()
    return jsonify({"temp_email": email})

@app.route('/get_messages/<email>', methods=['GET'])
def get_messages(email):
    # Returns messages for a given temporary email
    if email in temp_emails:
        return jsonify(temp_emails[email]["messages"])
    else:
        return jsonify({"error": "Email not found"}), 404

@app.route('/send_message/<email>', methods=['POST'])
def send_message(email):
    # Simulates receiving an email message
    if email in temp_emails:
        message = {"subject": "Test Message", "content": "This is a test email content."}
        temp_emails[email]["messages"].append(message)
        return jsonify({"message": "Message sent."})
    else:
        return jsonify({"error": "Email not found"}), 404

if __name__ == '__main__':
    # Use environment variable for the port, or default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
