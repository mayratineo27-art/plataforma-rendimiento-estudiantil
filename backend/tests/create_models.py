"""
Script para crear modelos básicos del backend
Soluciona: "cannot import name 'user' from 'app.models'"
"""

from pathlib import Path

# Modelos básicos para el sistema

USER_MODEL = '''"""
Modelo de Usuario
"""

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """Modelo de usuario del sistema"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre_completo = db.Column(db.String(200))
    carrera = db.Column(db.String(100))
    ciclo_actual = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    documentos = db.relationship('Document', backref='usuario', lazy=True)
    sesiones_video = db.relationship('VideoSession', backref='usuario', lazy=True)
    
    def set_password(self, password):
        """Establece el hash de la contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convierte el usuario a diccionario"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nombre_completo': self.nombre_completo,
            'carrera': self.carrera,
            'ciclo_actual': self.ciclo_actual,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'activo': self.activo
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
'''

DOCUMENT_MODEL = '''"""
Modelo de Documento
"""

from app import db
from datetime import datetime

class Document(db.Model):
    """Modelo de documentos académicos subidos por el usuario"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50))  # informe, trabajo_final, proyecto, tesis
    archivo_path = db.Column(db.String(500), nullable=False)
    archivo_nombre = db.Column(db.String(200), nullable=False)
    ciclo = db.Column(db.Integer)
    curso = db.Column(db.String(100))
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_documento = db.Column(db.Date)
    analizado = db.Column(db.Boolean, default=False)
    
    # Relaciones
    analisis_texto = db.relationship('TextAnalysis', backref='documento', lazy=True, uselist=False)
    
    def to_dict(self):
        """Convierte el documento a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'archivo_nombre': self.archivo_nombre,
            'ciclo': self.ciclo,
            'curso': self.curso,
            'fecha_subida': self.fecha_subida.isoformat() if self.fecha_subida else None,
            'analizado': self.analizado
        }
    
    def __repr__(self):
        return f'<Document {self.titulo}>'
'''

TEXT_ANALYSIS_MODEL = '''"""
Modelo de Análisis de Texto
"""

from app import db
from datetime import datetime

class TextAnalysis(db.Model):
    """Modelo para almacenar análisis de texto de documentos"""
    __tablename__ = 'text_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    
    # Métricas de análisis
    palabra_count = db.Column(db.Integer)
    palabras_unicas = db.Column(db.Integer)
    riqueza_vocabulario = db.Column(db.Float)  # palabras_unicas / palabra_count
    longitud_promedio_oracion = db.Column(db.Float)
    complejidad_sintactica = db.Column(db.Float)
    uso_terminologia_tecnica = db.Column(db.Integer)
    
    # Análisis de IA
    coherencia_score = db.Column(db.Float)
    cohesion_score = db.Column(db.Float)
    calidad_redaccion = db.Column(db.Float)
    areas_mejora = db.Column(db.Text)  # JSON con áreas de mejora
    
    fecha_analisis = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convierte el análisis a diccionario"""
        return {
            'id': self.id,
            'document_id': self.document_id,
            'palabra_count': self.palabra_count,
            'palabras_unicas': self.palabras_unicas,
            'riqueza_vocabulario': self.riqueza_vocabulario,
            'longitud_promedio_oracion': self.longitud_promedio_oracion,
            'complejidad_sintactica': self.complejidad_sintactica,
            'coherencia_score': self.coherencia_score,
            'cohesion_score': self.cohesion_score,
            'calidad_redaccion': self.calidad_redaccion,
            'fecha_analisis': self.fecha_analisis.isoformat() if self.fecha_analisis else None
        }
    
    def __repr__(self):
        return f'<TextAnalysis {self.id}>'
'''

