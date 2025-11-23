"""
Rutas del Dashboard - Núcleo de Comando
"""

from flask import Blueprint
from app.controllers.dashboard_controller import (
    get_dashboard_metrics,
    get_system_health,
    get_processing_statistics
)

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/metrics', methods=['GET'])
def dashboard_metrics():
    """
    GET /api/dashboard/metrics
    Obtiene todas las métricas del dashboard
    
    Por ahora usa user_id=1 por defecto
    En producción, esto vendría del token JWT
    """
    user_id = 1  # TODO: Obtener de JWT cuando tengamos autenticación
    return get_dashboard_metrics(user_id)


@dashboard_bp.route('/health', methods=['GET'])
def system_health():
    """
    GET /api/dashboard/health
    Verifica el estado de salud del sistema
    """
    return get_system_health()


@dashboard_bp.route('/statistics', methods=['GET'])
def processing_statistics():
    """
    GET /api/dashboard/statistics
    Obtiene estadísticas detalladas de procesamiento
    """
    user_id = 1  # TODO: Obtener de JWT
    return get_processing_statistics(user_id)


@dashboard_bp.route('/pipeline/<int:modulo_id>', methods=['GET'])
def pipeline_status(modulo_id):
    """
    GET /api/dashboard/pipeline/<modulo_id>
    Obtiene el estado detallado de un módulo específico
    """
    # TODO: Implementar endpoint específico por módulo
    return {
        'modulo': modulo_id,
        'status': 'active',
        'message': 'Endpoint en desarrollo'
    }, 200
