"""
app/models/ai_interactions.py - Modelo de Interacciones con IA
Plataforma Integral de Rendimiento Estudiantil
"""

from datetime import datetime
from app import db


class AIInteraction(db.Model):
    """
    Modelo de Interacciones con IA
    
    Registra todas las llamadas a APIs de IA para tracking, análisis de costos
    y debugging.
    """
    
    __tablename__ = 'ai_interactions'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    
    # Información de la interacción
    interaction_type = db.Column(db.String(100), nullable=False, index=True)
    ai_service = db.Column(db.String(50), nullable=False, index=True)  # 'gemini', 'openai', etc.
    model_used = db.Column(db.String(100))
    
    # Input/Output
    prompt_text = db.Column(db.Text)
    response_text = db.Column(db.Text)
    
    # Métricas
    tokens_used = db.Column(db.Integer)
    processing_time_ms = db.Column(db.Integer)
    cost_estimate = db.Column(db.Numeric(10, 6))  # Costo estimado en USD
    
    # Contexto
    related_entity_type = db.Column(db.String(50))  # 'document', 'video_session', etc.
    related_entity_id = db.Column(db.Integer)
    
    # Resultado
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AIInteraction {self.id} - {self.ai_service} - {self.interaction_type}>'