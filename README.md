# Task Manager API

A RESTful API for managing tasks with user authentication built using Flask, SQLAlchemy, and JWT.

## Features

- **User Authentication**: JWT-based authentication with user registration and login
- **Task Management**: Full CRUD operations for tasks
- **User Roles**: Admin and regular user roles with different permissions
- **Pagination**: Paginated task listing with configurable page size
- **Filtering**: Filter tasks by completion status and search in title/description
- **API Documentation**: Interactive Swagger documentation
- **Testing**: Comprehensive unit tests with pytest

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <folder-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python init_db.py
```

## Running the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:5000/api/docs`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get current user profile

### Tasks
- `GET /api/tasks` - Get all tasks (with pagination and filtering)
- `GET /api/tasks/{id}` - Get a specific task
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task

### Query Parameters for GET /api/tasks
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 10, max: 100)
- `completed` - Filter by completion status (true/false)
- `search` - Search in title and description

## Testing

Run the test suite:

```bash
python -m pytest
```

## Project Structure

```
task-manager-api/
├── app.py                 # Application file
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── models/               # Database models
│   ├── __init__.py
│   ├── user.py           # User model
│   └── task.py           # Task model
├── routes/               # API routes
│   ├── __init__.py
│   ├── auth.py           # Authentication routes
│   └── tasks.py          # Task routes
├── schemas/              # Data validation schemas
│   ├── __init__.py
│   ├── user_schema.py    # User validation
│   └── task_schema.py    # Task validation
├── static/               # Static files
│   └── swagger.json      # API documentation
├── tests/                # Test files
│   ├── __init__.py
│   ├── conftest.py       # Test configuration
│   ├── test_auth.py      # Authentication tests
│   └── test_tasks.py     # Task tests
└── README.md
```

## Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "password123"
  }'
```

### Create a task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Learn Flask",
    "description": "Complete Flask tutorial",
    "completed": false
  }'
```

### Get tasks with pagination
```bash
curl -X GET "http://localhost:5000/api/tasks?page=1&per_page=5&completed=false" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## User Roles

- **User**: Can create, read, update, and delete their own tasks
- **Admin**: Can perform all user operations plus access all tasks from all users

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `role` (user/admin)
- `created_at`
- `updated_at`

### Tasks Table
- `id` (Primary Key)
- `title`
- `description`
- `completed` (Boolean)
- `user_id` (Foreign Key)
- `created_at`
- `updated_at`
