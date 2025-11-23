"""
Script para corregir el archivo __init__.py del backend
Soluciona el error: "cannot import name 'create_app' from 'app'"
"""

import os
from pathlib import Path

# Contenido correcto para backend/app/__init__.py
APP_INIT_CONTENT = '''"""
Inicialización de la aplicación Flask
Plataforma Integral de Rendimiento Estudiantil
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# Inicializar extensiones
db = SQLAlchemy()

def create_app(config_name='development'):
    """
    Factory pattern para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar
        
    Returns:
        app: Instancia de la aplicación Flask
    """
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'mysql+mysqlconnector://root:password@localhost/plataforma_estudiantil'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max
    
    # Carpetas de subida
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    app.config['GENERATED_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated')
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Registrar blueprints (solo si existen)
    try:
        from app.routes import auth_routes, document_routes, analysis_routes
        from app.routes import video_routes, audio_routes, profile_routes, report_routes
        
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(document_routes.bp)
        app.register_blueprint(analysis_routes.bp)
        app.register_blueprint(video_routes.bp)
        app.register_blueprint(audio_routes.bp)
        app.register_blueprint(profile_routes.bp)
        app.register_blueprint(report_routes.bp)
    except ImportError as e:
        print(f"Warning: No se pudieron importar algunas rutas: {e}")
    
    # Ruta de prueba
    @app.route('/')
    def index():
        return {
            'message': 'Plataforma Integral de Rendimiento Estudiantil API',
            'status': 'running',
            'version': '1.0.0'
        }
    
    @app.route('/health')
    def health():
        """Endpoint de health check"""
        return {'status': 'healthy'}, 200
    
    @app.route('/api/test')
    def api_test():
        """Endpoint de prueba de la API"""
        return {
            'message': 'API funcionando correctamente',
            'endpoints': [
                '/ - Información general',
                '/health - Health check',
                '/api/test - Test de API'
            ]
        }, 200
    
    return app
'''

def fix_app_init():
    """Corrige el archivo __init__.py"""
    print("="*80)
    print("CORRIGIENDO ARCHIVO backend/app/__init__.py")
    print("="*80)
    
    # Verificar que exista la carpeta backend/app
    app_dir = Path("backend/app")
    if not app_dir.exists():
        print("❌ Error: No existe la carpeta backend/app")
        print("   Solución: Ejecuta primero setup_backend_structure.py")
        return False
    
    # Crear backup del archivo actual si existe
    init_file = app_dir / "__init__.py"
    if init_file.exists():
        backup_file = app_dir / "__init__.py.backup"
        print(f"📋 Creando backup: {backup_file}")
        with open(init_file, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(backup_content)
    
    # Escribir el contenido correcto
    print(f"✏️ Escribiendo archivo corregido: {init_file}")
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(APP_INIT_CONTENT)
    
    print("✅ Archivo backend/app/__init__.py corregido exitosamente")
    print()
    print("El archivo ahora incluye:")
    print("  ✓ Función create_app")
    print("  ✓ Configuración de Flask")
    print("  ✓ Configuración de CORS")
    print("  ✓ Configuración de SQLAlchemy")
    print("  ✓ Rutas básicas (/, /health, /api/test)")
    print()
    
    return True

if __name__ == "__main__":
    success = fix_app_init()
    if success:
        print("🎉 ¡Listo! Ahora puedes importar create_app")
        print()
        print("Próximo paso: Instalar dependencias faltantes")
        print("  pip install mysql-connector-python opencv-python google-generativeai SpeechRecognition")
    else:
        print("❌ No se pudo corregir el archivo")
