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

    # REGISTRAR BLUEPRINTS (AGREGAR ESTA LLAMADA)
    register_blueprints(app)
    

    
    return app

"""
AGREGAR ESTO a la función register_blueprints() en app/__init__.py
Reemplaza la función completa con esta versión actualizada:
"""

def register_blueprints(app):
    """Registrar todos los blueprints de la aplicación"""
    from app.routes.auth_routes import auth_bp
    from app.routes.video_routes import video_bp
    from app.routes.audio_routes import audio_bp
    # from app.routes.document_routes import document_bp
    # from app.routes.analysis_routes import analysis_bp
    # from app.routes.profile_routes import profile_bp
    # from app.routes.report_routes import report_bp
    
    # Registrar blueprints con prefijo /api
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(video_bp, url_prefix='/api/video')
    app.register_blueprint(audio_bp, url_prefix='/api/audio')
    # app.register_blueprint(document_bp, url_prefix='/api/documents')
    # app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    # app.register_blueprint(profile_bp, url_prefix='/api/profile')
    # app.register_blueprint(report_bp, url_prefix='/api/reports')
    
    # Ruta de prueba
    @app.route('/')
    def index():
        return {
            'message': 'Plataforma Integral de Rendimiento Estudiantil API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'auth': '/api/auth',
                'video': '/api/video',
                'audio': '/api/audio'
            }
        }
    
    @app.route('/health')
    def health():
        """Endpoint de health check"""
        return {'status': 'healthy', 'service': 'backend'}

# Importar modelos para que SQLAlchemy los reconozca
from app.models import *