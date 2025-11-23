from datetime import datetime
from app import db
import json

class SyllabusAnalysis(db.Model):
    """Modelo para Análisis de Sílabos con IA"""
    __tablename__ = 'syllabus_analysis'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('academic_courses.id'), nullable=False)
    
    file_path = db.Column(db.String(500))
    file_name = db.Column(db.String(255))
    
    # Información extraída del sílabo
    course_info_json = db.Column(db.Text)  # JSON con info del curso (profesor, créditos, etc.)
    topics_json = db.Column(db.Text)  # JSON con lista de temas
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', backref=db.backref('syllabus_analyses', lazy=True))
    course = db.relationship('AcademicCourse', backref=db.backref('syllabus_analyses', lazy=True))

    def get_course_info(self):
        """Obtiene la información del curso como diccionario"""
        if self.course_info_json:
            return json.loads(self.course_info_json)
        return {}
    
    def set_course_info(self, info_dict):
        """Guarda la información del curso como JSON"""
        self.course_info_json = json.dumps(info_dict, ensure_ascii=False)
    
    def get_topics(self):
        """Obtiene los temas como lista de diccionarios"""
        if self.topics_json:
            return json.loads(self.topics_json)
        return []
    
    def set_topics(self, topics_list):
        """Guarda los temas como JSON"""
        self.topics_json = json.dumps(topics_list, ensure_ascii=False)
    
    def toggle_topic_complete(self, topic_index):
        """Marca/desmarca un tema como completado"""
        topics = self.get_topics()
        if 0 <= topic_index < len(topics):
            topics[topic_index]['completed'] = not topics[topic_index].get('completed', False)
            if topics[topic_index]['completed']:
                topics[topic_index]['completed_at'] = datetime.utcnow().isoformat()
            else:
                topics[topic_index]['completed_at'] = None
            self.set_topics(topics)
            return True
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'course_name': self.course.name if self.course else 'Unknown',
            'file_name': self.file_name,
            'file_path': self.file_path,
            'course_info': self.get_course_info(),
            'topics': self.get_topics(),
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
