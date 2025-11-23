"""
test_services.py - Pruebas de servicios de procesamiento
Ejecutar: python test_services.py
"""

import sys
import os
import cv2
import numpy as np

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.services.video_processing.emotion_recognition import emotion_service
from app.services.audio_processing.transcription import transcription_service


def test_emotion_recognition():
    """Test 1: Reconocimiento de emociones en imagen"""
    print("\n" + "="*60)
    print("TEST 1: Reconocimiento de Emociones (DeepFace)")
    print("="*60)
    
    try:
        # Crear una imagen de prueba con rostro (usando webcam si está disponible)
        print("📹 Intentando capturar imagen de webcam...")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ No se pudo abrir la webcam")
            print("💡 TIP: Conecta una webcam o usa una imagen de prueba")
            return
        
        # Capturar frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            print("❌ No se pudo capturar frame")
            return
        
        print("✅ Frame capturado")
        
        # Analizar frame
        print("🔍 Analizando emociones...")
        result = emotion_service.analyze_frame(frame, enforce_detection=False)
        
        if result['face_detected']:
            print("✅ ÉXITO - Rostro detectado!")
            print(f"   Rostros: {result['face_count']}")
            print(f"   Emoción dominante: {result['dominant_emotion']}")
            print(f"   Edad estimada: {result.get('age', 'N/A')}")
            print(f"   Género: {result.get('gender', 'N/A')}")
            print(f"\n   📊 Emociones detectadas:")
            
            emotions = result.get('emotions', {})
            for emotion, score in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
                print(f"      {emotion:12s}: {score:5.2f}%")
        else:
            print("⚠️  No se detectó rostro en la imagen")
            print(f"   Error: {result.get('error', 'Desconocido')}")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


def test_emotion_with_image_file():
    """Test 2: Análisis de imagen desde archivo"""
    print("\n" + "="*60)
    print("TEST 2: Análisis de Imagen desde Archivo")
    print("="*60)
    
    # Crear imagen de prueba si no existe
    test_image_path = "test_face.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"⚠️  Archivo {test_image_path} no existe")
        print("💡 Coloca una imagen con un rostro como 'test_face.jpg'")
        print("   o usa la webcam en el Test 1")
        return
    
    try:
        result = emotion_service.analyze_image_file(test_image_path)
        
        if result['face_detected']:
            print("✅ ÉXITO")
            print(f"   Emoción: {result['dominant_emotion']}")
            print(f"   Confianza: {result.get('face_confidence', 0):.2f}%")
        else:
            print("❌ No se detectó rostro")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


def test_transcription():
    """Test 3: Transcripción de audio"""
    print("\n" + "="*60)
    print("TEST 3: Transcripción de Audio")
    print("="*60)
    
    # Buscar archivo de audio de prueba
    test_audio_path = "test_audio.wav"
    
    if not os.path.exists(test_audio_path):
        print(f"⚠️  Archivo {test_audio_path} no existe")
        print("💡 Para probar la transcripción:")
        print("   1. Graba un audio corto (5-10 segundos)")
        print("   2. Guárdalo como 'test_audio.wav' en la carpeta backend")
        print("   3. Ejecuta este test nuevamente")
        return
    
    try:
        print("🎵 Obteniendo información del audio...")
        info = transcription_service.get_audio_info(test_audio_path)
        
        if 'error' in info:
            print(f"❌ Error al leer audio: {info['error']}")
            return
        
        print(f"   Duración: {info['duration_formatted']}")
        print(f"   Tamaño: {info['file_size_mb']} MB")
        
        print("\n🎤 Transcribiendo audio...")
        result = transcription_service.transcribe_audio_file(test_audio_path)
        
        if result['success']:
            print("✅ TRANSCRIPCIÓN EXITOSA")
            print(f"\n   📝 Texto transcrito:")
            print(f"   '{result['text']}'")
            print(f"\n   📊 Métricas:")
            print(f"      Palabras: {result['word_count']}")
            print(f"      Confianza: {result['confidence']:.2%}")
            print(f"      Duración: {result['duration_seconds']:.2f}s")
        else:
            print("❌ ERROR EN TRANSCRIPCIÓN")
            print(f"   {result['error']}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


def test_transcription_with_segments():
    """Test 4: Transcripción con segmentación"""
    print("\n" + "="*60)
    print("TEST 4: Transcripción con Segmentos")
    print("="*60)
    
    test_audio_path = "test_audio.wav"
    
    if not os.path.exists(test_audio_path):
        print("⚠️  Archivo de audio no encontrado (usa test_audio.wav)")
        return
    
    try:
        print("🎵 Transcribiendo con segmentación automática...")
        result = transcription_service.transcribe_with_segments(test_audio_path)
        
        if result['success']:
            print("✅ TRANSCRIPCIÓN EXITOSA")
            print(f"\n   📊 Resumen:")
            print(f"      Segmentos procesados: {result['total_segments']}/{result['total_chunks']}")
            print(f"      Precisión: {result['accuracy_percentage']:.1f}%")
            print(f"      Cumple objetivo (>70%): {'✅ Sí' if result['meets_target'] else '❌ No'}")
            
            print(f"\n   📝 Texto completo:")
            print(f"   '{result['full_text'][:200]}...'")
            
            print(f"\n   🎬 Segmentos ({len(result['segments'])}):")
            for seg in result['segments'][:3]:  # Mostrar primeros 3
                print(f"      [{seg['start_time']:.1f}s - {seg['end_time']:.1f}s]: {seg['text'][:50]}...")
        else:
            print(f"❌ ERROR: {result['error']}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*60)
    print("🚀 INICIANDO TESTS DE SERVICIOS DE PROCESAMIENTO")
    print("="*60)
    
    # Crear contexto de aplicación
    app = create_app()
    
    with app.app_context():
        try:
            # Test de emociones
            print("\n⏳ Preparando tests de emociones (DeepFace)...")
            print("   Esto puede tomar unos segundos la primera vez...")
            test_emotion_recognition()
            test_emotion_with_image_file()
            
            # Test de transcripción
            print("\n⏳ Preparando tests de transcripción...")
            test_transcription()
            test_transcription_with_segments()
            
            print("\n" + "="*60)
            print("✅ TESTS COMPLETADOS")
            print("="*60)
            print("\n💡 NOTAS:")
            print("   - Para probar emociones: usa webcam o imagen 'test_face.jpg'")
            print("   - Para probar audio: crea 'test_audio.wav'")
            print("   - DeepFace descarga modelos la primera vez (puede tardar)")
            
        except Exception as e:
            print("\n" + "="*60)
            print("❌ ERROR GENERAL")
            print("="*60)
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    main()