# ============================================
# app/routes/video_routes.py - Módulo 2
# VERSIÓN CORREGIDA Y COMPLETA
# ============================================
"""
app/routes/video_routes.py - Rutas de Video y Audio (Módulo 2)
Plataforma Integral de Rendimiento Estudiantil

Endpoints para gestionar sesiones de análisis de video y audio en tiempo real.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.user import User
from app.models.video_session import VideoSession
from app.models.emotion_data import EmotionData
from app.models.audio_transcription import AudioTranscription
from app.models.attention_metrics import AttentionMetrics

# Importar controladores - TODOS ACTIVOS (con manejo de errores)
CONTROLLERS_AVAILABLE = False
try:
    from app.controllers.video_controller import VideoController
    from app.controllers.audio_controller import AudioController
    video_controller = VideoController()
    audio_controller = AudioController()
    CONTROLLERS_AVAILABLE = True
    print("   ✅ VideoController y AudioController disponibles")
except Exception as e:
    print(f"   ⚠️ Controllers no disponibles (TensorFlow issue): {str(e)[:80]}")
    print(f"   📝 Video routes funcionarán sin procesamiento de IA")
    video_controller = None
    audio_controller = None
    print("   ℹ️ Usando implementación manual de endpoints")
    video_controller = None
    audio_controller = None
    CONTROLLERS_AVAILABLE = False

# ========================================
# CREAR BLUEPRINTS (UNA SOLA VEZ)
# ========================================
video_bp = Blueprint('video', __name__)
audio_bp = Blueprint('audio', __name__)


# ========================================
# ENDPOINTS DE VIDEO
# ========================================

@video_bp.route('/session/start', methods=['POST'])
def start_video_session():
    """
    POST /api/video/session/start
    Iniciar una nueva sesión de análisis de video
    
    Body (JSON):
    {
        "user_id": 1,
        "session_name": "Clase de IA",
        "session_type": "clase",
        "course_name": "Inteligencia Artificial"
    }
    """
    if CONTROLLERS_AVAILABLE:
        return video_controller.start_session()
    
    try:
        data = request.get_json()
        
        if not data.get('user_id'):
            return jsonify({'error': 'user_id es requerido'}), 400
        
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
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


@video_bp.route('/analyze-frame', methods=['POST'])
def analyze_frame():
    """
    POST /api/video/analyze-frame
    Analizar frame con DeepFace en tiempo real
    
    Form data:
        - frame: Archivo de imagen (JPG/PNG)
        - session_id: ID de la sesión
        - timestamp: Timestamp del frame
    """
    if CONTROLLERS_AVAILABLE:
        return video_controller.analyze_frame()
    
    try:
        if 'frame' not in request.files:
            return jsonify({'error': 'No frame provided'}), 400
        
        frame_file = request.files['frame']
        session_id = request.form.get('session_id')
        timestamp = request.form.get('timestamp', 0, type=float)
        
        if not session_id:
            return jsonify({'error': 'session_id es requerido'}), 400
        
        # Verificar sesión
        session = VideoSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        # Procesar frame con servicio de IA
        try:
            from app.services.ai.vision_service import vision_service
            
            # Convertir a numpy array
            import cv2
            import numpy as np
            nparr = np.frombuffer(frame_file.read(), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Analizar
            result = vision_service.analyze_frame(frame)
            
            if result['face_detected']:
                # Crear registro de emoción
                emotion = EmotionData(
                    session_id=session_id,
                    user_id=session.user_id,
                    timestamp_seconds=timestamp,
                    frame_number=int(timestamp * 30),  # Asumiendo 30 FPS
                    face_detected=True,
                    face_count=result.get('face_count', 1),
                    age=result.get('age'),
                    gender=result.get('gender'),
                    face_bbox=result.get('face_bbox')
                )
                
                emotion.set_emotions(result['emotions'])
                
                db.session.add(emotion)
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'emotion': emotion.to_dict()
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'No face detected'
                }), 200
                
        except ImportError:
            return jsonify({
                'error': 'Vision service no disponible',
                'message': 'Instala DeepFace: pip install deepface'
            }), 500
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al analizar frame: {str(e)}'
        }), 500


@video_bp.route('/session/end', methods=['POST'])
def end_video_session():
    """
    POST /api/video/session/end
    Finalizar sesión de video
    
    Body (JSON):
    {
        "session_id": 1
    }
    """
    if CONTROLLERS_AVAILABLE:
        return video_controller.end_session()
    
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({'error': 'session_id es requerido'}), 400
        
        session = VideoSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        if not session.is_active:
            return jsonify({'error': 'La sesión ya fue finalizada'}), 400
        
        session.end_session()
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


@video_bp.route('/session/<int:session_id>/analysis', methods=['GET'])
def get_session_analysis(session_id):
    """
    GET /api/video/session/{id}/analysis
    Obtener análisis completo de la sesión
    """
    if CONTROLLERS_AVAILABLE:
        return video_controller.get_session_analysis(session_id)
    
    try:
        session = VideoSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        # Obtener todas las emociones
        emotions = EmotionData.query.filter_by(session_id=session_id)\
            .order_by(EmotionData.timestamp_seconds)\
            .all()
        
        # Calcular estadísticas
        total_emotions = len(emotions)
        faces_detected = sum(1 for e in emotions if e.face_detected)
        
        return jsonify({
            'success': True,
            'session': session.to_dict(),
            'total_emotions': total_emotions,
            'faces_detected': faces_detected,
            'detection_rate': round((faces_detected / total_emotions * 100) if total_emotions > 0 else 0, 2),
            'emotions': [e.to_dict() for e in emotions]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener análisis: {str(e)}'
        }), 500


@video_bp.route('/session/<int:session_id>/attention', methods=['GET'])
def get_attention_metrics(session_id):
    """
    GET /api/video/session/{id}/attention
    Obtener métricas de atención
    """
    if CONTROLLERS_AVAILABLE:
        return video_controller.get_attention_metrics(session_id)
    
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
            'metrics': [m.to_dict() for m in metrics]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener métricas: {str(e)}'
        }), 500


@video_bp.route('/sessions/<int:user_id>', methods=['GET'])
def get_user_sessions(user_id):
    """
    GET /api/video/sessions/{user_id}
    Obtener todas las sesiones de un usuario
    """
    if CONTROLLERS_AVAILABLE:
        return video_controller.get_user_sessions(user_id)
    
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        limit = request.args.get('limit', 20, type=int)
        
        sessions = VideoSession.query.filter_by(user_id=user_id)\
            .order_by(VideoSession.created_at.desc())\
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


# ========================================
# ENDPOINTS DE AUDIO
# ========================================

@audio_bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    POST /api/audio/transcribe
    Transcribir audio con Speech Recognition
    
    Form data:
        - audio: Archivo de audio
        - session_id: ID de la sesión
        - start_time: Tiempo de inicio
        - end_time: Tiempo de fin
    """
    if CONTROLLERS_AVAILABLE:
        return audio_controller.transcribe_audio()
    
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio provided'}), 400
        
        audio_file = request.files['audio']
        session_id = request.form.get('session_id')
        start_time = request.form.get('start_time', 0, type=float)
        end_time = request.form.get('end_time', 0, type=float)
        
        if not session_id:
            return jsonify({'error': 'session_id es requerido'}), 400
        
        # Verificar sesión
        session = VideoSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        # Procesar audio
        try:
            from app.services.ai.audio_service import audio_service
            
            # Guardar archivo temporal
            import os
            temp_path = f"/tmp/audio_{session_id}_{start_time}.wav"
            audio_file.save(temp_path)
            
            # Transcribir
            result = audio_service.transcribe_audio(temp_path)
            
            if result['success']:
                # Crear transcripción
                transcription = AudioTranscription(
                    session_id=session_id,
                    user_id=session.user_id,
                    start_time=start_time,
                    end_time=end_time,
                    text=result['text'],
                    confidence=result.get('confidence', 0)
                )
                
                # Analizar sentimiento
                transcription.analyze_sentiment_basic()
                
                db.session.add(transcription)
                db.session.commit()
                
                # Limpiar archivo temporal
                os.remove(temp_path)
                
                return jsonify({
                    'success': True,
                    'transcription': transcription.to_dict()
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Transcription failed')
                }), 200
                
        except ImportError:
            return jsonify({
                'error': 'Audio service no disponible',
                'message': 'Instala SpeechRecognition: pip install SpeechRecognition'
            }), 500
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': True,
            'message': f'Error al transcribir: {str(e)}'
        }), 500


