import pytest
import json

class TestTasks:
    """Test task endpoints"""
    
    def test_create_task_success(self, client, auth_headers):
        """Test successful task creation"""
        task_data = {
            'title': 'New Task',
            'description': 'Task description',
            'completed': False
        }
        
        response = client.post('/api/tasks', json=task_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json
        assert 'message' in data
        assert 'task' in data
        assert data['task']['title'] == 'New Task'
        assert data['task']['description'] == 'Task description'
        assert data['task']['completed'] == False
    
    def test_create_task_unauthorized(self, client):
        """Test task creation without authentication"""
        task_data = {
            'title': 'New Task',
            'description': 'Task description'
        }
        
        response = client.post('/api/tasks', json=task_data)
        
        assert response.status_code == 401
    
    def test_get_tasks_success(self, client, auth_headers):
        """Test getting all tasks"""
       
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description'
        }
        client.post('/api/tasks', json=task_data, headers=auth_headers)
        
        response = client.get('/api/tasks', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert 'tasks' in data
        assert 'pagination' in data
        assert len(data['tasks']) == 1
        assert data['tasks'][0]['title'] == 'Test Task'
    
    def test_get_tasks_with_pagination(self, client, auth_headers):
        """Test getting tasks with pagination"""
        
        for i in range(15):
            task_data = {
                'title': f'Task {i}',
                'description': f'Description {i}'
            }
            client.post('/api/tasks', json=task_data, headers=auth_headers)
        
        response = client.get('/api/tasks?page=1&per_page=10', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert len(data['tasks']) == 10
        assert data['pagination']['page'] == 1
        assert data['pagination']['per_page'] == 10
        assert data['pagination']['total'] == 15
        assert data['pagination']['has_next'] == True
    
    def test_get_tasks_with_filtering(self, client, auth_headers):
        """Test getting tasks with filtering"""
        
        task_data1 = {'title': 'Completed Task', 'completed': True}
        task_data2 = {'title': 'Incomplete Task', 'completed': False}
        
        client.post('/api/tasks', json=task_data1, headers=auth_headers)
        client.post('/api/tasks', json=task_data2, headers=auth_headers)
        
        response = client.get('/api/tasks?completed=true', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert len(data['tasks']) == 1
        assert data['tasks'][0]['completed'] == True
    
    def test_get_tasks_with_search(self, client, auth_headers):
        """Test getting tasks with search"""
        # Create tasks with different titles
        task_data1 = {'title': 'Python Task', 'description': 'Learn Python'}
        task_data2 = {'title': 'JavaScript Task', 'description': 'Learn JavaScript'}
        
        client.post('/api/tasks', json=task_data1, headers=auth_headers)
        client.post('/api/tasks', json=task_data2, headers=auth_headers)
        
        response = client.get('/api/tasks?search=Python', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert len(data['tasks']) == 1
        assert 'Python' in data['tasks'][0]['title']
    
    def test_get_task_success(self, client, auth_headers, sample_task):
        """Test getting a specific task"""
        task_id = sample_task['id']
        
        response = client.get(f'/api/tasks/{task_id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert 'task' in data
        assert data['task']['id'] == task_id
        assert data['task']['title'] == 'Test Task'
    
    def test_get_task_not_found(self, client, auth_headers):
        """Test getting non-existent task"""
        response = client.get('/api/tasks/999', headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_get_task_access_denied(self, client, auth_headers):
        """Test getting task from different user"""
        
        user_data = {
            'username': 'otheruser',
            'email': 'other@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        client.post('/api/auth/register', json=user_data)
        
        login_data = {'username': 'otheruser', 'password': 'password123'}
        login_response = client.post('/api/auth/login', json=login_data)
        other_token = login_response.json['access_token']
        other_headers = {'Authorization': f'Bearer {other_token}'}
        
        task_data = {'title': 'Other Task'}
        task_response = client.post('/api/tasks', json=task_data, headers=other_headers)
        task_id = task_response.json['task']['id']
        
        response = client.get(f'/api/tasks/{task_id}', headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_update_task_success(self, client, auth_headers, sample_task):
        """Test successful task update"""
        task_id = sample_task['id']
        update_data = {
            'title': 'Updated Task',
            'completed': True
        }
        
        response = client.put(f'/api/tasks/{task_id}', json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['task']['title'] == 'Updated Task'
        assert data['task']['completed'] == True
    
    def test_update_task_access_denied(self, client, auth_headers):
        """Test updating task from different user"""
       
        user_data = {
            'username': 'otheruser',
            'email': 'other@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        client.post('/api/auth/register', json=user_data)
        
        login_data = {'username': 'otheruser', 'password': 'password123'}
        login_response = client.post('/api/auth/login', json=login_data)
        other_token = login_response.json['access_token']
        other_headers = {'Authorization': f'Bearer {other_token}'}
        
        task_data = {'title': 'Other Task'}
        task_response = client.post('/api/tasks', json=task_data, headers=other_headers)
        task_id = task_response.json['task']['id']
        
        update_data = {'title': 'Hacked Task'}
        response = client.put(f'/api/tasks/{task_id}', json=update_data, headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_delete_task_success(self, client, auth_headers, sample_task):
        """Test successful task deletion"""
        task_id = sample_task['id']
        
        response = client.delete(f'/api/tasks/{task_id}', headers=auth_headers)
        
        assert response.status_code == 200
        assert 'deleted successfully' in response.json['message']
        
        get_response = client.get(f'/api/tasks/{task_id}', headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_task_access_denied(self, client, auth_headers):
        """Test deleting task from different user"""
        
        user_data = {
            'username': 'otheruser',
            'email': 'other@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        client.post('/api/auth/register', json=user_data)
        
        login_data = {'username': 'otheruser', 'password': 'password123'}
        login_response = client.post('/api/auth/login', json=login_data)
        other_token = login_response.json['access_token']
        other_headers = {'Authorization': f'Bearer {other_token}'}
        
        task_data = {'title': 'Other Task'}
        task_response = client.post('/api/tasks', json=task_data, headers=other_headers)
        task_id = task_response.json['task']['id']
        
        response = client.delete(f'/api/tasks/{task_id}', headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_admin_can_access_all_tasks(self, client, admin_headers, auth_headers):
        """Test that admin can access all tasks"""
        
        task_data = {'title': 'User Task'}
        task_response = client.post('/api/tasks', json=task_data, headers=auth_headers)
        task_id = task_response.json['task']['id']
        
        response = client.get(f'/api/tasks/{task_id}', headers=admin_headers)
        
        assert response.status_code == 200
        assert response.json['task']['title'] == 'User Task'
