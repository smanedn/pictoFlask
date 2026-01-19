import os
import secrets

# Base directory of the project (parent of app/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///chat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'profiles')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
