from flask import Blueprint, jsonify, request
from ..utils.database import get_db
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    db = get_db()
    username = request.json.get('username')
    password = request.json.get('password').encode('utf-8')  # Encode the password

    if not username or not password:
        return jsonify({"error": "Please provide username and password"}), 400

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_table WHERE email = %s", (username,))
    user_record = cursor.fetchone()
    cursor.close()

    if user_record:
        hashed_password = user_record['password'].encode('utf-8')  # Encode the stored hash

        if bcrypt.checkpw(password, hashed_password):  # Use bcrypt to compare passwords
            return jsonify({"message": "Login successful", "username": username}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"error": "User not found"}), 404
