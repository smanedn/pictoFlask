from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from ..extensions import db
from ..models import User, Message

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to restrict access to admin users only."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard with stats."""
    user_count = User.query.count()
    message_count = Message.query.count()
    admin_count = User.query.filter_by(is_admin=True).count()
    
    # Recent users (last 5)
    recent_users = User.query.order_by(User.registered_on.desc()).limit(5).all()
    
    return render_template(
        'admin/dashboard.html',
        user_count=user_count,
        message_count=message_count,
        admin_count=admin_count,
        recent_users=recent_users
    )


@admin_bp.route('/users')
@admin_required
def users():
    """List all users with search/filter."""
    search = request.args.get('search', '').strip().lower()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = User.query
    if search:
        query = query.filter(User.username.contains(search))
    
    users_pagination = query.order_by(User.registered_on.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template(
        'admin/users.html',
        users=users_pagination.items,
        pagination=users_pagination,
        search=search
    )


@admin_bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    """Promote/demote user admin status."""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-demotion
    if user.id == current_user.id:
        flash('Non puoi modificare il tuo stato admin!', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    try:
        db.session.commit()
        action = 'promosso ad admin' if user.is_admin else 'rimosso da admin'
        flash(f'{user.username} è stato {action}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Errore durante l\'aggiornamento.', 'danger')
    
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-deletion
    if user.id == current_user.id:
        flash('Non puoi eliminare te stesso!', 'danger')
        return redirect(url_for('admin.users'))
    
    username = user.username
    try:
        # Delete user's messages
        Message.query.filter_by(username=username).delete()
        db.session.delete(user)
        db.session.commit()
        flash(f'Utente {username} eliminato!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Errore durante l\'eliminazione.', 'danger')
    
    return redirect(url_for('admin.users'))


@admin_bp.route('/messages')
@admin_required
def messages():
    """View all messages with pagination."""
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    query = Message.query
    if search:
        query = query.filter(
            (Message.username.contains(search.lower())) | 
            (Message.content.contains(search))
        )
    
    messages_pagination = query.order_by(Message.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template(
        'admin/messages.html',
        messages=messages_pagination.items,
        pagination=messages_pagination,
        search=search
    )


@admin_bp.route('/messages/<int:message_id>/delete', methods=['POST'])
@admin_required
def delete_message(message_id):
    """Delete a single message."""
    message = Message.query.get_or_404(message_id)
    
    try:
        db.session.delete(message)
        db.session.commit()
        flash('Messaggio eliminato!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Errore durante l\'eliminazione.', 'danger')
    
    return redirect(url_for('admin.messages'))
