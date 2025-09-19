import pytest
import json

class TestAuth:
    """Test authentication endpoints"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        
        response = client.post('/api/auth/register', json=user_data)
        
        assert response.status_code == 201
        data = response.json
        assert 'message' in data
        assert 'user' in data
        assert data['user']['username'] == 'newuser'
        assert data['user']['email'] == 'newuser@example.com'
        assert data['user']['role'] == 'user'
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        
        client.post('/api/auth/register', json=user_data)
        
        response = client.post('/api/auth/register', json=user_data)
        
        assert response.status_code == 400
        assert 'Username already exists' in response.json['error']
    
    def test_register_password_mismatch(self, client):
        """Test registration with password mismatch"""
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'different123'
        }
        
        response = client.post('/api/auth/register', json=user_data)
        
        assert response.status_code == 400
        assert 'Validation error' in response.json['error']
    
    def test_login_success(self, client):
        """Test successful login"""
        
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        client.post('/api/auth/register', json=user_data)
        
        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        
        assert response.status_code == 200
        data = response.json
        assert 'access_token' in data
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        login_data = {
            'username': 'nonexistent',
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/auth/login', json=login_data)
        
        assert response.status_code == 401
        assert 'Invalid credentials' in response.json['error']
    
    def test_get_profile_success(self, client, auth_headers):
        """Test getting user profile"""
        response = client.get('/api/auth/profile', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
    
    def test_get_profile_unauthorized(self, client):
        """Test getting profile without authentication"""
        response = client.get('/api/auth/profile')
        
        assert response.status_code == 401
