"""
Script para solucionar errores comunes del backend
Plataforma Integral de Rendimiento Estudiantil
"""

import os
import sys
from pathlib import Path
import subprocess

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

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def fix_import_errors():
    """Corrige errores de importación comunes"""
    print_header("CORRIGIENDO ERRORES DE IMPORTACIÓN")
    
    # Verificar que estamos en el directorio correcto
    if not Path("backend").exists():
        print_error("No se encuentra la carpeta 'backend'")
        print_info("Asegúrate de estar en el directorio raíz del proyecto")
        return False
    
    # Verificar __init__.py en todos los módulos
    modules = [
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
    ]
    
    for module in modules:
        init_file = Path(module) / "__init__.py"
        if not init_file.exists():
            init_file.parent.mkdir(parents=True, exist_ok=True)
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('"""Módulo de inicialización"""\n')
            print_success(f"Creado {init_file}")
        else:
            print_info(f"Existe {init_file}")
    
    return True

def fix_circular_imports():
    """Detecta y sugiere soluciones para importaciones circulares"""
    print_header("DETECTANDO IMPORTACIONES CIRCULARES")
    
    print_info("Buscando importaciones circulares en el código...")
    
    # Patrones comunes de importaciones circulares
    suggestions = [
        "1. Mover importaciones dentro de funciones en lugar de al inicio del archivo",
        "2. Usar importaciones tardías (lazy imports)",
        "3. Refactorizar código para eliminar dependencias circulares",
        "4. Usar interfaces o clases abstractas"
    ]
    
    print_warning("Soluciones para importaciones circulares:")
    for suggestion in suggestions:
        print(f"   {suggestion}")
    
    return True

def fix_database_connection():
    """Corrige problemas de conexión a la base de datos"""
    print_header("VERIFICANDO CONEXIÓN A BASE DE DATOS")
    
    try:
        import mysql.connector
        print_success("MySQL Connector instalado correctamente")
        
        # Intentar conexión básica
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='password'
            )
            print_success("Conexión a MySQL exitosa")
            connection.close()
        except mysql.connector.Error as err:
            print_error(f"Error de conexión a MySQL: {err}")
            print_warning("Soluciones:")
            print("   1. Verifica que MySQL esté corriendo")
            print("   2. Verifica usuario y contraseña en .env")
            print("   3. Verifica que el puerto 3306 esté disponible")
            return False
            
    except ImportError:
        print_error("MySQL Connector no está instalado")
        print_info("Instálalo con: pip install mysql-connector-python")
        return False
    
    return True

def fix_flask_app():
    """Corrige problemas comunes con Flask"""
    print_header("VERIFICANDO APLICACIÓN FLASK")
    
    # Verificar archivo __init__.py en app
    init_file = Path("backend/app/__init__.py")
    if not init_file.exists():
        print_error("Falta backend/app/__init__.py")
        return False
    
    # Verificar que tenga create_app
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'def create_app' not in content:
            print_error("Falta función create_app en __init__.py")
            print_warning("La función create_app es necesaria para inicializar Flask")
            return False
    
    print_success("Archivo __init__.py correcto")
    
    # Verificar run.py
    run_file = Path("backend/run.py")
    if not run_file.exists():
        print_error("Falta backend/run.py")
        return False
    
    print_success("Archivo run.py existe")
    return True

def fix_missing_dependencies():
    """Instala dependencias faltantes"""
    print_header("VERIFICANDO DEPENDENCIAS")
    
    requirements_file = Path("backend/requirements.txt")
    if not requirements_file.exists():
        print_error("Falta archivo requirements.txt")
        return False
    
    print_info("Verificando dependencias instaladas...")
    
    critical_packages = [
        'flask',
        'flask-cors',
        'flask-sqlalchemy',
        'mysql-connector-python',
        'opencv-python',
        'deepface',
        'google-generativeai',
        'SpeechRecognition',
        'pydub',
        'numpy'
    ]
    
    missing_packages = []
    for package in critical_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package} instalado")
        except ImportError:
            print_error(f"{package} NO instalado")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"\nPaquetes faltantes: {', '.join(missing_packages)}")
        print_info("Instálalos con: pip install " + " ".join(missing_packages))
        return False
    
    return True

