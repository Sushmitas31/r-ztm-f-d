from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

db = SQLAlchemy()
jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    """Convert user object to identity for JWT"""
    return str(user.id) if user else None

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    from routes.auth import auth_bp
    from routes.tasks import tasks_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api')
    
    from flask_swagger_ui import get_swaggerui_blueprint
    
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Task Manager API"
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