VIDEO_SESSION_MODEL = '''"""
Modelo de Sesión de Video
"""

from app import db
from datetime import datetime

class VideoSession(db.Model):
    """Modelo para sesiones de análisis de video/audio"""
    __tablename__ = 'video_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    duracion_segundos = db.Column(db.Integer)
    video_path = db.Column(db.String(500))
    audio_path = db.Column(db.String(500))
    
    fecha_sesion = db.Column(db.DateTime, default=datetime.utcnow)
    analizado = db.Column(db.Boolean, default=False)
    
    # Relaciones
    metricas_atencion = db.relationship('AttentionMetrics', backref='sesion', lazy=True)
    transcripciones = db.relationship('AudioTranscription', backref='sesion', lazy=True)
    
    def to_dict(self):
        """Convierte la sesión a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'duracion_segundos': self.duracion_segundos,
            'fecha_sesion': self.fecha_sesion.isoformat() if self.fecha_sesion else None,
            'analizado': self.analizado
        }
    
    def __repr__(self):
        return f'<VideoSession {self.titulo}>'
'''

ATTENTION_METRICS_MODEL = '''"""
Modelo de Métricas de Atención
"""

from app import db
from datetime import datetime

class AttentionMetrics(db.Model):
    """Modelo para métricas de atención durante sesiones de video"""
    __tablename__ = 'attention_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('video_sessions.id'), nullable=False)
    
    timestamp_segundos = db.Column(db.Integer, nullable=False)  # Momento en el video
    emocion_detectada = db.Column(db.String(50))  # happy, sad, neutral, etc.
    nivel_atencion = db.Column(db.Float)  # 0-100
    postura = db.Column(db.String(50))  # atento, distraido, etc.
    
    # Datos raw de la IA
    emociones_raw = db.Column(db.Text)  # JSON con todas las emociones detectadas
    confianza = db.Column(db.Float)  # Nivel de confianza de la detección
    
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convierte las métricas a diccionario"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'timestamp_segundos': self.timestamp_segundos,
            'emocion_detectada': self.emocion_detectada,
            'nivel_atencion': self.nivel_atencion,
            'postura': self.postura,
            'confianza': self.confianza
        }
    
    def __repr__(self):
        return f'<AttentionMetrics {self.id}>'
'''

AUDIO_TRANSCRIPTION_MODEL = '''"""
Modelo de Transcripción de Audio
"""

from app import db
from datetime import datetime

class AudioTranscription(db.Model):
    """Modelo para transcripciones de audio"""
    __tablename__ = 'audio_transcriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('video_sessions.id'), nullable=False)
    
    transcripcion_completa = db.Column(db.Text, nullable=False)
    idioma_detectado = db.Column(db.String(10))
    confianza_transcripcion = db.Column(db.Float)
    
    # Análisis de sentimiento
    sentimiento_general = db.Column(db.String(50))  # positivo, negativo, neutral
    sentimiento_score = db.Column(db.Float)
    palabras_clave = db.Column(db.Text)  # JSON con palabras clave extraídas
    
    fecha_transcripcion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convierte la transcripción a diccionario"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'transcripcion_completa': self.transcripcion_completa,
            'idioma_detectado': self.idioma_detectado,
            'confianza_transcripcion': self.confianza_transcripcion,
            'sentimiento_general': self.sentimiento_general,
            'sentimiento_score': self.sentimiento_score
        }
    
    def __repr__(self):
        return f'<AudioTranscription {self.id}>'
'''

STUDENT_PROFILE_MODEL = '''"""
Modelo de Perfil del Estudiante
"""

from app import db
from datetime import datetime

class StudentProfile(db.Model):
    """Modelo para perfil integral del estudiante"""
    __tablename__ = 'student_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Fortalezas y debilidades (JSON)
    fortalezas = db.Column(db.Text)  # JSON con fortalezas identificadas
    debilidades = db.Column(db.Text)  # JSON con debilidades identificadas
    
    # Estilo de aprendizaje
    estilo_aprendizaje = db.Column(db.String(50))  # visual, auditivo, kinestesico
    preferencia_contenido = db.Column(db.String(50))  # conciso, detallado, intermedio
    
    # Métricas generales
    promedio_atencion = db.Column(db.Float)
    promedio_calidad_redaccion = db.Column(db.Float)
    documentos_analizados = db.Column(db.Integer, default=0)
    sesiones_completadas = db.Column(db.Integer, default=0)
    
    # Recomendaciones
    recomendaciones = db.Column(db.Text)  # JSON con recomendaciones personalizadas
    
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convierte el perfil a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'estilo_aprendizaje': self.estilo_aprendizaje,
            'preferencia_contenido': self.preferencia_contenido,
            'promedio_atencion': self.promedio_atencion,
            'promedio_calidad_redaccion': self.promedio_calidad_redaccion,
            'documentos_analizados': self.documentos_analizados,
            'sesiones_completadas': self.sesiones_completadas,
            'ultima_actualizacion': self.ultima_actualizacion.isoformat() if self.ultima_actualizacion else None
        }
    
    def __repr__(self):
        return f'<StudentProfile user_id={self.user_id}>'
'''

