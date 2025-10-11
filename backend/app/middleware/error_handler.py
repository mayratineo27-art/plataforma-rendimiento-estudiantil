"""
app/middleware/error_handler.py - Manejadores de Errores
Plataforma Integral de Rendimiento Estudiantil
"""

from flask import jsonify
import traceback
import logging

logger = logging.getLogger(__name__)


def handle_404(error):
    """Manejador para errores 404 - No Encontrado"""
    return jsonify({
        'error': 'Not Found',
        'message': 'El recurso solicitado no existe',
        'status': 404
    }), 404


def handle_400(error):
    """Manejador para errores 400 - Bad Request"""
    return jsonify({
        'error': 'Bad Request',
        'message': 'La solicitud no es válida',
        'status': 400
    }), 400


def handle_403(error):
    """Manejador para errores 403 - Forbidden"""
    return jsonify({
        'error': 'Forbidden',
        'message': 'No tienes permisos para acceder a este recurso',
        'status': 403
    }), 403


def handle_500(error):
    """Manejador para errores 500 - Internal Server Error"""
    logger.error(f"Error 500: {str(error)}")
    logger.error(traceback.format_exc())
    
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Ha ocurrido un error interno en el servidor',
        'status': 500
    }), 500


def handle_validation_error(error):
    """Manejador para errores de validación"""
    return jsonify({
        'error': 'Validation Error',
        'message': str(error),
        'status': 422
    }), 422


class APIError(Exception):
    """Excepción personalizada para errores de API"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['error'] = True
        rv['status'] = self.status_code
        return rv