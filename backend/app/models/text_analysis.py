"""
app/models/text_analysis.py - Modelo de Análisis de Texto
Plataforma Integral de Rendimiento Estudiantil - Módulo 1
"""

from datetime import datetime
from app import db


class TextAnalysis(db.Model):
    """
    Modelo de Análisis de Texto
    
    Almacena los resultados del análisis de texto de documentos académicos,
    incluyendo métricas de vocabulario, complejidad, coherencia y análisis
    semántico con IA.
    """
    
    __tablename__ = 'text_analysis'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(
        db.Integer,
        db.ForeignKey('documents.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Métricas de vocabulario
    total_words = db.Column(db.Integer)
    unique_words = db.Column(db.Integer)
    vocabulary_richness = db.Column(db.Numeric(5, 2))  # Porcentaje
    technical_terms_count = db.Column(db.Integer)
    technical_terms = db.Column(db.JSON)  # Lista de términos técnicos encontrados
    
    # Métricas de complejidad
    avg_sentence_length = db.Column(db.Numeric(6, 2))  # Palabras por oración
    avg_word_length = db.Column(db.Numeric(5, 2))  # Caracteres por palabra
    sentence_complexity_score = db.Column(db.Numeric(5, 2))  # 0-100
    readability_score = db.Column(db.Numeric(5, 2))  # 0-100
    
    # Análisis estructural
    paragraph_count = db.Column(db.Integer)
    sentence_count = db.Column(db.Integer)
    coherence_score = db.Column(db.Numeric(5, 2))  # 0-100
    cohesion_score = db.Column(db.Numeric(5, 2))  # 0-100
    
    # Análisis semántico con IA
    main_topics = db.Column(db.JSON)  # Temas principales identificados
    key_concepts = db.Column(db.JSON)  # Conceptos clave
    writing_quality_score = db.Column(db.Numeric(5, 2))  # 0-100
    academic_level_assessment = db.Column(db.String(50))  # 'básico', 'intermedio', 'avanzado'
    
    # Comparación con documentos previos
    improvement_percentage = db.Column(db.Numeric(5, 2))  # Mejora respecto al anterior
    comparison_notes = db.Column(db.Text)
    
    # Tiempo de desarrollo (si está disponible)
    development_time_minutes = db.Column(db.Integer)
    
    # Análisis completo generado por IA
    ai_analysis_summary = db.Column(db.Text)
    ai_recommendations = db.Column(db.Text)
    
    # Timestamp
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, document_id, user_id, **kwargs):
        """
        Inicializar análisis de texto
        
        Args:
            document_id (int): ID del documento
            user_id (int): ID del usuario
            **kwargs: Campos opcionales adicionales
        """
        self.document_id = document_id
        self.user_id = user_id
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def calculate_vocabulary_richness(self):
        """
        Calcular riqueza de vocabulario (Type-Token Ratio)
        Formula: (unique_words / total_words) * 100
        """
        if self.total_words and self.unique_words:
            self.vocabulary_richness = round(
                (self.unique_words / self.total_words) * 100, 2
            )
        else:
            self.vocabulary_richness = 0
    
    def set_basic_metrics(self, text):
        """
        Establecer métricas básicas a partir del texto
        
        Args:
            text (str): Texto completo del documento
        """
        if not text:
            return
        
        # Contar palabras
        words = text.split()
        self.total_words = len(words)
        self.unique_words = len(set(word.lower() for word in words))
        
        # Calcular longitud promedio de palabra
        if words:
            self.avg_word_length = round(
                sum(len(word) for word in words) / len(words), 2
            )
        
        # Contar oraciones (aproximación simple)
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        self.sentence_count = len(sentences)
        
        # Longitud promedio de oración
        if sentences:
            self.avg_sentence_length = round(
                sum(len(s.split()) for s in sentences) / len(sentences), 2
            )
        
        # Contar párrafos (aproximación)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        self.paragraph_count = len(paragraphs)
        
        # Calcular riqueza de vocabulario
        self.calculate_vocabulary_richness()
    
    def compare_with_previous(self, previous_analysis):
        """
        Comparar con análisis previo del mismo estudiante
        
        Args:
            previous_analysis: Objeto TextAnalysis previo
        """
        if not previous_analysis:
            self.improvement_percentage = 0
            self.comparison_notes = "Primer documento analizado - sin comparación previa"
            return
        
        # Calcular mejora en calidad de escritura
        if self.writing_quality_score and previous_analysis.writing_quality_score:
            current = float(self.writing_quality_score)
            previous = float(previous_analysis.writing_quality_score)
            
            self.improvement_percentage = round(
                ((current - previous) / previous) * 100, 2
            )
            
            # Generar notas de comparación
            improvements = []
            declines = []
            
            # Comparar vocabulario
            if float(self.vocabulary_richness or 0) > float(previous_analysis.vocabulary_richness or 0):
                improvements.append("vocabulario más rico")
            elif float(self.vocabulary_richness or 0) < float(previous_analysis.vocabulary_richness or 0):
                declines.append("vocabulario menos variado")
            
            # Comparar complejidad de oraciones
            if float(self.sentence_complexity_score or 0) > float(previous_analysis.sentence_complexity_score or 0):
                improvements.append("oraciones más complejas")
            elif float(self.sentence_complexity_score or 0) < float(previous_analysis.sentence_complexity_score or 0):
                declines.append("oraciones menos complejas")
            
            # Comparar coherencia
            if float(self.coherence_score or 0) > float(previous_analysis.coherence_score or 0):
                improvements.append("mejor coherencia")
            elif float(self.coherence_score or 0) < float(previous_analysis.coherence_score or 0):
                declines.append("menor coherencia")
            
            notes = []
            if improvements:
                notes.append(f"Mejoras: {', '.join(improvements)}")
            if declines:
                notes.append(f"Aspectos a trabajar: {', '.join(declines)}")
            
            self.comparison_notes = '. '.join(notes) if notes else "Rendimiento similar al anterior"
    
    @property
    def overall_quality_level(self):
        """Determinar nivel general de calidad"""
        if not self.writing_quality_score:
            return 'no_evaluado'
        
        score = float(self.writing_quality_score)
        if score >= 85:
            return 'excelente'
        elif score >= 70:
            return 'bueno'
        elif score >= 55:
            return 'regular'
        else:
            return 'necesita_mejora'
    
    @property
    def has_good_vocabulary(self):
        """Verificar si tiene buen vocabulario (>60%)"""
        if not self.vocabulary_richness:
            return False
        return float(self.vocabulary_richness) >= 60.0
    
    @property
    def is_improving(self):
        """Verificar si está mejorando respecto al anterior"""
        if not self.improvement_percentage:
            return None
        return float(self.improvement_percentage) > 0
    
    @property
    def word_density(self):
        """Calcular densidad de palabras por párrafo"""
        if not self.paragraph_count or not self.total_words:
            return 0
        return round(self.total_words / self.paragraph_count, 2)
    
    def to_dict(self):
        """Convertir análisis a diccionario"""
        return {
            'id': self.id,
            'document_id': self.document_id,
            'user_id': self.user_id,
            'total_words': self.total_words,
            'unique_words': self.unique_words,
            'vocabulary_richness': float(self.vocabulary_richness or 0),
            'technical_terms_count': self.technical_terms_count,
            'technical_terms': self.technical_terms or [],
            'avg_sentence_length': float(self.avg_sentence_length or 0),
            'avg_word_length': float(self.avg_word_length or 0),
            'sentence_complexity_score': float(self.sentence_complexity_score or 0),
            'readability_score': float(self.readability_score or 0),
            'paragraph_count': self.paragraph_count,
            'sentence_count': self.sentence_count,
            'coherence_score': float(self.coherence_score or 0),
            'cohesion_score': float(self.cohesion_score or 0),
            'main_topics': self.main_topics or [],
            'key_concepts': self.key_concepts or [],
            'writing_quality_score': float(self.writing_quality_score or 0),
            'academic_level_assessment': self.academic_level_assessment,
            'improvement_percentage': float(self.improvement_percentage or 0),
            'comparison_notes': self.comparison_notes,
            'development_time_minutes': self.development_time_minutes,
            'ai_analysis_summary': self.ai_analysis_summary,
            'ai_recommendations': self.ai_recommendations,
            'overall_quality_level': self.overall_quality_level,
            'has_good_vocabulary': self.has_good_vocabulary,
            'is_improving': self.is_improving,
            'word_density': self.word_density,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """Representación string"""
        return f'<TextAnalysis Document {self.document_id} - Quality: {self.writing_quality_score}>'