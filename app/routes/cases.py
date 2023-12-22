from flask import Blueprint, jsonify, request
from ..utils.database import get_db
from ..models.models import UserCases, Case, LawyerCases # Import your models

user_cases_bp = Blueprint('user_cases', __name__, url_prefix='/api/auth')

@user_cases_bp.route('/user_cases/<int:user_id>', methods=['GET'])
def get_user_cases(user_id):
    try:
        user_cases = UserCases.query.filter_by(user_id=user_id).all()
        cases_list = []

        for user_case in user_cases:
            case = Case.query.get(user_case.case_id)
            cases_list.append({
                'case_id': case.id,
                'case_name': case.case_name,
                'case_next_hearing': case.next_hearing,
                'case_description': case.case_description,
                'case_status':case.status,
                'case_start_date':case.start_date,
                'case_end_date':case.end_date,
                'case_latest_update':case.latest_update,
                'case_lawyer' : case.lawyer_assigned
                
                # Add other case details as needed
            })

        return jsonify({'user_cases': cases_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_cases_bp.route('/lawyer_cases/<int:lawyer_id>', methods=['GET'])
def get_lawyer_cases(lawyer_id):
    try:
        lawyer_cases = LawyerCases.query.filter_by(lawyer_id=lawyer_id).all()
        cases_list = []

        for lawyer_case in lawyer_cases:
            case = Case.query.get(lawyer_case.case_id)

            cases_list.append({
                'case_id': case.id,
                'case_name': case.case_name,
                'case_next_hearing': case.next_hearing,
                'case_description': case.case_description,
                'case_status':case.status,
                'case_start_date':case.start_date,
                'case_end_date':case.end_date,
                'case_latest_update':case.latest_update,
                'case_lawyer' : case.lawyer_assigned
                
                # Add other case details as needed
            })
        return jsonify({'lawyer_cases': cases_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500