@audio_bp.route('/session/<int:session_id>/transcriptions', methods=['GET'])
def get_session_transcriptions(session_id):
    """
    GET /api/audio/session/{id}/transcriptions
    Obtener todas las transcripciones de una sesión
    """
    if CONTROLLERS_AVAILABLE:
        return audio_controller.get_session_transcriptions(session_id)
    
    try:
        session = VideoSession.query.get(session_id)
        if not session:
            return jsonify({'error': 'Sesión no encontrada'}), 404
        
        transcriptions = AudioTranscription.query.filter_by(session_id=session_id)\
            .order_by(AudioTranscription.start_time)\
            .all()
        
        # Texto completo
        full_text = ' '.join([t.text for t in transcriptions if t.text])
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total_transcriptions': len(transcriptions),
            'full_text': full_text,
            'word_count': len(full_text.split()),
            'transcriptions': [t.to_dict() for t in transcriptions]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al obtener transcripciones: {str(e)}'
        }), 500


@audio_bp.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    """
    POST /api/audio/sentiment
    Analizar sentimiento de texto
    
    Body (JSON):
    {
        "text": "Texto a analizar"
    }
    """
    if CONTROLLERS_AVAILABLE:
        return audio_controller.analyze_sentiment()
    
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'text es requerido'}), 400
        
        # Análisis básico de sentimiento
        from app.services.ai.audio_service import audio_service
        sentiment = audio_service.analyze_sentiment_basic(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'sentiment': sentiment['sentiment'],
            'confidence': sentiment['confidence']
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error al analizar sentimiento: {str(e)}'
        }), 500


# ========================================
# ENDPOINT DE PRUEBA
# ========================================

@video_bp.route('/test', methods=['GET'])
def test_video():
    """GET /api/video/test - Verificar que el blueprint funciona"""
    return jsonify({
        'success': True,
        'message': 'Video routes funcionando correctamente',
        'controllers_available': CONTROLLERS_AVAILABLE
    }), 200


@audio_bp.route('/test', methods=['GET'])
def test_audio():
    """GET /api/audio/test - Verificar que el blueprint funciona"""
    return jsonify({
        'success': True,
        'message': 'Audio routes funcionando correctamente',
        'controllers_available': CONTROLLERS_AVAILABLE
    }), 200