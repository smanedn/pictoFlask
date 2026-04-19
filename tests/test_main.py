from app.models import User, BlockedUser
from app.extensions import db

def test_index_unauthenticated(client):
    response = client.get('/')
    # Should redirect to login
    assert response.status_code == 302
    assert '/login' in response.headers.get('Location')

def test_index_authenticated(auth_client):
    client, user = auth_client
    response = client.get('/')
    assert response.status_code == 200
    assert user.username.encode() in response.data

def test_profile_view(auth_client):
    client, user = auth_client
    response = client.get('/profile')
    assert response.status_code == 200
    assert b'Profilo' in response.data

def test_profile_username_change(auth_client):
    client, user = auth_client
    response = client.post('/profile', data={
        'new_username': 'changed_user'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Username cambiato con successo!' in response.data
    
    with client.application.app_context():
        u = db.session.get(User, user.id)
        assert u.username == 'changed_user'

def test_public_profile(auth_client, init_database):
    client, current_user = auth_client
    _, user2, _ = init_database
    
    response = client.get(f'/user/{user2.username}')
    assert response.status_code == 200
    assert user2.username.encode() in response.data

def test_block_user(auth_client, init_database):
    client, current_user = auth_client
    _, user2, _ = init_database
    
    # Block user2
    response = client.post(f'/block/{user2.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'stato bloccato.' in response.data
    
    with client.application.app_context():
        block = BlockedUser.query.filter_by(blocker_id=current_user.id, blocked_id=user2.id).first()
        assert block is not None

def test_unblock_user(auth_client, init_database):
    client, current_user = auth_client
    _, user2, _ = init_database
    
    # Block first
    client.post(f'/block/{user2.id}')
    
    # Then unblock
    response = client.post(f'/unblock/{user2.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'stato sbloccato.' in response.data
    
    with client.application.app_context():
        block = BlockedUser.query.filter_by(blocker_id=current_user.id, blocked_id=user2.id).first()
        assert block is None
