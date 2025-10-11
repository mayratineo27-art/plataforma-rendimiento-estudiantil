"""
app/models/video_session.py - Modelo de Sesión de Video
Plataforma Integral de Rendimiento Estudiantil - Módulo 2
"""

from datetime import datetime
from app import db


class VideoSession(db.Model):
    """
    Modelo de Sesión de Video
    
    Representa una sesión de análisis de video en tiempo real donde se captura
    la expresión facial y lenguaje corporal del estudiante durante una clase,
    estudio o exposición.
    """
    
    __tablename__ = 'video_sessions'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Información de la sesión
    session_name = db.Column(db.String(255))
    session_type = db.Column(
        db.Enum('clase', 'exposicion', 'estudio', 'tutorial', 'otro', name='session_types'),
        default='estudio'
    )
    course_name = db.Column(db.String(200))
    
    # Tiempos
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer)
    
    # Archivos de video
    video_file_path = db.Column(db.String(500))
    video_file_size = db.Column(db.Integer)
    
    # Estado de procesamiento
    processing_status = db.Column(
        db.Enum('recording', 'processing', 'completed', 'failed', name='processing_status_types'),
        default='recording'
    )
    processing_started_at = db.Column(db.DateTime)
    processing_completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    
    # Resumen de métricas (calculadas después del análisis)
    total_frames_analyzed = db.Column(db.Integer, default=0)
    faces_detected_count = db.Column(db.Integer, default=0)
    avg_attention_score = db.Column(db.Numeric(5, 2))
    dominant_emotion = db.Column(db.String(50))
    
    # Metadata adicional (JSON)
    metadata = db.Column(db.JSON)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    emotion_data = db.relationship(
        'EmotionData',
        backref='session',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    attention_metrics = db.relationship(
        'AttentionMetrics',
        backref='session',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    audio_sessions = db.relationship(
        'AudioSession',
        backref='video_session',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __init__(self, user_id, **kwargs):
        """
        Inicializar sesión de video
        
        Args:
            user_id (int): ID del usuario
            **kwargs: Campos opcionales adicionales
        """
        self.user_id = user_id
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def start_session(self):
        """Iniciar la sesión de grabación"""
        self.start_time = datetime.utcnow()
        self.processing_status = 'recording'
    
    def end_session(self):
        """Finalizar la sesión de grabación"""
        self.end_time = datetime.utcnow()
        if self.start_time:
            delta = self.end_time - self.start_time
            self.duration_seconds = int(delta.total_seconds())
        self.processing_status = 'processing'
    
    def complete_processing(self):
        """Marcar procesamiento como completado"""
        self.processing_status = 'completed'
        self.processing_completed_at = datetime.utcnow()
    
    def fail_processing(self, error_message):
        """
        Marcar procesamiento como fallido
        
        Args:
            error_message (str): Mensaje de error
        """
        self.processing_status = 'failed'
        self.error_message = error_message
        self.processing_completed_at = datetime.utcnow()
    
    def calculate_summary_metrics(self):
        """
        Calcular métricas resumen desde los datos de emoción
        Debe ejecutarse después de procesar todas las emociones
        """
        if not self.emotion_data.count():
            return
        
        # Total de frames analizados
        self.total_frames_analyzed = self.emotion_data.count()
        
        # Frames con rostro detectado
        self.faces_detected_count = self.emotion_data.filter_by(face_detected=True).count()
        
        # Emoción dominante más frecuente
        emotions = {}
        for emotion in self.emotion_data.filter(EmotionData.face_detected == True):
            emotion_name = emotion.dominant_emotion
            if emotion_name:
                emotions[emotion_name] = emotions.get(emotion_name, 0) + 1
        
        if emotions:
            self.dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        
        # Atención promedio
        if self.attention_metrics.count():
            avg_attention = db.session.query(
                db.func.avg(AttentionMetrics.attention_score)
            ).filter(
                AttentionMetrics.session_id == self.id
            ).scalar()
            self.avg_attention_score = avg_attention
    
    @property
    def duration_formatted(self):
        """Obtener duración formateada en HH:MM:SS"""
        if not self.duration_seconds:
            return "00:00:00"
        
        hours = self.duration_seconds // 3600
        minutes = (self.duration_seconds % 3600) // 60
        seconds = self.duration_seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    @property
    def is_active(self):
        """Verificar si la sesión está activa (grabando)"""
        return self.processing_status == 'recording'
    
    @property
    def is_completed(self):
        """Verificar si la sesión está completada"""
        return self.processing_status == 'completed'
    
    @property
    def has_video_file(self):
        """Verificar si tiene archivo de video asociado"""
        return bool(self.video_file_path)
    
    def to_dict(self, include_relations=False):
        """
        Convertir sesión a diccionario
        
        Args:
            include_relations (bool): Incluir relaciones (emociones, métricas)
            
        Returns:
            dict: Representación de la sesión
        """
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'session_name': self.session_name,
            'session_type': self.session_type,
            'course_name': self.course_name,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'duration_formatted': self.duration_formatted,
            'video_file_path': self.video_file_path,
            'video_file_size': self.video_file_size,
            'processing_status': self.processing_status,
            'total_frames_analyzed': self.total_frames_analyzed,
            'faces_detected_count': self.faces_detected_count,
            'avg_attention_score': float(self.avg_attention_score) if self.avg_attention_score else None,
            'dominant_emotion': self.dominant_emotion,
            'is_active': self.is_active,
            'is_completed': self.is_completed,
            'has_video_file': self.has_video_file,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_relations:
            data['emotion_data_count'] = self.emotion_data.count()
            data['attention_metrics_count'] = self.attention_metrics.count()
        
        return data
    
    def __repr__(self):
        """Representación string de la sesión"""
        return f'<VideoSession {self.id} - User {self.user_id} - {self.session_type}>'


# Importación necesaria para la relación (evitar import circular)
from app.models.emotion_data import EmotionData
from app.models.attention_metrics import AttentionMetrics