"""
Sistema de Logging para la aplicación
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Crear carpeta de logs si no existe
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Configurar logger
logger = logging.getLogger('plataforma_rendimiento')
logger.setLevel(logging.DEBUG)

# Formato de logs
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Handler para archivo
log_file = os.path.join(LOGS_DIR, 'app.log')
file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Agregar handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.propagate = False