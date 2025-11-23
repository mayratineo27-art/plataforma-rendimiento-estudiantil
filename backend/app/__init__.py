"""
app/__init__.py - Inicialización de la aplicación Flask
Plataforma Integral de Rendimiento Estudiantil

VERSIÓN CORREGIDA - Blueprints funcionando correctamente
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate # 👈 1. IMPORTAR ESTO

# Cargar variables de entorno
load_dotenv()

# Inicializar extensiones
db = SQLAlchemy()


def create_app(config_name='development'):
    """
    Factory para crear la aplicación Flask
    
    Args:
        config_name (str): Nombre de la configuración
        
    Returns:
        Flask app configurada
    """
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Base de datos MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
        f"{os.getenv('DB_PASSWORD', '')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'rendimiento_estudiantil')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    
    # Configuración de uploads
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB
    
    # CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:3001"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Inicializar extensiones
    db.init_app(app)
    
    Migrate(app, db) # 👈 2. AGREGAR ESTA LÍNEA (Vincula Flask-Migrate con tu App y DB)
    
    # Crear carpetas necesarias
    create_folders(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Crear tablas si no existen
    with app.app_context():
        try:
            db.create_all()
            print("\n✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"\n⚠️  Error al inicializar BD: {e}")
    
    return app


def create_folders(app):
    """Crear carpetas necesarias para uploads y archivos generados"""
    folders = [
        'uploads/documents',
        'uploads/videos',
        'uploads/audio',
        'generated/reports',
        'generated/templates',
        'logs'
    ]
    
    for folder in folders:
        path = os.path.join(app.root_path, '..', folder)
        os.makedirs(path, exist_ok=True)
    
    print("\n✅ Carpetas creadas correctamente")


def register_blueprints(app):
    """
    Registrar todos los blueprints de la aplicación
    """
    print("\n📦 Registrando blueprints...")
    # ========== MÓDULO 1 RENOVADO: Asistente Académico ==========
    try:
        from app.routes.academic_routes import academic_bp
        app.register_blueprint(academic_bp) # El prefix ya está definido en el archivo de rutas
        print("   ✅ Academic routes: /api/academic")
    except ImportError as e:
        print(f"   ⚠️  Academic routes no disponible: {e}")
    except Exception as e:
        print(f"   ❌ Error al registrar Academic routes: {e}")
    
    # ========== MÓDULO 2: Video & Audio ==========
    # IMPORTANTE: Este es el blueprint principal del Módulo 2
    try:
        from app.routes.video_routes import video_bp, audio_bp
        app.register_blueprint(video_bp, url_prefix='/api/video')
        app.register_blueprint(audio_bp, url_prefix='/api/audio')
        print("   ✅ Video routes: /api/video")
        print("   ✅ Audio routes: /api/audio")
    except ImportError as e:
        print(f"   ⚠️  Video/Audio routes no disponible: {e}")
    except Exception as e:
        print(f"   ❌ Error al registrar Video/Audio routes: {e}")
    
    # ========== DASHBOARD ==========
    try:
        from app.routes.dashboard_routes import dashboard_bp
        app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
        print("   ✅ Dashboard routes: /api/dashboard")
    except ImportError as e:
        print(f"   ⚠️  Dashboard routes no disponible: {e}")
    except Exception as e:
        print(f"   ❌ Error al registrar Dashboard routes: {e}")
    
    # ========== MÓDULO 1: Análisis de Documentos ==========
    try:
        from app.routes.analysis_routes import analysis_bp
        app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
        print("   ✅ Analysis routes: /api/analysis")
    except ImportError as e:
        print(f"   ⚠️  Analysis routes no disponible: {e}")
    except Exception as e:
        print(f"   ❌ Error al registrar Analysis routes: {e}")
    
    # ========== MÓDULO 3: Perfil Integral ==========
    try:
        from app.routes.profile_routes import profile_bp
        app.register_blueprint(profile_bp, url_prefix='/api/profile')
        print("   ✅ Profile routes: /api/profile")
    except ImportError as e:
        print(f"   ⚠️  Profile routes no disponible: {e}")
    except Exception as e:
        print(f"   ❌ Error al registrar Profile routes: {e}")
    
    # ========== MÓDULO 4: Reportes ==========
    try:
        from app.routes.report_routes import report_bp
        app.register_blueprint(report_bp, url_prefix='/api/reports')
        print("   ✅ Report routes: /api/reports")
    except ImportError as e:
        print(f"   ⚠️  Report routes no disponible: {e}")
    except Exception as e:
        print(f"   ❌ Error al registrar Report routes: {e}")
    
    # ========== AUTENTICACIÓN ==========
    try:
        from app.routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        print("   ✅ Auth routes: /api/auth")
    except ImportError as e:
        print(f"   ⚠️  Auth routes no disponible: {e}")
    except Exception as e:
        print(f"   ❌ Error al registrar Auth routes: {e}")
    
    # ========== CRONÓMETROS ==========
    try:
        from app.routes.timer_routes import timer_bp
        app.register_blueprint(timer_bp)
        print("   ✅ Timer routes: /api/timer")
    except ImportError as e:
        print(f"   ⚠️  Timer routes no disponible: {e}")
    except Exception as e:
        print(f"   ❌ Error al registrar Timer routes: {e}")
    
    # ========== PROYECTOS Y SESIONES DE TIEMPO ==========
    try:
        from app.routes.project_routes import project_bp
        app.register_blueprint(project_bp)
        print("   ✅ Project routes: /api/projects")
    except ImportError as e:
        print(f"   ⚠️  Project routes no disponible: {e}")
    except Exception as e:
        print(f"   ❌ Error al registrar Project routes: {e}")
    
    # ========== RUTAS DE PRUEBA ==========
    @app.route('/')
    def index():
        """Endpoint raíz con información de la API"""
        return {
            'message': 'Plataforma Integral de Rendimiento Estudiantil API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'video': '/api/video',
                'audio': '/api/audio',
                'dashboard': '/api/dashboard',
                'analysis': '/api/analysis',
                'profile': '/api/profile',
                'reports': '/api/reports',
                'auth': '/api/auth'
            },
            'test_endpoints': {
                'video': '/api/video/test',
                'audio': '/api/audio/test'
            }
        }
    
    @app.route('/health')
    def health():
        """Endpoint de health check"""
        try:
            # Probar conexión a BD
            db.session.execute('SELECT 1')
            db_status = 'connected'
        except:
            db_status = 'disconnected'
        
        return {
            'status': 'healthy',
            'service': 'backend',
            'database': db_status,
            'python_version': '3.13.8',
            'flask_version': 'OK'
        }
    
    print("\n✅ Blueprints registrados correctamente\n")


# ========================================
# IMPORTAR MODELOS
# ========================================
# Esto permite que SQLAlchemy reconozca los modelos

def import_models():
    """Importar todos los modelos para que SQLAlchemy los reconozca"""
    print("\n📋 Importando modelos...")
    
    try:
        from app.models.academic import AcademicCourse, AcademicTask
        print("   ✅ Academic Models (Course, Task)")
    except ImportError as e:
        print(f"   ⚠️  Academic Models: {e}")
    
    try:
        from app.models.timer import StudyTimer
        print("   ✅ Timer Models (StudyTimer)")
    except ImportError as e:
        print(f"   ⚠️  Timer Models: {e}")
    
    try:
        from app.models.project import Project, TimeSession
        print("   ✅ Project Models (Project, TimeSession)")
    except ImportError as e:
        print(f"   ⚠️  Project Models: {e}")

    print("✅ Modelos importados\n")
    
    try:
        from app.models.user import User
        print("   ✅ User")
    except ImportError as e:
        print(f"   ⚠️  User: {e}")
    
    try:
        from app.models.video_session import VideoSession
        print("   ✅ VideoSession")
    except ImportError as e:
        print(f"   ⚠️  VideoSession: {e}")
    
    try:
        from app.models.emotion_data import EmotionData
        print("   ✅ EmotionData")
    except ImportError as e:
        print(f"   ⚠️  EmotionData: {e}")
    
    try:
        from app.models.audio_transcription import AudioTranscription
        print("   ✅ AudioTranscription")
    except ImportError as e:
        print(f"   ⚠️  AudioTranscription: {e}")
    
    try:
        from app.models.attention_metrics import AttentionMetrics
        print("   ✅ AttentionMetrics")
    except ImportError as e:
        print(f"   ⚠️  AttentionMetrics: {e}")
    
    try:
        from app.models.student_profile import StudentProfile
        print("   ✅ StudentProfile")
    except ImportError as e:
        print(f"   ⚠️  StudentProfile: {e}")
    
    print("✅ Modelos importados\n")

# Importar modelos al cargar el módulo
import_models()