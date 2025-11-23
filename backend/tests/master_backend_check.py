"""
Script Maestro de Diagnóstico y Reparación del Backend
Plataforma Integral de Rendimiento Estudiantil

Este script ejecuta todos los diagnósticos y reparaciones necesarias
"""

import sys
import os
from pathlib import Path
import subprocess

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def print_banner():
    banner = f"""
{Colors.CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              PLATAFORMA INTEGRAL DE RENDIMIENTO ESTUDIANTIL                   ║
║                    Diagnóstico y Reparación del Backend                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)

def print_section(text):
    print(f"\n{Colors.MAGENTA}{'='*80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{'='*80}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def run_script(script_name, description):
    """Ejecuta un script de Python"""
    print_section(description)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"{description} completado exitosamente")
            return True
        else:
            print_error(f"{description} falló con código {result.returncode}")
            return False
            
    except Exception as e:
        print_error(f"Error al ejecutar {script_name}: {e}")
        return False

def check_prerequisites():
    """Verifica que los scripts necesarios existan"""
    print_section("VERIFICANDO PRERREQUISITOS")
    
    scripts = [
        'setup_backend_structure.py',
        'fix_backend_errors.py',
        'test_backend_diagnostics.py'
    ]
    
    all_exist = True
    for script in scripts:
        if Path(script).exists():
            print_success(f"Script encontrado: {script}")
        else:
            print_error(f"Script NO encontrado: {script}")
            all_exist = False
    
    return all_exist

def display_menu():
    """Muestra el menú de opciones"""
    print(f"\n{Colors.CYAN}¿Qué deseas hacer?{Colors.RESET}\n")
    print(f"{Colors.YELLOW}1.{Colors.RESET} Ejecutar TODOS los pasos (Recomendado)")
    print(f"{Colors.YELLOW}2.{Colors.RESET} Solo generar/reparar estructura del backend")
    print(f"{Colors.YELLOW}3.{Colors.RESET} Solo ejecutar verificación y reparación de errores")
    print(f"{Colors.YELLOW}4.{Colors.RESET} Solo ejecutar tests diagnósticos")
    print(f"{Colors.YELLOW}5.{Colors.RESET} Mostrar información del sistema")
    print(f"{Colors.YELLOW}0.{Colors.RESET} Salir")
    print()

def show_system_info():
    """Muestra información del sistema"""
    print_section("INFORMACIÓN DEL SISTEMA")
    
    # Python
    print(f"{Colors.CYAN}Python:{Colors.RESET}")
    print(f"  Versión: {sys.version}")
    print(f"  Ejecutable: {sys.executable}")
    
    # Directorio actual
    print(f"\n{Colors.CYAN}Directorio de trabajo:{Colors.RESET}")
    print(f"  {os.getcwd()}")
    
    # Verificar estructura
    print(f"\n{Colors.CYAN}Estructura del proyecto:{Colors.RESET}")
    if Path("backend").exists():
        print_success("Carpeta 'backend' existe")
        if Path("backend/app").exists():
            print_success("Carpeta 'backend/app' existe")
        else:
            print_warning("Carpeta 'backend/app' NO existe")
        
        if Path("backend/run.py").exists():
            print_success("Archivo 'backend/run.py' existe")
        else:
            print_warning("Archivo 'backend/run.py' NO existe")
    else:
        print_error("Carpeta 'backend' NO existe")
    
    # Dependencias críticas
    print(f"\n{Colors.CYAN}Dependencias críticas:{Colors.RESET}")
    critical_packages = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('mysql.connector', 'MySQL Connector'),
        ('cv2', 'OpenCV'),
        ('deepface', 'DeepFace'),
        ('google.generativeai', 'Google Generative AI'),
        ('speech_recognition', 'SpeechRecognition'),
    ]
    
    for package_name, display_name in critical_packages:
        try:
            pkg = __import__(package_name)
            version = getattr(pkg, '__version__', 'instalado')
            print_success(f"{display_name}: {version}")
        except ImportError:
            print_error(f"{display_name}: NO instalado")

def run_all_steps():
    """Ejecuta todos los pasos en orden"""
    print_section("EJECUTANDO PROCESO COMPLETO")
    
    steps = [
        ('setup_backend_structure.py', 'Paso 1: Generación de Estructura'),
        ('fix_backend_errors.py', 'Paso 2: Verificación y Reparación'),
        ('test_backend_diagnostics.py', 'Paso 3: Tests Diagnósticos'),
    ]
    
    results = []
    for script, description in steps:
        if Path(script).exists():
            success = run_script(script, description)
            results.append((description, success))
        else:
            print_error(f"Script {script} no encontrado - saltando")
            results.append((description, False))
    
    # Mostrar resumen final
    print_section("RESUMEN FINAL")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for step, success in results:
        if success:
            print_success(step)
        else:
            print_error(step)
    
    print(f"\n{Colors.CYAN}Resultado: {passed}/{total} pasos completados exitosamente{Colors.RESET}\n")
    
    if passed == total:
        print(f"""
{Colors.GREEN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         ¡PROCESO COMPLETADO EXITOSAMENTE!                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.CYAN}Próximos pasos:{Colors.RESET}

