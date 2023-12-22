from flask import Flask
from flask_cors import CORS
from .models.models import db, User, Lawyer
from .routes.authentication_routes import auth_bp
from .routes.fetchimage import user_bp
from .routes.sendotp import sendotp_bp
from .routes.verifyotp import verifyotp_bp
from .routes.register import register_bp
from .routes.cases import user_cases_bp
from .routes.searchlawyer import search_bp

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    password = 'Dipu@1234'.replace('@', '%40')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost/caseminister'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Import and register your blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/auth')
    app.register_blueprint(sendotp_bp, url_prefix='/api/auth')
    app.register_blueprint(verifyotp_bp, url_prefix='/api/auth')
    app.register_blueprint(register_bp, url_prefix='/api/auth')
    app.register_blueprint(user_cases_bp)
    app.register_blueprint(search_bp, url_prefix='/api/search')

    return app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
