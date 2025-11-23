"""
app/controllers/video_controller.py
Controlador de Video - Módulo 2
Plataforma Integral de Rendimiento Estudiantil
"""

from flask import request, jsonify
from datetime import datetime
from app import db
from app.models.video_session import VideoSession
from app.models.emotion_data import EmotionData
from app.models.attention_metrics import AttentionMetrics
from app.services.video_processing.emotion_recognition import emotion_service
import cv2
import numpy as np
import base64


class VideoController:
    """Controlador para endpoints de video"""
    
    def start_session(self):
        """
        POST /api/video/session/start
        Iniciar nueva sesión de video
        """
        try:
            data = request.get_json()
            
            # Validar user_id
            if not data.get('user_id'):
                return jsonify({'error': 'user_id es requerido'}), 400
            
            # Crear sesión
            session = VideoSession(
                user_id=data['user_id'],
                session_name=data.get('session_name', 'Sesión sin nombre'),
                session_type=data.get('session_type', 'estudio'),
                course_name=data.get('course_name')
            )
            
            session.start_session()
            
            db.session.add(session)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Sesión iniciada correctamente',
                'session': session.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': True,
                'message': f'Error al iniciar sesión: {str(e)}'
            }), 500
    
    def analyze_frame(self):
        """
        POST /api/video/analyze-frame
        Analizar un frame de video con DeepFace
        """
        try:
            data = request.get_json()
            
            # Validar campos requeridos
            if not data.get('session_id'):
                return jsonify({'error': 'session_id es requerido'}), 400
            
            if not data.get('frame_base64'):
                return jsonify({'error': 'frame_base64 es requerido'}), 400
            
            session_id = data['session_id']
            frame_base64 = data['frame_base64']
            timestamp_seconds = data.get('timestamp_seconds', 0)
            frame_number = data.get('frame_number', 0)
            
            # Verificar sesión
            session = VideoSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Sesión no encontrada'}), 404
            
            # Decodificar frame desde base64
            try:
                # Remover prefijo "data:image/jpeg;base64," si existe
                if ',' in frame_base64:
                    frame_base64 = frame_base64.split(',')[1]
                
                # Decodificar
                frame_bytes = base64.b64decode(frame_base64)
                nparr = np.frombuffer(frame_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is None:
                    return jsonify({'error': 'No se pudo decodificar el frame'}), 400
                
            except Exception as e:
                return jsonify({'error': f'Error al decodificar frame: {str(e)}'}), 400
            
            # Analizar con DeepFace
            result = emotion_service.analyze_frame(frame, enforce_detection=False)
            
            # Crear registro de emoción
            emotion = EmotionData(
                session_id=session_id,
                user_id=session.user_id,
                timestamp_seconds=timestamp_seconds,
                frame_number=frame_number,
                face_detected=result.get('face_detected', False),
                face_count=result.get('face_count', 0)
            )
            
            # Si se detectó rostro, guardar emociones
            if result.get('face_detected'):
                emotion.set_emotions(result['emotions'])
                emotion.age = result.get('age')
                emotion.gender = result.get('gender')
                emotion.face_bbox = result.get('face_bbox')
            
            db.session.add(emotion)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'emotion': emotion.to_dict(),
                'analysis': result
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': True,
                'message': f'Error al analizar frame: {str(e)}'
            }), 500
    
    def end_session(self):
        """
        POST /api/video/session/end
        Finalizar sesión de video
        """
        try:
            data = request.get_json()
            
            if not data.get('session_id'):
                return jsonify({'error': 'session_id es requerido'}), 400
            
            session_id = data['session_id']
            session = VideoSession.query.get(session_id)
            
            if not session:
                return jsonify({'error': 'Sesión no encontrada'}), 404
            
            # Finalizar sesión
            session.end_session()
            
            # Calcular métricas de atención
            self._calculate_attention_metrics(session)
            
            # Calcular métricas resumen
            session.calculate_summary_metrics()
            session.complete_processing()
            
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
    
    def get_session_analysis(self, session_id):
        """
        GET /api/video/session/{id}/analysis
        Obtener análisis completo de la sesión
        """
        try:
            session = VideoSession.query.get(session_id)
            
            if not session:
                return jsonify({'error': 'Sesión no encontrada'}), 404
            
            # Obtener emociones
            emotions = EmotionData.query.filter_by(session_id=session_id)\
                .order_by(EmotionData.timestamp_seconds)\
                .all()
            
            # Calcular estadísticas
            emotion_stats = self._calculate_emotion_statistics(emotions)
            
            return jsonify({
                'success': True,
                'session': session.to_dict(),
                'total_frames': len(emotions),
                'emotion_statistics': emotion_stats,
                'emotions': [e.to_dict() for e in emotions[:100]]  # Primeros 100
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': True,
                'message': f'Error al obtener análisis: {str(e)}'
            }), 500
    
    def get_attention_metrics(self, session_id):
        """
        GET /api/video/session/{id}/attention
        Obtener métricas de atención
        """
        try:
            session = VideoSession.query.get(session_id)
            
            if not session:
                return jsonify({'error': 'Sesión no encontrada'}), 404
            
            metrics = AttentionMetrics.query.filter_by(session_id=session_id)\
                .order_by(AttentionMetrics.time_interval_start)\
                .all()
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'total_metrics': len(metrics),
                'avg_attention_score': session.avg_attention_score,
                'metrics': [m.to_dict() for m in metrics]
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': True,
                'message': f'Error al obtener métricas: {str(e)}'
            }), 500
    
    def get_user_sessions(self, user_id):
        """
        GET /api/video/sessions/{user_id}
        Obtener sesiones del usuario
        """
        try:
            sessions = VideoSession.query.filter_by(user_id=user_id)\
                .order_by(VideoSession.created_at.desc())\
                .limit(20)\
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
    
    def _calculate_attention_metrics(self, session, interval_duration=30):
        """Calcular métricas de atención por intervalos"""
        if not session.duration_seconds:
            return
        
        emotions = EmotionData.query.filter_by(session_id=session.id)\
            .order_by(EmotionData.timestamp_seconds)\
            .all()
        
        if not emotions:
            return
        
        current_time = 0
        
        while current_time < session.duration_seconds:
            interval_end = min(current_time + interval_duration, session.duration_seconds)
            
            # Filtrar emociones en el intervalo
            interval_emotions = [
                e for e in emotions
                if current_time <= float(e.timestamp_seconds) < interval_end
            ]
            
            if interval_emotions:
                metric = AttentionMetrics(
                    session_id=session.id,
                    user_id=session.user_id,
                    time_interval_start=current_time,
                    time_interval_end=interval_end
                )
                
                metric.calculate_attention_score(interval_emotions)
                db.session.add(metric)
            
            current_time = interval_end
    
    def _calculate_emotion_statistics(self, emotions):
        """Calcular estadísticas de emociones"""
        if not emotions:
            return {}
        
        total = len(emotions)
        faces_detected = sum(1 for e in emotions if e.face_detected)
        
        # Contar emociones contextuales
        contextual_counts = {}
        for emotion in emotions:
            if emotion.face_detected and emotion.contextual_emotion:
                ctx = emotion.contextual_emotion
                contextual_counts[ctx] = contextual_counts.get(ctx, 0) + 1
        
        return {
            'total_frames': total,
            'faces_detected': faces_detected,
            'detection_rate': round((faces_detected / total) * 100, 2) if total > 0 else 0,
            'contextual_distribution': contextual_counts,
            'most_common_emotion': max(contextual_counts.items(), key=lambda x: x[1])[0] if contextual_counts else None
        }