from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'loca_pulse_db'

# Initialize MySQL
mysql = MySQL(app)

# Define routes

@app.route('/login', methods=['POST'])
def login():
    # Handle login request
    # Fetch user credentials from request
    data = request.get_json()
    phone = data['phone']
    password = data['password']

    # Query the database to validate user credentials
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE phone = %s AND password = %s", (phone, password))
    user = cur.fetchone()
    cur.close()

    if user:
        # User exists and credentials are correct
        return jsonify({'message': 'Login successful', 'user_id': user[0]}), 200
    else:
        # Invalid credentials
        return jsonify({'message': 'Invalid phone number or password'}), 401

@app.route('/lost-item', methods=['POST'])
def submit_lost_item():
    # Handle submission of lost item
    # Fetch item details from request
    data = request.get_json()
    category = data['category']
    description = data['description']
    date = data['date']
    location = data['location']
    image_url = data['image_url']

    # Insert item details into database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO lost_items (category, description, date, location, image_url) VALUES (%s, %s, %s, %s, %s)",
                (category, description, date, location, image_url))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Lost item submitted successfully'}), 200

# Add more routes as needed...

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
