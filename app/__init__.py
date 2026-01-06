from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.routes.auth import auth
    app.register_blueprint(auth)
    
    from app.routes.project import project
    app.register_blueprint(project)
    
    from app.routes.env import env
    app.register_blueprint(env)
    
    from app.routes.test_case import test_case
    app.register_blueprint(test_case)
    
    from app.routes.common_params import common_params
    app.register_blueprint(common_params)
    
    from app.routes.execution import execution
    app.register_blueprint(execution)
    
    return app