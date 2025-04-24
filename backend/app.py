from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import json
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/termtrack'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# ----------------------
# Database Models
# ----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class TermRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(100), nullable=False)
    term = db.Column(db.String(50), nullable=False)
    sba_score = db.Column(db.Float, nullable=False)
    eta_score = db.Column(db.Float, nullable=False)
    final_score = db.Column(db.Float, nullable=False)
    proficiency = db.Column(db.String(10), nullable=False)
    school_days = db.Column(db.Integer, nullable=True)

# ----------------------
# Authentication Routes
# ----------------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Received data:", data)  # Debugging log

    if not all(key in data for key in ['school_name', 'email', 'password']):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 409

    try:
        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User(
            school_name=data['school_name'],
            email=data['email'],
            password=hashed_pw.decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify(access_token=access_token), 200


# new code added to handle yearand students details

# ----------------------
# Database Models for Year Details and Students
# ----------------------
class YearDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    class_population = db.Column(db.Integer, nullable=False)
    year_begins = db.Column(db.Date, nullable=False)
    circuit = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    subjects = db.Column(db.Text, nullable=False)  # JSON string of subjects
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female'), nullable=False)
    parent_number = db.Column(db.String(15), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    #created_at = db.Column(db.DateTime, default=db.func.current_timestamp())



# ----------------------
# Routes for Year Details
# ----------------------
@app.route('/api/save_year_details', methods=['POST'])
@jwt_required()
def save_year_details():
    data = request.get_json()

    # Validate required fields
    required_fields = ['class_name', 'class_population', 'year_begins', 'circuit', 'district', 'subjects']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Save year details to the database
        new_year_details = YearDetails(
            class_name=data['class_name'],
            class_population=data['class_population'],
            year_begins=data['year_begins'],
            circuit=data['circuit'],
            district=data['district'],
            subjects=json.dumps(data['subjects'])  # Convert subjects list to JSON
        )
        db.session.add(new_year_details)
        db.session.commit()
        return jsonify({"message": "Year details saved successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ----------------------
# Routes for Student Details
# ----------------------
@app.route('/api/save_student', methods=['POST'])
@jwt_required()
def save_student():
    data = request.get_json()
    print("Received data:", data)  # Debugging log

    # Validate required fields
    required_fields = ['student_id', 'name', 'gender', 'parent_number', 'dob']
    if not all(field in data for field in required_fields):
        print("Missing required fields")  # Debugging log
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Save student details to the database
        new_student = Student(
            student_id=data['student_id'],
            name=data['name'],
            gender=data['gender'],
            parent_number=data['parent_number'],
            dob=data['dob']
        )
        db.session.add(new_student)
        db.session.commit()
        print("Student saved successfully")  # Debugging log
        return jsonify({"message": "Student details saved successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ----------------------
# Database Initialization
# ----------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)