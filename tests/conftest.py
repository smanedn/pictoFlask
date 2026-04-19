import pytest
from app import create_app
from app.extensions import db, socketio
from app.models import User
from app.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    user1 = User(username='testuser1', chat_color='#ff0000')
    user1.set_password('password123')
    user1.refresh_session_token()
    
    user2 = User(username='testuser2', chat_color='#00ff00')
    user2.set_password('password456')
    user2.refresh_session_token()
    
    user3 = User(username='adminuser', is_admin=True)
    user3.set_password('adminpass')
    user3.refresh_session_token()
    
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    
    return user1, user2, user3

@pytest.fixture
def auth_client(client, init_database):
    user1, _, _ = init_database
    client.post('/login', data={'username': user1.username, 'password': 'password123'})
    return client, user1

@pytest.fixture
def admin_client(client, init_database):
    _, _, user3 = init_database
    client.post('/login', data={'username': user3.username, 'password': 'adminpass'})
    return client, user3

@pytest.fixture
def socket_client(app, auth_client):
    client, user = auth_client
    sio_client = socketio.test_client(app, flask_test_client=client)
    sio_client.user = user
    yield sio_client
    if sio_client.is_connected():
        sio_client.disconnect()
