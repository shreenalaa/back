from flask import render_template, redirect, url_for, request, flash
from app import app, db, login_manager
from models import User, LostItem, FoundItem
from flask_login import login_user, logout_user, login_required

from app import app
from flask import render_template, request, redirect, url_for
from models import User
from flask_login import login_user, logout_user, current_user

# Define route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Define route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']
        user = User.query.filter_by(phone_number=phone_number).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid phone number or password')
    else:
        return render_template('login.html')

# Define route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        existing_user = User.query.filter_by(phone_number=phone_number).first()
        if existing_user:
            return render_template('register.html', error='User already exists')
        new_user = User(name=name, phone_number=phone_number)
        new_user.set_password(password)
        new_user.save()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

# Define route for the dashboard page
@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html', user=current_user)
    else:
        return redirect(url_for('login'))

# Define route for logging out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# routes.py

from flask import render_template, request, redirect, url_for
from app import app, db
from models import User

# Create a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Create a new user object
        new_user = User(username=username, email=email, password=password)
        
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Retrieve user information
@app.route('/user/<int:user_id>')
def user(user_id):
    user = User.query.get(user_id)
    return render_template('user.html', user=user)

# Update user information
@app.route('/user/<int:user_id>/update', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.password = request.form['password']
        
        db.session.commit()
        return redirect(url_for('user', user_id=user.id))
    
    return render_template('update_user.html', user=user)

# Delete a user
@app.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))
