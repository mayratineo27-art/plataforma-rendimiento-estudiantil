# backend/app/controllers/audio_controller.py
# Controlador para transcripción de audio

from flask import request, jsonify
from datetime import datetime
import os
import logging
from werkzeug.utils import secure_filename
from app.models.audio_transcription import AudioTranscription
from app.models.audio_session import AudioSession
from app.models.video_session import VideoSession
from app import db

# Importación condicional de servicios de audio
try:
    from app.services.ai.audio_service import AudioService
    AUDIO_SERVICE_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Audio service no disponible: {e}")
    AUDIO_SERVICE_AVAILABLE = False
    AudioService = None

# Para conversión de audio
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except Exception as e:
    print(f"⚠️  pydub no disponible: {e}")
    PYDUB_AVAILABLE = False

logger = logging.getLogger(__name__)


class AudioController:
    def __init__(self):
        self.audio_service = AudioService() if AUDIO_SERVICE_AVAILABLE else None
        self.upload_folder = 'uploads/audio'
        
        # Crear carpeta si no existe
        os.makedirs(self.upload_folder, exist_ok=True)

    def transcribe_audio(self):
        """Transcribe un archivo de audio recibido desde el frontend"""
        try:
            # Verificar que hay archivo
            if 'audio' not in request.files:
                return jsonify({'error': 'No se envió archivo de audio'}), 400

            audio_file = request.files['audio']
            video_session_id = request.form.get('session_id')
            user_id = request.form.get('user_id')

            if not video_session_id:
                return jsonify({'error': 'session_id es requerido'}), 400
            
            if not user_id:
                return jsonify({'error': 'user_id es requerido'}), 400

            # Verificar que la sesión de video existe
            video_session = VideoSession.query.get(video_session_id)
            if not video_session:
                return jsonify({'error': 'Sesión de video no encontrada'}), 404

            # Guardar archivo original temporalmente
            timestamp = int(datetime.utcnow().timestamp() * 1000)
            original_filename = secure_filename(f"audio_{video_session_id}_{timestamp}.webm")
            original_filepath = os.path.join(self.upload_folder, original_filename)
            audio_file.save(original_filepath)

            # Convertir a WAV si es necesario
            wav_filename = secure_filename(f"audio_{video_session_id}_{timestamp}.wav")
            wav_filepath = os.path.join(self.upload_folder, wav_filename)
            
            try:
                if PYDUB_AVAILABLE:
                    logger.info(f"🔄 Convirtiendo audio a WAV: {original_filepath}")
                    audio = AudioSegment.from_file(original_filepath)
                    audio.export(wav_filepath, format='wav')
                    logger.info(f"✅ Audio convertido a WAV")
                    
                    # Eliminar archivo original
                    os.remove(original_filepath)
                else:
                    logger.warning("⚠️  pydub no disponible, usando archivo original")
                    wav_filepath = original_filepath
            except Exception as conv_error:
                logger.error(f"❌ Error al convertir audio: {str(conv_error)}")
                # Si falla la conversión, usar el archivo original
                wav_filepath = original_filepath

            # Crear o obtener sesión de audio
            audio_session = AudioSession.query.filter_by(session_id=video_session_id).first()
            if not audio_session:
                audio_session = AudioSession(
                    user_id=int(user_id),
                    session_id=video_session_id,
                    audio_file_path=wav_filepath,
                    audio_format='wav',
                    processing_status='processing'
                )
                db.session.add(audio_session)
                db.session.commit()

            # Transcribir audio
            logger.info(f"🎤 Transcribiendo audio: {wav_filepath}")
            transcription_result = self.audio_service.transcribe(wav_filepath)
            
            text = transcription_result.get('text', '').strip()
            
            if not text:
                logger.warning("⚠️  No se detectó texto en el audio")
                return jsonify({
                    'success': True,
                    'transcription': None,
                    'message': 'No se detectó voz en el audio'
                }), 200

            # Guardar transcripción en la base de datos
            transcription = AudioTranscription(
                audio_session_id=audio_session.id,
                user_id=int(user_id),
                start_time=0.0,  # TODO: Calcular desde chunks de audio
                end_time=10.0,   # TODO: Calcular duración real
                text=text,
                confidence=transcription_result.get('confidence', 0),
                language=transcription_result.get('language', 'es')
            )
            
            db.session.add(transcription)
            
            # Actualizar sesión de audio
            audio_session.processing_status = 'completed'
            audio_session.processing_completed_at = datetime.utcnow()
            audio_session.transcription_text = text
            audio_session.language_detected = transcription_result.get('language', 'es')
            
            db.session.commit()
            
            logger.info(f"✅ Transcripción guardada: ID {transcription.id}")

            return jsonify({
                'success': True,
                'transcription': {
                    'id': transcription.id,
                    'text': transcription.text,
                    'confidence': float(transcription.confidence) if transcription.confidence else 0,
                    'language': transcription.language,
                    'audio_session_id': audio_session.id
                },
                'message': 'Audio transcrito correctamente'
            }), 200

        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Error transcribiendo audio: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    def get_session_transcriptions(self, session_id):
        """Obtiene todas las transcripciones de una sesión"""
        try:
            # Buscar audio_session por video_session_id
            audio_session = AudioSession.query.filter_by(session_id=session_id).first()
            
            if not audio_session:
                return jsonify({
                    'success': True,
                    'transcriptions': [],
                    'total': 0,
                    'message': 'No hay transcripciones para esta sesión'
                }), 200

            # Obtener transcripciones
            transcriptions = AudioTranscription.query\
                .filter_by(audio_session_id=audio_session.id)\
                .order_by(AudioTranscription.start_time)\
                .all()
            
            # Combinar todo el texto
            full_text = ' '.join([t.text for t in transcriptions if t.text])

            return jsonify({
                'success': True,
                'audio_session_id': audio_session.id,
                'total': len(transcriptions),
                'full_text': full_text,
                'transcriptions': [
                    {
                        'id': t.id,
                        'text': t.text,
                        'start_time': float(t.start_time) if t.start_time else 0,
                        'end_time': float(t.end_time) if t.end_time else 0,
                        'confidence': float(t.confidence) if t.confidence else 0,
                        'language': t.language
                    }
                    for t in transcriptions
                ]
            }), 200

        except Exception as e:
            logger.error(f"❌ Error al obtener transcripciones: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500
    
    def generate_summary(self, session_id):
        """Genera un resumen inteligente de las transcripciones usando IA"""
        try:
            # Buscar audio_session
            audio_session = AudioSession.query.filter_by(session_id=session_id).first()
            
            if not audio_session:
                return jsonify({
                    'error': 'No hay transcripciones para resumir'
                }), 404

            # Obtener transcripciones
            transcriptions = AudioTranscription.query\
                .filter_by(audio_session_id=audio_session.id)\
                .all()
            
            if not transcriptions:
                return jsonify({
                    'error': 'No hay transcripciones para resumir'
                }), 404
            
            # Combinar texto
            full_text = ' '.join([t.text for t in transcriptions if t.text])
            
            if not full_text.strip():
                return jsonify({
                    'error': 'No hay texto para resumir'
                }), 400

            # Generar resumen con IA
            try:
                from app.services.ai.gemini_service import gemini_service
                
                prompt = f"""
Eres un asistente educativo experto. A continuación está la transcripción de lo que dijo un estudiante durante una sesión de estudio.

Por favor, genera un resumen estructurado que incluya:

1. **Temas Principales**: Los conceptos o temas que el estudiante mencionó
2. **Puntos Clave**: Las ideas más importantes expresadas
3. **Dudas o Preguntas**: Si el estudiante expresó confusión o hizo preguntas
4. **Nivel de Comprensión**: Una evaluación breve del nivel de comprensión demostrado
5. **Recomendaciones**: Sugerencias para mejorar el aprendizaje

TRANSCRIPCIÓN:
{full_text}

Genera el resumen en formato JSON con esta estructura:
{{
    "temas_principales": ["tema1", "tema2", ...],
    "puntos_clave": ["punto1", "punto2", ...],
    "dudas": ["duda1", "duda2", ...],
    "nivel_comprension": "alto|medio|bajo",
    "recomendaciones": ["recomendacion1", "recomendacion2", ...]
}}
"""
                
                logger.info("🤖 Generando resumen con IA...")
                summary_response = gemini_service.generate_content(prompt)
                
                import json
                import re
                
                # Extraer JSON del response
                json_match = re.search(r'\{.*\}', summary_response, re.DOTALL)
                if json_match:
                    summary_data = json.loads(json_match.group())
                else:
                    # Si no hay JSON, crear estructura básica
                    summary_data = {
                        "resumen_texto": summary_response,
                        "temas_principales": [],
                        "puntos_clave": [],
                        "dudas": [],
                        "nivel_comprension": "medio",
                        "recomendaciones": []
                    }
                
                # Guardar resumen en audio_session
                audio_session.meta_info = audio_session.meta_info or {}
                audio_session.meta_info['ai_summary'] = summary_data
                audio_session.meta_info['summary_generated_at'] = datetime.utcnow().isoformat()
                db.session.commit()
                
                logger.info(f"✅ Resumen generado y guardado")
                
                return jsonify({
                    'success': True,
                    'summary': summary_data,
                    'full_text': full_text,
                    'word_count': len(full_text.split())
                }), 200
                
            except Exception as ai_error:
                logger.error(f"❌ Error al generar resumen con IA: {str(ai_error)}")
                # Fallback: resumen básico sin IA
                words = full_text.split()
                return jsonify({
                    'success': True,
                    'summary': {
                        'resumen_texto': full_text[:500] + '...' if len(full_text) > 500 else full_text,
                        'word_count': len(words),
                        'ai_available': False
                    },
                    'full_text': full_text
                }), 200

        except Exception as e:
            logger.error(f"❌ Error al generar resumen: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

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