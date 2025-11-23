from functools import wraps
from flask import request, jsonify
from app.utils.logger import logger

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("No authorization header")
            return jsonify({
                'success': False,
                'error': 'No autorizado',
                'message': 'Se requiere autenticación'
            }), 401
            
        try:
            # Aquí va tu lógica de validación del token
            token = auth_header.split(' ')[1]
            # validate_token(token)
            
        except Exception as e:
            logger.error(f"Error de autenticación: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Token inválido',
                'message': 'La sesión ha expirado o es inválida'
            }), 401
            
        return f(*args, **kwargs)
    return decorated