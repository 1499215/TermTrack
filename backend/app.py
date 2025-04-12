from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///termtrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# ----------------------
# Database Model
# ----------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

# ----------------------
# Authentication Routes
# ----------------------

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    if not all(key in data for key in ['school_name', 'email', 'password']):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 409
    
    try:
        # Hash password
        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Create new user
        new_user = User(
            school_name=data['school_name'],
            email=data['email'],
            password=hashed_pw.decode('utf-8')
        )
        
        # Add to database
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
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        # Validate credentials
        if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Create JWT token
        access_token = create_access_token(identity=user.email)
        return jsonify(access_token=access_token), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------
# Database Initialization
# ----------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)