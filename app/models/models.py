from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    state = db.Column(db.String(100))
    profession = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Lawyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    state = db.Column(db.String(100))
    profession = db.Column(db.String(100))
    experience = db.Column(db.String(50))
    practice_area = db.Column(db.String(255))
    court_contactNo = db.Column(db.String(20))
    dob = db.Column(db.Date)
    profile_image = db.Column(db.LargeBinary)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    barcode_number = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text,nullable=True)
    language = db.Column(db.String(50), nullable=True)


    def __repr__(self):
        return f"<Lawyer {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserCases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), unique=True)

class LawyerCases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyer.id'))
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), unique=True)

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnr_number = db.Column(db.String(50), nullable=False)
    case_name = db.Column(db.String(255), nullable=False)
    case_description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    next_hearing = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    latest_update = db.Column(db.Text)
    lawyer_assigned = db.Column(db.String(255))
