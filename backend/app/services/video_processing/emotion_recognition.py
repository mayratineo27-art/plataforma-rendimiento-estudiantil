"""
app/services/video_processing/emotion_recognition.py
Servicio de Reconocimiento de Emociones con DeepFace (LAZY LOADING)
Plataforma Integral de Rendimiento Estudiantil - Módulo 2
"""

import cv2
import numpy as np
# ⚠️ NO IMPORTAR DeepFace aquí - causa deadlock en Windows
# from deepface import DeepFace
from typing import Dict, List, Optional, Tuple
import os


class EmotionRecognitionService:
    """
    Servicio para análisis de emociones faciales usando DeepFace
    
    Detecta rostros en frames de video y analiza 7 emociones básicas,
    luego las mapea a 16 emociones contextuales.
    
    NOTA: DeepFace se carga LAZY (solo cuando se usa) para evitar deadlock
    """
    
    def __init__(self):
        """Inicializar servicio de reconocimiento de emociones"""
        # Configuración de DeepFace
        self.detector_backend = os.getenv('DEEPFACE_DETECTOR', 'mtcnn')
        self.model_name = os.getenv('DEEPFACE_MODEL', 'Facenet512')
        
        # Modelos disponibles
        self.available_detectors = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface']
        self.available_models = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 
                                'DeepFace', 'DeepID', 'ArcFace', 'Dlib']
        
        # Flag para indicar si DeepFace está cargado
        self._deepface_loaded = False
        self._DeepFace = None
        
        print(f"✅ EmotionRecognitionService inicializado (lazy mode)")
        print(f"   Detector: {self.detector_backend}")
        print(f"   Modelo: {self.model_name}")
        print(f"   ⏳ DeepFace se cargará en el primer uso")
    
    def _load_deepface(self):
        """Cargar DeepFace solo cuando se necesite (lazy loading)"""
        if not self._deepface_loaded:
            try:
                print("   ⏳ Cargando DeepFace (puede tardar 20-30 segundos)...")
                from deepface import DeepFace
                self._DeepFace = DeepFace
                self._deepface_loaded = True
                print("   ✅ DeepFace cargado exitosamente")
            except Exception as e:
                print(f"   ❌ Error cargando DeepFace: {str(e)}")
                raise
        return self._DeepFace
    
    def analyze_frame(
        self,
        frame: np.ndarray,
        enforce_detection: bool = False
    ) -> Dict:
        """
        Analizar un frame de video para detectar emociones
        
        Args:
            frame (np.ndarray): Frame de video (imagen BGR de OpenCV)
            enforce_detection (bool): Si True, lanza error si no detecta rostro
        
        Returns:
            dict: Resultados del análisis
                {
                    'face_detected': bool,
                    'face_count': int,
                    'emotions': dict,
                    'dominant_emotion': str,
                    'age': int,
                    'gender': str,
                    'face_bbox': dict,
                    'error': str (si hubo error)
                }
        """
        try:
            # Cargar DeepFace si aún no está cargado (lazy loading)
            DeepFace = self._load_deepface()
            
            # Analizar con DeepFace
            results = DeepFace.analyze(
                img_path=frame,
                actions=['emotion', 'age', 'gender'],
                detector_backend=self.detector_backend,
                enforce_detection=enforce_detection,
                silent=True
            )
            
            # DeepFace puede retornar lista (múltiples rostros) o dict (un rostro)
            if isinstance(results, list):
                if len(results) == 0:
                    return {
                        'face_detected': False,
                        'face_count': 0,
                        'emotions': {},
                        'error': None
                    }
                # Tomar el primer rostro (rostro principal)
                result = results[0]
                face_count = len(results)
            else:
                result = results
                face_count = 1
            
            # Extraer emociones
            emotions = result.get('emotion', {})
            
            # Extraer región facial
            region = result.get('region', {})
            face_bbox = {
                'x': region.get('x', 0),
                'y': region.get('y', 0),
                'w': region.get('w', 0),
                'h': region.get('h', 0)
            }
            
            # Determinar emoción dominante
            dominant_emotion = result.get('dominant_emotion', 'neutral')
            
            return {
                'face_detected': True,
                'face_count': face_count,
                'emotions': emotions,
                'dominant_emotion': dominant_emotion,
                'age': result.get('age', 0),
                'gender': result.get('dominant_gender', 'Unknown'),
                'face_bbox': face_bbox,
                'face_confidence': max(emotions.values()) if emotions else 0,
                'error': None
            }
            
        except ValueError as e:
            # No se detectó rostro
            return {
                'face_detected': False,
                'face_count': 0,
                'emotions': {},
                'error': 'No face detected'
            }
        except Exception as e:
            return {
                'face_detected': False,
                'face_count': 0,
                'emotions': {},
                'error': str(e)
            }
    
    def analyze_video_stream(
        self,
        video_source: str,
        frame_skip: int = 15,
        max_frames: Optional[int] = None,
        callback=None
    ) -> List[Dict]:
        """
        Analizar stream de video completo
        
        Args:
            video_source (str): Ruta al archivo de video o número de cámara (0, 1, etc.)
            frame_skip (int): Analizar cada N frames (para performance)
            max_frames (int): Máximo de frames a analizar
            callback (function): Función callback(frame_number, result) para progreso
        
        Returns:
            list: Lista de resultados de análisis por frame
        """
        results = []
        
        # Abrir video
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            raise ValueError(f"No se pudo abrir el video: {video_source}")
        
        # Obtener información del video
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📹 Procesando video:")
        print(f"   FPS: {fps}")
        print(f"   Total frames: {total_frames}")
        print(f"   Frame skip: {frame_skip}")
        
        frame_number = 0
        analyzed_count = 0
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Analizar solo cada N frames
            if frame_number % frame_skip == 0:
                timestamp_seconds = frame_number / fps
                
                # Analizar frame
                analysis = self.analyze_frame(frame, enforce_detection=False)
                analysis['frame_number'] = frame_number
                analysis['timestamp_seconds'] = round(timestamp_seconds, 3)
                
                results.append(analysis)
                analyzed_count += 1
                
                # Callback para progreso
                if callback:
                    callback(frame_number, analysis)
                
                # Imprimir progreso
                if analyzed_count % 10 == 0:
                    print(f"   Analizados: {analyzed_count} frames ({frame_number}/{total_frames})")
            
            frame_number += 1
            
            # Límite máximo de frames
            if max_frames and analyzed_count >= max_frames:
                break
        
        cap.release()
        
        print(f"✅ Análisis completado: {analyzed_count} frames analizados")
        
        return results
    
    def analyze_image_file(self, image_path: str) -> Dict:
        """
        Analizar archivo de imagen
        
        Args:
            image_path (str): Ruta a la imagen
        
        Returns:
            dict: Resultado del análisis
        """
        # Leer imagen
        img = cv2.imread(image_path)
        
        if img is None:
            return {
                'face_detected': False,
                'error': 'No se pudo leer la imagen'
            }
        
        return self.analyze_frame(img)
    
    def draw_emotions_on_frame(
        self,
        frame: np.ndarray,
        analysis: Dict
    ) -> np.ndarray:
        """
        Dibujar información de emociones sobre el frame
        
        Args:
            frame (np.ndarray): Frame original
            analysis (dict): Resultado del análisis
        
        Returns:
            np.ndarray: Frame con anotaciones
        """
        annotated_frame = frame.copy()
        
        if not analysis.get('face_detected'):
            # Sin rostro detectado
            cv2.putText(
                annotated_frame,
                "No face detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )
            return annotated_frame
        
        # Dibujar bounding box del rostro
        bbox = analysis.get('face_bbox', {})
        if bbox:
            x, y, w, h = bbox['x'], bbox['y'], bbox['w'], bbox['h']
            cv2.rectangle(
                annotated_frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )
        
        # Emoción dominante
        dominant = analysis.get('dominant_emotion', 'unknown')
        cv2.putText(
            annotated_frame,
            f"Emotion: {dominant}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        
        # Edad y género
        age = analysis.get('age', 0)
        gender = analysis.get('gender', 'Unknown')
        cv2.putText(
            annotated_frame,
            f"Age: {age} | Gender: {gender}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )
        
        # Top 3 emociones
        emotions = analysis.get('emotions', {})
        if emotions:
            sorted_emotions = sorted(
                emotions.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            y_offset = 90
            for emotion, score in sorted_emotions:
                text = f"{emotion}: {score:.1f}%"
                cv2.putText(
                    annotated_frame,
                    text,
                    (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )
                y_offset += 25
        
        return annotated_frame
    
    def get_statistics(self, results: List[Dict]) -> Dict:
        """
        Calcular estadísticas de los resultados de análisis
        
        Args:
            results (list): Lista de resultados de analyze_video_stream
        
        Returns:
            dict: Estadísticas generales
        """
        total_frames = len(results)
        faces_detected = sum(1 for r in results if r.get('face_detected'))
        
        # Contar emociones dominantes
        emotion_counts = {}
        for result in results:
            if result.get('face_detected'):
                emotion = result.get('dominant_emotion', 'unknown')
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Emoción más frecuente
        most_common_emotion = max(
            emotion_counts.items(),
            key=lambda x: x[1]
        )[0] if emotion_counts else 'none'
        
        return {
            'total_frames_analyzed': total_frames,
            'faces_detected_count': faces_detected,
            'detection_rate': round((faces_detected / total_frames * 100), 2) if total_frames > 0 else 0,
            'emotion_distribution': emotion_counts,
            'most_common_emotion': most_common_emotion
        }


# Instancia global del servicio
emotion_service = EmotionRecognitionService()