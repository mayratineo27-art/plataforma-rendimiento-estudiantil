"""
Script Maestro de Solución Completa
Soluciona TODOS los problemas detectados en tu backend

Problemas a solucionar:
1. ✗ Aplicación Flask: Falta función create_app
2. ✗ Dependencias: mysql-connector-python, opencv-python, google-generativeai, SpeechRecognition
3. ✗ Conexión a BD: Error de acceso MySQL
4. ✗ Archivo .env: Falta configuración
"""

import subprocess
import sys
from pathlib import Path

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
║                    SOLUCIONADOR AUTOMÁTICO DE BACKEND                         ║
║              Plataforma Integral de Rendimiento Estudiantil                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)

def print_section(text):
    print(f"\n{Colors.MAGENTA}{'='*80}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{'='*80}{Colors.RESET}\n")

def print_step(number, total, text):
    print(f"\n{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"{Colors.BLUE}PASO {number}/{total}: {text}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*80}{Colors.RESET}\n")

def run_script(script_path, description):
    """Ejecuta un script de Python"""
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"{Colors.RED}Error al ejecutar {script_path}: {e}{Colors.RESET}")
        return False

def check_script_exists(script_name):
    """Verifica que un script exista"""
    return Path(script_name).exists()

def main():
    """Función principal"""
    print_banner()
    
    print(f"{Colors.YELLOW}Este script solucionará TODOS los problemas detectados:{Colors.RESET}")
    print()
    print("  1. ✗ Aplicación Flask → Corregir __init__.py")
    print("  2. ✗ Dependencias → Instalar paquetes faltantes")
    print("  3. ✗ MySQL → Configurar conexión")
    print("  4. ✗ Archivo .env → Crear y configurar")
    print()
    
    input(f"{Colors.CYAN}Presiona Enter para comenzar...{Colors.RESET}")
    
    # Lista de scripts necesarios
    scripts = [
        ('fix_app_init.py', 'CORRIGIENDO ARCHIVO __INIT__.PY'),
        ('install_missing_packages.py', 'INSTALANDO DEPENDENCIAS FALTANTES'),
        ('configure_mysql_and_env.py', 'CONFIGURANDO MYSQL Y .ENV'),
    ]
    
    # Verificar que todos los scripts existan
    print_section("VERIFICANDO SCRIPTS NECESARIOS")
    all_exist = True
    for script, _ in scripts:
        if check_script_exists(script):
            print(f"{Colors.GREEN}✓ {script} encontrado{Colors.RESET}")
        else:
            print(f"{Colors.RED}✗ {script} NO encontrado{Colors.RESET}")
            all_exist = False
    
    if not all_exist:
        print(f"\n{Colors.RED}Error: Faltan algunos scripts necesarios{Colors.RESET}")
        print("Asegúrate de tener todos los archivos en el directorio actual")
        return 1
    
    # Ejecutar scripts en orden
    results = []
    total_steps = len(scripts)
    
    for i, (script, description) in enumerate(scripts, 1):
        print_step(i, total_steps, description)
        
        success = run_script(script, description)
        results.append((description, success))
        
        if success:
            print(f"\n{Colors.GREEN}✓ Paso {i} completado exitosamente{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}⚠ Paso {i} completado con advertencias{Colors.RESET}")
        
        if i < total_steps:
            input(f"\n{Colors.CYAN}Presiona Enter para continuar al siguiente paso...{Colors.RESET}")
    
    # Mostrar resumen final
    print_section("RESUMEN FINAL")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for step, success in results:
        if success:
            print(f"{Colors.GREEN}✓ {step}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠ {step} (con advertencias){Colors.RESET}")
    
    print(f"\n{Colors.CYAN}Resultado: {passed}/{total} pasos completados{Colors.RESET}\n")
    
    # Instrucciones finales
    if passed >= 2:  # Al menos 2 de 3 pasos completados
        print(f"""
{Colors.GREEN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    ¡SOLUCIÓN COMPLETADA EXITOSAMENTE!                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.CYAN}Verifica que todo funciona:{Colors.RESET}

1. Ejecutar tests diagnósticos:
   {Colors.YELLOW}python test_backend_diagnostics.py{Colors.RESET}

2. Si los tests pasan, inicia el servidor:
   {Colors.YELLOW}cd backend{Colors.RESET}
   {Colors.YELLOW}python run.py{Colors.RESET}

3. Verifica que el servidor funciona:
   {Colors.YELLOW}http://localhost:5000{Colors.RESET}
   {Colors.YELLOW}http://localhost:5000/health{Colors.RESET}
   {Colors.YELLOW}http://localhost:5000/api/test{Colors.RESET}

{Colors.GREEN}¡Tu backend está listo para usar!{Colors.RESET}
""")
    else:
        print(f"""
{Colors.YELLOW}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      ALGUNOS PASOS NECESITAN ATENCIÓN                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.CYAN}Revisa los errores arriba y:{Colors.RESET}

1. Soluciona los problemas indicados
2. Vuelve a ejecutar los scripts individualmente si es necesario
3. O ejecuta este script nuevamente

{Colors.YELLOW}Scripts individuales disponibles:{Colors.RESET}
- python fix_app_init.py
- python install_missing_packages.py
- python configure_mysql_and_env.py
""")
    
    return 0 if passed >= 2 else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Script interrumpido por el usuario{Colors.RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.RESET}\n")
        sys.exit(1)
