# ============================================
# app/services/video_processing/__init__.py
# ============================================
"""
Servicios de procesamiento de video
"""

# Importación lazy para evitar problemas con dependencias pesadas
try:
    from app.services.video_processing.emotion_recognition import emotion_service
    __all__ = ['emotion_service']
except Exception as e:
    print(f"⚠️  No se pudo cargar emotion_service: {e}")
    __all__ = []

