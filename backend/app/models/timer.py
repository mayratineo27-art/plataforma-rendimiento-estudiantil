"""
Modelo para gestión de cronómetros asociados a tareas y cursos
Permite tracking de tiempo dedicado a cada actividad académica
"""
from datetime import datetime
from app import db

class StudyTimer(db.Model):
    """Modelo para cronómetros de estudio"""
    __tablename__ = 'study_timers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('academic_courses.id'), nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('academic_tasks.id'), nullable=True)
    
    # Información del timer
    session_name = db.Column(db.String(200), nullable=True)  # Nombre opcional de la sesión
    total_seconds = db.Column(db.Integer, default=0)  # Tiempo total acumulado
    is_active = db.Column(db.Boolean, default=False)  # Si está corriendo actualmente
    started_at = db.Column(db.DateTime, nullable=True)  # Cuándo inició la sesión actual
    
    # Metadatos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', backref='study_timers')
    course = db.relationship('AcademicCourse', backref='timers')
    task = db.relationship('AcademicTask', backref='timers')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'course_name': self.course.name if self.course else None,
            'task_id': self.task_id,
            'task_name': self.task.title if self.task else None,
            'session_name': self.session_name,
            'total_seconds': self.total_seconds,
            'is_active': self.is_active,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def format_time(self):
        """Retorna el tiempo en formato HH:MM:SS"""
        hours = self.total_seconds // 3600
        minutes = (self.total_seconds % 3600) // 60
        seconds = self.total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
