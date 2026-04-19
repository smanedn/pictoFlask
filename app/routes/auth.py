import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from ..extensions import db
from ..models import User
from ..config import Config

auth_bp = Blueprint('auth', __name__)

# Allowed username pattern: letters, numbers, underscores only
_USERNAME_RE = re.compile(r'^[a-z0-9_]+$')


def _validate_username(username: str) -> str | None:
    """Return an error string if invalid, else None."""
    min_l = Config.USERNAME_MIN_LENGTH
    max_l = Config.USERNAME_MAX_LENGTH
    if len(username) < min_l:
        return f'Username troppo corto (minimo {min_l} caratteri).'
    if len(username) > max_l:
        return f'Username troppo lungo (massimo {max_l} caratteri).'
    if not _USERNAME_RE.match(username):
        return 'Username può contenere solo lettere, numeri e underscore.'
    return None


def _validate_password(password: str) -> str | None:
    """Return an error string if invalid, else None."""
    min_l = Config.PASSWORD_MIN_LENGTH
    if len(password) < min_l:
        return f'Password troppo corta (minimo {min_l} caratteri).'
    return None


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()

        # --- Validate inputs ---
        if not username or not password:
            flash('Compila tutti i campi!', 'danger')
            return redirect(url_for('auth.register'))

        err = _validate_username(username)
        if err:
            flash(err, 'danger')
            return redirect(url_for('auth.register'))

        err = _validate_password(password)
        if err:
            flash(err, 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Username già preso!', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username)
        user.set_password(password)
        user.refresh_session_token()
        db.session.add(user)
        try:
            db.session.commit()
            flash('Registrazione completata!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print(f"[ERRORE REGISTER] {str(e)}")
            flash('Errore durante la registrazione.', 'danger')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            user.refresh_session_token()
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"[ERRORE LOGIN COMMIT] {str(e)}")
                flash('Errore interno.', 'danger')
                return redirect(url_for('auth.login'))

            session['session_token'] = user.session_token
            login_user(user, remember=False)
            flash('Login effettuato!', 'success')
            return redirect(url_for('main.index'))
        flash('Credenziali errate.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    current_user.session_token = None
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"[ERRORE LOGOUT] {str(e)}")
    logout_user()
    session.clear()
    flash('Logout effettuato.', 'info')
    return redirect(url_for('auth.login'))
