# ============================================
# app/routes/video_routes.py - Módulo 2
# ============================================
"""
app/routes/video_routes.py - Rutas de Video (Módulo 2)
Plataforma Integral de Rendimiento Estudiantil

Endpoints para gestionar sesiones de análisis de video en tiempo real.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import VideoSession, EmotionData, AttentionMetrics, User
from app.services.video_processing.emotion_recognition import emotion_service


# Crear blueprint
video_bp = Blueprint('video', __name__)


@video_bp.route('/session/start', methods=['POST'])
def start_video_session():
    """
    Iniciar una nueva sesión de análisis de video
    
    Body (JSON):
    {
        "user_id": 1,
        "session_name": "Clase de IA",
        "session_type": "clase",  # clase, exposicion, estudio, tutorial, otro
        "course_name": "Inteligencia Artificial"
    }
    
    Returns:
        201: Sesión creada exitosamente
        400: Error en datos de entrada
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('user_id'):
            return jsonify({'error': 'user_id es requerido'}), 400
        
        # Verificar que el usuario existe
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Crear nueva sesión
        session = VideoSession(
            user_id=data['user_id'],
            session_name=data.get('session_name', 'Sesión sin nombre'),
            session_type=data.get('session_type', 'estudio'),
            course_name=data.get('course_name')
        )
        
        # Iniciar sesión
        session.start_session()
        
        # Guardar en BD
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sesión de video iniciada correctamente',
            'session': session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al iniciar sesión: {str(e)}'
        }), 500


@video_bp.route('/session/<int:session_id>', methods=['GET'])
def get_video_session(session_id):
    """
    Obtener información de una sesión de video
    
    Returns:
        200: Información de la sesión
        404: Sesión no encontrada
    """
    try:
        session = VideoSession.query.get(session_id)
        
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        return jsonify({
            'success': True,
            'session': session.to_dict(include_relations=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener sesión: {str(e)}'
        }), 500


@video_bp.route('/session/<int:session_id>/end', methods=['POST'])
def end_video_session(session_id):
    """
    Finalizar una sesión de video
    
    Returns:
        200: Sesión finalizada correctamente
        404: Sesión no encontrada
    """
    try:
        session = VideoSession.query.get(session_id)
        
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        if not session.is_active:
            return jsonify({'error': 'La sesión ya fue finalizada'}), 400
        
        # Finalizar sesión
        session.end_session()
        
        # Calcular métricas resumen
        session.calculate_summary_metrics()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sesión finalizada correctamente',
            'session': session.to_dict(include_relations=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al finalizar sesión: {str(e)}'
        }), 500


@video_bp.route('/session/<int:session_id>/emotion', methods=['POST'])
def add_emotion_data(session_id):
    """
    Agregar datos de emoción de un frame
    
    Body (JSON):
    {
        "timestamp_seconds": 10.5,
        "frame_number": 315,
        "face_detected": true,
        "face_count": 1,
        "emotions": {
            "angry": 0.5,
            "disgust": 0.2,
            "fear": 1.0,
            "happy": 85.3,
            "sad": 0.8,
            "surprise": 10.2,
            "neutral": 2.0
        },
        "age": 22,
        "gender": "Man",
        "face_bbox": {"x": 100, "y": 150, "w": 200, "h": 250}
    }
    
    Returns:
        201: Emoción registrada correctamente
        404: Sesión no encontrada
    """
    try:
        data = request.get_json()
        
        # Verificar que la sesión existe
        session = VideoSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        # Validar campos requeridos
        if data.get('timestamp_seconds') is None or data.get('frame_number') is None:
            return jsonify({'error': 'timestamp_seconds y frame_number son requeridos'}), 400
        
        # Crear registro de emoción
        emotion = EmotionData(
            session_id=session_id,
            user_id=session.user_id,
            timestamp_seconds=data['timestamp_seconds'],
            frame_number=data['frame_number'],
            face_detected=data.get('face_detected', False),
            face_count=data.get('face_count', 0),
            age=data.get('age'),
            gender=data.get('gender'),
            face_bbox=data.get('face_bbox')
        )
        
        # Establecer emociones si se detectó rostro
        if data.get('face_detected') and data.get('emotions'):
            emotion.set_emotions(data['emotions'])
        
        db.session.add(emotion)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Emoción registrada correctamente',
            'emotion': emotion.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al registrar emoción: {str(e)}'
        }), 500


