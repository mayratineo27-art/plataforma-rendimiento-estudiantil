"""
Script Maestro para Solucionar Nuevos Errores
Soluciona los errores mostrados en las últimas capturas:
1. No se pueden importar modelos (user, document, etc.)
2. Error en run.py: TypeError 'handle' must be a _ThreadHandle
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
║                  SOLUCIONADOR DE ERRORES ADICIONALES                          ║
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

def run_script(script_path):
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

def main():
    """Función principal"""
    print_banner()
    
    print(f"{Colors.YELLOW}NUEVOS PROBLEMAS DETECTADOS:{Colors.RESET}")
    print()
    print("  1. ❌ No se pueden importar modelos (user, document, etc.)")
    print("  2. ❌ Error en run.py: TypeError 'handle' must be a _ThreadHandle")
    print()
    print(f"{Colors.CYAN}Este script los solucionará automáticamente{Colors.RESET}")
    print()
    
    input(f"{Colors.CYAN}Presiona Enter para comenzar...{Colors.RESET}")
    
    # Verificar scripts necesarios
    scripts = [
        ('create_models.py', 'CREANDO MODELOS DEL BACKEND'),
        ('fix_run_py.py', 'CORRIGIENDO RUN.PY'),
    ]
    
    print_section("VERIFICANDO SCRIPTS")
    all_exist = True
    for script, _ in scripts:
        if Path(script).exists():
            print(f"{Colors.GREEN}✓ {script} encontrado{Colors.RESET}")
        else:
            print(f"{Colors.RED}✗ {script} NO encontrado{Colors.RESET}")
            all_exist = False
    
    if not all_exist:
        print(f"\n{Colors.RED}Error: Faltan algunos scripts{Colors.RESET}")
        return 1
    
    # Ejecutar scripts
    results = []
    total_steps = len(scripts)
    
    for i, (script, description) in enumerate(scripts, 1):
        print_step(i, total_steps, description)
        
        success = run_script(script)
        results.append((description, success))
        
        if success:
            print(f"\n{Colors.GREEN}✓ Paso {i} completado{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}⚠ Paso {i} con problemas{Colors.RESET}")
        
        if i < total_steps:
            input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.RESET}")
    
    # Resumen
    print_section("RESUMEN")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for step, success in results:
        if success:
            print(f"{Colors.GREEN}✓ {step}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠ {step}{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}Resultado: {passed}/{total} pasos completados{Colors.RESET}\n")
    
    if passed == total:
        print(f"""
{Colors.GREEN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      ¡ERRORES SOLUCIONADOS EXITOSAMENTE!                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.CYAN}Ahora puedes:{Colors.RESET}

1. Ejecutar tests para verificar:
   {Colors.YELLOW}python test_backend_diagnostics.py{Colors.RESET}

2. Iniciar el servidor:
   {Colors.YELLOW}cd backend{Colors.RESET}
   {Colors.YELLOW}python run.py{Colors.RESET}

3. Probar en el navegador:
   {Colors.GREEN}http://localhost:5000{Colors.RESET}
   {Colors.GREEN}http://localhost:5000/health{Colors.RESET}

{Colors.GREEN}¡Tu backend debería funcionar perfectamente ahora!{Colors.RESET}
""")
    else:
        print(f"""
{Colors.YELLOW}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        ALGUNOS PASOS FALLARON                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.CYAN}Revisa los errores arriba y:{Colors.RESET}

1. Verifica que la carpeta backend/app/models existe
2. Verifica que el archivo backend/run.py existe
3. Ejecuta los scripts individuales si es necesario:
   {Colors.YELLOW}python create_models.py{Colors.RESET}
   {Colors.YELLOW}python fix_run_py.py{Colors.RESET}
""")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Script interrumpido{Colors.RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}\n")
        sys.exit(1)
