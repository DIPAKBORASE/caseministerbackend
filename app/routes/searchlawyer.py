from flask import Blueprint, jsonify, request
from ..models.models import Lawyer

search_bp = Blueprint('search', __name__)

@search_bp.route('/search-lawyers', methods=['GET'])
def search_lawyers():
    try:
        # Get query parameters from the request
        data = request.json
        legal_issue = data.get('legal_issue')
        city = data.get('city')

        if not legal_issue or not city:
            return jsonify({"error": "Please provide both legal_issue and city parameters"}), 400

        # Query the database to find matching lawyers
        matching_lawyers = Lawyer.query.filter(
        Lawyer.practice_area.ilike(f"%{legal_issue}%"),
        Lawyer.state.ilike(f"%{city}%")
    ).all()


        # Prepare the response data
        lawyers_data = []
        for lawyer in matching_lawyers:
            lawyer_info = {
                "id": lawyer.id,
                "full_name": lawyer.full_name,
                "username": lawyer.username,
                "state": lawyer.state,
                "practice_area": lawyer.practice_area,
                
                # Add any other relevant fields you want to include
            }
            lawyers_data.append(lawyer_info)

        return jsonify({"lawyers": lawyers_data}), 200

    except Exception as e:
        # Log the general exception for debugging purposes
        print(f"An error occurred during search: {str(e)}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
