import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
CORS(app)

# Retrieve database connection parameters from environment variables
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'devdb')  # Default to 'devdb' if not set

# Retry logic to connect to PostgreSQL
for i in range(10):
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )
        conn.autocommit = True
        cursor = conn.cursor()
        break
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}, retrying in 5 seconds...")
        time.sleep(5)
else:
    raise Exception("Failed to connect to the database after multiple attempts.")

# Initialize the database schema
def initialize_database():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS your_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)
    conn.commit()

initialize_database()

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
