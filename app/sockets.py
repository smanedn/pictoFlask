from datetime import datetime, timezone
from flask import session, request
from flask_socketio import emit, join_room
from flask_login import current_user, login_required

from .extensions import db, socketio
from .models import Message, PrivateMessage
from .utils import check_rate_limit

ROOM = "main_chat"
online_users = {}
user_sid_map = {}


def get_online_users_list():
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
    emit('online_users', {'users': get_online_users_list()}, room=ROOM)


@socketio.on('connect')
@login_required
def handle_connect():
    if session.get('session_token') != current_user.session_token:
        emit('kicked', {'msg': 'Login effettuato da altro dispositivo. Sessione terminata.'})
        return False

    join_room(ROOM)
    join_room(f"user_{current_user.id}")
    
    online_users[request.sid] = {
        'username': current_user.username,
        'profile_pic': current_user.profile_pic,
        'color': current_user.chat_color or '#61829a',
        'user_id': current_user.id
    }
    user_sid_map[current_user.id] = request.sid
    
    emit('status', {'msg': f"{current_user.username} è entrato nella chat!"}, room=ROOM)
    broadcast_online_users()


@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in online_users:
        username = online_users[request.sid]['username']
        user_id = online_users[request.sid].get('user_id')
        del online_users[request.sid]
        if user_id and user_sid_map.get(user_id) == request.sid:
            del user_sid_map[user_id]
        emit('status', {'msg': f"{username} ha lasciato la chat."}, room=ROOM)
        broadcast_online_users()


@socketio.on('typing')
@login_required
def handle_typing(data):
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


@socketio.on('private_message')
@login_required
def handle_private_message(data):
    if not check_rate_limit(current_user.id):
        emit('pm_error', {'msg': "Aspetta un attimo tra un messaggio e l'altro"}, to=request.sid)
        return

    recipient_id = data.get('recipient_id')
    msg = str(data.get('msg', '')).strip()[:500]
    
    if not msg or not recipient_id:
        return

    new_pm = PrivateMessage(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        content=msg
    )
    db.session.add(new_pm)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        emit('pm_error', {'msg': 'Errore nel salvataggio del messaggio'}, to=request.sid)
        return

    message_data = {
        'id': new_pm.id,
        'sender_id': current_user.id,
        'sender_username': current_user.username,
        'sender_profile_pic': current_user.profile_pic,
        'content': msg,
        'timestamp': datetime.now(timezone.utc).strftime("%H:%M")
    }

    emit('pm_sent', message_data, to=request.sid)
    emit('pm_received', message_data, room=f"user_{recipient_id}")


def notify_private_message(recipient_id, sender_username):
    emit('pm_notification', {
        'sender': sender_username
    }, room=f"user_{recipient_id}", namespace='/')
