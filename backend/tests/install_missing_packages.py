"""
Script para instalar las dependencias faltantes
"""

import subprocess
import sys

# Lista de paquetes faltantes según el diagnóstico
MISSING_PACKAGES = [
    'mysql-connector-python',
    'opencv-python', 
    'google-generativeai',
    'SpeechRecognition'
]

def install_package(package_name):
    """Instala un paquete usando pip"""
    print(f"\n📦 Instalando {package_name}...")
    try:
        subprocess.check_call([
            sys.executable, 
            '-m', 
            'pip', 
            'install', 
            package_name,
            '--break-system-packages'  # Para sistemas que requieren esta flag
        ])
        print(f"✅ {package_name} instalado correctamente")
        return True
    except subprocess.CalledProcessError:
        # Intentar sin --break-system-packages
        try:
            subprocess.check_call([
                sys.executable, 
                '-m', 
                'pip', 
                'install', 
                package_name
            ])
            print(f"✅ {package_name} instalado correctamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al instalar {package_name}: {e}")
            return False

def main():
    """Función principal"""
    print("="*80)
    print("INSTALANDO DEPENDENCIAS FALTANTES")
    print("="*80)
    print()
    print("Paquetes a instalar:")
    for pkg in MISSING_PACKAGES:
        print(f"  • {pkg}")
    print()
    
    results = {}
    for package in MISSING_PACKAGES:
        results[package] = install_package(package)
    
    print()
    print("="*80)
    print("RESUMEN DE INSTALACIÓN")
    print("="*80)
    print()
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for package, success in results.items():
        status = "✅ OK" if success else "❌ FALLO"
        print(f"{status}: {package}")
    
    print()
    print(f"Resultado: {success_count}/{total_count} paquetes instalados")
    print()
    
    if success_count == total_count:
        print("🎉 ¡Todas las dependencias instaladas exitosamente!")
        print()
        print("Próximo paso: Configurar MySQL")
        print("  1. Verifica que MySQL esté corriendo")
        print("  2. Crea la base de datos:")
        print("     mysql -u root -p")
        print("     CREATE DATABASE plataforma_estudiantil;")
        print("  3. Configura el archivo .env")
    else:
        print("⚠️ Algunas dependencias no se instalaron")
        print("Intenta instalarlas manualmente:")
        for package, success in results.items():
            if not success:
                print(f"  pip install {package}")

if __name__ == "__main__":
    main()
