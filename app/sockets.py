from datetime import datetime, timezone
from flask import session, request
from flask_socketio import emit, join_room
from flask_login import current_user, login_required

from .extensions import db, socketio
from .models import Message
from .utils import check_rate_limit

ROOM = "main_chat"

# Track online users: {sid: {username, profile_pic, color}}
online_users = {}


def get_online_users_list():
    """Get unique online users list"""
    seen = set()
    users = []
    for data in online_users.values():
        if data['username'] not in seen:
            seen.add(data['username'])
            users.append({
                'username': data['username'],
                'profile_pic': data['profile_pic'],
                'color': data['color']
            })
    return users


def broadcast_online_users():
    """Send updated online users list to all clients"""
    emit('online_users', {'users': get_online_users_list()}, room=ROOM)


@socketio.on('connect')
@login_required
def handle_connect():
    if session.get('session_token') != current_user.session_token:
        emit('kicked', {'msg': 'Login effettuato da altro dispositivo. Sessione terminata.'})
        return False

    join_room(ROOM)
    
    # Add user to online list
    online_users[request.sid] = {
        'username': current_user.username,
        'profile_pic': current_user.profile_pic,
        'color': current_user.chat_color or '#61829a'
    }
    
    emit('status', {'msg': f"{current_user.username} è entrato nella chat!"}, room=ROOM)
    broadcast_online_users()


@socketio.on('disconnect')
def handle_disconnect():
    # Remove user from online list
    if request.sid in online_users:
        username = online_users[request.sid]['username']
        del online_users[request.sid]
        emit('status', {'msg': f"{username} ha lasciato la chat."}, room=ROOM)
        broadcast_online_users()


@socketio.on('typing')
@login_required
def handle_typing(data):
    """Handle typing indicator"""
    is_typing = data.get('typing', False)
    emit('user_typing', {
        'username': current_user.username,
        'typing': is_typing
    }, room=ROOM, include_self=False)


@socketio.on('message')
@login_required
def handle_message(data):
    if not check_rate_limit(current_user.id):
        emit('status', {'msg': "Aspetta un attimo tra un messaggio e l'altro"}, to=request.sid)
        return

    msg = str(data.get('msg', '')).strip()[:500]
    if not msg:
        return

    current_user.message_count += 1

    new_message = Message(
        username=current_user.username,
        content=msg,
        profile_pic=current_user.profile_pic
    )
    db.session.add(new_message)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"[ERRORE SALVATAGGIO MSG] {str(e)}")
        emit('status', {'msg': 'Errore nel salvataggio del messaggio'}, to=request.sid)
        return

    emit('message', {
        'username': current_user.username,
        'msg': msg,
        'time': datetime.now(timezone.utc).strftime("%H:%M"),
        'profile_pic': current_user.profile_pic,
        'color': current_user.chat_color or '#61829a'
    }, room=ROOM)
