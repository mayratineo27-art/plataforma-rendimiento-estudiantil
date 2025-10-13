"""
app/models/audio_session.py - Modelo de Sesión de Audio
Plataforma Integral de Rendimiento Estudiantil - Módulo 2
"""

from datetime import datetime
from app import db


class AudioSession(db.Model):
    """
    Modelo de Sesión de Audio
    
    Representa una sesión de captura y transcripción de audio, que puede estar
    asociada a una sesión de video o ser independiente. Almacena el audio
    y su transcripción completa.
    """
    
    __tablename__ = 'audio_sessions'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer,
        db.ForeignKey('video_sessions.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Información del audio
    audio_file_path = db.Column(db.String(500))
    audio_file_size = db.Column(db.Integer)  # En bytes
    audio_duration_seconds = db.Column(db.Integer)
    audio_format = db.Column(db.String(20))  # mp3, wav, ogg, etc.
    
    # Estado de procesamiento
    processing_status = db.Column(
        db.Enum('pending', 'processing', 'completed', 'failed', name='audio_processing_status'),
        default='pending',
        index=True
    )
    processing_started_at = db.Column(db.DateTime)
    processing_completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    
    # Transcripción completa
    transcription_text = db.Column(db.Text)  # Transcripción completa
    transcription_confidence = db.Column(db.Numeric(5, 2))  # Confianza promedio
    transcription_accuracy_percentage = db.Column(db.Numeric(5, 2))  # Objetivo: >70%
    language_detected = db.Column(db.String(10))  # es-ES, en-US, etc.
    
    # Metadata (JSON)
    # Puede incluir: sample_rate, channels, bitrate, etc.
    meta_info = db.Column(db.JSON)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    transcriptions = db.relationship(
        'AudioTranscription',
        backref='audio_session',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __init__(self, user_id, **kwargs):
        """
        Inicializar sesión de audio
        
        Args:
            user_id (int): ID del usuario
            **kwargs: Campos opcionales adicionales
        """
        self.user_id = user_id
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def start_processing(self):
        """Iniciar procesamiento del audio"""
        self.processing_status = 'processing'
        self.processing_started_at = datetime.utcnow()
    
    def complete_processing(self, transcription_text, confidence, accuracy):
        """
        Completar procesamiento exitoso
        
        Args:
            transcription_text (str): Texto transcrito completo
            confidence (float): Confianza promedio
            accuracy (float): Porcentaje de precisión
        """
        self.processing_status = 'completed'
        self.processing_completed_at = datetime.utcnow()
        self.transcription_text = transcription_text
        self.transcription_confidence = confidence
        self.transcription_accuracy_percentage = accuracy
    
    def fail_processing(self, error_message):
        """
        Marcar procesamiento como fallido
        
        Args:
            error_message (str): Mensaje de error
        """
        self.processing_status = 'failed'
        self.error_message = error_message
        self.processing_completed_at = datetime.utcnow()
    
    @property
    def duration_formatted(self):
        """Obtener duración formateada en MM:SS"""
        if not self.audio_duration_seconds:
            return "00:00"
        
        minutes = self.audio_duration_seconds // 60
        seconds = self.audio_duration_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    @property
    def file_size_mb(self):
        """Obtener tamaño del archivo en MB"""
        if not self.audio_file_size:
            return 0
        return round(self.audio_file_size / (1024 * 1024), 2)
    
    @property
    def is_completed(self):
        """Verificar si el procesamiento está completado"""
        return self.processing_status == 'completed'
    
    @property
    def is_processing(self):
        """Verificar si está en procesamiento"""
        return self.processing_status == 'processing'
    
    @property
    def has_good_accuracy(self):
        """Verificar si cumple el objetivo de >70% de precisión"""
        if not self.transcription_accuracy_percentage:
            return False
        return float(self.transcription_accuracy_percentage) >= 70.0
    
    @property
    def is_linked_to_video(self):
        """Verificar si está asociado a una sesión de video"""
        return self.session_id is not None
    
    @property
    def word_count(self):
        """Contar palabras en la transcripción"""
        if not self.transcription_text:
            return 0
        return len(self.transcription_text.split())
    
    @property
    def processing_time_seconds(self):
        """Calcular tiempo de procesamiento en segundos"""
        if not self.processing_started_at or not self.processing_completed_at:
            return None
        
        delta = self.processing_completed_at - self.processing_started_at
        return int(delta.total_seconds())
    
    def get_transcription_summary(self, max_words=50):
        """
        Obtener resumen de la transcripción
        
        Args:
            max_words (int): Número máximo de palabras
            
        Returns:
            str: Resumen de la transcripción
        """
        if not self.transcription_text:
            return ""
        
        words = self.transcription_text.split()
        if len(words) <= max_words:
            return self.transcription_text
        
        return ' '.join(words[:max_words]) + '...'
    
    def calculate_statistics(self):
        """
        Calcular estadísticas de la transcripción
        
        Returns:
            dict: Estadísticas calculadas
        """
        if not self.transcription_text:
            return {}
        
        text = self.transcription_text
        words = text.split()
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        return {
            'total_words': len(words),
            'total_sentences': len(sentences),
            'avg_words_per_sentence': round(len(words) / len(sentences), 2) if sentences else 0,
            'total_characters': len(text),
            'unique_words': len(set(word.lower() for word in words)),
            'vocabulary_richness': round(len(set(word.lower() for word in words)) / len(words) * 100, 2) if words else 0
        }
    
    def to_dict(self, include_transcription=True):
        """
        Convertir a diccionario
        
        Args:
            include_transcription (bool): Incluir texto completo de transcripción
            
        Returns:
            dict: Representación de la sesión de audio
        """
        data = {
            'id': self.id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'audio_file_path': self.audio_file_path,
            'audio_file_size': self.audio_file_size,
            'file_size_mb': self.file_size_mb,
            'audio_duration_seconds': self.audio_duration_seconds,
            'duration_formatted': self.duration_formatted,
            'audio_format': self.audio_format,
            'processing_status': self.processing_status,
            'is_completed': self.is_completed,
            'is_processing': self.is_processing,
            'transcription_confidence': float(self.transcription_confidence or 0),
            'transcription_accuracy_percentage': float(self.transcription_accuracy_percentage or 0),
            'has_good_accuracy': self.has_good_accuracy,
            'language_detected': self.language_detected,
            'word_count': self.word_count,
            'is_linked_to_video': self.is_linked_to_video,
            'processing_time_seconds': self.processing_time_seconds,
            'transcription_segments_count': self.transcriptions.count(),
            'meta_info': self.meta_info,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_transcription:
            data['transcription_text'] = self.transcription_text
            data['transcription_summary'] = self.get_transcription_summary()
            data['statistics'] = self.calculate_statistics()
        
        return data
    
    def __repr__(self):
        """Representación string"""
        return f'<AudioSession {self.id} - User {self.user_id} - {self.processing_status}>'