REPORT_MODEL = '''"""
Modelo de Reporte
"""

from app import db
from datetime import datetime

class Report(db.Model):
    """Modelo para reportes generados"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50))  # semestral, por_curso, por_sesion
    formato = db.Column(db.String(20))  # pdf, pptx, docx
    archivo_path = db.Column(db.String(500))
    
    # Periodo del reporte
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    
    contenido_json = db.Column(db.Text)  # Datos del reporte en JSON
    
    fecha_generacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convierte el reporte a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'formato': self.formato,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'fecha_generacion': self.fecha_generacion.isoformat() if self.fecha_generacion else None
        }
    
    def __repr__(self):
        return f'<Report {self.titulo}>'
'''

MODELS_INIT = '''"""
Inicialización de modelos
"""

from app.models.user import User
from app.models.document import Document
from app.models.text_analysis import TextAnalysis
from app.models.video_session import VideoSession
from app.models.attention_metrics import AttentionMetrics
from app.models.audio_transcription import AudioTranscription
from app.models.student_profile import StudentProfile
from app.models.report import Report

__all__ = [
    'User',
    'Document',
    'TextAnalysis',
    'VideoSession',
    'AttentionMetrics',
    'AudioTranscription',
    'StudentProfile',
    'Report'
]
'''

def create_models():
    """Crea todos los archivos de modelos"""
    print("="*80)
    print("CREANDO MODELOS DEL BACKEND")
    print("="*80)
    print()
    
    models_dir = Path("backend/app/models")
    if not models_dir.exists():
        print("❌ Error: No existe backend/app/models")
        print("   Ejecuta primero: python setup_backend_structure.py")
        return False
    
    models = {
        'user.py': USER_MODEL,
        'document.py': DOCUMENT_MODEL,
        'text_analysis.py': TEXT_ANALYSIS_MODEL,
        'video_session.py': VIDEO_SESSION_MODEL,
        'attention_metrics.py': ATTENTION_METRICS_MODEL,
        'audio_transcription.py': AUDIO_TRANSCRIPTION_MODEL,
        'student_profile.py': STUDENT_PROFILE_MODEL,
        'report.py': REPORT_MODEL,
        '__init__.py': MODELS_INIT
    }
    
    for filename, content in models.items():
        filepath = models_dir / filename
        
        # Backup si existe
        if filepath.exists():
            backup_path = models_dir / f"{filename}.backup"
            print(f"📋 Backup: {filename} → {filename}.backup")
            with open(filepath, 'r', encoding='utf-8') as f:
                with open(backup_path, 'w', encoding='utf-8') as bf:
                    bf.write(f.read())
        
        # Crear archivo
        print(f"✏️ Creando: {filename}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print()
    print("✅ Todos los modelos creados exitosamente")
    print()
    print("Modelos creados:")
    print("  ✓ User - Usuario del sistema")
    print("  ✓ Document - Documentos académicos")
    print("  ✓ TextAnalysis - Análisis de texto")
    print("  ✓ VideoSession - Sesiones de video")
    print("  ✓ AttentionMetrics - Métricas de atención")
    print("  ✓ AudioTranscription - Transcripciones de audio")
    print("  ✓ StudentProfile - Perfil del estudiante")
    print("  ✓ Report - Reportes generados")
    print()
    
    return True

if __name__ == "__main__":
    success = create_models()
    if success:
        print("🎉 ¡Modelos listos!")
        print()
        print("Próximo paso: Corregir run.py")
        print("  python fix_run_py.py")
    else:
        print("❌ No se pudieron crear los modelos")
