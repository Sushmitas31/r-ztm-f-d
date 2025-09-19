from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from app import db
from models.task import Task
from models.user import User
from schemas.task_schema import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from marshmallow import ValidationError

tasks_bp = Blueprint('tasks', __name__)

task_schema = TaskSchema()
task_create_schema = TaskCreateSchema()
task_update_schema = TaskUpdateSchema()

def get_current_user():
    """Get current authenticated user"""
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))

def is_admin_or_owner(task_user_id):
    """Check if current user is admin or task owner"""
    current_user = get_current_user()
    return current_user.is_admin() or current_user.id == task_user_id

@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get all tasks with pagination and filtering"""
    current_user = get_current_user()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 100)  # Limit max per_page
    
    completed = request.args.get('completed', type=bool)
    search = request.args.get('search', type=str)
    
    if current_user.is_admin():
        query = Task.query
    else:
        query = Task.query.filter_by(user_id=current_user.id)
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    if search:
        query = query.filter(
            or_(
                Task.title.contains(search),
                Task.description.contains(search)
            )
        )
    
    query = query.order_by(Task.created_at.desc())
    
    paginated_tasks = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'tasks': [task_schema.dump(task) for task in paginated_tasks.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': paginated_tasks.total,
            'pages': paginated_tasks.pages,
            'has_next': paginated_tasks.has_next,
            'has_prev': paginated_tasks.has_prev
        }
    }), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Get a specific task by ID"""
    task = Task.query.get_or_404(task_id)
    
    if not is_admin_or_owner(task.user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({'task': task_schema.dump(task)}), 200

@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """Create a new task"""
    try:
        data = task_create_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'details': err.messages}), 400
    
    current_user = get_current_user()
    
    task = Task(
        title=data['title'],
        description=data.get('description'),
        completed=data.get('completed', False),
        user_id=current_user.id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'message': 'Task created successfully',
        'task': task_schema.dump(task)
    }), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Update a specific task"""
    task = Task.query.get_or_404(task_id)
    
    if not is_admin_or_owner(task.user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = task_update_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'details': err.messages}), 400
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': task_schema.dump(task)
    }), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a specific task"""
    task = Task.query.get_or_404(task_id)
    
    if not is_admin_or_owner(task.user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'}), 200
