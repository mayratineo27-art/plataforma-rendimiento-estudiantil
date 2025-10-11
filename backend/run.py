## # Punto de entrada
"""
run.py - Punto de entrada principal para la aplicación Flask
Plataforma Integral de Rendimiento Estudiantil
"""

import os
from app import create_app
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Flask
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Configuración del servidor
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║  Plataforma Integral de Rendimiento Estudiantil             ║
    ║  Backend Server Starting...                                  ║
    ╚══════════════════════════════════════════════════════════════╝
    
    🚀 Servidor corriendo en: http://{host}:{port}
    🔧 Modo: {os.getenv('FLASK_ENV', 'development')}
    🐛 Debug: {debug}
    📚 Documentación API: http://{host}:{port}/api/docs
    
    Presiona CTRL+C para detener el servidor
    """)
    
    # Iniciar el servidor
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )