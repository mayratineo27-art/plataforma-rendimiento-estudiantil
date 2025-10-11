"""
app/models/emotion_data.py - Modelo de Datos de Emociones
Plataforma Integral de Rendimiento Estudiantil - Módulo 2
"""

from datetime import datetime
from app import db


class EmotionData(db.Model):
    """
    Modelo de Datos de Emociones
    
    Almacena los datos de emociones detectadas frame por frame durante
    una sesión de video. Incluye las 7 emociones básicas de DeepFace
    y mapeo a emociones contextuales.
    """
    
    __tablename__ = 'emotion_data'
    
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
    
    # Timestamp del frame
    timestamp_seconds = db.Column(db.Numeric(10, 3), nullable=False, index=True)
    frame_number = db.Column(db.Integer, nullable=False, index=True)
    
    # Detección facial
    face_detected = db.Column(db.Boolean, default=False)
    face_count = db.Column(db.Integer, default=0)
    face_confidence = db.Column(db.Numeric(5, 2))
    
    # Emociones básicas (7 emociones de DeepFace)
    # Valores entre 0 y 100
    emotion_angry = db.Column(db.Numeric(5, 2), default=0)
    emotion_disgust = db.Column(db.Numeric(5, 2), default=0)
    emotion_fear = db.Column(db.Numeric(5, 2), default=0)
    emotion_happy = db.Column(db.Numeric(5, 2), default=0)
    emotion_sad = db.Column(db.Numeric(5, 2), default=0)
    emotion_surprise = db.Column(db.Numeric(5, 2), default=0)
    emotion_neutral = db.Column(db.Numeric(5, 2), default=0)
    
    # Emoción dominante
    dominant_emotion = db.Column(db.String(50))
    dominant_emotion_confidence = db.Column(db.Numeric(5, 2))
    
    # Emociones contextuales (16 emociones mapeadas)
    contextual_emotion = db.Column(db.String(50))
    contextual_emotion_confidence = db.Column(db.Numeric(5, 2))
    
    # Atributos adicionales de DeepFace
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    
    # Datos del rostro (JSON)
    face_bbox = db.Column(db.JSON)  # Bounding box: {x, y, w, h}
    face_landmarks = db.Column(db.JSON)  # Puntos faciales
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, session_id, user_id, timestamp_seconds, frame_number, **kwargs):
        """
        Inicializar datos de emoción
        
        Args:
            session_id (int): ID de la sesión de video
            user_id (int): ID del usuario
            timestamp_seconds (float): Timestamp en segundos
            frame_number (int): Número de frame
            **kwargs: Campos opcionales adicionales
        """
        self.session_id = session_id
        self.user_id = user_id
        self.timestamp_seconds = timestamp_seconds
        self.frame_number = frame_number
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def set_emotions(self, emotion_dict):
        """
        Establecer emociones desde diccionario de DeepFace
        
        Args:
            emotion_dict (dict): Diccionario con emociones de DeepFace
                {
                    'angry': 0.1,
                    'disgust': 0.0,
                    'fear': 0.0,
                    'happy': 85.3,
                    'sad': 0.5,
                    'surprise': 10.1,
                    'neutral': 4.0
                }
        """
        self.emotion_angry = emotion_dict.get('angry', 0)
        self.emotion_disgust = emotion_dict.get('disgust', 0)
        self.emotion_fear = emotion_dict.get('fear', 0)
        self.emotion_happy = emotion_dict.get('happy', 0)
        self.emotion_sad = emotion_dict.get('sad', 0)
        self.emotion_surprise = emotion_dict.get('surprise', 0)
        self.emotion_neutral = emotion_dict.get('neutral', 0)
        
        # Determinar emoción dominante
        emotions = {
            'angry': self.emotion_angry,
            'disgust': self.emotion_disgust,
            'fear': self.emotion_fear,
            'happy': self.emotion_happy,
            'sad': self.emotion_sad,
            'surprise': self.emotion_surprise,
            'neutral': self.emotion_neutral
        }
        
        self.dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        self.dominant_emotion_confidence = max(emotions.values())
        
        # Mapear a emoción contextual
        self.map_contextual_emotion()
    
    def map_contextual_emotion(self):
        """
        Mapear las 7 emociones básicas a 16 emociones contextuales
        usando combinaciones y pesos de atención
        
        Emociones contextuales:
        - focused, interested, confused, bored, tired, frustrated
        - engaged, distracted, anxious, calm, motivated, discouraged
        - curious, overwhelmed, confident, uncertain
        """
        # Obtener valores de emociones
        angry = float(self.emotion_angry or 0)
        disgust = float(self.emotion_disgust or 0)
        fear = float(self.emotion_fear or 0)
        happy = float(self.emotion_happy or 0)
        sad = float(self.emotion_sad or 0)
        surprise = float(self.emotion_surprise or 0)
        neutral = float(self.emotion_neutral or 0)
        
        # Reglas de mapeo contextual
        contextual_scores = {}
        
        # FOCUSED: neutral alto + surprise bajo
        contextual_scores['focused'] = neutral * 0.7 + (100 - surprise) * 0.3
        
        # INTERESTED: happy medio + surprise medio + neutral bajo
        contextual_scores['interested'] = happy * 0.4 + surprise * 0.4 + (100 - neutral) * 0.2
        
        # CONFUSED: surprise alto + fear medio + disgust bajo
        contextual_scores['confused'] = surprise * 0.5 + fear * 0.3 + disgust * 0.2
        
        # BORED: neutral alto + sad bajo + (100 - happy)
        contextual_scores['bored'] = neutral * 0.5 + sad * 0.2 + (100 - happy) * 0.3
        
        # TIRED: sad medio + neutral alto + (100 - happy)
        contextual_scores['tired'] = sad * 0.4 + neutral * 0.3 + (100 - happy) * 0.3
        
        # FRUSTRATED: angry medio + sad bajo + disgust bajo
        contextual_scores['frustrated'] = angry * 0.5 + sad * 0.3 + disgust * 0.2
        
        # ENGAGED: happy alto + surprise medio + (100 - neutral)
        contextual_scores['engaged'] = happy * 0.6 + surprise * 0.2 + (100 - neutral) * 0.2
        
        # DISTRACTED: neutral bajo + (variación de emociones)
        emotion_variance = max(angry, fear, sad, surprise) - min(angry, fear, sad, surprise)
        contextual_scores['distracted'] = (100 - neutral) * 0.6 + emotion_variance * 0.4
        
        # ANXIOUS: fear alto + angry bajo + sad bajo
        contextual_scores['anxious'] = fear * 0.6 + angry * 0.2 + sad * 0.2
        
        # CALM: neutral alto + happy bajo + (100 - anger, fear)
        contextual_scores['calm'] = neutral * 0.5 + happy * 0.2 + (100 - angry - fear) * 0.3
        
        # MOTIVATED: happy alto + neutral bajo + surprise medio
        contextual_scores['motivated'] = happy * 0.6 + (100 - neutral) * 0.2 + surprise * 0.2
        
        # DISCOURAGED: sad alto + (100 - happy) + angry bajo
        contextual_scores['discouraged'] = sad * 0.5 + (100 - happy) * 0.3 + angry * 0.2
        
        # CURIOUS: surprise alto + happy medio + neutral bajo
        contextual_scores['curious'] = surprise * 0.5 + happy * 0.3 + (100 - neutral) * 0.2
        
        # OVERWHELMED: fear medio + surprise medio + sad bajo
        contextual_scores['overwhelmed'] = fear * 0.4 + surprise * 0.4 + sad * 0.2
        
        # CONFIDENT: happy alto + neutral medio + (100 - fear)
        contextual_scores['confident'] = happy * 0.5 + neutral * 0.2 + (100 - fear) * 0.3
        
        # UNCERTAIN: fear bajo + neutral medio + surprise bajo
        contextual_scores['uncertain'] = fear * 0.3 + neutral * 0.4 + surprise * 0.3
        
        # Determinar emoción contextual dominante
        if contextual_scores:
            self.contextual_emotion = max(contextual_scores.items(), key=lambda x: x[1])[0]
            self.contextual_emotion_confidence = max(contextual_scores.values())
    
    @property
    def emotions_dict(self):
        """Obtener diccionario de emociones básicas"""
        return {
            'angry': float(self.emotion_angry or 0),
            'disgust': float(self.emotion_disgust or 0),
            'fear': float(self.emotion_fear or 0),
            'happy': float(self.emotion_happy or 0),
            'sad': float(self.emotion_sad or 0),
            'surprise': float(self.emotion_surprise or 0),
            'neutral': float(self.emotion_neutral or 0)
        }
    
    @property
    def is_positive_emotion(self):
        """Verificar si la emoción dominante es positiva"""
        positive_emotions = ['happy', 'engaged', 'interested', 'motivated', 'curious', 'confident', 'calm']
        return self.contextual_emotion in positive_emotions
    
    @property
    def is_attention_indicator(self):
        """Verificar si indica buena atención"""
        attention_emotions = ['focused', 'interested', 'engaged', 'curious', 'motivated']
        return self.contextual_emotion in attention_emotions
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'timestamp_seconds': float(self.timestamp_seconds),
            'frame_number': self.frame_number,
            'face_detected': self.face_detected,
            'face_count': self.face_count,
            'emotions': self.emotions_dict,
            'dominant_emotion': self.dominant_emotion,
            'dominant_emotion_confidence': float(self.dominant_emotion_confidence or 0),
            'contextual_emotion': self.contextual_emotion,
            'contextual_emotion_confidence': float(self.contextual_emotion_confidence or 0),
            'is_positive': self.is_positive_emotion,
            'indicates_attention': self.is_attention_indicator,
            'age': self.age,
            'gender': self.gender,
            'face_bbox': self.face_bbox,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """Representación string"""
        return f'<EmotionData Frame {self.frame_number} - {self.contextual_emotion}>'