"""
Script para corregir run.py
Soluciona: TypeError 'handle' must be a _ThreadHandle
"""

from pathlib import Path

RUN_PY_CONTENT = '''"""
Punto de entrada de la aplicación
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"\\n{'='*60}")
    print(f"Servidor corriendo en: http://localhost:{port}")
    print(f"Modo debug: {debug}")
    print(f"{'='*60}\\n")
    
    # IMPORTANTE: NO usar host='0.0.0.0' ni threaded=True en Windows
    # Estos parámetros causan el error: 'handle' must be a _ThreadHandle
    
    app.run(
        host='127.0.0.1',  # Usar 127.0.0.1 en lugar de 0.0.0.0
        port=port,
        debug=debug,
        use_reloader=True  # Permitir hot reload en desarrollo
    )
'''

def fix_run_py():
    """Corrige el archivo run.py"""
    print("="*80)
    print("CORRIGIENDO ARCHIVO backend/run.py")
    print("="*80)
    print()
    
    run_file = Path("backend/run.py")
    
    if not run_file.exists():
        print("❌ Error: No existe backend/run.py")
        return False
    
    # Backup
    backup_file = Path("backend/run.py.backup")
    print(f"📋 Creando backup: {backup_file}")
    with open(run_file, 'r', encoding='utf-8') as f:
        backup_content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(backup_content)
    
    # Corregir archivo
    print(f"✏️ Corrigiendo: {run_file}")
    with open(run_file, 'w', encoding='utf-8') as f:
        f.write(RUN_PY_CONTENT)
    
    print("✅ Archivo run.py corregido exitosamente")
    print()
    print("Cambios realizados:")
    print("  ✓ host='127.0.0.1' (en lugar de '0.0.0.0')")
    print("  ✓ Removido parámetro threaded")
    print("  ✓ Añadido use_reloader para desarrollo")
    print()
    print("Esto soluciona el error:")
    print("  TypeError: 'handle' must be a _ThreadHandle")
    print()
    
    return True

if __name__ == "__main__":
    success = fix_run_py()
    if success:
        print("🎉 ¡run.py corregido!")
        print()
        print("Ahora puedes iniciar el servidor:")
        print("  cd backend")
        print("  python run.py")
    else:
        print("❌ No se pudo corregir run.py")
