from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

# Configure DB
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "termtrack"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

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
