#!/usr/bin/env python3
"""
Database initialization script
Creates tables and optionally creates an admin user
"""

from app import create_app, db
from models.user import User

def init_db():
    """Initialize database and create tables"""
    app = create_app()
    
    with app.app_context():
        
        db.create_all()
        print("Database tables created successfully!")
        
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")
            print("Username: admin")
            print("Password: admin123")
            print("Email: admin@example.com")
        else:
            print("Admin user already exists!")

if __name__ == '__main__':
    init_db()
