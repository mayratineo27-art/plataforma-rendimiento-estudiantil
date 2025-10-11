
# ============================================
# app/routes/audio_routes.py - Módulo 2
# ============================================

from flask import Blueprint, jsonify

audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/session/<int:session_id>/upload', methods=['POST'])
def upload_audio(session_id):
    '''Subir audio para transcripción'''
    return jsonify({
        'message': f'Endpoint para subir audio de sesión {session_id} - Módulo 2'
    }), 501

@audio_bp.route('/session/<int:session_id>/transcription', methods=['GET'])
def get_transcription(session_id):
    '''Obtener transcripción del audio'''
    return jsonify({
        'message': f'Endpoint de transcripción de sesión {session_id} - Módulo 2'
    }), 501

@audio_bp.route('/session/<int:session_id>/sentiment', methods=['GET'])
def get_audio_sentiment(session_id):
    '''Obtener análisis de sentimiento del audio'''
    return jsonify({
        'message': f'Endpoint de sentimiento de audio {session_id} - Módulo 2'
    }), 501

@audio_bp.route('/test', methods=['GET'])
def test():
    return {'message': 'Audio routes working'}