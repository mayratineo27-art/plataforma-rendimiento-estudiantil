"""
app/config/settings.py - Configuración de la aplicación
Plataforma Integral de Rendimiento Estudiantil
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Configuración base compartida por todos los entornos"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'rendimiento_estudiantil')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        "?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_MAX_OVERFLOW = 20
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000')
    
    # File Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    VIDEO_UPLOAD_FOLDER = os.getenv('VIDEO_UPLOAD_FOLDER', 'uploads/videos')
    AUDIO_UPLOAD_FOLDER = os.getenv('AUDIO_UPLOAD_FOLDER', 'uploads/audio')
    GENERATED_FOLDER = os.getenv('GENERATED_FOLDER', 'generated')
    REPORTS_FOLDER = os.getenv('REPORTS_FOLDER', 'generated/reports')
    TEMPLATES_FOLDER = os.getenv('TEMPLATES_FOLDER', 'generated/templates')
    
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 52428800))  # 50MB
    MAX_VIDEO_SIZE = int(os.getenv('MAX_VIDEO_SIZE', 104857600))  # 100MB
    MAX_AUDIO_SIZE = int(os.getenv('MAX_AUDIO_SIZE', 52428800))  # 50MB
    
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx,doc,txt').split(',')
    ALLOWED_VIDEO_EXTENSIONS = os.getenv('ALLOWED_VIDEO_EXTENSIONS', 'mp4,avi,mov,webm').split(',')
    ALLOWED_AUDIO_EXTENSIONS = os.getenv('ALLOWED_AUDIO_EXTENSIONS', 'mp3,wav,ogg,m4a,webm').split(',')
    
    # Google Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    GEMINI_VISION_MODEL = os.getenv('GEMINI_VISION_MODEL', 'gemini-pro-vision')
    GEMINI_MAX_TOKENS = int(os.getenv('GEMINI_MAX_TOKENS', 2048))
    GEMINI_TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', 0.7))
    
    # OpenAI API (opcional)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    # DeepFace Configuration
    DEEPFACE_MODEL = os.getenv('DEEPFACE_MODEL', 'Facenet512')
    DEEPFACE_DETECTOR = os.getenv('DEEPFACE_DETECTOR', 'mtcnn')
    DEEPFACE_DISTANCE_METRIC = os.getenv('DEEPFACE_DISTANCE_METRIC', 'cosine')
    
    # Emotion Analysis
    EMOTION_ANALYSIS_ENABLED = os.getenv('EMOTION_ANALYSIS_ENABLED', 'True').lower() == 'true'
    EMOTION_CONFIDENCE_THRESHOLD = float(os.getenv('EMOTION_CONFIDENCE_THRESHOLD', 0.6))
    EMOTIONS_TO_TRACK = os.getenv(
        'EMOTIONS_TO_TRACK',
        'angry,disgust,fear,happy,sad,surprise,neutral,confused,focused,bored,interested,tired'
    ).split(',')
    
    # Audio Transcription
    SPEECH_RECOGNITION_LANGUAGE = os.getenv('SPEECH_RECOGNITION_LANGUAGE', 'es-ES')
    TRANSCRIPTION_ACCURACY_THRESHOLD = float(os.getenv('TRANSCRIPTION_ACCURACY_THRESHOLD', 0.7))
    
    # NLP
    SPACY_MODEL = os.getenv('SPACY_MODEL', 'es_core_news_md')
    MIN_WORD_LENGTH = int(os.getenv('MIN_WORD_LENGTH', 3))
    VOCABULARY_ANALYSIS_ENABLED = os.getenv('VOCABULARY_ANALYSIS_ENABLED', 'True').lower() == 'true'
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000)))
    
    # Session
    SESSION_TYPE = os.getenv('SESSION_TYPE', 'filesystem')
    SESSION_PERMANENT = os.getenv('SESSION_PERMANENT', 'False').lower() == 'true'
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=int(os.getenv('PERMANENT_SESSION_LIFETIME', 3600)))
    
    # Security
    BCRYPT_LOG_ROUNDS = int(os.getenv('BCRYPT_LOG_ROUNDS', 12))
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
    LOCKOUT_DURATION = int(os.getenv('LOCKOUT_DURATION', 900))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # Analysis Configuration
    MIN_DOCUMENTS_FOR_ANALYSIS = int(os.getenv('MIN_DOCUMENTS_FOR_ANALYSIS', 3))
    ANALYSIS_COMPARISON_ENABLED = os.getenv('ANALYSIS_COMPARISON_ENABLED', 'True').lower() == 'true'
    PROGRESS_TRACKING_CYCLES = int(os.getenv('PROGRESS_TRACKING_CYCLES', 10))
    
    # Real-time Session
    SESSION_FRAME_RATE = int(os.getenv('SESSION_FRAME_RATE', 2))
    SESSION_MIN_DURATION = int(os.getenv('SESSION_MIN_DURATION', 60))
    SESSION_MAX_DURATION = int(os.getenv('SESSION_MAX_DURATION', 7200))
    
    # Report Generation
    REPORT_DEFAULT_FORMAT = os.getenv('REPORT_DEFAULT_FORMAT', 'pdf')
    REPORT_INCLUDE_CHARTS = os.getenv('REPORT_INCLUDE_CHARTS', 'True').lower() == 'true'
    REPORT_LANGUAGE = os.getenv('REPORT_LANGUAGE', 'es')
    PPT_DEFAULT_TEMPLATE = os.getenv('PPT_DEFAULT_TEMPLATE', 'templates/default.pptx')
    
    # Feature Flags
    FEATURE_VIDEO_ANALYSIS = os.getenv('FEATURE_VIDEO_ANALYSIS', 'True').lower() == 'true'
    FEATURE_AUDIO_ANALYSIS = os.getenv('FEATURE_AUDIO_ANALYSIS', 'True').lower() == 'true'
    FEATURE_DOCUMENT_ANALYSIS = os.getenv('FEATURE_DOCUMENT_ANALYSIS', 'True').lower() == 'true'
    FEATURE_REPORT_GENERATION = os.getenv('FEATURE_REPORT_GENERATION', 'True').lower() == 'true'
    FEATURE_REAL_TIME_PROCESSING = os.getenv('FEATURE_REAL_TIME_PROCESSING', 'True').lower() == 'true'


class DevelopmentConfig(BaseConfig):
    """Configuración para entorno de desarrollo"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True  # Mostrar queries SQL en consola


