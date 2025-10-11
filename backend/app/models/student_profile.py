"""
app/models/student_profile.py - Modelo de Perfil Integral del Estudiante
Plataforma Integral de Rendimiento Estudiantil - Módulo 3
"""

from datetime import datetime
from app import db


class StudentProfile(db.Model):
    """
    Modelo de Perfil Integral del Estudiante
    
    Consolida y sintetiza toda la información de los módulos 1 y 2 en un perfil
    unificado que identifica fortalezas, debilidades, estilo de aprendizaje
    y preparación para la tesis.
    """
    
    __tablename__ = 'student_profiles'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
        index=True
    )
    
    # Análisis académico (Módulo 1 data)
    total_documents_analyzed = db.Column(db.Integer, default=0)
    total_sessions_completed = db.Column(db.Integer, default=0)
    avg_writing_quality = db.Column(db.Numeric(5, 2))
    avg_vocabulary_richness = db.Column(db.Numeric(5, 2))
    writing_improvement_trend = db.Column(db.String(50))  # 'improving', 'stable', 'declining'
    
    # Fortalezas identificadas (JSON)
    academic_strengths = db.Column(db.JSON)  # ["análisis crítico", "investigación"]
    writing_strengths = db.Column(db.JSON)  # ["vocabulario técnico", "coherencia"]
    technical_strengths = db.Column(db.JSON)  # ["programación", "matemáticas"]
    
    # Debilidades identificadas (JSON)
    academic_weaknesses = db.Column(db.JSON)  # ["gestión del tiempo", "redacción"]
    writing_weaknesses = db.Column(db.JSON)  # ["ortografía", "sintaxis"]
    areas_for_improvement = db.Column(db.JSON)  # ["atención en clases largas"]
    
    # Estilo de aprendizaje
    learning_style = db.Column(db.String(100))  # 'visual', 'auditivo', 'kinestésico', 'mixto'
    learning_preferences = db.Column(db.JSON)  # {"visual": 70, "textual": 30}
    optimal_session_duration = db.Column(db.Integer)  # minutos
    attention_pattern = db.Column(db.String(100))  # 'consistent', 'fluctuating', 'declining'
    
    # Preparación para tesis
    thesis_readiness_score = db.Column(db.Numeric(5, 2))  # 0-100
    thesis_readiness_level = db.Column(
        db.Enum('bajo', 'medio', 'alto', 'excelente', name='readiness_levels')
    )
    estimated_preparation_months = db.Column(db.Integer)
    
    # Patrones de comportamiento (Módulo 2 data)
    most_productive_time = db.Column(db.String(50))  # 'morning', 'afternoon', 'evening'
    avg_attention_span_minutes = db.Column(db.Integer)
    emotion_patterns = db.Column(db.JSON)  # {"focused": 45, "confused": 15, ...}
    
    # Recomendaciones personalizadas (JSON)
    study_recommendations = db.Column(db.JSON)
    resource_recommendations = db.Column(db.JSON)
    
    # Resumen generado por IA
    ai_profile_summary = db.Column(db.Text)
    ai_personalized_advice = db.Column(db.Text)
    
    # Control de actualización
    last_updated = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, **kwargs):
        """
        Inicializar perfil de estudiante
        
        Args:
            user_id (int): ID del usuario
            **kwargs: Campos opcionales adicionales
        """
        self.user_id = user_id
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def regenerate_profile(self):
        """
        Regenerar perfil completo basado en datos actuales
        Este método debe ser llamado cuando hay nuevos datos de análisis
        """
        from app.models.user import User
        from app.models.document import Document
        from app.models.text_analysis import TextAnalysis
        from app.models.video_session import VideoSession
        from app.models.attention_metrics import AttentionMetrics
        
        user = User.query.get(self.user_id)
        if not user:
            return
        
        # Actualizar contadores básicos
        self.total_documents_analyzed = Document.query.filter_by(
            user_id=self.user_id,
            processing_status='completed'
        ).count()
        
        self.total_sessions_completed = VideoSession.query.filter_by(
            user_id=self.user_id,
            processing_status='completed'
        ).count()
        
        # Calcular promedios de escritura
        text_analyses = TextAnalysis.query.filter_by(user_id=self.user_id).all()
        if text_analyses:
            self.avg_writing_quality = sum(
                float(ta.writing_quality_score or 0) for ta in text_analyses
            ) / len(text_analyses)
            
            self.avg_vocabulary_richness = sum(
                float(ta.vocabulary_richness or 0) for ta in text_analyses
            ) / len(text_analyses)
        
        # Calcular patrones de atención
        attention_metrics = AttentionMetrics.query.filter_by(user_id=self.user_id).all()
        if attention_metrics:
            self.avg_attention_span_minutes = int(
                sum(am.interval_duration_seconds or 0 for am in attention_metrics) / 
                len(attention_metrics) / 60
            )
        
        # Determinar preparación para tesis
        self.calculate_thesis_readiness()
        
        # Actualizar timestamp
        self.last_updated = datetime.utcnow()
    
    def calculate_thesis_readiness(self):
        """
        Calcular score de preparación para tesis basado en múltiples factores
        """
        score = 0
        factors = []
        
        # Factor 1: Número de documentos analizados (0-25 puntos)
        if self.total_documents_analyzed >= 8:
            doc_score = 25
        else:
            doc_score = (self.total_documents_analyzed / 8) * 25
        score += doc_score
        factors.append(('documents', doc_score))
        
        # Factor 2: Calidad de escritura (0-30 puntos)
        if self.avg_writing_quality:
            writing_score = (float(self.avg_writing_quality) / 100) * 30
            score += writing_score
            factors.append(('writing_quality', writing_score))
        
        # Factor 3: Riqueza de vocabulario (0-20 puntos)
        if self.avg_vocabulary_richness:
            vocab_score = (float(self.avg_vocabulary_richness) / 100) * 20
            score += vocab_score
            factors.append(('vocabulary', vocab_score))
        
        # Factor 4: Capacidad de atención (0-15 puntos)
        if self.avg_attention_span_minutes:
            # Óptimo: 45-60 minutos
            if 45 <= self.avg_attention_span_minutes <= 60:
                attention_score = 15
            elif self.avg_attention_span_minutes > 60:
                attention_score = 12
            else:
                attention_score = (self.avg_attention_span_minutes / 45) * 15
            score += attention_score
            factors.append(('attention', attention_score))
        
        # Factor 5: Consistencia (0-10 puntos)
        if self.writing_improvement_trend == 'improving':
            consistency_score = 10
        elif self.writing_improvement_trend == 'stable':
            consistency_score = 7
        else:
            consistency_score = 3
        score += consistency_score
        factors.append(('consistency', consistency_score))
        
        self.thesis_readiness_score = round(score, 2)
        
        # Determinar nivel
        if score >= 80:
            self.thesis_readiness_level = 'excelente'
            self.estimated_preparation_months = 2
        elif score >= 65:
            self.thesis_readiness_level = 'alto'
            self.estimated_preparation_months = 4
        elif score >= 45:
            self.thesis_readiness_level = 'medio'
            self.estimated_preparation_months = 8
        else:
            self.thesis_readiness_level = 'bajo'
            self.estimated_preparation_months = 12
    
    def identify_strengths_and_weaknesses(self):
        """
        Identificar fortalezas y debilidades basado en análisis
        """
        strengths = {
            'academic': [],
            'writing': [],
            'technical': []
        }
        
        weaknesses = {
            'academic': [],
            'writing': [],
            'areas_improvement': []
        }
        
        # Análisis de escritura
        if self.avg_writing_quality:
            if float(self.avg_writing_quality) >= 75:
                strengths['writing'].append('Alta calidad de escritura')
            elif float(self.avg_writing_quality) < 50:
                weaknesses['writing'].append('Calidad de escritura necesita mejora')
        
        # Análisis de vocabulario
        if self.avg_vocabulary_richness:
            if float(self.avg_vocabulary_richness) >= 70:
                strengths['writing'].append('Vocabulario rico y técnico')
            elif float(self.avg_vocabulary_richness) < 40:
                weaknesses['writing'].append('Vocabulario limitado')
        
        # Análisis de atención
        if self.avg_attention_span_minutes:
            if self.avg_attention_span_minutes >= 45:
                strengths['academic'].append('Excelente capacidad de concentración')
            elif self.avg_attention_span_minutes < 20:
                weaknesses['areas_improvement'].append('Mejorar tiempo de atención')
        
        self.academic_strengths = strengths['academic']
        self.writing_strengths = strengths['writing']
        self.technical_strengths = strengths['technical']
        
        self.academic_weaknesses = weaknesses['academic']
        self.writing_weaknesses = weaknesses['writing']
        self.areas_for_improvement = weaknesses['areas_improvement']
    
    def generate_recommendations(self):
        """
        Generar recomendaciones personalizadas
        """
        study_recs = []
        resource_recs = []
        
        # Basado en estilo de aprendizaje
        if self.learning_style == 'visual':
            study_recs.append('Utiliza diagramas, mapas mentales y videos educativos')
            resource_recs.append('YouTube educational channels, Khan Academy')
        elif self.learning_style == 'auditivo':
            study_recs.append('Graba y escucha tus propias notas, participa en grupos de discusión')
            resource_recs.append('Podcasts educativos, audiolibros')
        
        # Basado en atención
        if self.avg_attention_span_minutes and self.avg_attention_span_minutes < 30:
            study_recs.append('Usa la técnica Pomodoro: 25 minutos de estudio, 5 de descanso')
        
        # Basado en preparación para tesis
        if self.thesis_readiness_level in ['bajo', 'medio']:
            study_recs.append('Incrementa la lectura de papers académicos')
            study_recs.append('Practica escritura académica semanalmente')
            resource_recs.append('Google Scholar, ResearchGate')
        
        self.study_recommendations = study_recs
        self.resource_recommendations = resource_recs
    
    @property
    def readiness_percentage(self):
        """Obtener porcentaje de preparación para tesis"""
        return float(self.thesis_readiness_score or 0)
    
    @property
    def has_sufficient_data(self):
        """Verificar si hay suficientes datos para análisis confiable"""
        return (self.total_documents_analyzed >= 3 or 
                self.total_sessions_completed >= 5)
    
    @property
    def overall_performance_level(self):
        """Calcular nivel de rendimiento general"""
        if not self.avg_writing_quality:
            return 'insuficiente_data'
        
        score = float(self.avg_writing_quality)
        if score >= 85:
            return 'excelente'
        elif score >= 70:
            return 'bueno'
        elif score >= 55:
            return 'regular'
        else:
            return 'necesita_mejora'
    
    def to_dict(self, include_detailed=False):
        """
        Convertir perfil a diccionario
        
        Args:
            include_detailed (bool): Incluir análisis detallado
            
        Returns:
            dict: Representación del perfil
        """
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'total_documents_analyzed': self.total_documents_analyzed,
            'total_sessions_completed': self.total_sessions_completed,
            'avg_writing_quality': float(self.avg_writing_quality or 0),
            'avg_vocabulary_richness': float(self.avg_vocabulary_richness or 0),
            'writing_improvement_trend': self.writing_improvement_trend,
            'learning_style': self.learning_style,
            'optimal_session_duration': self.optimal_session_duration,
            'thesis_readiness_score': float(self.thesis_readiness_score or 0),
            'thesis_readiness_level': self.thesis_readiness_level,
            'estimated_preparation_months': self.estimated_preparation_months,
            'most_productive_time': self.most_productive_time,
            'avg_attention_span_minutes': self.avg_attention_span_minutes,
            'has_sufficient_data': self.has_sufficient_data,
            'overall_performance_level': self.overall_performance_level,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_detailed:
            data.update({
                'academic_strengths': self.academic_strengths or [],
                'writing_strengths': self.writing_strengths or [],
                'technical_strengths': self.technical_strengths or [],
                'academic_weaknesses': self.academic_weaknesses or [],
                'writing_weaknesses': self.writing_weaknesses or [],
                'areas_for_improvement': self.areas_for_improvement or [],
                'learning_preferences': self.learning_preferences or {},
                'attention_pattern': self.attention_pattern,
                'emotion_patterns': self.emotion_patterns or {},
                'study_recommendations': self.study_recommendations or [],
                'resource_recommendations': self.resource_recommendations or [],
                'ai_profile_summary': self.ai_profile_summary,
                'ai_personalized_advice': self.ai_personalized_advice
            })
        
        return data
    
    def __repr__(self):
        """Representación string"""
        return f'<StudentProfile User {self.user_id} - Readiness: {self.thesis_readiness_level}>'