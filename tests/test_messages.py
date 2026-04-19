from app.models import PrivateMessage, User, BlockedUser
from app.extensions import db

def test_messages_inbox(auth_client):
    client, user = auth_client
    response = client.get('/messages/')
    assert response.status_code == 200
    assert b'Messaggi Privati' in response.data

def test_conversation_view(auth_client, init_database):
    client, current_user = auth_client
    _, user2, _ = init_database
    
    # Send a message to user2
    msg = PrivateMessage(sender_id=current_user.id, recipient_id=user2.id, content='Hello!')
    db.session.add(msg)
    db.session.commit()
    
    response = client.get(f'/messages/conversation/{user2.id}')
    assert response.status_code == 200
    assert b'Hello!' in response.data
    assert user2.username.encode() in response.data

def test_send_message_post(auth_client, init_database):
    client, current_user = auth_client
    _, user2, _ = init_database
    
    response = client.post(f'/messages/send/{user2.id}', data={
        'content': 'Test message'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    with client.application.app_context():
        msg = PrivateMessage.query.filter_by(sender_id=current_user.id, recipient_id=user2.id).first()
        assert msg is not None
        assert msg.content == 'Test message'

def test_cannot_send_empty_message(auth_client, init_database):
    client, current_user = auth_client
    _, user2, _ = init_database
    
    response = client.post(f'/messages/send/{user2.id}', data={
        'content': '    '
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_sendMessage_to_blocked_user(auth_client, init_database):
    client, current_user = auth_client
    _, user2, _ = init_database
    
    # Block user2
    db.session.add(BlockedUser(blocker_id=current_user.id, blocked_id=user2.id))
    db.session.commit()
    
    response = client.post(f'/messages/send/{user2.id}', data={
        'content': 'Test message'
    })
    
    assert response.status_code == 403
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data
