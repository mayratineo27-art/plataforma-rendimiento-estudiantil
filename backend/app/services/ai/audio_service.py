### Transcripción y análisis

# backend/app/services/ai/audio_service.py
import speech_recognition as sr
from pydub import AudioSegment
import os

class AudioService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = 'es-ES'  # Español

    def transcribe(self, audio_file_path):
        """
        Transcribe un archivo de audio a texto
        
        Args:
            audio_file_path: ruta al archivo de audio
            
        Returns:
            dict con transcripción y confianza
        """
        try:
            # Convertir audio a WAV si es necesario
            if not audio_file_path.endswith('.wav'):
                audio_file_path = self._convert_to_wav(audio_file_path)

            # Cargar audio
            with sr.AudioFile(audio_file_path) as source:
                # Ajustar para ruido ambiente
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Grabar audio
                audio_data = self.recognizer.record(source)

            # Transcribir con Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(
                    audio_data,
                    language=self.language
                )
                
                return {
                    'text': text,
                    'confidence': 0.85,  # Google no devuelve confidence
                    'language': self.language,
                    'success': True
                }

            except sr.UnknownValueError:
                return {
                    'text': '[Audio no comprensible]',
                    'confidence': 0,
                    'language': self.language,
                    'success': False
                }

            except sr.RequestError as e:
                print(f"Error en el servicio de reconocimiento: {str(e)}")
                return {
                    'text': f'[Error: {str(e)}]',
                    'confidence': 0,
                    'language': self.language,
                    'success': False
                }

        except Exception as e:
            print(f"Error transcribiendo audio: {str(e)}")
            return {
                'text': f'[Error: {str(e)}]',
                'confidence': 0,
                'language': self.language,
                'success': False
            }

    def _convert_to_wav(self, audio_file_path):
        """Convierte audio a formato WAV"""
        try:
            audio = AudioSegment.from_file(audio_file_path)
            wav_path = audio_file_path.rsplit('.', 1)[0] + '.wav'
            audio.export(wav_path, format='wav')
            return wav_path
        except Exception as e:
            print(f"Error convirtiendo audio: {str(e)}")
            return audio_file_path

    def analyze_sentiment(self, text):
        """
        Analiza el sentimiento de un texto
        (Simplificado, puedes mejorarlo con Gemini)
        """
        # Palabras positivas y negativas (simplificado)
        positive_words = ['bien', 'bueno', 'excelente', 'feliz', 'genial', 'perfecto']
        negative_words = ['mal', 'malo', 'triste', 'horrible', 'terrible', 'pésimo']

        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return {'sentiment': 'positive', 'score': 0.7}
        elif negative_count > positive_count:
            return {'sentiment': 'negative', 'score': 0.7}
        else:
            return {'sentiment': 'neutral', 'score': 0.5}