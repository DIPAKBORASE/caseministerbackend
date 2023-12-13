# run.py

from flask import Flask
from flask_cors import CORS
import mysql.connector
from .utils.database import init_db

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Your database connection parameters
app.config['DB_HOST'] = "localhost"
app.config['DB_USER'] = "dipak@1"
app.config['DB_PASS'] = "dipak@123"
app.config['DB_NAME'] = "caseminister"

# Create a MySQL connector instance
conn = mysql.connector.connect(
    host=app.config['DB_HOST'],
    database=app.config['DB_NAME'],
    user=app.config['DB_USER'],
    password=app.config['DB_PASS']
)

# Initialize the database (if needed)
init_db(app, conn)  # Pass both app and conn to init_db

# Import and register your blueprints
from .routes.authentication_routes import auth_bp
from .routes.sendotp import sendotp_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(sendotp_bp, url_prefix='/api/auth')

# Any other configurations or setup code can go here

# Ensure that the app is run only when executed directly
if __name__ == '__main__':
    app.run(debug=True)