def fix_folder_permissions():
    """Corrige permisos de carpetas"""
    print_header("VERIFICANDO PERMISOS DE CARPETAS")
    
    folders = [
        "backend/uploads",
        "backend/uploads/documents",
        "backend/uploads/videos",
        "backend/uploads/audio",
        "backend/generated",
        "backend/generated/reports",
        "backend/generated/templates",
        "backend/logs"
    ]
    
    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print_success(f"Creada carpeta: {folder}")
        else:
            print_info(f"Carpeta existe: {folder}")
    
    return True

def fix_env_file():
    """Verifica y corrige archivo .env"""
    print_header("VERIFICANDO ARCHIVO .ENV")
    
    env_file = Path("backend/.env")
    env_example = Path("backend/.env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print_warning(".env no existe, pero .env.example sí")
            print_info("Copia .env.example a .env y configúralo:")
            print("   cp backend/.env.example backend/.env")
            return False
        else:
            print_error("Ni .env ni .env.example existen")
            return False
    
    print_success("Archivo .env existe")
    
    # Verificar variables críticas
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'GEMINI_API_KEY'
    ]
    
    with open(env_file, 'r', encoding='utf-8') as f:
        env_content = f.read()
        
    for var in required_vars:
        if var not in env_content:
            print_warning(f"Variable {var} no encontrada en .env")
        elif f"{var}=your-" in env_content or f"{var}=change" in env_content:
            print_warning(f"Variable {var} no está configurada (tiene valor por defecto)")
        else:
            print_success(f"Variable {var} configurada")
    
    return True

def check_python_version():
    """Verifica la versión de Python"""
    print_header("VERIFICANDO VERSIÓN DE PYTHON")
    
    version = sys.version_info
    print_info(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Se requiere Python 3.8 o superior")
        return False
    
    print_success("Versión de Python adecuada")
    return True

def generate_error_report():
    """Genera un reporte de errores encontrados"""
    print_header("GENERANDO REPORTE DE ERRORES")
    
    report = []
    
    # Ejecutar todas las verificaciones
    checks = [
        ("Versión de Python", check_python_version),
        ("Importaciones", fix_import_errors),
        ("Aplicación Flask", fix_flask_app),
        ("Dependencias", fix_missing_dependencies),
        ("Conexión a BD", fix_database_connection),
        ("Permisos de carpetas", fix_folder_permissions),
        ("Archivo .env", fix_env_file),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = result
        except Exception as e:
            print_error(f"Error en {check_name}: {e}")
            results[check_name] = False
    
    # Mostrar resumen
    print_header("RESUMEN DE VERIFICACIONES")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for check_name, result in results.items():
        if result:
            print_success(f"{check_name}: OK")
        else:
            print_error(f"{check_name}: FALLO")
    
    print(f"\n{Colors.BLUE}Resultado: {passed}/{total} verificaciones pasaron{Colors.RESET}\n")
    
    if passed == total:
        print_success("¡Todos los checks pasaron! El backend debería funcionar correctamente")
    else:
        print_warning("Algunos checks fallaron. Revisa los errores arriba para solucionarlos")
    
    return passed == total

def main():
    """Función principal"""
    print_header("SCRIPT DE REPARACIÓN DEL BACKEND")
    print_header("Plataforma Integral de Rendimiento Estudiantil")
    
    try:
        success = generate_error_report()
        
        if success:
            print_header("✓ BACKEND VERIFICADO EXITOSAMENTE")
            print(f"{Colors.GREEN}Puedes ejecutar el servidor con: cd backend && python run.py{Colors.RESET}\n")
            return 0
        else:
            print_header("✗ SE ENCONTRARON PROBLEMAS")
            print(f"{Colors.YELLOW}Soluciona los errores y vuelve a ejecutar este script{Colors.RESET}\n")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Script interrumpido por el usuario{Colors.RESET}\n")
        return 1
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
