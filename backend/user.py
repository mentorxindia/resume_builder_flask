import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db
import json
import os
import sqlite3
import binascii

from flask import Blueprint, request, render_template, jsonify, redirect, url_for, g, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from werkzeug.utils import secure_filename

from image_util import save_base64_image



UPLOAD_FOLDER = 'static/uploads/profile'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

user_bp = Blueprint('user', __name__)

def generate_salt():
    return binascii.hexlify(os.urandom(16)).decode()

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    fullName = data.get('fullName')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    gender = data.get('gender')

    if not all([fullName, email, phone, password, gender]):
        return jsonify({'message': 'All fields are required.'}), 400
    
    salt = generate_salt()
    hashed_password = generate_password_hash(password + salt)

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO users (full_name, email, phone, password, salt, gender) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (fullName, email, phone, hashed_password, salt, gender))
        db.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 409
    except Exception as error:
        return jsonify({'message': f'Error {error}'}), 500
    finally:
        cursor.close()

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT u.id, u.full_name, u.password, u.salt, u.is_active, r.name AS role 
        FROM users u 
        JOIN user_roles r ON u.role_id = r.id 
        WHERE u.email = ?
    """, (email,))
    user = cursor.fetchone()

    if user:
        user_id, full_name, hashed_password, salt, is_active, role = user
        if check_password_hash(hashed_password, password + salt):
            if is_active:
                access_token = create_access_token(
                    identity=user_id,
                    additional_claims={
                        "sub": str(user_id),
                        "role": role
                    }
                )
                return jsonify({
                    "access_token": access_token,
                    "user": {
                        "full_name": full_name,
                        "email": email,
                        "role": role
                    }
                }), 200
            else:
                return jsonify({"message": "Account is deactivated. Contact Support"}), 403
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    else:
        return jsonify({"message": "User doesn't exist"}), 400


@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    token = request.headers.get('Authorization').split()[1]
    db = get_db()
    cursor = db.cursor()        
    cursor.execute('''
        INSERT INTO blacklist (token) VALUES (?)
        ''', (token,))
    db.commit()

    return jsonify({'message': 'Logged out successfully'}), 200

@user_bp.route('/deactivate_account', methods=['PATCH'])
@jwt_required()
def deactivate_account():
    user_id = get_jwt_identity()
    token = request.headers.get('Authorization').split()[1]

    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute('''
            UPDATE users
            SET is_active = ?
            WHERE id = ?
        ''', (False, user_id))
        
        cursor.execute('''
            INSERT INTO blacklist (token)
            VALUES (?)
        ''', (token,))
        
        db.commit()

        cursor.close()

        return jsonify({'message': 'Account deactivated successfully.'}), 200
    
    except Exception as e:
        db.rollback()
        print(f"Error deactivating account: {e}")
        return jsonify({'message': 'Failed to deactivate account.'}), 500

@user_bp.before_request
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

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_details():
    """
    Fetch details of the currently authenticated user.
    """
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    db = get_db()
    cursor = db.cursor()
    
    # Query to fetch user details
    cursor.execute("SELECT id, full_name, email, phone, gender, profile_image FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Map query result to a dictionary
    user_data = {
        "id": user[0],
        "full_name": user[1],
        "email": user[2],
        "phone": user[3],
        "gender": user[4],
        "profile_image": user[5] if user[5] else 'static/uploads/profile/default_profile.jpeg',
    }

    return jsonify(user_data), 200

@user_bp.route('/', methods=['PUT'])
@jwt_required()
def update_user_details():
    """
    Update details of the currently authenticated user.
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    full_name = data.get('full_name')
    email = data.get('email')
    phone = data.get('phone')
    gender = data.get('gender')
    profile_image_base64 = data.get('profile_image')

    if not full_name or not email:
        return jsonify({"error": "Full name and email are required"}), 400

    profile_image_path = None

    if profile_image_base64:
        profile_image_path = save_base64_image(profile_image_base64, user_id, UPLOAD_FOLDER)
        if not profile_image_path:
            return jsonify({"error": "Invalid image data or format"}), 400

    db = get_db()
    cursor = db.cursor()

    query = "UPDATE users SET full_name = ?, email = ?, phone = ?, gender = ?"
    params = [full_name, email, phone, gender]

    if profile_image_path:
        query += ", profile_image = ?"
        params.append(profile_image_path)

    query += " WHERE id = ?"
    params.append(user_id)

    cursor.execute(query, tuple(params))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User details updated successfully"}), 200


@user_bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:
        return jsonify({"message": "Old and new password are required"}), 400

    user_id = get_jwt_identity()
    db = get_db()
    cursor = db.cursor()

    # Get the stored hashed password and salt for the logged-in user
    cursor.execute("SELECT password, salt FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    current_hashed_password, salt = user

    # Verify current hashed password with current_password + salt
    if not check_password_hash(current_hashed_password, current_password + salt):
        return jsonify({"message": "Old password is incorrect"}), 401

    # Hash new password with existing salt
    hashed_new_password = generate_password_hash(new_password + salt)

    # Update new hashed password in database
    cursor.execute("UPDATE users SET password = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (hashed_new_password, user_id))
    db.commit()

    return jsonify({"message": "Password updated successfully"}), 200


# @user_bp.route('/request_password_reset', methods=['POST'])
# def request_password_reset():
#     data = request.get_json()
#     email = data.get("email")

#     if not email:
#         return jsonify({"message": "Email is required"}), 400

#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
#     user = cursor.fetchone()

#     if not user:
#         return jsonify({"message": "User not found"}), 404

#     reset_token = create_access_token(identity=user["id"], expires_delta=datetime.timedelta(hours=1))

#     reset_link = f"http://localhost:5001/reset_password?token={reset_token}"

#     msg = Message("Password Reset Request",
#                   sender="noreply@yourapp.com",
#                   recipients=[email])
#     msg.body = f"Click the link to reset your password: {reset_link}"
    
#     mail.send(msg)

#     return jsonify({"message": "Password reset link sent to email"}), 200


# @user_bp.route('/reset-password', methods=['POST'])
# @jwt_required()
# def reset_password():
#     data = request.get_json()
#     new_password = data.get("new_password")

#     if not new_password:
#         return jsonify({"message": "New password is required"}), 400

#     # Get user ID from token
#     user_id = get_jwt_identity()

#     # Generate new salt and hash new password
#     new_salt = generate_salt()
#     hashed_new_password = generate_password_hash(new_password + new_salt)

#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("UPDATE users SET password = ?, salt = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", 
#                    (hashed_new_password, new_salt, user_id))
#     db.commit()

#     return jsonify({"message": "Password has been reset successfully"}), 200

