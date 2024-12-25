import json
import sqlite3
from flask import Blueprint, request, render_template, jsonify, redirect, url_for, g, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from db import get_db


dashboard_bp = Blueprint('dashboard', __name__)

# @dashboard_bp.route('/', methods=['GET'])
# def dashboard():
#     return render_template('dashboard.html')