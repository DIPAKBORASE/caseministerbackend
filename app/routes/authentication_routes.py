from flask import Blueprint, jsonify, request
from ..utils.database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    db = get_db()
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Please provide username and password"}), 400

    cursor = db.cursor(dictionary=True)  # Use the 'db' connection instead of 'conn'
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_record = cursor.fetchone()
    cursor.close()

    if user_record and user_record['password_hash'] == password:  # Fix the comparison
        return jsonify({"message": "Login successful", "username": username}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