1. Configura tu archivo .env:
   {Colors.YELLOW}cp backend/.env.example backend/.env{Colors.RESET}
   {Colors.YELLOW}# Luego edita backend/.env con tus configuraciones{Colors.RESET}

2. Instala las dependencias (si aún no lo has hecho):
   {Colors.YELLOW}pip install -r backend/requirements.txt{Colors.RESET}

3. Inicia el servidor:
   {Colors.YELLOW}cd backend{Colors.RESET}
   {Colors.YELLOW}python run.py{Colors.RESET}

4. El servidor estará disponible en:
   {Colors.GREEN}http://localhost:5000{Colors.RESET}

5. Verifica que funciona:
   {Colors.YELLOW}curl http://localhost:5000/health{Colors.RESET}

{Colors.CYAN}Documentación:{Colors.RESET}
- README: backend/README.md
- Estructura: Revisar carpetas en backend/
- Tests: backend/tests/

{Colors.GREEN}¡Tu backend está listo para usar!{Colors.RESET}
""")
    else:
        print(f"""
{Colors.YELLOW}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     ALGUNOS PASOS NECESITAN ATENCIÓN                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.CYAN}Revisa los errores arriba y:{Colors.RESET}

1. Soluciona los problemas indicados
2. Vuelve a ejecutar este script
3. O ejecuta pasos individuales desde el menú

{Colors.YELLOW}Si necesitas ayuda, revisa:{Colors.RESET}
- Los mensajes de error arriba
- La documentación en backend/README.md
- Los logs en backend/logs/
""")

def main():
    """Función principal"""
    print_banner()
    
    # Verificar prerrequisitos
    if not check_prerequisites():
        print_error("\nFaltan algunos scripts necesarios")
        print_info("Asegúrate de tener todos los archivos en el directorio actual")
        return 1
    
    while True:
        display_menu()
        
        try:
            choice = input(f"{Colors.CYAN}Selecciona una opción (0-5): {Colors.RESET}").strip()
            
            if choice == '0':
                print(f"\n{Colors.CYAN}¡Hasta luego!{Colors.RESET}\n")
                return 0
                
            elif choice == '1':
                run_all_steps()
                input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.RESET}")
                
            elif choice == '2':
                run_script('setup_backend_structure.py', 'Generación de Estructura')
                input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.RESET}")
                
            elif choice == '3':
                run_script('fix_backend_errors.py', 'Verificación y Reparación')
                input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.RESET}")
                
            elif choice == '4':
                run_script('test_backend_diagnostics.py', 'Tests Diagnósticos')
                input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.RESET}")
                
            elif choice == '5':
                show_system_info()
                input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.RESET}")
                
            else:
                print_error("Opción no válida. Por favor selecciona 0-5")
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Script interrumpido por el usuario{Colors.RESET}\n")
            return 1
        except Exception as e:
            print_error(f"Error: {e}")
            return 1

if __name__ == "__main__":
    sys.exit(main())
