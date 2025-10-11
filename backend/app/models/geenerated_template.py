"""
app/models/generated_template.py - Modelo de Plantillas Generadas
Plataforma Integral de Rendimiento Estudiantil - Módulo 4
"""

from datetime import datetime
from app import db


class GeneratedTemplate(db.Model):
    """
    Modelo de Plantillas Generadas
    
    Representa plantillas personalizadas (PPT, DOCX, PDF) generadas para
    estudiantes basadas en su perfil y necesidades específicas.
    """
    
    __tablename__ = 'generated_templates'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    report_id = db.Column(
        db.Integer,
        db.ForeignKey('reports.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    
    # Información de la plantilla
    title = db.Column(db.String(255), nullable=False)
    template_type = db.Column(
        db.Enum('ppt', 'docx', 'pdf', 'otro', name='template_types'),
        nullable=False,
        index=True
    )
    topic = db.Column(db.String(255))  # Tema de la plantilla
    description = db.Column(db.Text)
    
    # Archivo generado
    file_path = db.Column(db.String(500), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)  # bytes
    
    # Personalización aplicada (JSON)
    personalization_applied = db.Column(db.JSON)
    visual_style = db.Column(db.String(100))  # 'minimalist', 'colorful', 'professional', 'academic'
    content_focus = db.Column(db.JSON)  # Áreas de enfoque del contenido
    
    # IA utilizada para generación
    ai_model_used = db.Column(db.String(100))  # 'gemini-pro', 'gpt-4', etc.
    ai_prompt_used = db.Column(db.Text)  # Prompt utilizado
    
    # Estado de generación
    generation_status = db.Column(
        db.Enum('pending', 'generating', 'completed', 'failed', name='template_generation_status'),
        default='pending'
    )
    generation_time_seconds = db.Column(db.Integer)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, title, template_type, file_path, file_name, **kwargs):
        """
        Inicializar plantilla generada
        
        Args:
            user_id (int): ID del usuario
            title (str): Título de la plantilla
            template_type (str): Tipo de plantilla (ppt, docx, pdf)
            file_path (str): Ruta del archivo
            file_name (str): Nombre del archivo
            **kwargs: Campos opcionales adicionales
        """
        self.user_id = user_id
        self.title = title
        self.template_type = template_type
        self.file_path = file_path
        self.file_name = file_name
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def set_personalization(self, student_profile, preferences=None):
        """
        Establecer personalización basada en el perfil del estudiante
        
        Args:
            student_profile: Objeto StudentProfile
            preferences (dict): Preferencias adicionales del usuario
        """
        if not student_profile:
            return
        
        personalization = {
            'learning_style': student_profile.learning_style,
            'thesis_readiness_level': student_profile.thesis_readiness_level,
            'strengths': student_profile.academic_strengths or [],
            'weaknesses': student_profile.academic_weaknesses or []
        }
        
        # Agregar preferencias adicionales si existen
        if preferences:
            personalization['user_preferences'] = preferences
        
        self.personalization_applied = personalization
        
        # Determinar estilo visual basado en perfil
        if student_profile.learning_style == 'visual':
            self.visual_style = 'colorful'
        elif student_profile.thesis_readiness_level in ['alto', 'excelente']:
            self.visual_style = 'professional'
        else:
            self.visual_style = 'academic'
    
    def build_ai_prompt(self, topic, content_requirements):
        """
        Construir prompt mega-detallado para IA
        
        Args:
            topic (str): Tema de la plantilla
            content_requirements (dict): Requerimientos de contenido
                {
                    "num_slides": 10,
                    "include_images": True,
                    "depth_level": "intermediate"
                }
        
        Returns:
            str: Prompt completo para la IA
        """
        personalization = self.personalization_applied or {}
        learning_style = personalization.get('learning_style', 'mixto')
        strengths = personalization.get('strengths', [])
        weaknesses = personalization.get('weaknesses', [])
        
        prompt = f"""
Genera contenido para una {self.template_type.upper()} sobre: {topic}

PERFIL DEL ESTUDIANTE:
- Estilo de aprendizaje: {learning_style}
- Fortalezas: {', '.join(strengths) if strengths else 'No especificadas'}
- Áreas de mejora: {', '.join(weaknesses) if weaknesses else 'No especificadas'}

ESTILO VISUAL: {self.visual_style}

REQUISITOS DE CONTENIDO:
- Número de slides/páginas: {content_requirements.get('num_slides', 10)}
- Profundidad: {content_requirements.get('depth_level', 'intermediate')}
- Incluir imágenes: {'Sí' if content_requirements.get('include_images', True) else 'No'}

INSTRUCCIONES ESPECÍFICAS:
"""
        
        if learning_style == 'visual':
            prompt += """
1. USA MUCHAS ANALOGÍAS VISUALES y ejemplos gráficos
2. Cada concepto debe venir con una descripción visual
3. Incluye sugerencias de imágenes descriptivas
4. Usa bullet points cortos y concisos
5. Incluye diagramas cuando sea posible
"""
        elif learning_style == 'auditivo':
            prompt += """
1. Usa lenguaje narrativo y conversacional
2. Incluye preguntas retóricas para mantener engagement
3. Estructura el contenido como si fuera una presentación oral
4. Incluye notas del presentador detalladas
"""
        else:  # textual o mixto
            prompt += """
1. Proporciona explicaciones detalladas y completas
2. Incluye definiciones precisas
3. Usa ejemplos concretos y casos de estudio
4. Balancea texto con elementos visuales
"""
        
        if weaknesses:
            prompt += f"""
IMPORTANTE - El estudiante tiene dificultades en: {', '.join(weaknesses)}
Por favor, simplifica estos aspectos y proporciona explicaciones adicionales.
"""
        
        prompt += """
FORMATO DE SALIDA:
Proporciona el contenido en formato JSON estructurado con:
{
    "slides": [
        {
            "number": 1,
            "title": "Título de la slide",
            "content": "Contenido principal",
            "notes": "Notas del presentador",
            "visual_suggestions": "Sugerencias de imágenes/gráficos"
        }
    ]
}
"""
        
        self.ai_prompt_used = prompt
        return prompt
    
    @property
    def is_completed(self):
        """Verificar si está completada"""
        return self.generation_status == 'completed'
    
    @property
    def is_powerpoint(self):
        """Verificar si es PowerPoint"""
        return self.template_type == 'ppt'
    
    @property
    def is_word(self):
        """Verificar si es Word"""
        return self.template_type == 'docx'
    
    @property
    def is_pdf(self):
        """Verificar si es PDF"""
        return self.template_type == 'pdf'
    
    @property
    def file_size_mb(self):
        """Obtener tamaño del archivo en MB"""
        if not self.file_size:
            return 0
        return round(self.file_size / (1024 * 1024), 2)
    
    @property
    def file_extension(self):
        """Obtener extensión del archivo"""
        type_extensions = {
            'ppt': '.pptx',
            'docx': '.docx',
            'pdf': '.pdf'
        }
        return type_extensions.get(self.template_type, '')
    
    @property
    def generation_time_formatted(self):
        """Obtener tiempo de generación formateado"""
        if not self.generation_time_seconds:
            return "00:00"
        
        minutes = self.generation_time_seconds // 60
        seconds = self.generation_time_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_personalization_summary(self):
        """
        Obtener resumen de personalización aplicada
        
        Returns:
            dict: Resumen de personalización
        """
        if not self.personalization_applied:
            return {}
        
        return {
            'learning_style': self.personalization_applied.get('learning_style'),
            'visual_style': self.visual_style,
            'strengths_count': len(self.personalization_applied.get('strengths', [])),
            'weaknesses_count': len(self.personalization_applied.get('weaknesses', [])),
            'content_focus': self.content_focus
        }
    
    def to_dict(self, include_prompt=False):
        """
        Convertir plantilla a diccionario
        
        Args:
            include_prompt (bool): Incluir prompt de IA completo
            
        Returns:
            dict: Representación de la plantilla
        """
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'report_id': self.report_id,
            'title': self.title,
            'template_type': self.template_type,
            'topic': self.topic,
            'description': self.description,
            'file_path': self.file_path,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'file_size_mb': self.file_size_mb,
            'file_extension': self.file_extension,
            'visual_style': self.visual_style,
            'content_focus': self.content_focus,
            'ai_model_used': self.ai_model_used,
            'generation_status': self.generation_status,
            'is_completed': self.is_completed,
            'is_powerpoint': self.is_powerpoint,
            'is_word': self.is_word,
            'is_pdf': self.is_pdf,
            'generation_time_seconds': self.generation_time_seconds,
            'generation_time_formatted': self.generation_time_formatted,
            'personalization_summary': self.get_personalization_summary(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_prompt:
            data['ai_prompt_used'] = self.ai_prompt_used
            data['personalization_applied'] = self.personalization_applied
        
        return data
    
    def __repr__(self):
        """Representación string"""
        return f'<GeneratedTemplate {self.id} - {self.title} ({self.template_type})>'