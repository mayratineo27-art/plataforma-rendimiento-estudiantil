from datetime import datetime
from app import db

class AcademicCourse(db.Model):
    """Modelo para Cursos/Materias"""
    __tablename__ = 'academic_courses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(50))  # Código del curso (ej: MAT-101)
    professor = db.Column(db.String(150))
    schedule_info = db.Column(db.String(255)) 
    category = db.Column(db.String(50), default='general')  # Categoría del curso
    icon = db.Column(db.String(50), default='BookOpen')  # Icono del curso
    color = db.Column(db.String(20), default="blue")  # Color del curso
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación inversa segura: No tocamos User, pero User podrá acceder a .courses
    user = db.relationship('User', backref=db.backref('courses', lazy=True))
    
    # Relaciones internas
    tasks = db.relationship('AcademicTask', backref='course', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'professor': self.professor,
            'schedule_info': self.schedule_info,
            'category': self.category,
            'icon': self.icon,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AcademicTask(db.Model):
    """Modelo para Tareas y Exámenes"""
    __tablename__ = 'academic_tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('academic_courses.id'), nullable=True)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Enum('baja', 'media', 'alta', 'critica', name='task_priority'), default='media')
    status = db.Column(db.Enum('pendiente', 'en_progreso', 'completada', name='task_status'), default='pendiente')
    origin = db.Column(db.String(50), default='manual') # 'manual' o 'syllabus_ai'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'course_name': self.course.name if self.course else 'General',
            'title': self.title,
            'due_date': self.due_date.isoformat(),
            'priority': self.priority,
            'status': self.status,
            'origin': self.origin
        }