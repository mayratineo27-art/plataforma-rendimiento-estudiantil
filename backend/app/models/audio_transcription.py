"""
app/models/audio_transcription.py - Modelo de Transcripción de Audio
Plataforma Integral de Rendimiento Estudiantil - Módulo 2
"""

from datetime import datetime
from app import db


class AudioTranscription(db.Model):
    """
    Modelo de Transcripción de Audio
    
    Almacena segmentos individuales de transcripción de audio con su análisis
    de sentimiento y palabras clave. Permite análisis granular del contenido.
    """
    
    __tablename__ = 'audio_transcriptions'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    audio_session_id = db.Column(
        db.Integer,
        db.ForeignKey('audio_sessions.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    
    # Segmento de tiempo
    start_time = db.Column(db.Numeric(10, 3), nullable=False)
    end_time = db.Column(db.Numeric(10, 3), nullable=False)
    duration_seconds = db.Column(db.Numeric(6, 3))
    
    # Transcripción del segmento
    text = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.Numeric(5, 2))  # Confianza del reconocimiento
    
    # Análisis de sentimiento
    sentiment = db.Column(db.String(50))  # positive, negative, neutral, mixed
    sentiment_score = db.Column(db.Numeric(5, 2))  # -100 a +100
    
    # Palabras clave extraídas (JSON)
    # Ejemplo: ["inteligencia artificial", "machine learning", "python"]
    keywords = db.Column(db.JSON)
    
    # Análisis con Gemini (opcional)
    ai_analysis = db.Column(db.Text)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Índice compuesto para búsquedas por rango de tiempo
    __table_args__ = (
        db.Index('idx_time_range', 'start_time', 'end_time'),
    )
    
    def __init__(self, audio_session_id, user_id, start_time, end_time, text, **kwargs):
        """
        Inicializar transcripción de audio
        
        Args:
            audio_session_id (int): ID de la sesión de audio
            user_id (int): ID del usuario
            start_time (float): Tiempo de inicio en segundos
            end_time (float): Tiempo de fin en segundos
            text (str): Texto transcrito
            **kwargs: Campos opcionales adicionales
        """
        self.audio_session_id = audio_session_id
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.text = text
        
        # Calcular duración
        self.duration_seconds = float(end_time) - float(start_time)
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def analyze_sentiment_basic(self):
        """
        Análisis de sentimiento básico usando palabras clave
        (Mejorar con Gemini API para análisis más preciso)
        """
        if not self.text:
            self.sentiment = 'neutral'
            self.sentiment_score = 0
            return
        
        text_lower = self.text.lower()
        
        # Palabras positivas en español
        positive_words = [
            'excelente', 'bien', 'bueno', 'genial', 'perfecto', 'me gusta',
            'interesante', 'increíble', 'fantástico', 'maravilloso', 'claro',
            'entiendo', 'comprendo', 'sí', 'correcto', 'gracias'
        ]
        
        # Palabras negativas en español
        negative_words = [
            'mal', 'malo', 'terrible', 'difícil', 'complicado', 'confuso',
            'no entiendo', 'problema', 'error', 'fallo', 'aburrido',
            'cansado', 'frustrado', 'no', 'nunca', 'imposible'
        ]
        
        # Contar ocurrencias
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Calcular score
        total = positive_count + negative_count
        if total == 0:
            self.sentiment = 'neutral'
            self.sentiment_score = 0
        else:
            score = ((positive_count - negative_count) / total) * 100
            self.sentiment_score = round(score, 2)
            
            if score > 30:
                self.sentiment = 'positive'
            elif score < -30:
                self.sentiment = 'negative'
            else:
                self.sentiment = 'neutral'
    
    def extract_keywords_basic(self, top_n=5):
        """
        Extracción básica de palabras clave
        (Mejorar con NLP avanzado o Gemini API)
        
        Args:
            top_n (int): Número de palabras clave a extraer
        """
        if not self.text:
            self.keywords = []
            return
        
        # Palabras comunes a ignorar (stop words básicos en español)
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no',
            'haber', 'por', 'con', 'su', 'para', 'como', 'estar', 'tener',
            'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'o', 'poder', 'decir',
            'este', 'ir', 'otro', 'ese', 'la', 'si', 'me', 'ya', 'ver', 'porque',
            'dar', 'cuando', 'él', 'muy', 'sin', 'vez', 'mucho', 'saber', 'qué',
            'sobre', 'mi', 'alguno', 'mismo', 'yo', 'también', 'hasta', 'año',
            'dos', 'querer', 'entre', 'así', 'primero', 'desde', 'grande', 'eso',
            'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella', 'sí', 'día', 'uno',
            'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa', 'tanto', 'hombre',
            'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte', 'después', 'vida',
            'es', 'son', 'del', 'los', 'las', 'una', 'al'
        }
        
        # Tokenizar y limpiar
        words = self.text.lower().split()
        words = [w.strip('.,;:!?()[]{}\"\'') for w in words]
        
        # Filtrar palabras cortas y stop words
        words = [w for w in words if len(w) > 3 and w not in stop_words]
        
        # Contar frecuencias
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Obtener top N palabras más frecuentes
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        self.keywords = [word for word, freq in top_words]
    
    @property
    def timestamp_formatted(self):
        """Obtener rango de tiempo formateado MM:SS - MM:SS"""
        def format_time(seconds):
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes:02d}:{secs:02d}"
        
        start = format_time(float(self.start_time))
        end = format_time(float(self.end_time))
        return f"{start} - {end}"
    
    @property
    def word_count(self):
        """Contar palabras en el segmento"""
        if not self.text:
            return 0
        return len(self.text.split())
    
    @property
    def is_positive(self):
        """Verificar si el sentimiento es positivo"""
        return self.sentiment == 'positive'
    
    @property
    def is_negative(self):
        """Verificar si el sentimiento es negativo"""
        return self.sentiment == 'negative'
    
    @property
    def has_high_confidence(self):
        """Verificar si tiene alta confianza (>80%)"""
        if not self.confidence:
            return False
        return float(self.confidence) >= 80.0
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'audio_session_id': self.audio_session_id,
            'start_time': float(self.start_time),
            'end_time': float(self.end_time),
            'duration_seconds': float(self.duration_seconds or 0),
            'timestamp_formatted': self.timestamp_formatted,
            'text': self.text,
            'word_count': self.word_count,
            'confidence': float(self.confidence or 0),
            'has_high_confidence': self.has_high_confidence,
            'sentiment': self.sentiment,
            'sentiment_score': float(self.sentiment_score or 0),
            'is_positive': self.is_positive,
            'is_negative': self.is_negative,
            'keywords': self.keywords or [],
            'ai_analysis': self.ai_analysis,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """Representación string"""
        return f'<AudioTranscription {self.id} - [{self.timestamp_formatted}]>'