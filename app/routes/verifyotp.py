from flask import Blueprint, jsonify, request
from ..utils.database import get_db
import datetime

verifyotp_bp = Blueprint('verifyotp', __name__)

@verifyotp_bp.route('/verifyotp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    user_otp = data.get('user_otp')

    if not email or not user_otp:
        return jsonify({"error": "Email and OTP are required"}), 400

    db = get_db()

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
                    with db.cursor() as delete_cursor:
                        delete_cursor.execute("DELETE FROM otp_table WHERE email = %s", (email,))
                        db.commit()
                    return jsonify({"message": "OTP verified"}), 200
                else:
                    return jsonify({"error": "Invalid or expired OTP"}), 401
            else:
                return jsonify({"error": "OTP not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error verifying OTP: {str(e)}"}), 500
