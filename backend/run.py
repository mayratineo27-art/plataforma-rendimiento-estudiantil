"""
Punto de entrada de la aplicación
Plataforma Integral de Rendimiento Estudiantil
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║  Plataforma Integral de Rendimiento Estudiantil             ║
    ║  Backend Server Starting...                                  ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🚀 Servidor corriendo en: http://localhost:{port}
    🔧 Modo: development
    
    Presiona CTRL+C para detener el servidor
    """)
    
    try:
        # Intentar usar waitress (mejor para Windows)
        from waitress import serve
        print("    ✓ Usando servidor Waitress")
        print()
        serve(app, host='127.0.0.1', port=port)
    except ImportError:
        print("    ⚠️  Waitress no instalado, instalando...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'waitress'])
        from waitress import serve
        print("    ✓ Waitress instalado y ejecutando")
        print()
        serve(app, host='127.0.0.1', port=port)