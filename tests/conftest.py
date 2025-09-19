import pytest
from app import create_app, db
from models.user import User
from models.task import Task

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return auth headers"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }
    client.post('/api/auth/register', json=user_data)
    
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = client.post('/api/auth/login', json=login_data)
    token = response.json['access_token']
    
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def admin_headers(client):
    """Create admin user and return auth headers"""
    
    with client.application.app_context():
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('adminpass123')
        db.session.add(admin)
        db.session.commit()
    
    login_data = {
        'username': 'admin',
        'password': 'adminpass123'
    }
    response = client.post('/api/auth/login', json=login_data)
    token = response.json['access_token']
    
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_task(client, auth_headers):
    """Create a sample task for testing"""
    task_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'completed': False
    }
    response = client.post('/api/tasks', json=task_data, headers=auth_headers)
    return response.json['task']
