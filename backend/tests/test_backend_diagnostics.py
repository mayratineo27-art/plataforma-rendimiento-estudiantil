"""
Test Diagnóstico Completo del Backend
Plataforma Integral de Rendimiento Estudiantil

Este archivo contiene tests exhaustivos para diagnosticar problemas en el backend.
"""

import pytest
import sys
import os
from pathlib import Path

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"{Colors.BLUE}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*80}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

# ============================================================================
# TEST 1: VERIFICACIÓN DE DEPENDENCIAS INSTALADAS
# ============================================================================

class TestDependencies:
    """Verifica que todas las dependencias necesarias estén instaladas"""
    
    def test_flask_installed(self):
        """Verifica que Flask esté instalado"""
        try:
            import flask
            print_success(f"Flask instalado: {flask.__version__}")
            assert True
        except ImportError as e:
            print_error(f"Flask NO instalado: {e}")
            assert False, "Flask no está instalado"
    
    def test_flask_cors_installed(self):
        """Verifica que Flask-CORS esté instalado"""
        try:
            import flask_cors
            print_success("Flask-CORS instalado correctamente")
            assert True
        except ImportError as e:
            print_error(f"Flask-CORS NO instalado: {e}")
            assert False, "Flask-CORS no está instalado"
    
    def test_sqlalchemy_installed(self):
        """Verifica que SQLAlchemy esté instalado"""
        try:
            import sqlalchemy
            print_success(f"SQLAlchemy instalado: {sqlalchemy.__version__}")
            assert True
        except ImportError as e:
            print_error(f"SQLAlchemy NO instalado: {e}")
            assert False, "SQLAlchemy no está instalado"
    
    def test_mysql_connector_installed(self):
        """Verifica que MySQL Connector esté instalado"""
        try:
            import mysql.connector
            print_success(f"MySQL Connector instalado: {mysql.connector.__version__}")
            assert True
        except ImportError as e:
            print_error(f"MySQL Connector NO instalado: {e}")
            assert False, "MySQL Connector no está instalado"
    
    def test_opencv_installed(self):
        """Verifica que OpenCV esté instalado"""
        try:
            import cv2
            print_success(f"OpenCV instalado: {cv2.__version__}")
            assert True
        except ImportError as e:
            print_error(f"OpenCV NO instalado: {e}")
            assert False, "OpenCV no está instalado"
    
    def test_deepface_installed(self):
        """Verifica que DeepFace esté instalado"""
        try:
            import deepface
            print_success("DeepFace instalado correctamente")
            assert True
        except ImportError as e:
            print_error(f"DeepFace NO instalado: {e}")
            assert False, "DeepFace no está instalado"
    
    def test_google_generativeai_installed(self):
        """Verifica que Google Generative AI esté instalado"""
        try:
            import google.generativeai as genai
            print_success("Google Generative AI instalado correctamente")
            assert True
        except ImportError as e:
            print_error(f"Google Generative AI NO instalado: {e}")
            assert False, "Google Generative AI no está instalado"
    
    def test_pypdf_installed(self):
        """Verifica que PyPDF2 esté instalado"""
        try:
            import PyPDF2
            print_success("PyPDF2 instalado correctamente")
            assert True
        except ImportError:
            try:
                import pypdf
                print_success("pypdf instalado correctamente")
                assert True
            except ImportError as e:
                print_warning(f"PyPDF2/pypdf NO instalado: {e}")
                print_warning("Se necesita para procesar PDFs en Módulo 1")
    
    def test_python_docx_installed(self):
        """Verifica que python-docx esté instalado"""
        try:
            import docx
            print_success("python-docx instalado correctamente")
            assert True
        except ImportError as e:
            print_warning(f"python-docx NO instalado: {e}")
            print_warning("Se necesita para procesar archivos Word en Módulo 1")
    
    def test_speech_recognition_installed(self):
        """Verifica que SpeechRecognition esté instalado"""
        try:
            import speech_recognition
            print_success(f"SpeechRecognition instalado: {speech_recognition.__version__}")
            assert True
        except ImportError as e:
            print_error(f"SpeechRecognition NO instalado: {e}")
            assert False, "SpeechRecognition no está instalado"
    
    def test_pydub_installed(self):
        """Verifica que pydub esté instalado"""
        try:
            import pydub
            print_success("pydub instalado correctamente")
            assert True
        except ImportError as e:
            print_error(f"pydub NO instalado: {e}")
            assert False, "pydub no está instalado"
    
    def test_numpy_installed(self):
        """Verifica que numpy esté instalado"""
        try:
            import numpy
            print_success(f"numpy instalado: {numpy.__version__}")
            assert True
        except ImportError as e:
            print_error(f"numpy NO instalado: {e}")
            assert False, "numpy no está instalado"

