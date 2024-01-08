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

    if profession == 'lawyer':
        # Check if the username already exists in the Lawyer table
        existing_user = Lawyer.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400

        barcode_number = data.get('barcode_number')
        experience = data.get('experience')
        profile_image = request.files.get('profile_image').read()
        practice_area = data.get('practice_area')
        mobile_number = data.get('mobile_number')
        dob = data.get('dob')
        description = data.get('description')
        language = data.get('language')
        organisation = data.get('organisation')
        consultation_fees = data.get('consultation_fees')
        job_title = data.get('job_title')
        employername = data.get('employername')
        period_of_employment = data.get('period_of_employment')
        degree = data.get('degree')
        passing_year = data.get('passing_year')
        university = data.get('university')
        linkedin = data.get('linkedin')
        twitter = data.get('twitter')
        facebook = data.get('facebook')
        address = data.get('address')
        city = data.get('city')
        postal_code = data.get('postal_code')
        published_works = data.get('published_works')
        honors_and_awards = data.get('honors_and_awards')

        if not barcode_number or not experience or not practice_area or not mobile_number or not dob:
            return jsonify({"error": "Please provide all required fields for lawyers"}), 400

        new_lawyer = Lawyer(
            full_name=full_name,
            username=username,
            state=state,
            email=email,
            barcode_number=barcode_number,
            experience=experience,
            practice_area=practice_area,
            mobile_number=mobile_number,
            dob=dob,
            profile_image=profile_image,
            profession=profession,
            description=description,
            language=language,
            organisation=organisation,
            consultation_fees=consultation_fees,
            job_title=job_title,
            employername=employername,
            period_of_employment=period_of_employment,
            degree=degree,
            passing_year=passing_year,
            university=university,
            linkedin=linkedin,
            twitter=twitter,
            facebook=facebook,
            address=address,
            city=city,
            postal_code=postal_code,
            published_works=published_works,
            honors_and_awards=honors_and_awards
        )
        new_lawyer.set_password(password)  # Hash the password

        db.session.add(new_lawyer)
        db.session.commit()

        user_id = new_lawyer.id
        user_type = "lawyer"

    else:
        # Check if the username already exists in the User table
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400

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

        user_id = new_user.id
        user_type = "normal_user"

    return jsonify({"message": "Registration successful", "username": username, "user_type": user_type}), 201
    

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.json
        email = data.get('email')
        new_password = data.get('new_password')

        if not email or not new_password:
            return jsonify({"error": "Please provide email and new password"}), 400

        # Check if the user exists in the User table
        user = User.query.filter_by(email=email).first()

        if user:
            # Hash the new password before saving it
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_password
            db.session.commit()

            return jsonify({"message": "Password reset successful"}), 200

        # Check if the user exists in the Lawyer table
        lawyer = Lawyer.query.filter_by(email=email).first()

        if lawyer:
            # Hash the new password before saving it
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            lawyer.password = hashed_password
            db.session.commit()

            return jsonify({"message": "Password reset successful"}), 200

        # If the email is not found in either table
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500