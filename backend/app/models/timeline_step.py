"""
Modelo mejorado para líneas de tiempo con pasos en tabla separada
"""
from datetime import datetime
from app import db


class TimelineStep(db.Model):
    """Modelo para pasos individuales de una línea de tiempo"""
    __tablename__ = 'timeline_steps'

    id = db.Column(db.Integer, primary_key=True)
    timeline_id = db.Column(db.Integer, db.ForeignKey('timelines.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)  # Orden del paso
    
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    timeline = db.relationship('Timeline', back_populates='steps')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'order': self.order,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def toggle_complete(self):
        """Alterna el estado de completado"""
        self.completed = not self.completed
        if self.completed:
            self.completed_at = datetime.utcnow()
        else:
            self.completed_at = None
