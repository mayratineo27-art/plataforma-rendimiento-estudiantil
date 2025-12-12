"""
app/services/ai/attention_analyzer.py
Servicio de Análisis de Atención Estudiantil

Evalúa el nivel de atención del estudiante basado en:
- Análisis facial de emociones
- Dirección de la mirada
- Nivel de engagement
- Indicadores de confusión o comprensión
"""

import logging
from typing import List, Dict, Any
from decimal import Decimal

logger = logging.getLogger(__name__)


class AttentionAnalyzer:
    """Analiza la atención del estudiante durante una sesión"""
    
    # Pesos para cálculo de atención
    EMOTION_WEIGHTS = {
        # Emociones positivas para aprendizaje
        'concentrado': 100,
        'interesado': 95,
        'pensativo': 90,
        'curioso': 90,
        'happy': 70,
        'neutral': 60,
        
        # Emociones negativas para aprendizaje
        'confundido': 40,
        'aburrido': 30,
        'distraido': 25,
        'frustrado': 35,
        'sad': 35,
        'angry': 20,
        'fear': 30,
        'disgust': 25,
        'surprise': 65
    }
    
    # Niveles de engagement
    ENGAGEMENT_LEVELS = [
        (0, 20, 'muy_bajo'),
        (20, 40, 'bajo'),
        (40, 60, 'medio'),
        (60, 80, 'alto'),
        (80, 100, 'muy_alto')
    ]
    
    def __init__(self):
        """Inicializar el analizador de atención"""
        logger.info("✅ AttentionAnalyzer inicializado")
    
    def calculate_attention_score(self, emotions_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcula el score de atención basado en emociones detectadas
        
        Args:
            emotions_data: Lista de diccionarios con datos de emoción
                Cada elemento debe tener: {
                    'face_detected': bool,
                    'dominant_emotion': str,
                    'emotion_scores': dict,
                    'contextual_emotion': str
                }
        
        Returns:
            dict: {
                'attention_score': float (0-100),
                'engagement_level': str,
                'predominant_emotions': dict,
                'face_presence_rate': float,
                'confusion_indicators': dict,
                'comprehension_indicators': dict
            }
        """
        if not emotions_data:
            return self._empty_result()
        
        total_frames = len(emotions_data)
        frames_with_face = sum(1 for e in emotions_data if e.get('face_detected', False))
        face_presence_rate = (frames_with_face / total_frames) * 100
        
        # Si no hay rostros detectados, atención muy baja
        if frames_with_face == 0:
            return {
                'attention_score': 15.0,
                'engagement_level': 'muy_bajo',
                'predominant_emotions': {},
                'face_presence_rate': 0.0,
                'confusion_indicators': {'no_face_detected': True},
                'comprehension_indicators': {}
            }
        
        # Calcular scores de atención por frame
        frame_scores = []
        emotion_counts = {}
        contextual_counts = {}
        
        for emotion_data in emotions_data:
            if not emotion_data.get('face_detected'):
                # Sin rostro = muy baja atención (penalización)
                frame_scores.append(15.0)
                continue
            
            # Usar emoción contextual si está disponible
            contextual = emotion_data.get('contextual_emotion')
            if contextual:
                contextual_counts[contextual] = contextual_counts.get(contextual, 0) + 1
                score = self.EMOTION_WEIGHTS.get(contextual, 50)
                frame_scores.append(score)
            else:
                # Usar emoción dominante
                dominant = emotion_data.get('dominant_emotion', 'neutral')
                emotion_counts[dominant] = emotion_counts.get(dominant, 0) + 1
                score = self.EMOTION_WEIGHTS.get(dominant, 50)
                frame_scores.append(score)
        
        # Calcular score promedio de atención
        avg_score = sum(frame_scores) / len(frame_scores)
        
        # Ajustar por presencia de rostro
        # Si el rostro está ausente mucho tiempo, penalizar
        face_penalty = max(0, (70 - face_presence_rate) * 0.3)
        final_score = max(0, min(100, avg_score - face_penalty))
        
        # Determinar nivel de engagement
        engagement_level = self._get_engagement_level(final_score)
        
        # Calcular emociones predominantes
        total_detected = frames_with_face
        predominant = {}
        
        if contextual_counts:
            for emotion, count in contextual_counts.items():
                percentage = (count / total_detected) * 100
                predominant[emotion] = round(percentage, 2)
        elif emotion_counts:
            for emotion, count in emotion_counts.items():
                percentage = (count / total_detected) * 100
                predominant[emotion] = round(percentage, 2)
        
        # Indicadores de confusión
        confusion = self._calculate_confusion_indicators(predominant, emotions_data)
        
        # Indicadores de comprensión
        comprehension = self._calculate_comprehension_indicators(predominant, emotions_data)
        
        return {
            'attention_score': round(final_score, 2),
            'engagement_level': engagement_level,
            'predominant_emotions': predominant,
            'face_presence_rate': round(face_presence_rate, 2),
            'confusion_indicators': confusion,
            'comprehension_indicators': comprehension
        }
    
    def _get_engagement_level(self, score: float) -> str:
        """Determina el nivel de engagement basado en el score"""
        for min_score, max_score, level in self.ENGAGEMENT_LEVELS:
            if min_score <= score < max_score:
                return level
        return 'muy_alto'
    
    def _calculate_confusion_indicators(self, predominant: Dict[str, float], 
                                       emotions_data: List[Dict]) -> Dict[str, Any]:
        """Calcula indicadores de confusión"""
        confusion_emotions = {'confundido', 'frustrado', 'angry', 'disgust'}
        
        confusion_percentage = sum(
            predominant.get(emotion, 0) 
            for emotion in confusion_emotions
        )
        
        # Detectar picos de confusión
        confusion_peaks = 0
        for i in range(len(emotions_data) - 1):
            curr_emotion = emotions_data[i].get('contextual_emotion') or emotions_data[i].get('dominant_emotion')
            next_emotion = emotions_data[i+1].get('contextual_emotion') or emotions_data[i+1].get('dominant_emotion')
            
            # Si cambia a emoción de confusión
            if curr_emotion not in confusion_emotions and next_emotion in confusion_emotions:
                confusion_peaks += 1
        
        return {
            'confusion_percentage': round(confusion_percentage, 2),
            'confusion_peaks': confusion_peaks,
            'high_confusion': confusion_percentage > 25
        }
    
    def _calculate_comprehension_indicators(self, predominant: Dict[str, float],
                                           emotions_data: List[Dict]) -> Dict[str, Any]:
        """Calcula indicadores de comprensión"""
        comprehension_emotions = {'concentrado', 'interesado', 'pensativo', 'curioso'}
        
        comprehension_percentage = sum(
            predominant.get(emotion, 0) 
            for emotion in comprehension_emotions
        )
        
        # Detectar momentos de claridad (transición de confusión a comprensión)
        clarity_moments = 0
        for i in range(len(emotions_data) - 1):
            curr_emotion = emotions_data[i].get('contextual_emotion') or emotions_data[i].get('dominant_emotion')
            next_emotion = emotions_data[i+1].get('contextual_emotion') or emotions_data[i+1].get('dominant_emotion')
            
            if curr_emotion in {'confundido', 'frustrado'} and next_emotion in comprehension_emotions:
                clarity_moments += 1
        
        return {
            'comprehension_percentage': round(comprehension_percentage, 2),
            'clarity_moments': clarity_moments,
            'high_comprehension': comprehension_percentage > 60
        }
    
    def _empty_result(self) -> Dict[str, Any]:
        """Resultado vacío cuando no hay datos"""
        return {
            'attention_score': 0.0,
            'engagement_level': 'muy_bajo',
            'predominant_emotions': {},
            'face_presence_rate': 0.0,
            'confusion_indicators': {'no_data': True},
            'comprehension_indicators': {'no_data': True}
        }


# Instancia global
attention_analyzer = AttentionAnalyzer()
