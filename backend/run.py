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
    🔧 Modo: development (DEBUG ACTIVADO)
    
    Presiona CTRL+C para detener el servidor
    """)
    
    # Configurar logging
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    
    print("    ✓ Usando servidor Flask con DEBUG")
    print("    ✓ Logging activado\n")
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)