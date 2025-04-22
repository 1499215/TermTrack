from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Flask App Setup
app = Flask(__name__)
CORS(app)

# Configurations
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/termtrack"  # Use your MySQL credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # For testing
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# ----------------------
# Database Models
# ----------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

class TermRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(100), nullable=False)
    term = db.Column(db.String(20), nullable=False)
    sba_score = db.Column(db.Float, nullable=False)
    eta_score = db.Column(db.Float, nullable=False)
    final_score = db.Column(db.Float, nullable=False)
    proficiency = db.Column(db.String(10), nullable=False)
    school_days = db.Column(db.Integer, default=0)

# ----------------------
# Routes
# ----------------------

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

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

    try:
        user = User.query.filter_by(email=data['email']).first()

        if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=user.email)
        return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/term-records', methods=['POST'])
@jwt_required()
def save_term_record():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        required_fields = ['studentId', 'sba', 'eta', 'term']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        final_score = float(data['sba']) * 0.3 + float(data['eta']) * 0.7
        proficiency = calculate_proficiency(final_score)

        new_record = TermRecord(
            student_id=data['studentId'],
            teacher_id=current_user,
            term=data['term'],
            sba_score=data['sba'],
            eta_score=data['eta'],
            final_score=final_score,
            proficiency=proficiency,
            school_days=data.get('schoolDays', 0)
        )

        db.session.add(new_record)
        db.session.commit()

        return jsonify({
            "message": "Record saved successfully",
            "recordId": new_record.id
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Server error"}), 500

@app.route('/api/term-records', methods=['GET'])
def get_term_records():
    try:
        term_records = TermRecord.query.all()
        records = [{
            "id": record.id,
            "student_id": record.student_id,
            "teacher_id": record.teacher_id,
            "term": record.term,
            "sba_score": record.sba_score,
            "eta_score": record.eta_score,
            "final_score": record.final_score,
            "proficiency": record.proficiency,
            "school_days": record.school_days
        } for record in term_records]

        return jsonify(records), 200

    except Exception as e:
        return jsonify({"error": "Server error"}), 500

@app.route('/api/test', methods=['GET'])
def test():
    return {'message': 'Server is running!'}, 200

# ----------------------
# Helper Functions
# ----------------------

def calculate_proficiency(score):
    if score >= 80: return 'A'
    if score >= 75: return 'P'
    if score >= 70: return 'AP'
    if score >= 65: return 'D'
    return 'B'

# ----------------------
# Initialize Database
# ----------------------
with app.app_context():
    db.create_all()

# ----------------------
# Run App
# ----------------------
if __name__ == '__main__':
    print("Available Routes:")
    print(app.url_map)
    app.run(debug=True, port=5000)
