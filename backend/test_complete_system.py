"""
Suite de Pruebas Completas - Plataforma de Rendimiento Estudiantil
Prueba todos los módulos y funcionalidades principales
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text
import requests
import json
from datetime import datetime

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if passed else f"{Colors.RED}❌ FAIL{Colors.RESET}"
    print(f"{status} | {name}")
    if details and not passed:
        print(f"         {Colors.YELLOW}└─ {details}{Colors.RESET}")

def test_database_connection():
    """Prueba 1: Conexión a la base de datos"""
    print_header("PRUEBA 1: BASE DE DATOS")
    
    app = create_app()
    results = []
    
    with app.app_context():
        # Test 1.1: Conexión básica
        try:
            db.session.execute(text("SELECT 1"))
            results.append(("Conexión a MySQL", True, ""))
        except Exception as e:
            results.append(("Conexión a MySQL", False, str(e)))
        
        # Test 1.2: Verificar tablas principales
        tables = [
            'users',
            'academic_courses', 
            'academic_tasks',
            'study_timers',
            'projects',
            'time_sessions',
            'timelines',
            'timeline_steps',
            'writing_evaluations'
        ]
        
        for table in tables:
            try:
                result = db.session.execute(text(f"SHOW TABLES LIKE '{table}'"))
                exists = result.fetchone() is not None
                results.append((f"Tabla '{table}'", exists, f"Tabla no encontrada" if not exists else ""))
            except Exception as e:
                results.append((f"Tabla '{table}'", False, str(e)))
        
        # Test 1.3: Verificar modelos
        models_to_test = [
            'User', 'AcademicCourse', 'AcademicTask', 'StudyTimer',
            'Project', 'TimeSession', 'Timeline', 'TimelineStep',
            'WritingEvaluation'
        ]
        
        for model_name in models_to_test:
            try:
                from app import models
                model_class = getattr(models, model_name)
                count = model_class.query.count()
                results.append((f"Modelo {model_name}", True, f"{count} registros"))
            except Exception as e:
                results.append((f"Modelo {model_name}", False, str(e)))
    
    for test_name, passed, details in results:
        print_test(test_name, passed, details)
    
    return results

def test_api_endpoints():
    """Prueba 2: Endpoints API"""
    print_header("PRUEBA 2: API ENDPOINTS")
    
    base_url = "http://localhost:5000"
    results = []
    
    # Test 2.1: Health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        passed = response.status_code == 200
        results.append(("Health endpoint", passed, f"Status: {response.status_code}"))
    except Exception as e:
        results.append(("Health endpoint", False, str(e)))
    
    # Test 2.2: Academic routes
    endpoints_to_test = [
        ("/api/academic/courses", "GET"),
        ("/api/academic/tasks", "GET"),
        ("/api/timer/sessions", "GET"),
        ("/api/projects", "GET"),
        ("/api/timelines/user/1", "GET"),
    ]
    
    for endpoint, method in endpoints_to_test:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            
            # Considerar exitoso si no es 500 (puede ser 404 si no hay datos)
            passed = response.status_code != 500
            details = f"Status: {response.status_code}"
            
            if not passed:
                try:
                    error_msg = response.json().get('error', 'Unknown error')
                    details += f" - {error_msg}"
                except:
                    pass
                    
            results.append((f"{method} {endpoint}", passed, details))
        except requests.exceptions.ConnectionError:
            results.append((f"{method} {endpoint}", False, "Backend no está corriendo"))
        except Exception as e:
            results.append((f"{method} {endpoint}", False, str(e)))
    
    for test_name, passed, details in results:
        print_test(test_name, passed, details)
    
    return results

def test_gemini_integration():
    """Prueba 3: Integración con Gemini AI"""
    print_header("PRUEBA 3: GEMINI AI")
    
    results = []
    
    # Test 3.1: API Key configurada
    api_key = os.getenv('GEMINI_API_KEY')
    has_key = api_key is not None and len(api_key) > 20
    results.append(("API Key configurada", has_key, "Falta en .env" if not has_key else ""))
    
    # Test 3.2: Importar google.generativeai
    try:
        import google.generativeai as genai
        results.append(("Librería google-generativeai", True, ""))
    except ImportError as e:
        results.append(("Librería google-generativeai", False, "pip install google-generativeai"))
    
    # Test 3.3: Configuración y conexión
    if has_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Intentar listar modelos
            models = list(genai.list_models())
            results.append(("Conexión API Gemini", True, f"{len(models)} modelos disponibles"))
            
            # Buscar modelo que soporte generateContent
            available = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
            if available:
                results.append(("Modelos para generación", True, f"{len(available)} disponibles"))
            else:
                results.append(("Modelos para generación", False, "No hay modelos disponibles"))
                
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower():
                results.append(("Conexión API Gemini", False, "Cuota excedida"))
            elif "leaked" in error_msg.lower():
                results.append(("Conexión API Gemini", False, "API Key bloqueada"))
            else:
                results.append(("Conexión API Gemini", False, error_msg[:100]))
    
    # Test 3.4: Servicios que usan Gemini
    app = create_app()
    with app.app_context():
        try:
            from app.services.academic.study_tools_service import StudyToolsService
            results.append(("Servicio StudyTools", True, ""))
        except Exception as e:
            results.append(("Servicio StudyTools", False, str(e)))
        
        try:
            from app.services.academic.writing_evaluator import WritingEvaluator
            results.append(("Servicio WritingEvaluator", True, ""))
        except Exception as e:
            results.append(("Servicio WritingEvaluator", False, str(e)))
    
    for test_name, passed, details in results:
        print_test(test_name, passed, details)
    
    return results

def test_file_handlers():
    """Prueba 4: Manejadores de archivos"""
    print_header("PRUEBA 4: MANEJADORES DE ARCHIVOS")
    
    results = []
    app = create_app()
    
    with app.app_context():
        # Test 4.1: PDFExtractor
        try:
            from app.services.document_processing.pdf_extractor import PDFExtractor
            results.append(("PDFExtractor", True, ""))
        except Exception as e:
            results.append(("PDFExtractor", False, str(e)))
        
        # Test 4.2: FileHandler
        try:
            from app.services.academic.file_handler import FileHandler
            results.append(("FileHandler", True, ""))
        except Exception as e:
            results.append(("FileHandler", False, str(e)))
        
        # Test 4.3: PDFGenerator
        try:
            from app.services.academic.pdf_generator import PDFGenerator
            results.append(("PDFGenerator", True, ""))
        except Exception as e:
            results.append(("PDFGenerator", False, str(e)))
        
        # Test 4.4: Verificar carpetas necesarias
        folders = [
            'uploads',
            'generated/pdf',
            'generated/docx',
            'generated/ppt',
            'generated/reports'
        ]
        
        for folder in folders:
            folder_path = os.path.join(os.path.dirname(__file__), folder)
            exists = os.path.exists(folder_path)
            results.append((f"Carpeta '{folder}'", exists, "No existe" if not exists else ""))
    
    for test_name, passed, details in results:
        print_test(test_name, passed, details)
    
    return results

def test_video_analysis():
    """Prueba 5: Análisis de video y emociones"""
    print_header("PRUEBA 5: ANÁLISIS DE VIDEO")
    
    results = []
    
    # Test 5.1: DeepFace
    try:
        from deepface import DeepFace
        results.append(("Librería DeepFace", True, ""))
    except ImportError:
        results.append(("Librería DeepFace", False, "pip install deepface"))
    
    # Test 5.2: TensorFlow
    try:
        import tensorflow as tf
        results.append(("TensorFlow", True, f"v{tf.__version__}"))
    except ImportError:
        results.append(("TensorFlow", False, "pip install tensorflow"))
    
    # Test 5.3: OpenCV
    try:
        import cv2
        results.append(("OpenCV", True, f"v{cv2.__version__}"))
    except ImportError:
        results.append(("OpenCV", False, "pip install opencv-python"))
    
    # Test 5.4: Servicio de reconocimiento de emociones
    app = create_app()
    with app.app_context():
        try:
            from app.services.video.emotion_recognition_service import EmotionRecognitionService
            results.append(("EmotionRecognitionService", True, ""))
        except Exception as e:
            results.append(("EmotionRecognitionService", False, str(e)))
    
    for test_name, passed, details in results:
        print_test(test_name, passed, details)
    
    return results

def test_frontend_files():
    """Prueba 6: Archivos del frontend"""
    print_header("PRUEBA 6: FRONTEND")
    
    results = []
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    
    # Test 6.1: Carpeta frontend existe
    exists = os.path.exists(frontend_path)
    results.append(("Carpeta frontend", exists, "No encontrada"))
    
    if exists:
        # Test 6.2: package.json
        package_json = os.path.join(frontend_path, 'package.json')
        results.append(("package.json", os.path.exists(package_json), ""))
        
        # Test 6.3: node_modules
        node_modules = os.path.join(frontend_path, 'node_modules')
        results.append(("node_modules", os.path.exists(node_modules), "Ejecutar: npm install"))
        
        # Test 6.4: Componentes principales
        components = [
            'src/App.jsx',
            'src/components/WritingEvaluator.jsx',
            'src/components/CreateTopicTimeline.jsx',
            'src/components/CreateEventsTimeline.jsx',
            'src/pages/AcademicDashboard.jsx',
            'src/pages/EventsTimelineView.jsx'
        ]
        
        for component in components:
            component_path = os.path.join(frontend_path, component)
            exists = os.path.exists(component_path)
            results.append((f"Componente {component}", exists, "No encontrado" if not exists else ""))
    
    # Test 6.5: Frontend corriendo
    try:
        response = requests.get("http://localhost:3000", timeout=2)
        results.append(("Frontend en localhost:3000", True, ""))
    except:
        try:
            response = requests.get("http://localhost:3001", timeout=2)
            results.append(("Frontend en localhost:3001", True, ""))
        except:
            results.append(("Frontend corriendo", False, "No está activo"))
    
    for test_name, passed, details in results:
        print_test(test_name, passed, details)
    
    return results

def generate_summary(all_results):
    """Genera resumen final"""
    print_header("RESUMEN DE PRUEBAS")
    
    total_tests = sum(len(results) for results in all_results)
    passed_tests = sum(sum(1 for _, passed, _ in results if passed) for results in all_results)
    failed_tests = total_tests - passed_tests
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total de pruebas: {Colors.BOLD}{total_tests}{Colors.RESET}")
    print(f"Exitosas: {Colors.GREEN}{passed_tests}{Colors.RESET}")
    print(f"Fallidas: {Colors.RED}{failed_tests}{Colors.RESET}")
    print(f"Tasa de éxito: {Colors.BOLD}{success_rate:.1f}%{Colors.RESET}\n")
    
    # Problemas críticos
    if failed_tests > 0:
        print(f"{Colors.RED}{Colors.BOLD}PROBLEMAS CRÍTICOS DETECTADOS:{Colors.RESET}\n")
        
        for category_results in all_results:
            for test_name, passed, details in category_results:
                if not passed and details:
                    print(f"  {Colors.RED}•{Colors.RESET} {test_name}: {Colors.YELLOW}{details}{Colors.RESET}")
    
    print("\n" + "="*70)
    
    if success_rate >= 80:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ SISTEMA MAYORMENTE FUNCIONAL{Colors.RESET}")
    elif success_rate >= 50:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  SISTEMA CON PROBLEMAS MODERADOS{Colors.RESET}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ SISTEMA CON PROBLEMAS CRÍTICOS{Colors.RESET}")
    
    print("="*70 + "\n")
    
    return success_rate

def main():
    """Ejecuta todas las pruebas"""
    print(f"\n{Colors.BOLD}{Colors.PURPLE}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║   SUITE DE PRUEBAS - PLATAFORMA RENDIMIENTO ESTUDIANTIL        ║")
    print("║   Análisis Completo de Módulos y Funcionalidades               ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_results = []
    
    try:
        # Ejecutar todas las pruebas
        all_results.append(test_database_connection())
        all_results.append(test_api_endpoints())
        all_results.append(test_gemini_integration())
        all_results.append(test_file_handlers())
        all_results.append(test_video_analysis())
        all_results.append(test_frontend_files())
        
        # Generar resumen
        success_rate = generate_summary(all_results)
        
        return 0 if success_rate >= 70 else 1
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Pruebas interrumpidas por el usuario{Colors.RESET}\n")
        return 1
    except Exception as e:
        print(f"\n\n{Colors.RED}Error durante las pruebas: {e}{Colors.RESET}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
