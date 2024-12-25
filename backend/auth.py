import json
import sqlite3
from flask import Blueprint, request, render_template, jsonify, redirect, url_for, g, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from db import get_db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    fullName = data.get('fullName')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    gender = data.get('gender')

    if not all([fullName, email, phone, password, gender]):
        return jsonify({'message': 'All fields are required.'}), 400

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO users (full_name, email, phone, password, gender) 
            VALUES (?, ?, ?, ?, ?)
        ''', (fullName, email, phone, password, gender))
        db.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, full_name FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()

    if user:
        # Create JWT token with user ID as identity, and include `sub` (subject) claim if needed
        access_token = create_access_token(
            identity=user[0], 
            additional_claims={"sub": str(user[0])}  # Add the `sub` claim
        )
        
        return jsonify({'access_token': access_token, 'user': {'full_name': user[1], 'email': email}}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()  # Ensure JWT authentication for logout
def logout():
    token = request.headers.get('Authorization').split()[1]
    db = get_db()
    cursor = db.cursor()        
    cursor.execute('''
        INSERT INTO blacklist (token) VALUES (?)
        ''', (token,))
    db.commit()

    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.before_request
def check_blacklist():
    token = request.headers.get('Authorization')
    if token:
        token = token.split()[1]
        if _check_if_token_blacklisted(token):
            return jsonify({"message": "Token has been blacklisted. Please log in again."}), 401

def _check_if_token_blacklisted(token):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM blacklist WHERE token = ?', (token,))
    result = cursor.fetchone()
    return result is not None