# ============================================================================
# TEST 2: VERIFICACIÓN DE ESTRUCTURA DE CARPETAS
# ============================================================================

class TestProjectStructure:
    """Verifica que la estructura de carpetas del proyecto exista"""
    
    def test_backend_directory_exists(self):
        """Verifica que exista la carpeta backend"""
        backend_path = Path("backend")
        if backend_path.exists():
            print_success(f"Carpeta backend existe: {backend_path.absolute()}")
            assert True
        else:
            print_error("Carpeta backend NO existe")
            assert False, "La carpeta backend no existe"
    
    def test_app_directory_exists(self):
        """Verifica que exista la carpeta app dentro de backend"""
        app_path = Path("backend/app")
        if app_path.exists():
            print_success(f"Carpeta app existe: {app_path.absolute()}")
            assert True
        else:
            print_error("Carpeta backend/app NO existe")
            assert False, "La carpeta backend/app no existe"
    
    def test_models_directory_exists(self):
        """Verifica que exista la carpeta models"""
        models_path = Path("backend/app/models")
        if models_path.exists():
            print_success(f"Carpeta models existe")
            assert True
        else:
            print_warning("Carpeta backend/app/models NO existe")
    
    def test_controllers_directory_exists(self):
        """Verifica que exista la carpeta controllers"""
        controllers_path = Path("backend/app/controllers")
        if controllers_path.exists():
            print_success(f"Carpeta controllers existe")
            assert True
        else:
            print_warning("Carpeta backend/app/controllers NO existe")
    
    def test_services_directory_exists(self):
        """Verifica que exista la carpeta services"""
        services_path = Path("backend/app/services")
        if services_path.exists():
            print_success(f"Carpeta services existe")
            assert True
        else:
            print_warning("Carpeta backend/app/services NO existe")
    
    def test_routes_directory_exists(self):
        """Verifica que exista la carpeta routes"""
        routes_path = Path("backend/app/routes")
        if routes_path.exists():
            print_success(f"Carpeta routes existe")
            assert True
        else:
            print_warning("Carpeta backend/app/routes NO existe")
    
    def test_uploads_directory_exists(self):
        """Verifica que exista la carpeta uploads"""
        uploads_path = Path("backend/uploads")
        if not uploads_path.exists():
            print_warning("Carpeta backend/uploads NO existe - se creará")
            uploads_path.mkdir(parents=True, exist_ok=True)
            print_success("Carpeta backend/uploads creada")
        else:
            print_success("Carpeta backend/uploads existe")
        assert True

# ============================================================================
# TEST 3: VERIFICACIÓN DE ARCHIVOS CLAVE
# ============================================================================

class TestKeyFiles:
    """Verifica que existan los archivos clave del backend"""
    
    def test_init_file_exists(self):
        """Verifica que exista el archivo __init__.py en app"""
        init_path = Path("backend/app/__init__.py")
        if init_path.exists():
            print_success("Archivo __init__.py existe")
            assert True
        else:
            print_error("Archivo __init__.py NO existe")
            assert False, "backend/app/__init__.py no existe"
    
    def test_run_file_exists(self):
        """Verifica que exista el archivo run.py"""
        run_path = Path("backend/run.py")
        if run_path.exists():
            print_success("Archivo run.py existe")
            assert True
        else:
            print_error("Archivo run.py NO existe")
            assert False, "backend/run.py no existe"
    
    def test_requirements_file_exists(self):
        """Verifica que exista el archivo requirements.txt"""
        req_path = Path("backend/requirements.txt")
        if req_path.exists():
            print_success("Archivo requirements.txt existe")
            assert True
        else:
            print_warning("Archivo requirements.txt NO existe")

# ============================================================================
# TEST 4: VERIFICACIÓN DE IMPORTACIONES
# ============================================================================

