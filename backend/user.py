import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db

user_bp = Blueprint('user', __name__)

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
    cursor.execute("SELECT id, full_name, email, phone, gender FROM users WHERE id = ?", (user_id,))
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
    }

    return jsonify(user_data), 200

@user_bp.route('/', methods=['PUT'])
@jwt_required()
def update_user_details():
    """
    Update details of the currently authenticated user.
    """
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    data = request.get_json()  # Get the updated user data

    # Extract updated fields
    full_name = data.get('full_name')
    email = data.get('email')
    phone = data.get('phone')
    gender = data.get('gender')

    # Validate input
    if not full_name or not email:
        return jsonify({"error": "FullName and email are required"}), 400

    db = get_db()
    cursor = db.cursor()

    # Update the user details in the database
    cursor.execute(
        "UPDATE users SET full_name = ?, email = ?, phone = ?, gender = ? WHERE id = ?",
        (full_name, email, phone, gender, user_id)
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User details updated successfully"}), 200

@user_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Handle forgot password functionality by sending a reset link or token.
    """
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    db = get_db()
    cursor = db.cursor()

    # Check if the email exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Email not found"}), 404

    # Generate a password reset token (in a real app, you'd send this via email)
    reset_token = "reset-token-placeholder"  # Replace with actual token generation logic

    # TODO: Implement email sending functionality
    return jsonify({"message": "Password reset link sent", "reset_token": reset_token}), 200

@user_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset the user's password using a token.
    """
    data = request.get_json()
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')

    if not reset_token or not new_password:
        return jsonify({"error": "Reset token and new password are required"}), 400

    # TODO: Validate reset token (implementation depends on token storage mechanism)

    db = get_db()
    cursor = db.cursor()

    # Assuming we fetch the user ID from the reset token
    user_id = 1  # Placeholder: Replace with user ID fetched using the token

    # Update the user's password
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "Password reset successfully"}), 200
