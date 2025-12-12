"""
app/models/attention_metrics.py - Modelo de Métricas de Atención
Plataforma Integral de Rendimiento Estudiantil - Módulo 2
"""

from datetime import datetime
from app import db


class AttentionMetrics(db.Model):
    """
    Modelo de Métricas de Atención
    
    Calcula y almacena métricas de atención basadas en el análisis de emociones
    durante intervalos de tiempo específicos en una sesión de video.
    """
    
    __tablename__ = 'attention_metrics'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer,
        db.ForeignKey('video_sessions.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    
    # Intervalo de tiempo
    time_interval_start = db.Column(db.Numeric(10, 3), nullable=False)
    time_interval_end = db.Column(db.Numeric(10, 3), nullable=False)
    interval_duration_seconds = db.Column(db.Integer)
    
    # Score de atención (0-100)
    attention_score = db.Column(db.Numeric(5, 2), nullable=False)
    engagement_level = db.Column(
        db.Enum('muy_bajo', 'bajo', 'medio', 'alto', 'muy_alto', name='engagement_levels')
    )
    
    # Emociones predominantes en el intervalo (JSON)
    # Ejemplo: {"focused": 45.2, "interested": 30.5, "bored": 15.3}
    predominant_emotions = db.Column(db.JSON)
    
    # Indicadores de comprensión (JSON)
    # Ejemplo: {"confusion_percentage": 25.5, "clarity_moments": 3}
    comprehension_indicators = db.Column(db.JSON)
    
    # Métricas adicionales de análisis
    face_presence_rate = db.Column(db.Numeric(5, 2))  # Porcentaje de presencia del rostro
    confusion_percentage = db.Column(db.Numeric(5, 2))  # Porcentaje de confusión
    confusion_peaks = db.Column(db.Integer, default=0)  # Picos de confusión detectados
    comprehension_percentage = db.Column(db.Numeric(5, 2))  # Porcentaje de comprensión
    clarity_moments = db.Column(db.Integer, default=0)  # Momentos de claridad
    
    # Flags de detección
    confusion_detected = db.Column(db.Boolean, default=False)
    boredom_detected = db.Column(db.Boolean, default=False)
    
    # Análisis adicional
    notes = db.Column(db.Text)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Índices compuestos para búsquedas por rango de tiempo
    __table_args__ = (
        db.Index('idx_time_interval', 'time_interval_start', 'time_interval_end'),
    )
    
    def __init__(self, session_id, user_id, time_interval_start, time_interval_end, **kwargs):
        """
        Inicializar métrica de atención
        
        Args:
            session_id (int): ID de la sesión
            user_id (int): ID del usuario
            time_interval_start (float): Inicio del intervalo en segundos
            time_interval_end (float): Fin del intervalo en segundos
            **kwargs: Campos opcionales adicionales
        """
        self.session_id = session_id
        self.user_id = user_id
        self.time_interval_start = time_interval_start
        self.time_interval_end = time_interval_end
        
        # Calcular duración del intervalo
        self.interval_duration_seconds = int(float(time_interval_end) - float(time_interval_start))
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def calculate_attention_score(self, emotion_data_list):
        """
        Calcular score de atención basado en emociones del intervalo
        
        Args:
            emotion_data_list (list): Lista de objetos EmotionData en el intervalo
            
        Formula de atención:
        - Emociones positivas (focused, interested, engaged, etc.): +peso alto
        - Emociones neutras (neutral, calm): +peso medio
        - Emociones negativas (bored, tired, distracted): -peso alto
        """
        if not emotion_data_list:
            self.attention_score = 0
            self.engagement_level = 'muy_bajo'
            return
        
        # Pesos para diferentes emociones contextuales
        emotion_weights = {
            # Muy positivas para atención
            'focused': 95,
            'engaged': 90,
            'interested': 85,
            'motivated': 80,
            'curious': 75,
            
            # Positivas moderadas
            'confident': 70,
            'calm': 65,
            
            # Neutras
            'neutral': 50,
            'uncertain': 45,
            
            # Negativas para atención
            'confused': 35,
            'anxious': 30,
            'overwhelmed': 25,
            'frustrated': 20,
            'tired': 15,
            'bored': 10,
            'distracted': 5,
            'discouraged': 5
        }
        
        # Contadores de emociones
        emotion_counts = {}
        total_frames = len(emotion_data_list)
        
        # Contar emociones
        for emotion in emotion_data_list:
            if emotion.face_detected and emotion.contextual_emotion:
                ctx_emotion = emotion.contextual_emotion
                emotion_counts[ctx_emotion] = emotion_counts.get(ctx_emotion, 0) + 1
        
        # Calcular score ponderado
        weighted_score = 0
        for emotion, count in emotion_counts.items():
            weight = emotion_weights.get(emotion, 50)  # Default 50 si no está definido
            percentage = (count / total_frames) * 100
            weighted_score += (weight * percentage) / 100
        
        self.attention_score = round(weighted_score, 2)
        
        # Guardar emociones predominantes
        if emotion_counts:
            self.predominant_emotions = {
                emotion: round((count / total_frames) * 100, 2)
                for emotion, count in sorted(
                    emotion_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]  # Top 5 emociones
            }
        
        # Detectar confusión y aburrimiento
        self.confusion_detected = emotion_counts.get('confused', 0) / total_frames > 0.3
        self.boredom_detected = emotion_counts.get('bored', 0) / total_frames > 0.2
        
        # Calcular indicadores de comprensión
        confusion_percentage = (emotion_counts.get('confused', 0) / total_frames) * 100
        clarity_emotions = ['focused', 'engaged', 'interested', 'confident']
        clarity_frames = sum(emotion_counts.get(e, 0) for e in clarity_emotions)
        
        self.comprehension_indicators = {
            'confusion_percentage': round(confusion_percentage, 2),
            'clarity_percentage': round((clarity_frames / total_frames) * 100, 2),
            'total_frames_analyzed': total_frames,
            'faces_detected': sum(1 for e in emotion_data_list if e.face_detected)
        }
        
        # Determinar nivel de engagement
        self.determine_engagement_level()
    
    def determine_engagement_level(self):
        """Determinar nivel de engagement basado en attention_score"""
        score = float(self.attention_score or 0)
        
        if score >= 80:
            self.engagement_level = 'muy_alto'
        elif score >= 65:
            self.engagement_level = 'alto'
        elif score >= 45:
            self.engagement_level = 'medio'
        elif score >= 25:
            self.engagement_level = 'bajo'
        else:
            self.engagement_level = 'muy_bajo'
    
    @property
    def interval_duration_formatted(self):
        """Obtener duración formateada del intervalo"""
        if not self.interval_duration_seconds:
            return "00:00"
        
        minutes = self.interval_duration_seconds // 60
        seconds = self.interval_duration_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    @property
    def is_high_attention(self):
        """Verificar si es alta atención"""
        return float(self.attention_score or 0) >= 65
    
    @property
    def is_low_attention(self):
        """Verificar si es baja atención"""
        return float(self.attention_score or 0) < 45
    
    @property
    def needs_intervention(self):
        """Verificar si necesita intervención del instructor"""
        return self.confusion_detected or self.boredom_detected or self.is_low_attention
    
    def generate_feedback_message(self):
        """
        Generar mensaje de retroalimentación basado en las métricas
        
        Returns:
            str: Mensaje de retroalimentación
        """
        score = float(self.attention_score or 0)
        
        if self.engagement_level == 'muy_alto':
            return "¡Excelente! Mantienes un nivel de atención muy alto. Sigue así."
        elif self.engagement_level == 'alto':
            return "Buen nivel de atención. Estás concentrado en el material."
        elif self.engagement_level == 'medio':
            return "Nivel de atención moderado. Intenta eliminar distracciones."
        elif self.confusion_detected:
            return "Se detectó confusión. Considera revisar el material o pedir aclaraciones."
        elif self.boredom_detected:
            return "Pareces desconectado. Toma un breve descanso o cambia de actividad."
        else:
            return "Nivel de atención bajo. Intenta tomar un descanso y retomar con energía."
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'time_interval_start': float(self.time_interval_start),
            'time_interval_end': float(self.time_interval_end),
            'interval_duration_seconds': self.interval_duration_seconds,
            'interval_duration_formatted': self.interval_duration_formatted,
            'attention_score': float(self.attention_score or 0),
            'engagement_level': self.engagement_level,
            'predominant_emotions': self.predominant_emotions,
            'comprehension_indicators': self.comprehension_indicators,
            'face_presence_rate': float(self.face_presence_rate) if self.face_presence_rate else None,
            'confusion_percentage': float(self.confusion_percentage) if self.confusion_percentage else None,
            'confusion_peaks': self.confusion_peaks,
            'comprehension_percentage': float(self.comprehension_percentage) if self.comprehension_percentage else None,
            'clarity_moments': self.clarity_moments,
            'confusion_detected': self.confusion_detected,
            'boredom_detected': self.boredom_detected,
            'is_high_attention': self.is_high_attention,
            'is_low_attention': self.is_low_attention,
            'needs_intervention': self.needs_intervention,
            'feedback_message': self.generate_feedback_message(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """Representación string"""
        return f'<AttentionMetrics Session {self.session_id} - Score: {self.attention_score}>'