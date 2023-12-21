from flask import Blueprint, jsonify, send_file
from ..models.models import User, Lawyer # Adjust the import path based on your project structure
import io

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile/image/<int:user_id>', methods=['GET'])
def get_profile_image(user_id):
    # Retrieve the User from the database using user_id
    user = Lawyer.query.get(user_id)

    if user:
        if user.profile_image:
            # Return the image data
            return send_file(
                io.BytesIO(user.profile_image),
                mimetype='image/png',
                as_attachment=True,
                download_name=f'{user.username}_profile.png'
            )
        else:
            return jsonify({"error": "User does not have a profile image"}), 404
    else:
        return jsonify({"error": "User not found"}), 404
