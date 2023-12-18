import random
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, jsonify, request
from email.mime.text import MIMEText
from ..utils.database import get_db

sendotp_bp = Blueprint('sendotp', __name__)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "borasedipak18@gmail.com"  # Replace with your email
SMTP_PASSWORD = "wpzbdvlpxgcmqqjo"  # Replace with your app password

def generate_otp():
    return random.randint(100000, 999999)

def send_email(recipient, subject, body):
    try:
        # Setup email client
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)

@sendotp_bp.route('/sendotp', methods=['POST'])
def send_otp():
    email = request.json.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    db = get_db()

    # Check if the email already exists in user_table
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM user_table WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"error": "Email already exists"}), 409

    # If the email doesn't exist, proceed with sending OTP
    otp = generate_otp()

    email_subject = "Your OTP for Case Minister"
    email_body = f"Your OTP is: {otp}"
    send_email(email, email_subject, email_body)

    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

    with db.cursor() as cursor:
        cursor.execute("INSERT INTO otp_table (email, otp, expiration) VALUES (%s, %s, %s)",
                       (email, otp, expiration_time))

    db.commit()

    return jsonify({"message": "OTP sent to email"}), 200
