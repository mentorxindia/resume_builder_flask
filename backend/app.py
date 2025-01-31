import os
from flask import Flask, render_template, jsonify
from flask_jwt_extended import JWTManager
from user import user_bp
from resume import resume_bp
from resume import get_resume_data
from flask_cors import CORS, cross_origin
from flask_mail import Mail


from db import init_db

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})

app.config.from_object('config.Config')
mail = Mail(app)


with app.app_context():
    init_db()

jwt = JWTManager(app)



app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(resume_bp, url_prefix='/api/resume')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/user.html')

@app.route('/dashboard_admin')
def dashboard_admin():
    return render_template('dashboard/admin.html')

@app.route('/dashboard_support')
def dashboard_support():
    return render_template('dashboard/support.html')

@app.route('/user/profile')
def profile_page():
    return render_template('user/profile.html')

@app.route('/user/change_password', methods=['GET'])
def change_password():
    return render_template('user/change_password.html')


@app.route('/user/deactivate_account', methods=['GET'])
def deactivate_account():
    return render_template('user/deactivate_account.html')

@app.route('/resume/')
def resume():
    return render_template('resume/resumes.html')

@app.route('/resume/<int:resume_id>', methods=['GET'])
def get_resume_detail(resume_id):
    return render_template('resume/resume_detail.html')

@app.route('/resume/preview/<int:resume_id>', methods=['GET'])
def get_resume_preview(resume_id):
    return render_template('resume/resume_preview.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5001")
