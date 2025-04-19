from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from app.models import db
from app.api import api_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Simple root route for health check
    @app.route('/')
    def health_check():
        return {'status': 'ok', 'version': '1.0.0'}
    
    # Redirect for notion API endpoints
    @app.route('/notion/validate-connection', methods=['POST'])
    def redirect_notion_validate():
        return redirect('/api/notion/validate-connection', code=307)
    
    return app 