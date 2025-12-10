"""
Modelo de Evaluación de Escritura
==================================

Almacena todas las evaluaciones de escritura realizadas por los estudiantes,
incluyendo scores, métricas, feedback de IA y archivos asociados.
"""

from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship


class WritingEvaluation(db.Model):
    """
    Evaluación de escritura realizada por un estudiante
    
    Almacena:
    - Información del documento evaluado
    - Scores y métricas calculadas
    - Feedback detallado de la IA
    - Comparación con versiones anteriores
    - Archivos originales
    """
    __tablename__ = 'writing_evaluations'
    
    # Identificación
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('academic_courses.id'), nullable=True)
    
    # Archivos
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    previous_file_path = Column(String(500), nullable=True)
    
    # Metadata del documento
    word_count = Column(Integer, nullable=False)
    sentence_count = Column(Integer, nullable=False)
    paragraph_count = Column(Integer, nullable=False)
    vocabulary_size = Column(Integer, nullable=False)
    readability_score = Column(Float, nullable=False)
    
    # Scores de evaluación (0-100)
    overall_score = Column(Float, nullable=False)
    grammar_score = Column(Float, nullable=False)
    coherence_score = Column(Float, nullable=False)
    vocabulary_score = Column(Float, nullable=False)
    structure_score = Column(Float, nullable=False)
    
    # Análisis adicional
    tone_analysis = Column(String(50), nullable=True)  # formal, informal, académico, etc.
    formality_score = Column(Float, nullable=True)  # 0-100
    complexity_level = Column(String(50), nullable=True)  # básico, intermedio, avanzado
    
    # Comparación con versión anterior
    improvement_percentage = Column(Float, nullable=True)
    improvements_made = Column(JSON, nullable=True)  # Lista de mejoras
    
    # Feedback de IA
    strengths = Column(JSON, nullable=False)  # Lista de fortalezas
    weaknesses = Column(JSON, nullable=False)  # Lista de debilidades
    recommendations = Column(JSON, nullable=False)  # Lista de recomendaciones
    specific_errors = Column(JSON, nullable=True)  # Lista de errores específicos detectados
    suggestions = Column(JSON, nullable=True)  # Sugerencias de corrección
    
    # Resumen
    summary = Column(Text, nullable=False)
    
    # Métricas adicionales (JSON flexible)
    additional_metrics = Column(JSON, nullable=True)
    
    # Timestamps
    evaluated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    user = relationship('User', backref='writing_evaluations', lazy=True)
    course = relationship('AcademicCourse', backref='writing_evaluations', lazy=True)
    
    def __repr__(self):
        return f'<WritingEvaluation {self.id}: {self.file_name} - Score: {self.overall_score}>'
    
    def to_dict(self):
        """Convierte la evaluación a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'file_name': self.file_name,
            'evaluated_at': self.evaluated_at.isoformat() if self.evaluated_at else None,
            'metrics': {
                'word_count': self.word_count,
                'sentence_count': self.sentence_count,
                'paragraph_count': self.paragraph_count,
                'vocabulary_size': self.vocabulary_size,
                'readability_score': self.readability_score
            },
            'scores': {
                'overall': self.overall_score,
                'grammar': self.grammar_score,
                'coherence': self.coherence_score,
                'vocabulary': self.vocabulary_score,
                'structure': self.structure_score
            },
            'analysis': {
                'tone': self.tone_analysis,
                'formality': self.formality_score,
                'complexity': self.complexity_level
            },
            'evaluation': {
                'strengths': self.strengths,
                'weaknesses': self.weaknesses,
                'recommendations': self.recommendations,
                'specific_errors': self.specific_errors,
                'suggestions': self.suggestions,
                'summary': self.summary
            },
            'comparison': {
                'improvement_percentage': self.improvement_percentage,
                'improvements_made': self.improvements_made
            },
            'additional_metrics': self.additional_metrics
        }
    
    def to_summary_dict(self):
        """Versión resumida para listados"""
        return {
            'id': self.id,
            'file_name': self.file_name,
            'evaluated_at': self.evaluated_at.isoformat() if self.evaluated_at else None,
            'overall_score': self.overall_score,
            'word_count': self.word_count,
            'improvement_percentage': self.improvement_percentage
        }