class TestingConfig(BaseConfig):
    """Configuración para entorno de testing"""
    DEBUG = False
    TESTING = True
    
    # Base de datos de prueba separada
    DB_NAME = 'rendimiento_estudiantil_test'
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASSWORD}@"
        f"{BaseConfig.DB_HOST}:{BaseConfig.DB_PORT}/{DB_NAME}"
        "?charset=utf8mb4"
    )
    
    # Desactivar algunas features en testing
    FEATURE_REAL_TIME_PROCESSING = False
    
    # Archivos de prueba en carpeta temporal
    UPLOAD_FOLDER = 'tests/temp/uploads'
    VIDEO_UPLOAD_FOLDER = 'tests/temp/videos'
    AUDIO_UPLOAD_FOLDER = 'tests/temp/audio'


class ProductionConfig(BaseConfig):
    """Configuración para entorno de producción"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    
    # En producción, asegurar que las variables críticas estén configuradas
    if not BaseConfig.SECRET_KEY or BaseConfig.SECRET_KEY == 'dev-secret-key-change-in-production':
        raise ValueError("SECRET_KEY debe estar configurada en producción")
    
    if not BaseConfig.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY debe estar configurada en producción")
    
    # Logging más estricto en producción
    LOG_LEVEL = 'WARNING'


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}