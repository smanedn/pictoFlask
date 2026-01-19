from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from ..extensions import db
from ..models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password'].strip()

        if not username or not password:
            flash('Compila tutti i campi!', 'danger')
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
        username = request.form['username'].strip().lower()
        password = request.form['password'].strip()

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
