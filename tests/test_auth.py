from app.models import User
from app.extensions import db

def test_register_success(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'password123'
    }, follow_redirects=True)
    
    # After register it should redirect and say "Registrazione completata!"
    assert response.status_code == 200
    assert b'Registrazione completata!' in response.data
    
    with client.application.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None

def test_register_duplicate(client, init_database):
    response = client.post('/register', data={
        'username': 'testuser1',  # already exists
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Username gi\xc3\xa0 preso!' in response.data

def test_register_invalid_username(client):
    response = client.post('/register', data={
        'username': 'ab',  # too short
        'password': 'password123'
    }, follow_redirects=True)
    assert b'Username troppo corto' in response.data

def test_login_success(client, init_database):
    response = client.post('/login', data={
        'username': 'testuser1',
        'password': 'password123'
    }, follow_redirects=True)
    
    # Should redirect to index and maybe show PictoChat/Online users
    assert response.status_code == 200
    assert b'Login effettuato!' in response.data
    assert b'Logout' in response.data

def test_login_failure(client, init_database):
    response = client.post('/login', data={
        'username': 'testuser1',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Credenziali errate.' in response.data
    assert b'Login' in response.data

def test_logout(auth_client):
    client, user = auth_client
    response = client.get('/logout', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Logout effettuato.' in response.data
    assert b'Login' in response.data
