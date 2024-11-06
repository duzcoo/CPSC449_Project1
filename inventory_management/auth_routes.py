from flask import Blueprint, request, jsonify, session
from extensions import db, bcrypt
from models import User
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

# Register a new user
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create a new user
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

# Login a user
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    # Check if user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        session['user_id'] = user.id  # Store user ID in session
        return jsonify({'message': 'Logged in successfully!'}), 200

    return jsonify({'error': 'Invalid username or password'}), 401

# Logout a user
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()  # Logs the user out
    session.pop('user_id', None)  # Clear the session
    return jsonify({'message': 'Logged out successfully!'}), 200
