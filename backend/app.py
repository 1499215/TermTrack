from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from dotenv import load_dotenv
import os
from flask_cors import CORS
import mysql.connector
import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from frontend
# Load environment variables
load_dotenv()

# Configure DB
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "termtrack"
}
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Initialize Flask app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/termtrack'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

#--------------------------#
#Login Code down here
# -------------------------#
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

#Login Authntication
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify(access_token=access_token), 200 

#Save year detail route
@app.route('/api/save_year_details', methods=['POST'])
def save_year_details():
    try:
        data = request.get_json()

        class_name = data['class_name']
        class_population = data['class_population']
        year_begins = data['year_begins']
        circuit = data['circuit']
        district = data['district']
        subject = data['subjectName']

        #subjectName = data['subjectName']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert class details
        cursor.execute('''
            INSERT INTO year_details (class_name, class_population, year_begins, circuit, district)
            VALUES (%s, %s, %s, %s, %s)
        ''', (class_name, class_population, year_begins, circuit, district))
        class_id = cursor.lastrowid

        # Insert subjects
        for subject in subject:
            cursor.execute('''
            INSERT INTO subjects (subjectName)
            VALUES (%s)
            ''', (subject,))


        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Class and subjects saved successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#Save Student Data
@app.route('/api/save_student', methods=['POST'])
def save_student():
    try:
        data = request.get_json()

        student_id = data['student_id']
        name = data['name']
        gender = data['gender']
        parent_number = data['parent_number']
        dob = data['dob']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO student (student_id, name, gender, parent_number, dob)
            VALUES (%s, %s, %s, %s, %s)
        ''', (student_id, name, gender, parent_number, dob))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Student saved successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#FEtch Student Data and Display it dynamically
@app.route('/api/get_student', methods=['GET'])
def get_student():
    try:
        # Get page and limit from query parameters (default: page=1, limit=10)
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch students with pagination
        cursor.execute(f"""
            SELECT student_id, name, gender, parent_number, DATE_FORMAT(dob, '%Y-%m-%d') as dob
            FROM student
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        students = cursor.fetchall()

        # Get total number of students for pagination metadata
        cursor.execute("SELECT COUNT(*) as total FROM student")
        total_students = cursor.fetchone()['total']

        cursor.close()
        conn.close()

        # Return students and pagination metadata
        return jsonify({
            "students": students,
            "total": total_students,
            "page": page,
            "limit": limit
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



if __name__ == '__main__':
    app.run(debug=True)
