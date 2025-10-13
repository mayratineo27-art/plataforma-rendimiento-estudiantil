# ============================================
# app/services/audio_processing/__init__.py
# ============================================
"""
Servicios de procesamiento de audio
"""
from app.services.audio_processing.transcription import transcription_service

__all__ = ['transcription_service']