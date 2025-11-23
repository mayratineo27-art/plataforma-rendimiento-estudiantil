"""
Modelo para proyectos asociados a cursos
Permite gestionar múltiples proyectos/trabajos por curso
"""
from datetime import datetime
from app import db

class Project(db.Model):
    """Modelo para proyectos/trabajos dentro de un curso"""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('academic_courses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Información del proyecto
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(
        db.Enum('pendiente', 'en_progreso', 'completado', name='project_status'), 
        default='pendiente'
    )
    priority = db.Column(
        db.Enum('baja', 'media', 'alta', 'critica', name='project_priority'),
        default='media'
    )
    
    # Fechas
    start_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    
    # Tiempo total acumulado (en segundos)
    total_time_seconds = db.Column(db.Integer, default=0)
    
    # Metadatos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    course = db.relationship('AcademicCourse', backref='projects')
    user = db.relationship('User', backref='projects')
    time_sessions = db.relationship('TimeSession', backref='project', cascade='all, delete-orphan', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'course_name': self.course.name if self.course else None,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'total_time_seconds': self.total_time_seconds,
            'total_time_formatted': self.format_time(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'sessions_count': self.time_sessions.count()
        }

    def format_time(self):
        """Retorna el tiempo en formato HH:MM:SS"""
        hours = self.total_time_seconds // 3600
        minutes = (self.total_time_seconds % 3600) // 60
        seconds = self.total_time_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def format_time_static(seconds):
        """Método estático para formatear tiempo sin instancia"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


class TimeSession(db.Model):
    """Modelo para sesiones de tiempo de trabajo en proyectos"""
    __tablename__ = 'time_sessions'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Información de la sesión
    duration_seconds = db.Column(db.Integer, nullable=False, default=0)  # Duración de esta sesión
    notes = db.Column(db.Text)  # Notas opcionales sobre qué se hizo en esta sesión
    
    # Control de sesión activa
    is_active = db.Column(db.Boolean, default=False)
    is_paused = db.Column(db.Boolean, default=False)  # Si está pausada
    started_at = db.Column(db.DateTime)
    paused_at = db.Column(db.DateTime)
    resumed_at = db.Column(db.DateTime)
    last_activity_at = db.Column(db.DateTime)  # Última actividad detectada
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    
    # Relaciones
    user = db.relationship('User', backref='time_sessions')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'duration_seconds': self.duration_seconds,
            'duration_formatted': self.format_duration(),
            'notes': self.notes,
            'is_active': self.is_active,
            'is_paused': self.is_paused,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'paused_at': self.paused_at.isoformat() if self.paused_at else None,
            'resumed_at': self.resumed_at.isoformat() if self.resumed_at else None,
            'last_activity_at': self.last_activity_at.isoformat() if self.last_activity_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'created_at': self.created_at.isoformat()
        }

    def format_duration(self):
        """Retorna la duración en formato HH:MM:SS"""
        hours = self.duration_seconds // 3600
        minutes = (self.duration_seconds % 3600) // 60
        seconds = self.duration_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
