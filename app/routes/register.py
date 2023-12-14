from flask import Blueprint, jsonify, request
from ..utils.database import get_db
import datetime
import bcrypt  # Import bcrypt

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user_otp = data.get('user_otp')

    if not email or not user_otp or not password:
        return jsonify({"error": "Email, OTP, and password are required"}), 400

    db = get_db()

    # Verify OTP
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM otp_table WHERE email = %s", (email,))
            otp_record = cursor.fetchone()

            if otp_record:
                stored_otp = otp_record['otp']
                expiration = otp_record['expiration']

                if isinstance(expiration, str):
                    expiration = datetime.datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S.%f")

                current_time = datetime.datetime.now()

                if str(stored_otp) == str(user_otp) and current_time < expiration:
                    # OTP is valid, proceed to hash password and register user
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Hash the password
                    try:
                        with db.cursor() as user_cursor:
                            user_cursor.execute("INSERT INTO user_table (email, password) VALUES (%s, %s)", (email, hashed_password))
                            db.commit()  

                            # Optionally delete the OTP record
                            user_cursor.execute("DELETE FROM otp_table WHERE email = %s", (email,))
                            db.commit()

                        return jsonify({"message": "Registration successful"}), 201
                    except Exception as e:
                        db.rollback()  # Rollback in case of error
                        return jsonify({"error": f"Error during registration: {str(e)}"}), 500
                else:
                    return jsonify({"error": "Invalid or expired OTP"}), 401
            else:
                return jsonify({"error": "OTP not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error verifying OTP: {str(e)}"}), 500
