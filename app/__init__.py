# app/__init__.py

from flask import Flask
from flask_cors import CORS
from .models.user import db,User
from .routes.authentication_routes import auth_bp
from .routes.sendotp import sendotp_bp
from .routes.verifyotp import verifyotp_bp
from .routes.register import register_bp

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # Your database connection parameters
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/caseminister'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Import and register your blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(sendotp_bp, url_prefix='/api/auth')
    app.register_blueprint(verifyotp_bp, url_prefix='/api/auth')
    app.register_blueprint(register_bp, url_prefix='/api/auth')

    return app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
