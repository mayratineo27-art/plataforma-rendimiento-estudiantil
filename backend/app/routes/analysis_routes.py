# ============================================
# app/routes/analysis_routes.py
# ============================================

from flask import Blueprint, jsonify

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/progress/<int:user_id>', methods=['GET'])
def get_progress_analysis(user_id):
    '''Obtener análisis de progreso del estudiante'''
    return jsonify({
        'message': 'Endpoint de análisis de progreso - Módulo 1'
    }), 501

@analysis_bp.route('/compare', methods=['POST'])
def compare_documents():
    '''Comparar múltiples documentos'''
    return jsonify({
        'message': 'Endpoint de comparación de documentos - Módulo 1'
    }), 501


@analysis_bp.route('/test', methods=['GET'])
def test():
    return {'message': 'Analysis routes working'}