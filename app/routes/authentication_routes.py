from flask import Blueprint, jsonify, request
from ..utils.database import get_db
import bcrypt
from ..models.user import db, User

auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     db = get_db()
#     username = request.json.get('username')
#     password = request.json.get('password').encode('utf-8')  # Encode the password

#     if not username or not password:
#         return jsonify({"error": "Please provide username and password"}), 400

#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM user_table WHERE email = %s", (username,))
#     user_record = cursor.fetchone()
#     cursor.close()

#     if user_record:
#         hashed_password = user_record['password'].encode('utf-8')  # Encode the stored hash

#         if bcrypt.checkpw(password, hashed_password):  # Use bcrypt to compare passwords
#             return jsonify({"message": "Login successful", "username": username}), 200
#         else:
#             return jsonify({"error": "Invalid credentials"}), 401
#     else:
#         return jsonify({"error": "User not found"}), 404


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    full_name = data.get('full_name')
    username = data.get('username')
    state = data.get('state')
    profession = data.get('profession')
    email = data.get('email')
    password = data.get('password')

    if not full_name or not username or not state or not profession or not email or not password:
        return jsonify({"error": "Please provide all required fields"}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(
        full_name=full_name,
        username=username,
        state=state,
        profession=profession,
        email=email
    )

    if profession == 'lawyer':
        barcode_number = data.get('barcode_number')
        if barcode_number:
            new_user.barcode_number = barcode_number
        else:
            return jsonify({"error": "Please provide a barcode number for lawyers"}), 400

    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful", "username": username}), 201