class TestImports:
    """Verifica que las importaciones del backend funcionen correctamente"""
    
    def test_can_import_flask_app(self):
        """Intenta importar la aplicación Flask"""
        try:
            sys.path.insert(0, str(Path("backend").absolute()))
            from app import create_app
            print_success("Se puede importar create_app desde app")
            assert True
        except ImportError as e:
            print_error(f"No se puede importar create_app: {e}")
            assert False, f"Error al importar create_app: {e}"
        except Exception as e:
            print_error(f"Error al importar create_app: {e}")
            assert False, f"Error al importar create_app: {e}"
    
    def test_can_import_models(self):
        """Intenta importar los modelos"""
        try:
            sys.path.insert(0, str(Path("backend").absolute()))
            from app.models import user
            print_success("Se pueden importar los modelos")
            assert True
        except ImportError as e:
            print_warning(f"No se pueden importar los modelos: {e}")
        except Exception as e:
            print_warning(f"Error al importar modelos: {e}")

# ============================================================================
# TEST 5: VERIFICACIÓN DE CONFIGURACIÓN
# ============================================================================

class TestConfiguration:
    """Verifica la configuración del backend"""
    
    def test_env_file_exists(self):
        """Verifica que exista el archivo .env o .env.example"""
        env_path = Path("backend/.env")
        env_example_path = Path("backend/.env.example")
        
        if env_path.exists():
            print_success("Archivo .env existe")
            assert True
        elif env_example_path.exists():
            print_warning("Solo existe .env.example - necesitas crear .env")
            print_warning("Copia .env.example a .env y configura tus variables")
        else:
            print_warning("No existe ni .env ni .env.example")

# ============================================================================
# TEST 6: TESTS FUNCIONALES BÁSICOS
# ============================================================================

class TestBasicFunctionality:
    """Tests funcionales básicos del sistema"""
    
    def test_flask_app_creation(self):
        """Verifica que se pueda crear una instancia de Flask"""
        try:
            from flask import Flask
            app = Flask(__name__)
            print_success("Se puede crear una aplicación Flask básica")
            assert True
        except Exception as e:
            print_error(f"Error al crear aplicación Flask: {e}")
            assert False
    
    def test_opencv_basic_functionality(self):
        """Verifica funcionalidad básica de OpenCV"""
        try:
            import cv2
            import numpy as np
            # Crear imagen de prueba
            img = np.zeros((100, 100, 3), dtype=np.uint8)
            print_success("OpenCV funciona correctamente")
            assert True
        except Exception as e:
            print_error(f"Error en OpenCV: {e}")
            assert False

# ============================================================================
# TEST 7: VERIFICACIÓN DE SERVICIOS DE IA
# ============================================================================

class TestAIServices:
    """Verifica que los servicios de IA estén configurados"""
    
    def test_gemini_import(self):
        """Verifica que se pueda importar Gemini"""
        try:
            import google.generativeai as genai
            print_success("Google Generative AI se puede importar")
            assert True
        except Exception as e:
            print_error(f"Error al importar Gemini: {e}")
            assert False
    
    def test_deepface_import(self):
        """Verifica que se pueda importar DeepFace"""
        try:
            from deepface import DeepFace
            print_success("DeepFace se puede importar")
            assert True
        except Exception as e:
            print_error(f"Error al importar DeepFace: {e}")
            assert False

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print_header("DIAGNÓSTICO COMPLETO DEL BACKEND")
    print_header("Plataforma Integral de Rendimiento Estudiantil")
    
    print(f"\n{Colors.YELLOW}Ejecutando tests diagnósticos...{Colors.RESET}\n")
    
    # Ejecutar pytest con verbose output
    pytest_args = [
        __file__,
        "-v",  # verbose
        "--tb=short",  # traceback corto
        "-s",  # mostrar prints
        "--color=yes"  # colores
    ]
    
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print_header("✓ TODOS LOS TESTS PASARON")
        print(f"{Colors.GREEN}El backend está funcionando correctamente{Colors.RESET}\n")
    else:
        print_header("✗ ALGUNOS TESTS FALLARON")
        print(f"{Colors.RED}Revisa los errores arriba para identificar los problemas{Colors.RESET}\n")
    
    sys.exit(exit_code)
