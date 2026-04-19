from app.models import User, Message
from app.extensions import db

def test_admin_dashboard_nonadmin(auth_client):
    client, _ = auth_client
    response = client.get('/admin/')
    # auth_client is user1, not admin. Should 403 or redirect
    assert response.status_code == 403 or response.status_code == 302

def test_admin_dashboard_admin(admin_client):
    client, user = admin_client
    response = client.get('/admin/')
    assert response.status_code == 200
    assert b'ADMIN PANEL' in response.data

def test_admin_users_view(admin_client):
    client, _ = admin_client
    response = client.get('/admin/users')
    assert response.status_code == 200
    assert b'testuser1' in response.data

def test_admin_toggle_admin(admin_client, init_database):
    client, admin_user = admin_client
    user1, _, _ = init_database
    
    response = client.post(f'/admin/users/{user1.id}/toggle-admin', follow_redirects=True)
    assert response.status_code == 200
    
    with client.application.app_context():
        u1 = db.session.get(User, user1.id)
        assert u1.is_admin is True

def test_admin_delete_user(admin_client, init_database):
    client, admin_user = admin_client
    user1, user2, _ = init_database
    
    response = client.post(f'/admin/users/{user2.id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'eliminato!' in response.data
    
    with client.application.app_context():
        u = db.session.get(User, user2.id)
        assert u is None

def test_admin_messages_view(admin_client, init_database):
    client, _ = admin_client
    user1, _, _ = init_database
    
    # create a message
    msg = Message(user_id=user1.id, username=user1.username, content='Hello admin')
    db.session.add(msg)
    db.session.commit()
    
    response = client.get('/admin/messages')
    assert response.status_code == 200
    assert b'Hello admin' in response.data

def test_admin_delete_message(admin_client, init_database):
    client, _ = admin_client
    user1, _, _ = init_database
    
    # create a message
    msg = Message(user_id=user1.id, username=user1.username, content='Hello admin')
    db.session.add(msg)
    db.session.commit()
    msg_id = msg.id
    
    response = client.post(f'/admin/messages/{msg_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'eliminato!' in response.data
    
    with client.application.app_context():
        m = db.session.get(Message, msg_id)
        assert m is None
