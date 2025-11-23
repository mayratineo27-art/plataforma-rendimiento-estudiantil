"""
app/models/__init__.py - Importación de todos los modelos
Plataforma Integral de Rendimiento Estudiantil

Este archivo centraliza la importación de todos los modelos para facilitar
su uso en toda la aplicación.
"""

# Importar modelos base
from app.models.user import User

# Módulo 1: Análisis de Progreso Académico
from app.models.document import Document
from app.models.text_analysis import TextAnalysis

# Módulo 2: Interacción en Tiempo Real
from app.models.video_session import VideoSession
from app.models.emotion_data import EmotionData
from app.models.attention_metrics import AttentionMetrics
from app.models.audio_session import AudioSession
from app.models.audio_transcription import AudioTranscription

# Módulo 3: Perfil Integral del Estudiante
from app.models.student_profile import StudentProfile

# Módulo 4: Reportes y Plantillas Personalizadas
from app.models.report import Report
from app.models.generated_template import GeneratedTemplate

# Lista de todos los modelos (útil para importaciones)
__all__ = [
    # Base
    'User',
    
    # Módulo 1
    'Document',
    'TextAnalysis',
    
    # Módulo 2
    'VideoSession',
    'EmotionData',
    'AttentionMetrics',
    'AudioSession',
    'AudioTranscription',
    
    # Módulo 3
    'StudentProfile',
    
    # Módulo 4
    'Report',
    'GeneratedTemplate'
]

# Al final del archivo, después de register_cli_commands

# Importar TODOS los modelos para que SQLAlchemy los reconozca
from app.models import (
    User, Document, TextAnalysis, VideoSession, EmotionData,
    AttentionMetrics, AudioSession, AudioTranscription,
    StudentProfile, Report, GeneratedTemplate
)

# En app/models/__init__.py, agregar al final:
from app.models.ai_interactions import AIInteraction

# Y agregarlo también a __all__:
__all__ = [
    # ... todos los anteriores
    'AIInteraction'  # ← Agregar esta línea
]

# 🆕 NUEVOS MODELOS ACADÉMICOS
from app.models.academic import AcademicCourse, AcademicTask 
from app.models.timer import StudyTimer
from app.models.project import Project, TimeSession

__all__ = [
    'User',
    # ... los demás ...
    'Report',
    'GeneratedTemplate',
    'AIInteraction',
    'AcademicCourse', # 🆕
    'AcademicTask',   # 🆕
    'StudyTimer',     # 🆕
    'Project',        # 🆕
    'TimeSession'     # 🆕
]

# ... import final ...
from app.models import (
    User, Document, TextAnalysis, VideoSession, EmotionData,
    AttentionMetrics, AudioSession, AudioTranscription,
    StudentProfile, Report, GeneratedTemplate, AIInteraction,
    AcademicCourse, AcademicTask, StudyTimer, Project, TimeSession # 🆕
)