@video_bp.route('/session/<int:session_id>/emotions', methods=['GET'])
def get_session_emotions(session_id):
    """
    Obtener timeline de emociones de una sesión
    
    Query params:
        - limit: Número máximo de registros (default: 100)
        - offset: Offset para paginación (default: 0)
    
    Returns:
        200: Lista de emociones
        404: Sesión no encontrada
    """
    try:
        session = VideoSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        # Parámetros de paginación
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Obtener emociones
        emotions = EmotionData.query.filter_by(session_id=session_id)\
            .order_by(EmotionData.timestamp_seconds)\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        return jsonify({
            'success': True,
            'total': session.emotion_data.count(),
            'limit': limit,
            'offset': offset,
            'emotions': [e.to_dict() for e in emotions]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener emociones: {str(e)}'
        }), 500


@video_bp.route('/session/<int:session_id>/attention', methods=['GET'])
def get_attention_metrics(session_id):
    """
    Obtener métricas de atención de una sesión
    
    Returns:
        200: Métricas de atención
        404: Sesión no encontrada
    """
    try:
        session = VideoSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        # Obtener métricas de atención
        metrics = AttentionMetrics.query.filter_by(session_id=session_id)\
            .order_by(AttentionMetrics.time_interval_start)\
            .all()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total_metrics': len(metrics),
            'metrics': [m.to_dict() for m in metrics]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener métricas: {str(e)}'
        }), 500


@video_bp.route('/session/<int:session_id>/calculate-attention', methods=['POST'])
def calculate_attention_metrics(session_id):
    """
    Calcular métricas de atención para intervalos de tiempo
    
    Body (JSON):
    {
        "interval_duration": 30  # segundos por intervalo (default: 30)
    }
    
    Returns:
        200: Métricas calculadas
        404: Sesión no encontrada
    """
    try:
        data = request.get_json() or {}
        interval_duration = data.get('interval_duration', 30)
        
        session = VideoSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        if not session.duration_seconds:
            return jsonify({'error': 'La sesión no tiene duración definida'}), 400
        
        # Obtener todas las emociones de la sesión
        all_emotions = EmotionData.query.filter_by(session_id=session_id)\
            .order_by(EmotionData.timestamp_seconds)\
            .all()
        
        if not all_emotions:
            return jsonify({'error': 'No hay datos de emociones para esta sesión'}), 400
        
        # Dividir en intervalos y calcular métricas
        metrics_created = []
        current_time = 0
        
        while current_time < session.duration_seconds:
            interval_end = min(current_time + interval_duration, session.duration_seconds)
            
            # Filtrar emociones en este intervalo
            interval_emotions = [
                e for e in all_emotions 
                if current_time <= float(e.timestamp_seconds) < interval_end
            ]
            
            if interval_emotions:
                # Crear métrica de atención
                metric = AttentionMetrics(
                    session_id=session_id,
                    user_id=session.user_id,
                    time_interval_start=current_time,
                    time_interval_end=interval_end
                )
                
                # Calcular score de atención
                metric.calculate_attention_score(interval_emotions)
                
                db.session.add(metric)
                metrics_created.append(metric)
            
            current_time = interval_end
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(metrics_created)} métricas de atención calculadas',
            'metrics': [m.to_dict() for m in metrics_created]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al calcular métricas: {str(e)}'
        }), 500


@video_bp.route('/user/<int:user_id>/sessions', methods=['GET'])
def get_user_sessions(user_id):
    """
    Obtener todas las sesiones de un usuario
    
    Query params:
        - status: Filtrar por estado (recording, completed, etc.)
        - limit: Número máximo de sesiones (default: 20)
    
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
        
        # Query base
        query = VideoSession.query.filter_by(user_id=user_id)
        
        # Aplicar filtro de estado si existe
        if status:
            query = query.filter_by(processing_status=status)
        
        # Ordenar y limitar
        sessions = query.order_by(VideoSession.created_at.desc())\
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
    
# AGREGAR ESTE NUEVO ENDPOINT (no reemplazar nada)
from app.services.video_processing.emotion_recognition import emotion_service

@video_bp.route('/session/<int:session_id>/analyze-frame', methods=['POST'])
def analyze_frame_realtime(session_id):
    """Analizar frame con DeepFace en tiempo real"""
    
    # Recibir imagen del frontend (base64 o file)
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame provided'}), 400
    
    frame_file = request.files['frame']
    
    # Convertir a numpy array
    import cv2
    import numpy as np
    nparr = np.frombuffer(frame_file.read(), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Analizar con DeepFace
    result = emotion_service.analyze_frame(frame)
    
    if result['face_detected']:
        # Crear EmotionData
        emotion = EmotionData(...)
        emotion.set_emotions(result['emotions'])
        
        db.session.add(emotion)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'emotion': emotion.to_dict()
        })
    
    return jsonify({'success': False, 'error': 'No face detected'})