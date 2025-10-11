"""
app/models/report.py - Modelo de Reportes
Plataforma Integral de Rendimiento Estudiantil - Módulo 4
"""

from datetime import datetime
from app import db


class Report(db.Model):
    """
    Modelo de Reportes
    
    Representa reportes generados para estudiantes con análisis personalizado
    de su progreso académico, sesiones de video y recomendaciones.
    """
    
    __tablename__ = 'reports'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Información del reporte
    title = db.Column(db.String(255), nullable=False)
    report_type = db.Column(
        db.Enum('semestral', 'curso', 'sesion', 'progreso', 'integral', 'personalizado', 
                name='report_types'),
        nullable=False,
        index=True
    )
    description = db.Column(db.Text)
    
    # Período del reporte
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    cycle = db.Column(db.Integer)
    course_name = db.Column(db.String(200))
    
    # Archivos generados
    file_path = db.Column(db.String(500))
    file_name = db.Column(db.String(255))
    file_format = db.Column(db.String(20))  # pdf, docx, html, json
    file_size = db.Column(db.Integer)  # bytes
    
    # Estado de generación
    generation_status = db.Column(
        db.Enum('pending', 'generating', 'completed', 'failed', name='generation_status_types'),
        default='pending',
        index=True
    )
    generation_started_at = db.Column(db.DateTime)
    generation_completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    
    # Contenido del reporte (JSON)
    # Almacena todos los datos estructurados del reporte
    report_data = db.Column(db.JSON)
    
    # Datos para gráficos (JSON)
    # Formato: {"chart1": {...}, "chart2": {...}}
    charts_data = db.Column(db.JSON)
    
    # Personalización aplicada (JSON)
    # Perfil del estudiante usado para personalizar el reporte
    personalization_profile = db.Column(db.JSON)
    content_style = db.Column(db.String(100))  # 'visual', 'detailed', 'summary'
    
    # Metadata adicional
    meta_info = db.Column(db.JSON)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    templates = db.relationship(
        'GeneratedTemplate',
        backref='report',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __init__(self, user_id, title, report_type, **kwargs):
        """
        Inicializar reporte
        
        Args:
            user_id (int): ID del usuario
            title (str): Título del reporte
            report_type (str): Tipo de reporte
            **kwargs: Campos opcionales adicionales
        """
        self.user_id = user_id
        self.title = title
        self.report_type = report_type
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def start_generation(self):
        """Iniciar generación del reporte"""
        self.generation_status = 'generating'
        self.generation_started_at = datetime.utcnow()
    
    def complete_generation(self, file_path, file_name, file_format, file_size):
        """
        Marcar generación como completada
        
        Args:
            file_path (str): Ruta del archivo generado
            file_name (str): Nombre del archivo
            file_format (str): Formato del archivo
            file_size (int): Tamaño en bytes
        """
        self.generation_status = 'completed'
        self.generation_completed_at = datetime.utcnow()
        self.file_path = file_path
        self.file_name = file_name
        self.file_format = file_format
        self.file_size = file_size
    
    def fail_generation(self, error_message):
        """
        Marcar generación como fallida
        
        Args:
            error_message (str): Mensaje de error
        """
        self.generation_status = 'failed'
        self.error_message = error_message
        self.generation_completed_at = datetime.utcnow()
    
    @property
    def is_completed(self):
        """Verificar si está completado"""
        return self.generation_status == 'completed'
    
    @property
    def is_generating(self):
        """Verificar si está en generación"""
        return self.generation_status == 'generating'
    
    @property
    def has_file(self):
        """Verificar si tiene archivo generado"""
        return bool(self.file_path)
    
    @property
    def file_size_mb(self):
        """Obtener tamaño del archivo en MB"""
        if not self.file_size:
            return 0
        return round(self.file_size / (1024 * 1024), 2)
    
    @property
    def generation_time_seconds(self):
        """Calcular tiempo de generación en segundos"""
        if not self.generation_started_at or not self.generation_completed_at:
            return None
        
        delta = self.generation_completed_at - self.generation_started_at
        return int(delta.total_seconds())
    
    @property
    def period_duration_days(self):
        """Calcular duración del período en días"""
        if not self.period_start or not self.period_end:
            return None
        
        delta = self.period_end - self.period_start
        return delta.days
    
    def set_report_data(self, data_dict):
        """
        Establecer datos del reporte
        
        Args:
            data_dict (dict): Diccionario con datos estructurados del reporte
                {
                    "summary": {...},
                    "academic_performance": {...},
                    "attention_analysis": {...},
                    "recommendations": [...]
                }
        """
        self.report_data = data_dict
    
    def set_charts_data(self, charts_dict):
        """
        Establecer datos para gráficos
        
        Args:
            charts_dict (dict): Diccionario con datos de gráficos
                {
                    "progress_chart": {
                        "labels": [...],
                        "datasets": [...]
                    },
                    "attention_timeline": {...}
                }
        """
        self.charts_data = charts_dict
    
    def apply_personalization(self, student_profile):
        """
        Aplicar personalización basada en el perfil del estudiante
        
        Args:
            student_profile: Objeto StudentProfile
        """
        if not student_profile:
            return
        
        # Guardar perfil usado
        self.personalization_profile = {
            'learning_style': student_profile.learning_style,
            'thesis_readiness': student_profile.thesis_readiness_level,
            'strengths': student_profile.academic_strengths,
            'weaknesses': student_profile.academic_weaknesses
        }
        
        # Determinar estilo de contenido
        if student_profile.learning_style == 'visual':
            self.content_style = 'visual'
        elif student_profile.avg_writing_quality and float(student_profile.avg_writing_quality) >= 75:
            self.content_style = 'detailed'
        else:
            self.content_style = 'summary'
    
    def get_report_summary(self):
        """
        Obtener resumen ejecutivo del reporte
        
        Returns:
            dict: Resumen del reporte
        """
        if not self.report_data:
            return {}
        
        return {
            'title': self.title,
            'type': self.report_type,
            'period': f"{self.period_start} - {self.period_end}" if self.period_start else None,
            'main_insights': self.report_data.get('summary', {}).get('main_insights', []),
            'overall_score': self.report_data.get('summary', {}).get('overall_score'),
            'key_recommendations': self.report_data.get('recommendations', [])[:3]
        }
    
    def to_dict(self, include_data=False):
        """
        Convertir reporte a diccionario
        
        Args:
            include_data (bool): Incluir report_data completo
            
        Returns:
            dict: Representación del reporte
        """
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'report_type': self.report_type,
            'description': self.description,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'period_duration_days': self.period_duration_days,
            'cycle': self.cycle,
            'course_name': self.course_name,
            'file_path': self.file_path,
            'file_name': self.file_name,
            'file_format': self.file_format,
            'file_size': self.file_size,
            'file_size_mb': self.file_size_mb,
            'generation_status': self.generation_status,
            'is_completed': self.is_completed,
            'is_generating': self.is_generating,
            'has_file': self.has_file,
            'generation_time_seconds': self.generation_time_seconds,
            'content_style': self.content_style,
            'templates_count': self.templates.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_data:
            data['report_data'] = self.report_data
            data['charts_data'] = self.charts_data
            data['personalization_profile'] = self.personalization_profile
            data['summary'] = self.get_report_summary()
        
        return data
    
    def __repr__(self):
        """Representación string"""
        return f'<Report {self.id} - {self.title} ({self.report_type})>'