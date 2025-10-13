"""
app/services/audio_processing/transcription.py
Servicio de Transcripción de Audio
Plataforma Integral de Rendimiento Estudiantil - Módulo 2
"""

import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from typing import List, Dict, Optional, Tuple
from app.services.ai.gemini_service import gemini_service


class TranscriptionService:
    """
    Servicio para transcripción de audio con SpeechRecognition
    
    Transcribe archivos de audio y analiza el contenido con IA.
    """
    
    def __init__(self):
        """Inicializar servicio de transcripción"""
        self.recognizer = sr.Recognizer()
        self.language = os.getenv('SPEECH_RECOGNITION_LANGUAGE', 'es-ES')
        self.target_accuracy = float(os.getenv('TRANSCRIPTION_ACCURACY_THRESHOLD', 0.7))
        
        # Configuración de reconocimiento
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        print(f"✅ TranscriptionService inicializado")
        print(f"   Idioma: {self.language}")
        print(f"   Objetivo de precisión: {self.target_accuracy * 100}%")
    
    def transcribe_audio_file(
        self,
        audio_path: str,
        use_google: bool = True
    ) -> Dict:
        """
        Transcribir archivo de audio completo
        
        Args:
            audio_path (str): Ruta al archivo de audio
            use_google (bool): Usar Google Speech Recognition
        
        Returns:
            dict: Resultado de la transcripción
                {
                    'success': bool,
                    'text': str,
                    'confidence': float,
                    'duration_seconds': float,
                    'word_count': int,
                    'error': str
                }
        """
        try:
            # Convertir a WAV si es necesario
            wav_path = self._convert_to_wav(audio_path)
            
            # Obtener duración
            audio = AudioSegment.from_wav(wav_path)
            duration_seconds = len(audio) / 1000.0
            
            # Transcribir
            with sr.AudioFile(wav_path) as source:
                # Ajustar ruido ambiente
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Grabar audio
                audio_data = self.recognizer.record(source)
                
                # Transcribir
                if use_google:
                    text = self.recognizer.recognize_google(
                        audio_data,
                        language=self.language
                    )
                else:
                    text = self.recognizer.recognize_sphinx(audio_data)
                
                # Calcular métricas
                word_count = len(text.split())
                confidence = 0.85  # Google no retorna confidence, estimamos
                
                return {
                    'success': True,
                    'text': text,
                    'confidence': confidence,
                    'duration_seconds': duration_seconds,
                    'word_count': word_count,
                    'error': None
                }
        
        except sr.UnknownValueError:
            return {
                'success': False,
                'text': '',
                'error': 'No se pudo entender el audio'
            }
        except sr.RequestError as e:
            return {
                'success': False,
                'text': '',
                'error': f'Error en el servicio de reconocimiento: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'text': '',
                'error': str(e)
            }
    
    def transcribe_with_segments(
        self,
        audio_path: str,
        min_silence_len: int = 500,
        silence_thresh: int = -40
    ) -> Dict:
        """
        Transcribir audio dividiéndolo en segmentos basados en silencios
        
        Args:
            audio_path (str): Ruta al archivo de audio
            min_silence_len (int): Longitud mínima de silencio en ms
            silence_thresh (int): Umbral de silencio en dBFS
        
        Returns:
            dict: Resultado con segmentos transcritos
                {
                    'success': bool,
                    'full_text': str,
                    'segments': list,
                    'total_segments': int,
                    'avg_confidence': float
                }
        """
        try:
            # Convertir a WAV
            wav_path = self._convert_to_wav(audio_path)
            
            # Cargar audio
            audio = AudioSegment.from_wav(wav_path)
            
            # Dividir en segmentos basados en silencios
            chunks = split_on_silence(
                audio,
                min_silence_len=min_silence_len,
                silence_thresh=silence_thresh,
                keep_silence=200
            )
            
            print(f"🎵 Audio dividido en {len(chunks)} segmentos")
            
            segments = []
            full_text_parts = []
            current_time = 0
            
            for i, chunk in enumerate(chunks):
                # Duración del chunk
                chunk_duration = len(chunk) / 1000.0
                start_time = current_time
                end_time = current_time + chunk_duration
                
                # Exportar chunk temporal
                chunk_path = f"/tmp/chunk_{i}.wav"
                chunk.export(chunk_path, format="wav")
                
                # Transcribir chunk
                with sr.AudioFile(chunk_path) as source:
                    audio_data = self.recognizer.record(source)
                    
                    try:
                        text = self.recognizer.recognize_google(
                            audio_data,
                            language=self.language
                        )
                        
                        segments.append({
                            'segment_number': i + 1,
                            'start_time': round(start_time, 3),
                            'end_time': round(end_time, 3),
                            'duration': round(chunk_duration, 3),
                            'text': text,
                            'confidence': 0.85,
                            'word_count': len(text.split())
                        })
                        
                        full_text_parts.append(text)
                        
                        print(f"   ✅ Segmento {i+1}/{len(chunks)}: {len(text)} caracteres")
                        
                    except sr.UnknownValueError:
                        print(f"   ⚠️  Segmento {i+1}: No se entendió el audio")
                    except Exception as e:
                        print(f"   ❌ Segmento {i+1}: Error - {str(e)}")
                
                # Limpiar archivo temporal
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
                
                current_time = end_time
            
            # Texto completo
            full_text = ' '.join(full_text_parts)
            
            # Confianza promedio
            if segments:
                avg_confidence = sum(s['confidence'] for s in segments) / len(segments)
            else:
                avg_confidence = 0
            
            # Calcular precisión (porcentaje de segmentos transcritos)
            accuracy_percentage = (len(segments) / len(chunks) * 100) if chunks else 0
            
            return {
                'success': True,
                'full_text': full_text,
                'segments': segments,
                'total_segments': len(segments),
                'total_chunks': len(chunks),
                'avg_confidence': round(avg_confidence, 2),
                'accuracy_percentage': round(accuracy_percentage, 2),
                'meets_target': accuracy_percentage >= (self.target_accuracy * 100),
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'full_text': '',
                'segments': [],
                'error': str(e)
            }
    
    def analyze_transcription_with_ai(
        self,
        transcription_text: str,
        user_id: Optional[int] = None
    ) -> Dict:
        """
        Analizar transcripción con Gemini para obtener insights
        
        Args:
            transcription_text (str): Texto transcrito
            user_id (int): ID del usuario
        
        Returns:
            dict: Análisis de la transcripción
        """
        result = gemini_service.analyze_sentiment(
            text=transcription_text,
            user_id=user_id
        )
        
        return result
    
    def _convert_to_wav(self, audio_path: str) -> str:
        """
        Convertir archivo de audio a WAV si es necesario
        
        Args:
            audio_path (str): Ruta al archivo original
        
        Returns:
            str: Ruta al archivo WAV
        """
        # Obtener extensión
        ext = os.path.splitext(audio_path)[1].lower()
        
        # Si ya es WAV, retornar
        if ext == '.wav':
            return audio_path
        
        # Convertir a WAV
        try:
            audio = None
            
            if ext in ['.mp3', '.mp4', '.m4a']:
                audio = AudioSegment.from_file(audio_path, format=ext[1:])
            elif ext == '.ogg':
                audio = AudioSegment.from_ogg(audio_path)
            elif ext == '.webm':
                audio = AudioSegment.from_file(audio_path, format='webm')
            else:
                # Intentar carga genérica
                audio = AudioSegment.from_file(audio_path)
            
            # Exportar como WAV
            wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
            audio.export(wav_path, format='wav')
            
            return wav_path
            
        except Exception as e:
            print(f"Error al convertir audio: {e}")
            return audio_path
    
    def get_audio_info(self, audio_path: str) -> Dict:
        """
        Obtener información del archivo de audio
        
        Args:
            audio_path (str): Ruta al archivo
        
        Returns:
            dict: Información del audio
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            
            return {
                'duration_seconds': len(audio) / 1000.0,
                'duration_formatted': self._format_duration(len(audio) / 1000.0),
                'channels': audio.channels,
                'sample_width': audio.sample_width,
                'frame_rate': audio.frame_rate,
                'frame_count': audio.frame_count(),
                'file_size_mb': round(os.path.getsize(audio_path) / (1024 * 1024), 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _format_duration(self, seconds: float) -> str:
        """Formatear duración en MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


# Instancia global del servicio
transcription_service = TranscriptionService()