### Análisis de video/imagen

# backend/app/services/ai/vision_service.py
from deepface import DeepFace
import cv2
import numpy as np

class VisionService:
    def __init__(self):
        # Configuración de DeepFace
        self.actions = ['emotion']
        self.enforce_detection = False  # Permite procesar aunque no detecte rostro perfectamente

    def detect_emotions(self, img_array):
        """
        Detecta emociones en una imagen usando DeepFace
        
        Args:
            img_array: numpy array de la imagen (RGB)
            
        Returns:
            lista de diccionarios con emociones detectadas
        """
        try:
            # Analizar imagen con DeepFace
            result = DeepFace.analyze(
                img_path=img_array,
                actions=self.actions,
                enforce_detection=self.enforce_detection,
                detector_backend='opencv'  # Más rápido
            )

            # Si result es una lista, procesarla
            if isinstance(result, list):
                emotions_list = []
                for face in result:
                    emotions_list.append({
                        'dominant_emotion': face.get('dominant_emotion'),
                        'emotions': face.get('emotion', {}),
                        'confidence': self._get_confidence(face.get('emotion', {})),
                        'region': face.get('region', {})
                    })
                return emotions_list
            
            # Si result es un dict (una cara)
            else:
                return [{
                    'dominant_emotion': result.get('dominant_emotion'),
                    'emotions': result.get('emotion', {}),
                    'confidence': self._get_confidence(result.get('emotion', {})),
                    'region': result.get('region', {})
                }]

        except Exception as e:
            print(f"Error detectando emociones: {str(e)}")
            return []

    def _get_confidence(self, emotions_dict):
        """Calcula la confianza promedio de las emociones"""
        if not emotions_dict:
            return 0
        
        values = list(emotions_dict.values())
        return sum(values) / len(values) if values else 0