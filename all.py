from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_mysqldb import MySQL
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'loca_pulse'
mysql = MySQL(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, phone_number, password) VALUES (%s, %s, %s)", (name, phone_number, password))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password_entered = request.form['password']
        
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE phone_number = %s", [phone_number])
        
        if result > 0:
            user = cur.fetchone()
            password = user['password'].encode('utf-8')
            
            if bcrypt.checkpw(password_entered.encode('utf-8'), password):
                session['logged_in'] = True
                session['phone_number'] = phone_number
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid phone number or password')
        else:
            return render_template('login.html', error='User not found')
        
        cur.close()
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html', phone_number=session['phone_number'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/lost', methods=['GET', 'POST'])
def lost():
    if request.method == 'POST':
        # Handle form submission for lost items
        # Example: Save data to the database
        return redirect(url_for('dashboard'))
    return render_template('lost.html')

@app.route('/found', methods=['GET', 'POST'])
def found():
    if request.method == 'POST':
        # Handle form submission for found items
        # Example: Save data to the database
        return redirect(url_for('dashboard'))
    return render_template('found.html')

if __name__ == '__main__':
    app.run(debug=True)
