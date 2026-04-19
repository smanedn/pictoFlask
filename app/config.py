import os
import secrets

# Base directory of the project (parent of app/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Config:
    # ── Core ────────────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    # ── Database ─────────────────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///chat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Uploads ──────────────────────────────────────────────────────────────
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'profiles')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024   # 2 MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # ── Session / Cookie security ─────────────────────────────────────────────
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Set to True only when served over HTTPS in production
    SESSION_COOKIE_SECURE = os.environ.get('HTTPS', 'false').lower() == 'true'

    # ── Password policy ──────────────────────────────────────────────────────
    PASSWORD_MIN_LENGTH = 6
    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 20
