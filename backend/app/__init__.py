"""
app/__init__.py - Inicialización simplificada
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
        f"{os.getenv('DB_PASSWORD', '')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'rendimiento_estudiantil')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # CORS
    CORS(app)
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Ruta de prueba
    @app.route('/')
    def index():
        return {
            'message': 'Plataforma Integral de Rendimiento Estudiantil API',
            'version': '1.0.0',
            'status': 'running',
            "documentation": "/api/docs"
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy', "service": "backend"}
    
    # Registrar blueprints (comentados por ahora)
    # from app.routes.auth_routes import auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return app