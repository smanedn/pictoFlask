import os
import json
import secrets
from datetime import datetime, timezone

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import User, Message, PICTOFLASK_COLORS
from ..utils import allowed_file
import re

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    session['session_token'] = current_user.session_token

    # Load last 100 messages
    messages = Message.query.order_by(Message.timestamp.asc()).limit(100).all()
    
    # Get user colors for message history
    usernames = list(set(msg.username for msg in messages))
    users = User.query.filter(User.username.in_(usernames)).all()
    user_colors = {u.username: u.chat_color or '#61829a' for u in users}

    history_list = [
        {
            'username': msg.username,
            'msg': msg.content,
            'time': msg.timestamp.strftime("%H:%M"),
            'profile_pic': msg.profile_pic,
            'color': user_colors.get(msg.username, '#61829a')
        }
        for msg in messages
    ]

    history_json = json.dumps(history_list, ensure_ascii=False)

    return render_template(
        'index.html', 
        history_json=history_json,
        current_user_color=current_user.chat_color or '#61829a'
    )


@main_bp.route('/check_session')
@login_required
def check_session():
    if session.get('session_token') != current_user.session_token:
        return jsonify({'valid': False})
    return jsonify({'valid': True})


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    days_until_next_change = None
    if current_user.last_username_change:
        delta = datetime.now(timezone.utc) - current_user.last_username_change
        days_passed = delta.days
        days_until_next_change = max(0, 30 - days_passed)

    if request.method == 'POST':
        if 'new_username' in request.form:
            new_username = request.form['new_username'].strip().lower()
            if new_username == current_user.username:
                flash('Username uguale al precedente!', 'warning')
            elif not current_user.can_change_username():
                flash('Puoi cambiare username solo ogni 30 giorni!', 'danger')
            elif User.query.filter_by(username=new_username).first():
                flash('Username già preso!', 'danger')
            else:
                current_user.username = new_username
                current_user.last_username_change = datetime.now(timezone.utc)
                try:
                    db.session.commit()
                    flash('Username cambiato con successo!', 'success')
                except Exception as e:
                    db.session.rollback()
                    print(f"[ERRORE USERNAME CHANGE] {str(e)}")
                    flash("Errore durante l'aggiornamento.", 'danger')

        # Handle chat color change
        if 'chat_color' in request.form:
            new_color = request.form['chat_color'].strip()
            # Validate hex color
            if re.match(r'^#[0-9A-Fa-f]{6}$', new_color):
                current_user.chat_color = new_color
                try:
                    db.session.commit()
                    flash('Colore chat aggiornato!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash('Errore durante il salvataggio del colore.', 'danger')
            else:
                flash('Colore non valido!', 'danger')

        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file.filename == '':
                flash('Nessun file selezionato.', 'warning')
            elif file and allowed_file(file.filename):
                filename = secure_filename(
                    f"{current_user.id}_{secrets.token_hex(8)}.{file.filename.rsplit('.', 1)[1].lower()}"
                )
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                if current_user.profile_pic != 'default.jpg':
                    old = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_pic)
                    if os.path.exists(old):
                        os.remove(old)
                current_user.profile_pic = filename
                try:
                    db.session.commit()
                    flash('Foto profilo aggiornata!', 'success')
                except Exception as e:
                    db.session.rollback()
                    print(f"[ERRORE FOTO PROFILO] {str(e)}")
                    flash('Errore durante il salvataggio della foto.', 'danger')
            else:
                flash('Formato non valido (solo PNG/JPG)!', 'danger')

        return redirect(url_for('main.profile'))

    return render_template(
        'profile.html', 
        days_until_next_change=days_until_next_change,
        PICTOFLASK_COLORS=PICTOFLASK_COLORS
    )


@main_bp.route('/user/<username>')
@login_required
def public_profile(username):
    user = User.query.filter_by(username=username.lower()).first_or_404()
    is_own_profile = (user.id == current_user.id)

    days_until_next_change = None
    if user.last_username_change:
        delta = datetime.now(timezone.utc) - user.last_username_change
        days_passed = delta.days
        days_until_next_change = max(0, 30 - days_passed)

    return render_template(
        'public_profile.html',
        profile_user=user,
        is_own_profile=is_own_profile,
        days_until_next_change=days_until_next_change
    )


@main_bp.route('/uploads/profiles/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
