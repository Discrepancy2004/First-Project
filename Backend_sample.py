from flask import Flask, request, jsonify
import os
from cryptography.fernet import Fernet
import csv

app = Flask(__name__)

# Utility functions (from above snippets)
def generate_key():
    key = Fernet.generate_key()
    with open('fileData/secret.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    return open('fileData/secret.key', 'rb').read()

def encrypt_data(data):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

def save_password(website, username, encrypted_password):
    os.makedirs('fileData', exist_ok=True)
    with open('fileData/passwords.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([website, username, encrypted_password])

def load_passwords():
    if not os.path.exists('fileData/passwords.csv'):
        return []
    with open('fileData/passwords.csv', 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader]

# Flask routes
@app.route('/check_strength', methods=['POST'])
def check_strength():
    data = request.json
    password = data.get('password')

    # Placeholder strength check


    is_strong = len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password)

    if is_strong:
        return jsonify({"strength": "strong"})
    else:
        recommendations = [
            "Use at least 8 characters.",
            "Include uppercase letters, numbers, and symbols.",
            "Avoid common words and repeated patterns."
        ]
        return jsonify({"strength": "weak", "recommendations": recommendations})

@app.route('/encrypt_password', methods=['POST'])
def encrypt_password():
    data = request.json
    password = data.get('password')
    encrypted_password = encrypt_data(password)
    return jsonify({"encrypted_password": encrypted_password.decode()})

# Ensure key exists
if not os.path.exists('fileData/secret.key'):
    generate_key()

if __name__ == '__main__':
    app.run(debug=True)
