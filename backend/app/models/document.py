"""
app/models/document.py - Modelo de Documento
Plataforma Integral de Rendimiento Estudiantil - Módulo 1
"""

from datetime import datetime
from app import db


class Document(db.Model):
    """
    Modelo de Documento
    
    Representa documentos académicos (PDFs, DOCX) subidos por estudiantes
    para análisis de progreso en redacción, vocabulario y estructura.
    """
    
    __tablename__ = 'documents'
    
    # Identificadores
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Información del documento
    title = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # pdf, docx, doc
    file_size = db.Column(db.Integer, nullable=False)  # bytes
    mime_type = db.Column(db.String(100))
    
    # Contexto académico
    cycle = db.Column(db.Integer, nullable=False, index=True)  # 1-10
    course_name = db.Column(db.String(200))
    document_type = db.Column(
        db.Enum('informe', 'trabajo_final', 'proyecto', 'ensayo', 'monografia', 'otro', 
                name='document_types'),
        default='informe'
    )
    
    # Tiempos
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Estado de procesamiento
    processing_status = db.Column(
        db.Enum('pending', 'processing', 'completed', 'failed', name='doc_processing_status'),
        default='pending',
        index=True
    )
    processing_started_at = db.Column(db.DateTime)
    processing_completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    
    # Metadata adicional (JSON)
    metadata = db.Column(db.JSON)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    text_analysis = db.relationship(
        'TextAnalysis',
        backref='document',
        uselist=False,
        cascade='all, delete-orphan'
    )
    
    def __init__(self, user_id, title, file_name, file_path, file_type, 
                 file_size, cycle, **kwargs):
        """
        Inicializar documento
        
        Args:
            user_id (int): ID del usuario
            title (str): Título del documento
            file_name (str): Nombre del archivo
            file_path (str): Ruta del archivo
            file_type (str): Tipo de archivo
            file_size (int): Tamaño en bytes
            cycle (int): Ciclo académico
            **kwargs: Campos opcionales adicionales
        """
        self.user_id = user_id
        self.title = title
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = file_type
        self.file_size = file_size
        self.cycle = cycle
        
        # Campos opcionales
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def start_processing(self):
        """Iniciar procesamiento del documento"""
        self.processing_status = 'processing'
        self.processing_started_at = datetime.utcnow()
    
    def complete_processing(self):
        """Completar procesamiento exitoso"""
        self.processing_status = 'completed'
        self.processing_completed_at = datetime.utcnow()
    
    def fail_processing(self, error_message):
        """
        Marcar procesamiento como fallido
        
        Args:
            error_message (str): Mensaje de error
        """
        self.processing_status = 'failed'
        self.error_message = error_message
        self.processing_completed_at = datetime.utcnow()
    
    @property
    def file_size_mb(self):
        """Obtener tamaño del archivo en MB"""
        return round(self.file_size / (1024 * 1024), 2)
    
    @property
    def is_pdf(self):
        """Verificar si es PDF"""
        return self.file_type.lower() == 'pdf'
    
    @property
    def is_word(self):
        """Verificar si es Word"""
        return self.file_type.lower() in ['docx', 'doc']
    
    @property
    def is_completed(self):
        """Verificar si el procesamiento está completado"""
        return self.processing_status == 'completed'
    
    @property
    def is_processing(self):
        """Verificar si está en procesamiento"""
        return self.processing_status == 'processing'
    
    @property
    def has_analysis(self):
        """Verificar si tiene análisis de texto"""
        return self.text_analysis is not None
    
    @property
    def processing_time_seconds(self):
        """Calcular tiempo de procesamiento en segundos"""
        if not self.processing_started_at or not self.processing_completed_at:
            return None
        
        delta = self.processing_completed_at - self.processing_started_at
        return int(delta.total_seconds())
    
    @property
    def age_days(self):
        """Calcular edad del documento en días"""
        delta = datetime.utcnow() - self.upload_date
        return delta.days
    
    def get_file_extension(self):
        """Obtener extensión del archivo"""
        extensions = {
            'pdf': '.pdf',
            'docx': '.docx',
            'doc': '.doc'
        }
        return extensions.get(self.file_type.lower(), '')
    
    def to_dict(self, include_analysis=False):
        """
        Convertir documento a diccionario
        
        Args:
            include_analysis (bool): Incluir análisis de texto
            
        Returns:
            dict: Representación del documento
        """
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'file_size_mb': self.file_size_mb,
            'file_extension': self.get_file_extension(),
            'mime_type': self.mime_type,
            'cycle': self.cycle,
            'course_name': self.course_name,
            'document_type': self.document_type,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'processing_status': self.processing_status,
            'is_completed': self.is_completed,
            'is_processing': self.is_processing,
            'is_pdf': self.is_pdf,
            'is_word': self.is_word,
            'has_analysis': self.has_analysis,
            'processing_time_seconds': self.processing_time_seconds,
            'age_days': self.age_days,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_analysis and self.text_analysis:
            data['analysis'] = self.text_analysis.to_dict()
        
        return data
    
    def __repr__(self):
        """Representación string"""
        return f'<Document {self.id} - {self.title} (Ciclo {self.cycle})>'