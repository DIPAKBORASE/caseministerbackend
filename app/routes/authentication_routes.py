from flask import Blueprint, jsonify, request
from ..utils.database import get_db
import bcrypt
from ..models.models import db, User, Lawyer

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Please provide username and password"}), 400

        # Check if the user is a normal user
        normal_user = User.query.filter_by(username=username).first()

        # Check if the user is a lawyer
        lawyer = Lawyer.query.filter_by(username=username).first()

        if normal_user and normal_user.check_password(password):
          return jsonify({"message": "Login successful", "user_type": "normal_user", "user_id": normal_user.id, "username": username}), 200

        elif lawyer and lawyer.check_password(password):
           return jsonify({"message": "Login successful", "user_type": "lawyer", "user_id": lawyer.id, "username": username}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        # Log the general exception for debugging purposes
        print(f"An error occurred during login: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    full_name = data.get('full_name')
    username = data.get('username')
    state = data.get('state')
    profession = data.get('profession')
    email = data.get('email')
    password = data.get('password')

    if not full_name or not username or not state or not profession or not email or not password:
        return jsonify({"error": "Please provide all required fields"}), 400

    if profession not in ['user', 'client', 'lawyer']:
        return jsonify({"error": "Invalid profession"}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    if profession == 'lawyer':
        barcode_number = data.get('barcode_number')
        experience = data.get('experience')
        practice_area = data.get('practice_area')
        court_contactNo = data.get('court_contactNo')
        dob = data.get('dob')
        profile_image = request.files.get('profile_image').read()
        description = data.get('description')
        language = data.get('language')

        if not barcode_number or not experience or not practice_area or not court_contactNo or not dob or not profile_image:
            return jsonify({"error": "Please provide all required fields for lawyers"}), 400

        new_lawyer = Lawyer(
            full_name=full_name,
            username=username,
            state=state,
            email=email,
            barcode_number=barcode_number,
            experience=experience,
            practice_area=practice_area,
            court_contactNo=court_contactNo,
            dob=dob,
            profile_image=profile_image,
            profession=profession,
            description=description,
            language=language
        )
        new_lawyer.set_password(password)  # Hash the password

        db.session.add(new_lawyer)
        db.session.commit()

        # Retrieve the lawyer's ID after committing to the database
        user_id = new_lawyer.id
        user_type = "lawyer"

    else:
        new_user = User(
            full_name=full_name,
            username=username,
            state=state,
            email=email,
            profession=profession
        )
        new_user.set_password(password)  # Hash the password

        db.session.add(new_user)
        db.session.commit()

        # Retrieve the user's ID after committing to the database
        user_id = new_user.id
        user_type = "normal_user"  # You can customize this based on your needs

    return jsonify({"message": "Registration successful", "username": username, "user_id": user_id, "user_type": user_type}), 201
