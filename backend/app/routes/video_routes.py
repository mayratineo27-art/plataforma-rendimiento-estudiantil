# ============================================
# app/routes/video_routes.py - Módulo 2
# ============================================

from flask import Blueprint, jsonify

video_bp = Blueprint('video', __name__)

@video_bp.route('/session/start', methods=['POST'])
def start_video_session():
    '''Iniciar una sesión de análisis de video'''
    return jsonify({
        'message': 'Endpoint para iniciar sesión de video - Módulo 2'
    }), 501

@video_bp.route('/session/<int:session_id>/frame', methods=['POST'])
def process_frame(session_id):
    '''Procesar un frame de video y analizar emociones'''
    return jsonify({
        'message': f'Endpoint para procesar frame de sesión {session_id} - Módulo 2'
    }), 501

@video_bp.route('/session/<int:session_id>/end', methods=['POST'])
def end_video_session(session_id):
    '''Finalizar sesión de video'''
    return jsonify({
        'message': f'Endpoint para finalizar sesión {session_id} - Módulo 2'
    }), 501

@video_bp.route('/session/<int:session_id>/emotions', methods=['GET'])
def get_session_emotions(session_id):
    '''Obtener timeline de emociones de una sesión'''
    return jsonify({
        'message': f'Endpoint de emociones de sesión {session_id} - Módulo 2'
    }), 501

@video_bp.route('/session/<int:session_id>/attention', methods=['GET'])
def get_attention_metrics(session_id):
    '''Obtener métricas de atención de una sesión'''
    return jsonify({
        'message': f'Endpoint de atención de sesión {session_id} - Módulo 2'
    }), 501

@video_bp.route('/test', methods=['GET'])
def test():
    return {'message': 'Video routes working'}