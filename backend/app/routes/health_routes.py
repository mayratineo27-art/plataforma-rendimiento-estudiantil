# backend/app/routes/health_routes.py
# Endpoint simple para verificar que el backend está funcionando

from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificación de salud del servidor.
    Usado por Cypress para verificar que el backend está corriendo.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Backend is running',
        'service': 'Plataforma Integral de Rendimiento Estudiantil'
    }), 200

@health_bp.route('/', methods=['GET'])
def root():
    """
    Endpoint raíz del backend.
    """
    return jsonify({
        'message': 'Plataforma Integral de Rendimiento Estudiantil API',
        'version': '1.0.0',
        'status': 'online'
    }), 200