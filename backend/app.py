from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from auth import auth_bp
from user import user_bp
from resume import resume_bp
from resume import get_resume_data

from db import init_db

app = Flask(__name__)

app.config.from_object('config.Config')

with app.app_context():
    init_db()

jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(resume_bp, url_prefix='/api/resume')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile_page():
    return render_template('user_profile.html')

@app.route('/resume/')
def resume():
    return render_template('resume.html')

@app.route('/resume/<int:resume_id>', methods=['GET'])
def get_resume_detail(resume_id):
    return render_template('resume_detail.html')

@app.route('/resume/preview/<int:resume_id>', methods=['GET'])
def get_resume_preview(resume_id):
    return render_template('resume_preview.html')


if __name__ == '__main__':
    app.run(debug=True)
