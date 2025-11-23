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
    
    # Usar Flask directamente (temporalmente para debug)
    print("    ✓ Usando servidor Flask")
    print()
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)