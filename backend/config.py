import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv('dev.env')

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'dev')
    DEBUG = os.getenv('FLASK_ENV') != 'prod'

    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DATABASE = os.getenv('DATABASE', 'resume_builder')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # Flask-Mail configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your-email-password')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)