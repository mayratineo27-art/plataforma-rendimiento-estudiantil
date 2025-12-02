"""
Modelo para líneas de tiempo generadas
Permite guardar, visualizar y marcar pasos como completos
"""
from datetime import datetime
from app import db
import json


class Timeline(db.Model):
    """Modelo para líneas de tiempo generadas por IA"""
    __tablename__ = 'timelines'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('academic_courses.id'), nullable=True)
    
    # Información de la línea de tiempo
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    timeline_type = db.Column(
        db.Enum('academic', 'course', 'project', 'free', name='timeline_type'),
        default='project'
    )
    course_topic = db.Column(db.String(300), nullable=True)  # Tema específico del curso para timelines 'free'
    end_date = db.Column(db.DateTime)  # Fecha límite de la línea de tiempo
    
    # Contenido JSON con los pasos (mantener por compatibilidad)
    # Estructura: [{"step": 1, "title": "...", "description": "...", "duration": "...", "completed": false}, ...]
    steps_json = db.Column(db.Text, nullable=True)
    
    # Control de visibilidad y estado
    is_visible = db.Column(db.Boolean, default=True)
    is_completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.DateTime)
    
    # Metadatos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', backref='timelines')
    project = db.relationship('Project', backref='timelines')
    course = db.relationship('AcademicCourse', backref='timelines')
    steps = db.relationship('TimelineStep', back_populates='timeline', cascade="all, delete-orphan", order_by="TimelineStep.order")

    def to_dict(self):
        """Convierte el modelo a diccionario"""
        # Usar steps de la relación si existen, sino usar steps_json
        if self.steps:
            steps_list = [step.to_dict() for step in self.steps]
        else:
            steps_list = json.loads(self.steps_json) if self.steps_json else []
        
        # Calcular progreso
        completed_steps = sum(1 for step in steps_list if step.get('completed', False))
        total_steps = len(steps_list)
        progress = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'course_id': self.course_id,
            'course_name': self.course.name if self.course else None,
            'title': self.title,
            'description': self.description,
            'timeline_type': self.timeline_type,
            'course_topic': self.course_topic,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'steps': steps_list,
            'is_visible': self.is_visible,
            'is_completed': self.is_completed,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'progress': round(progress, 2),
            'completed_steps': completed_steps,
            'total_steps': total_steps,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update_steps(self, steps):
        """Actualiza los pasos de la línea de tiempo"""
        self.steps_json = json.dumps(steps)
        self.updated_at = datetime.utcnow()
        
        # Verificar si todos los pasos están completados
        all_completed = all(step.get('completed', False) for step in steps)
        if all_completed and not self.is_completed:
            self.is_completed = True
            self.completed_date = datetime.utcnow()
        elif not all_completed and self.is_completed:
            self.is_completed = False
            self.completed_date = None
    
    def mark_step_complete(self, step_index):
        """Marca un paso como completado"""
        steps = json.loads(self.steps_json) if self.steps_json else []
        if 0 <= step_index < len(steps):
            steps[step_index]['completed'] = True
            steps[step_index]['completed_at'] = datetime.utcnow().isoformat()
            self.update_steps(steps)
            return True
        return False
    
    def mark_step_incomplete(self, step_index):
        """Marca un paso como no completado"""
        steps = json.loads(self.steps_json) if self.steps_json else []
        if 0 <= step_index < len(steps):
            steps[step_index]['completed'] = False
            if 'completed_at' in steps[step_index]:
                del steps[step_index]['completed_at']
            self.update_steps(steps)
            return True
        return False
