"""
Script para generar/reparar la estructura del backend
Plataforma Integral de Rendimiento Estudiantil
"""

import os
from pathlib import Path

# Colores para output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def create_directory(path):
    """Crea un directorio si no existe"""
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"{Colors.GREEN}✓ Creado: {path}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}  Ya existe: {path}{Colors.RESET}")

def create_file(path, content=""):
    """Crea un archivo si no existe"""
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"{Colors.GREEN}✓ Creado: {path}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}  Ya existe: {path}{Colors.RESET}")

def setup_backend_structure():
    """Crea toda la estructura del backend"""
    
    print(f"\n{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"{Colors.BLUE}Generando estructura del backend...{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*80}{Colors.RESET}\n")
    
    # Estructura de directorios
    directories = [
        "backend",
        "backend/app",
        "backend/app/models",
        "backend/app/controllers",
        "backend/app/services",
        "backend/app/services/ai",
        "backend/app/services/document_processing",
        "backend/app/services/video_processing",
        "backend/app/services/audio_processing",
        "backend/app/services/report_generation",
        "backend/app/routes",
        "backend/app/middleware",
        "backend/app/utils",
        "backend/app/config",
        "backend/tests",
        "backend/tests/unit",
        "backend/tests/integration",
        "backend/tests/functional",
        "backend/uploads",
        "backend/uploads/documents",
        "backend/uploads/videos",
        "backend/uploads/audio",
        "backend/generated",
        "backend/generated/reports",
        "backend/generated/templates",
        "backend/logs",
        "backend/migrations",
        "backend/migrations/versions",
    ]
    
    print(f"{Colors.BLUE}Creando directorios...{Colors.RESET}\n")
    for directory in directories:
        create_directory(directory)
    
    # Archivos __init__.py
    print(f"\n{Colors.BLUE}Creando archivos __init__.py...{Colors.RESET}\n")
    init_files = [
        "backend/app/__init__.py",
        "backend/app/models/__init__.py",
        "backend/app/controllers/__init__.py",
        "backend/app/services/__init__.py",
        "backend/app/services/ai/__init__.py",
        "backend/app/services/document_processing/__init__.py",
        "backend/app/services/video_processing/__init__.py",
        "backend/app/services/audio_processing/__init__.py",
        "backend/app/services/report_generation/__init__.py",
        "backend/app/routes/__init__.py",
        "backend/app/middleware/__init__.py",
        "backend/app/utils/__init__.py",
        "backend/app/config/__init__.py",
        "backend/tests/__init__.py",
        "backend/tests/unit/__init__.py",
        "backend/tests/integration/__init__.py",
        "backend/tests/functional/__init__.py",
    ]
    
    for init_file in init_files:
        create_file(init_file, '"""Módulo de inicialización"""\n')
    
    # Archivo principal de la aplicación Flask
    print(f"\n{Colors.BLUE}Creando archivo principal de Flask...{Colors.RESET}\n")
    
    app_init_content = '''"""
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
        'mysql://root:password@localhost/plataforma_estudiantil'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max
    
    # Carpetas de subida
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['GENERATED_FOLDER'] = os.path.join(os.getcwd(), 'generated')
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Registrar blueprints
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
    
    return app
'''
    
    create_file("backend/app/__init__.py", app_init_content)
    
    # Archivo run.py
    print(f"\n{Colors.BLUE}Creando archivo run.py...{Colors.RESET}\n")
    
    run_content = '''"""
Punto de entrada de la aplicación
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"\\nServidor corriendo en: http://localhost:{port}")
    print(f"Modo debug: {debug}\\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
'''
    
    create_file("backend/run.py", run_content)
    
    # Archivo requirements.txt
    print(f"\n{Colors.BLUE}Creando requirements.txt...{Colors.RESET}\n")
    
    requirements_content = '''# Flask y extensiones
Flask==3.1.2
Flask-CORS==6.0.1
Flask-SQLAlchemy==3.1.1
Werkzeug==3.1.3

# Base de datos
mysql-connector-python==9.4.0
SQLAlchemy==2.0.43

# Procesamiento de imágenes y video
opencv-python==4.12.0.88
opencv-contrib-python==4.12.0.88
Pillow==11.3.0
numpy==2.2.6

# IA y reconocimiento facial
deepface==0.0.95
tensorflow==2.20.0
tf-keras==2.20.1

# Procesamiento de documentos
PyPDF2==3.0.1
python-docx==1.1.2

# Procesamiento de audio
SpeechRecognition==3.13.0
pydub==0.25.1
pyaudio==0.2.14

# API de Google Gemini
google-generativeai==0.4.6

# Testing
pytest==8.4.2
pytest-cov==7.0.0
coverage==7.10.7

# Utilidades
python-dotenv==1.0.1
'''
    
    create_file("backend/requirements.txt", requirements_content)
    
    # Archivo .env.example
    print(f"\n{Colors.BLUE}Creando .env.example...{Colors.RESET}\n")
    
    env_example_content = '''# Configuración de la aplicación
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
PORT=5000

# Base de datos
DATABASE_URL=mysql://root:password@localhost/plataforma_estudiantil

# API Keys
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here  # opcional

# Configuración de archivos
MAX_FILE_SIZE=100  # MB
ALLOWED_EXTENSIONS=pdf,docx,doc,txt

# Configuración de video/audio
MAX_VIDEO_LENGTH=3600  # segundos (1 hora)
MAX_AUDIO_LENGTH=3600  # segundos (1 hora)
'''
    
    create_file("backend/.env.example", env_example_content)
    
    # Archivo .gitignore
    print(f"\n{Colors.BLUE}Creando .gitignore...{Colors.RESET}\n")
    
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Archivos de entorno
.env
.env.local

# Base de datos
*.db
*.sqlite
*.sqlite3

# Uploads y generados
uploads/
generated/
logs/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
'''
    
    create_file("backend/.gitignore", gitignore_content)
    
    # Archivo de configuración
    print(f"\n{Colors.BLUE}Creando archivo de configuración...{Colors.RESET}\n")
    
    config_content = '''"""
Configuración de la aplicación
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()

class Config:
    """Configuración base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
    
    # Carpetas
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    GENERATED_FOLDER = os.path.join(BASE_DIR, 'generated')
    LOGS_FOLDER = os.path.join(BASE_DIR, 'logs')
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql://root:password@localhost/plataforma_estudiantil'
    )

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
'''
    
    create_file("backend/app/config/settings.py", config_content)
    
    # README
    print(f"\n{Colors.BLUE}Creando README.md...{Colors.RESET}\n")
    
    readme_content = '''# Backend - Plataforma Integral de Rendimiento Estudiantil

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
```

2. Activar entorno virtual:
- Windows: `venv\\Scripts\\activate`
- Linux/Mac: `source venv/bin/activate`

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Ejecutar la aplicación:
```bash
python run.py
```

## Estructura del Proyecto

- `app/` - Código principal de la aplicación
  - `models/` - Modelos de base de datos
  - `controllers/` - Lógica de negocio
  - `services/` - Servicios de IA y procesamiento
  - `routes/` - Rutas de la API
  - `middleware/` - Middleware de la aplicación
  - `utils/` - Utilidades
  - `config/` - Configuración
- `tests/` - Tests unitarios, integración y funcionales
- `uploads/` - Archivos subidos por usuarios
- `generated/` - Archivos generados por el sistema
- `logs/` - Logs de la aplicación

## Endpoints Principales

- `GET /` - Información de la API
- `GET /health` - Health check
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login de usuario
- `POST /api/documents/upload` - Subir documento
- `POST /api/video/analyze` - Analizar video
- `POST /api/audio/transcribe` - Transcribir audio
- `GET /api/profile/:id` - Obtener perfil del estudiante
- `POST /api/reports/generate` - Generar reporte

## Testing

Ejecutar todos los tests:
```bash
pytest
```

Con cobertura:
```bash
pytest --cov=app tests/
```
'''
    
    create_file("backend/README.md", readme_content)
    
    print(f"\n{Colors.GREEN}{'='*80}{Colors.RESET}")
    print(f"{Colors.GREEN}✓ Estructura del backend generada exitosamente{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*80}{Colors.RESET}\n")
    
    print(f"{Colors.BLUE}Próximos pasos:{Colors.RESET}")
    print(f"1. Copia .env.example a .env y configura tus variables")
    print(f"2. Instala las dependencias: pip install -r backend/requirements.txt")
    print(f"3. Ejecuta los tests diagnósticos: python test_backend_diagnostics.py")
    print(f"4. Inicia el servidor: cd backend && python run.py\n")

if __name__ == "__main__":
    setup_backend_structure()
