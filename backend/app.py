import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Retry logic to connect to PostgreSQL
for i in range(10):
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="your_database",
            user="your_user1",
            password="your_password1"
        )
        cursor = conn.cursor()
        break
    except psycopg2.OperationalError:
        print("Database connection failed, retrying in 5 seconds...")
        time.sleep(5)
else:
    raise Exception("Failed to connect to the database after multiple attempts.")

@app.route('/api/data', methods=['GET'])
def get_data():
    cursor.execute("SELECT * FROM your_table")
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.get_json()
    name = data.get('name')
    if name:
        cursor.execute("INSERT INTO your_table (name) VALUES (%s) RETURNING id", (name,))
        new_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"id": new_id, "name": name}), 201
    return jsonify({"error": "Invalid input"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
