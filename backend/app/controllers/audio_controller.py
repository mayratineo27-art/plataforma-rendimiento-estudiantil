# backend/app/controllers/audio_controller.py
# Controlador para transcripción de audio

from flask import request, jsonify
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from app.models.audio_transcription import AudioTranscription
from app.models.video_session import VideoSession
from app.services.ai.audio_service import AudioService
from app import db

class AudioController:
    def __init__(self):
        self.audio_service = AudioService()
        self.upload_folder = 'uploads/audio'
        
        # Crear carpeta si no existe
        os.makedirs(self.upload_folder, exist_ok=True)

    def transcribe_audio(self):
        """Transcribe un archivo de audio"""
        try:
            # Verificar que hay archivo
            if 'audio' not in request.files:
                return jsonify({'error': 'No se envió archivo de audio'}), 400

            audio_file = request.files['audio']
            session_id = request.form.get('session_id')

            if not session_id:
                return jsonify({'error': 'session_id es requerido'}), 400

            # Verificar que la sesión existe
            session = VideoSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Sesión no encontrada'}), 404

            # Guardar archivo temporalmente
            filename = secure_filename(f"audio_{session_id}_{datetime.utcnow().timestamp()}.wav")
            filepath = os.path.join(self.upload_folder, filename)
            audio_file.save(filepath)

            # Transcribir audio
            transcription_result = self.audio_service.transcribe(filepath)

            # Guardar transcripción en la base de datos
            transcription = AudioTranscription(
                session_id=session_id,
                timestamp=datetime.utcnow(),
                text=transcription_result.get('text', ''),
                confidence=transcription_result.get('confidence', 0),
                language=transcription_result.get('language', 'es'),
                audio_file_path=filepath
            )
            
            db.session.add(transcription)
            db.session.commit()

            # Eliminar archivo temporal (opcional)
            # os.remove(filepath)

            return jsonify({
                'success': True,
                'transcription': {
                    'id': transcription.id,
                    'text': transcription.text,
                    'confidence': transcription.confidence,
                    'language': transcription.language,
                    'timestamp': transcription.timestamp.isoformat()
                },
                'message': 'Audio transcrito correctamente'
            }), 200

        except Exception as e:
            db.session.rollback()
            print(f"Error transcribiendo audio: {str(e)}")
            return jsonify({'error': str(e)}), 500

    def get_session_transcriptions(self, session_id):
        """Obtiene todas las transcripciones de una sesión"""
        try:
            # Verificar que la sesión existe
            session = VideoSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Sesión no encontrada'}), 404

            # Obtener transcripciones
            transcriptions = AudioTranscription.query\
                .filter_by(session_id=session_id)\
                .order_by(AudioTranscription.timestamp)\
                .all()

            return jsonify({
                'success': True,
                'session_id': session_id,
                'transcriptions': [
                    {
                        'id': t.id,
                        'timestamp': t.timestamp.isoformat() if t.timestamp else None,
                        'text': t.text,
                        'confidence': t.confidence,
                        'language': t.language
                    } for t in transcriptions
                ],
                'total_transcriptions': len(transcriptions)
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def analyze_sentiment(self):
        """Analiza el sentimiento del audio transcrito"""
        try:
            data = request.get_json()
            transcription_id = data.get('transcription_id')

            if not transcription_id:
                return jsonify({'error': 'transcription_id es requerido'}), 400

            # Buscar transcripción
            transcription = AudioTranscription.query.get(transcription_id)
            if not transcription:
                return jsonify({'error': 'Transcripción no encontrada'}), 404

            # Analizar sentimiento
            sentiment = self.audio_service.analyze_sentiment(transcription.text)

            return jsonify({
                'success': True,
                'transcription_id': transcription_id,
                'text': transcription.text,
                'sentiment': sentiment
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500