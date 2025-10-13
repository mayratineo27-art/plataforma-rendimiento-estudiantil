
# ============================================
# app/routes/audio_routes.py - Módulo 2
# ============================================

"""
app/routes/audio_routes.py - Rutas de Audio (Módulo 2)
Plataforma Integral de Rendimiento Estudiantil

Endpoints para gestionar sesiones de audio y transcripción en tiempo real.
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import AudioSession, AudioTranscription, VideoSession, User
from app.utils.file_handler import file_handler

# Crear blueprint
audio_bp = Blueprint('audio', __name__)


@audio_bp.route('/session/create', methods=['POST'])
def create_audio_session():
    """
    Crear una nueva sesión de audio
    
    Body (JSON):
    {
        "user_id": 1,
        "video_session_id": 5,  # Opcional, si está vinculado a video
        "audio_format": "webm"
    }
    
    Returns:
        201: Sesión creada
        400: Error en datos
    """
    try:
        data = request.get_json()
        
        # Validar user_id
        if not data.get('user_id'):
            return jsonify({'error': 'user_id es requerido'}), 400
        
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Verificar video_session si se proporcionó
        video_session_id = data.get('video_session_id')
        if video_session_id:
            video_session = VideoSession.query.get(video_session_id)
            if not video_session:
                return jsonify({'error': 'Sesión de video no encontrada'}), 404
        
        # Crear sesión de audio
        audio_session = AudioSession(
            user_id=data['user_id'],
            session_id=video_session_id,
            audio_format=data.get('audio_format', 'webm')
        )
        
        db.session.add(audio_session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sesión de audio creada correctamente',
            'audio_session': audio_session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al crear sesión: {str(e)}'
        }), 500


@audio_bp.route('/session/<int:audio_session_id>/upload', methods=['POST'])
def upload_audio(audio_session_id):
    """
    Subir archivo de audio para transcripción
    
    Form data:
        - audio_file: Archivo de audio
    
    Returns:
        200: Audio subido correctamente
        404: Sesión no encontrada
    """
    try:
        # Verificar sesión
        audio_session = AudioSession.query.get(audio_session_id)
        if not audio_session:
            return jsonify({'error': 'Sesión de audio no encontrada'}), 404
        
        # Verificar archivo
        if 'audio_file' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo de audio'}), 400
        
        audio_file = request.files['audio_file']
        
        # Validar archivo
        allowed_extensions = ['mp3', 'wav', 'ogg', 'm4a', 'webm']
        max_size_mb = 50
        
        is_valid, error_msg = file_handler.validate_file(
            audio_file,
            allowed_extensions,
            max_size_mb
        )
        
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Guardar archivo
        upload_folder = file_handler.get_upload_path('audio')
        file_info = file_handler.save_file(
            audio_file,
            upload_folder,
            prefix=f'audio_session_{audio_session_id}'
        )
        
        # Actualizar sesión de audio
        audio_session.audio_file_path = file_info['filepath']
        audio_session.audio_file_size = file_info['file_size']
        audio_session.audio_format = file_info['filename'].split('.')[-1]
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Audio subido correctamente',
            'file_info': {
                'filename': file_info['filename'],
                'size_mb': round(file_info['file_size'] / (1024 * 1024), 2),
                'format': audio_session.audio_format
            },
            'audio_session': audio_session.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al subir audio: {str(e)}'
        }), 500


@audio_bp.route('/session/<int:audio_session_id>/transcription', methods=['GET'])
def get_transcription(audio_session_id):
    """
    Obtener transcripción completa del audio
    
    Returns:
        200: Transcripción completa
        404: Sesión no encontrada
    """
    try:
        audio_session = AudioSession.query.get(audio_session_id)
        if not audio_session:
            return jsonify({'error': 'Sesión de audio no encontrada'}), 404
        
        # Obtener segmentos de transcripción
        transcriptions = AudioTranscription.query.filter_by(
            audio_session_id=audio_session_id
        ).order_by(AudioTranscription.start_time).all()
        
        return jsonify({
            'success': True,
            'audio_session_id': audio_session_id,
            'transcription_text': audio_session.transcription_text,
            'confidence': float(audio_session.transcription_confidence or 0),
            'accuracy_percentage': float(audio_session.transcription_accuracy_percentage or 0),
            'has_good_accuracy': audio_session.has_good_accuracy,
            'word_count': audio_session.word_count,
            'statistics': audio_session.calculate_statistics(),
            'segments_count': len(transcriptions),
            'segments': [t.to_dict() for t in transcriptions]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener transcripción: {str(e)}'
        }), 500


@audio_bp.route('/session/<int:audio_session_id>/transcription/segment', methods=['POST'])
def add_transcription_segment(audio_session_id):
    """
    Agregar segmento de transcripción
    
    Body (JSON):
    {
        "start_time": 0.0,
        "end_time": 5.2,
        "text": "Texto transcrito del segmento",
        "confidence": 0.95
    }
    
    Returns:
        201: Segmento añadido
        404: Sesión no encontrada
    """
    try:
        data = request.get_json()
        
        # Verificar sesión
        audio_session = AudioSession.query.get(audio_session_id)
        if not audio_session:
            return jsonify({'error': 'Sesión de audio no encontrada'}), 404
        
        # Validar campos requeridos
        required_fields = ['start_time', 'end_time', 'text']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} es requerido'}), 400
        
        # Crear segmento de transcripción
        transcription = AudioTranscription(
            audio_session_id=audio_session_id,
            user_id=audio_session.user_id,
            start_time=data['start_time'],
            end_time=data['end_time'],
            text=data['text'],
            confidence=data.get('confidence', 0)
        )
        
        # Analizar sentimiento básico
        transcription.analyze_sentiment_basic()
        
        # Extraer palabras clave básicas
        transcription.extract_keywords_basic()
        
        db.session.add(transcription)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Segmento de transcripción añadido',
            'transcription': transcription.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al añadir segmento: {str(e)}'
        }), 500


@audio_bp.route('/session/<int:audio_session_id>/complete', methods=['POST'])
def complete_transcription(audio_session_id):
    """
    Marcar transcripción como completada
    
    Body (JSON):
    {
        "transcription_text": "Texto completo transcrito",
        "confidence": 0.85,
        "accuracy_percentage": 75.5
    }
    
    Returns:
        200: Transcripción completada
        404: Sesión no encontrada
    """
    try:
        data = request.get_json()
        
        audio_session = AudioSession.query.get(audio_session_id)
        if not audio_session:
            return jsonify({'error': 'Sesión de audio no encontrada'}), 404
        
        # Completar procesamiento
        audio_session.complete_processing(
            transcription_text=data.get('transcription_text', ''),
            confidence=data.get('confidence', 0),
            accuracy=data.get('accuracy_percentage', 0)
        )
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transcripción completada correctamente',
            'audio_session': audio_session.to_dict(include_transcription=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al completar transcripción: {str(e)}'
        }), 500


@audio_bp.route('/session/<int:audio_session_id>/sentiment', methods=['GET'])
def get_audio_sentiment(audio_session_id):
    """
    Obtener análisis de sentimiento del audio
    
    Returns:
        200: Análisis de sentimiento
        404: Sesión no encontrada
    """
    try:
        audio_session = AudioSession.query.get(audio_session_id)
        if not audio_session:
            return jsonify({'error': 'Sesión de audio no encontrada'}), 404
        
        # Obtener segmentos
        transcriptions = AudioTranscription.query.filter_by(
            audio_session_id=audio_session_id
        ).order_by(AudioTranscription.start_time).all()
        
        # Calcular estadísticas de sentimiento
        sentiments = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        total_score = 0
        
        for trans in transcriptions:
            if trans.sentiment:
                sentiments[trans.sentiment] = sentiments.get(trans.sentiment, 0) + 1
            if trans.sentiment_score:
                total_score += float(trans.sentiment_score)
        
        avg_sentiment_score = total_score / len(transcriptions) if transcriptions else 0
        
        return jsonify({
            'success': True,
            'audio_session_id': audio_session_id,
            'sentiment_distribution': sentiments,
            'average_sentiment_score': round(avg_sentiment_score, 2),
            'total_segments': len(transcriptions),
            'segments_with_sentiment': [
                {
                    'start_time': t.start_time,
                    'end_time': t.end_time,
                    'sentiment': t.sentiment,
                    'sentiment_score': float(t.sentiment_score or 0),
                    'text_preview': t.text[:100] + '...' if len(t.text) > 100 else t.text
                }
                for t in transcriptions if t.sentiment
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener sentimiento: {str(e)}'
        }), 500


@audio_bp.route('/session/<int:audio_session_id>', methods=['GET'])
def get_audio_session(audio_session_id):
    """
    Obtener información completa de sesión de audio
    
    Returns:
        200: Información de la sesión
        404: Sesión no encontrada
    """
    try:
        audio_session = AudioSession.query.get(audio_session_id)
        if not audio_session:
            return jsonify({'error': 'Sesión de audio no encontrada'}), 404
        
        return jsonify({
            'success': True,
            'audio_session': audio_session.to_dict(include_transcription=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener sesión: {str(e)}'
        }), 500


@audio_bp.route('/user/<int:user_id>/sessions', methods=['GET'])
def get_user_audio_sessions(user_id):
    """
    Obtener todas las sesiones de audio de un usuario
    
    Query params:
        - status: Filtrar por estado
        - limit: Número máximo (default: 20)
    
    Returns:
        200: Lista de sesiones
        404: Usuario no encontrado
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Filtros
        status = request.args.get('status')
        limit = request.args.get('limit', 20, type=int)
        
        # Query
        query = AudioSession.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(processing_status=status)
        
        sessions = query.order_by(AudioSession.created_at.desc())\
            .limit(limit)\
            .all()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'total_sessions': len(sessions),
            'sessions': [s.to_dict() for s in sessions]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener sesiones: {str(e)}'
        }), 500