from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json

app = Flask(__name__)

# Simple in-memory store for encrypted passwords
passwords = {}
users = {"admin": generate_password_hash("adminpass")}  # Example user for authentication

def authenticate(username, password):
    """ Check if the provided username and password are valid. """
    user_password = users.get(username)
    return user_password and check_password_hash(user_password, password)

def requires_auth(f):
    """ Decorator to require authentication for certain routes. """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate(auth.username, auth.password):
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/add_password', methods=['POST'])
@requires_auth
def add_password():
    data = request.get_json()
    site = data.get('site')
    password = data.get('password')
    
    if not site or not password:
        return jsonify({"error": "Invalid input"}), 400

    # Encrypt the password before storing
    encrypted_password = generate_password_hash(password)
    passwords[site] = encrypted_password
    return jsonify({"message": "Password added successfully"}), 200

@app.route('/get_password', methods=['GET'])
@requires_auth
def get_password():
    site = request.args.get('site')
    encrypted_password = passwords.get(site)
    
    if encrypted_password:
        return jsonify({"site": site, "password": "Password is encrypted"}), 200
    else:
        return jsonify({"error": "Password not found"}), 404

@app.route('/list_passwords', methods=['GET'])
@requires_auth
def list_passwords():
    # Return only site names for privacy reasons
    return jsonify({"sites": list(passwords.keys())}), 200

if __name__ == '__main__':
    app.run(debug=True)
