from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, and_, func

from ..extensions import db
from ..models import User, PrivateMessage, BlockedUser

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')


def get_unread_count(user_id):
    return PrivateMessage.query.filter_by(
        recipient_id=user_id,
        is_read=False
    ).count()


@messages_bp.route('/')
@login_required
def inbox():
    subquery = db.session.query(
        func.max(PrivateMessage.id).label('max_id'),
        db.case(
            (PrivateMessage.sender_id == current_user.id, PrivateMessage.recipient_id),
            else_=PrivateMessage.sender_id
        ).label('other_user_id')
    ).filter(
        or_(
            PrivateMessage.sender_id == current_user.id,
            PrivateMessage.recipient_id == current_user.id
        )
    ).group_by('other_user_id').subquery()

    conversations = db.session.query(
        PrivateMessage,
        User
    ).join(
        subquery,
        PrivateMessage.id == subquery.c.max_id
    ).join(
        User,
        User.id == subquery.c.other_user_id
    ).order_by(PrivateMessage.timestamp.desc()).all()

    conversation_list = []
    for msg, user in conversations:
        unread = PrivateMessage.query.filter_by(
            sender_id=user.id,
            recipient_id=current_user.id,
            is_read=False
        ).count()
        conversation_list.append({
            'user': user,
            'last_message': msg,
            'unread_count': unread
        })

    return render_template(
        'messages/inbox.html',
        conversations=conversation_list,
        total_unread=get_unread_count(current_user.id)
    )


@messages_bp.route('/conversation/<int:user_id>')
@login_required
def conversation(user_id):
    other_user = User.query.get_or_404(user_id)
    
    if other_user.id == current_user.id:
        flash('Non puoi inviare messaggi a te stesso!', 'warning')
        return redirect(url_for('messages.inbox'))
    
    is_blocked_by = BlockedUser.query.filter_by(
        blocker_id=user_id, blocked_id=current_user.id
    ).first() is not None
    
    if is_blocked_by:
        flash('Non puoi inviare messaggi a questo utente.', 'danger')
        return redirect(url_for('messages.inbox'))

    messages = PrivateMessage.query.filter(
        or_(
            and_(
                PrivateMessage.sender_id == current_user.id,
                PrivateMessage.recipient_id == user_id
            ),
            and_(
                PrivateMessage.sender_id == user_id,
                PrivateMessage.recipient_id == current_user.id
            )
        )
    ).order_by(PrivateMessage.timestamp.asc()).all()

    PrivateMessage.query.filter_by(
        sender_id=user_id,
        recipient_id=current_user.id,
        is_read=False
    ).update({'is_read': True})
    db.session.commit()

    return render_template(
        'messages/conversation.html',
        other_user=other_user,
        messages=messages,
        total_unread=get_unread_count(current_user.id)
    )


@messages_bp.route('/send/<int:user_id>', methods=['POST'])
@login_required
def send_message(user_id):
    other_user = User.query.get_or_404(user_id)
    
    if other_user.id == current_user.id:
        return jsonify({'success': False, 'error': 'Non puoi inviare messaggi a te stesso'}), 400
    
    is_blocked = BlockedUser.query.filter(
        or_(
            and_(BlockedUser.blocker_id == current_user.id, BlockedUser.blocked_id == user_id),
            and_(BlockedUser.blocker_id == user_id, BlockedUser.blocked_id == current_user.id)
        )
    ).first() is not None
    
    if is_blocked:
        return jsonify({'success': False, 'error': 'Non puoi inviare messaggi a questo utente'}), 403

    content = request.form.get('content', '').strip()[:500]
    if not content:
        return jsonify({'success': False, 'error': 'Messaggio vuoto'}), 400

    message = PrivateMessage(
        sender_id=current_user.id,
        recipient_id=user_id,
        content=content
    )
    db.session.add(message)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': {
                'id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%H:%M'),
                'sender_id': message.sender_id
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Errore nel salvataggio'}), 500


@messages_bp.route('/new/<username>')
@login_required
def new_conversation(username):
    other_user = User.query.filter_by(username=username.lower()).first_or_404()
    return redirect(url_for('messages.conversation', user_id=other_user.id))


@messages_bp.route('/unread_count')
@login_required
def unread_count():
    count = get_unread_count(current_user.id)
    return jsonify({'count': count})
