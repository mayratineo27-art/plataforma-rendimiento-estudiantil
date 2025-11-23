"""
Script para crear datos de prueba del Módulo 2
Ejecutar: python create_test_data.py
"""

from app import create_app, db
from app.models.user import User
from app.models.video_session import VideoSession
from app.models.emotion_data import EmotionData
from app.models.attention_metrics import AttentionMetrics
from app.models.audio_session import AudioSession
from app.models.audio_transcription import AudioTranscription
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    print("=" * 60)
    print("CREANDO DATOS DE PRUEBA - MÓDULO 2")
    print("=" * 60)
    
    # 1. Verificar/Crear usuario
    user = User.query.filter_by(email='test@test.com').first()
    if not user:
        user = User(
            email='test@test.com',
            password_hash='pbkdf2:sha256:test',
            full_name='Estudiante de Prueba',
            career='Ingeniería de Sistemas',
            semester=8
        )
        db.session.add(user)
        db.session.commit()
        print(f"✅ Usuario creado: {user.full_name} (ID: {user.id})")
    else:
        print(f"✅ Usuario existente: {user.full_name} (ID: {user.id})")
    
    # 2. Crear sesiones de video
    print("\n📹 Creando sesiones de video...")
    
    session1 = VideoSession(
        user_id=user.id,
        session_name='Sesión de estudio - Matemáticas',
        start_time=datetime.utcnow() - timedelta(days=5),
        end_time=datetime.utcnow() - timedelta(days=5, hours=-1, minutes=-30),
        duration_seconds=5400,  # 90 minutos
        total_frames_analyzed=2700
    )
    db.session.add(session1)
    db.session.commit()
    print(f"  ✅ Sesión 1 creada (ID: {session1.id})")
    
    # Agregar emociones a la sesión 1
    emotions1 = [
        ('focused', 0.8, 0),
        ('interested', 0.7, 1800),
        ('focused', 0.75, 3600),
        ('tired', 0.6, 4500)
    ]
    
    for emotion, score, timestamp in emotions1:
        em = EmotionData(
            video_session_id=session1.id,
            timestamp_seconds=timestamp,
            dominant_emotion='neutral'
        )
        em.set_contextual_emotion(emotion, score)
        db.session.add(em)
    
    db.session.commit()
    print(f"  ✅ {len(emotions1)} emociones agregadas")
    
    # Calcular métricas de atención
    attention1 = AttentionMetrics(
        video_session_id=session1.id,
        start_time=session1.start_time,
        end_time=session1.end_time,
        interval_seconds=1800
    )
    attention1.calculate_attention_score([80, 75, 70, 65])
    db.session.add(attention1)
    db.session.commit()
    print(f"  ✅ Métricas de atención calculadas (Score: {attention1.attention_score})")
    
    # Segunda sesión de video
    session2 = VideoSession(
        user_id=user.id,
        session_name='Sesión de estudio - Física',
        start_time=datetime.utcnow() - timedelta(days=2),
        end_time=datetime.utcnow() - timedelta(days=2, hours=-2),
        duration_seconds=7200,  # 120 minutos
        total_frames_analyzed=3600
    )
    db.session.add(session2)
    db.session.commit()
    print(f"  ✅ Sesión 2 creada (ID: {session2.id})")
    
    emotions2 = [
        ('engaged', 0.85, 0),
        ('focused', 0.8, 1800),
        ('interested', 0.75, 3600),
        ('motivated', 0.7, 5400)
    ]
    
    for emotion, score, timestamp in emotions2:
        em = EmotionData(
            video_session_id=session2.id,
            timestamp_seconds=timestamp,
            dominant_emotion='happy'
        )
        em.set_contextual_emotion(emotion, score)
        db.session.add(em)
    
    db.session.commit()
    print(f"  ✅ {len(emotions2)} emociones agregadas")
    
    attention2 = AttentionMetrics(
        video_session_id=session2.id,
        start_time=session2.start_time,
        end_time=session2.end_time,
        interval_seconds=1800
    )
    attention2.calculate_attention_score([85, 80, 75, 70])
    db.session.add(attention2)
    db.session.commit()
    print(f"  ✅ Métricas de atención calculadas (Score: {attention2.attention_score})")
    
    # 3. Crear sesiones de audio
    print("\n🎤 Creando sesiones de audio...")
    
    audio1 = AudioSession(
        user_id=user.id,
        session_name='Grabación clase - Algoritmos',
        start_time=datetime.utcnow() - timedelta(days=3),
        end_time=datetime.utcnow() - timedelta(days=3, hours=-1),
        duration_seconds=3600
    )
    db.session.add(audio1)
    db.session.commit()
    print(f"  ✅ Sesión de audio creada (ID: {audio1.id})")
    
    # Agregar transcripciones
    transcriptions = [
        ("En esta clase veremos los algoritmos de ordenamiento más importantes.", 0, 5, 0.8),
        ("El algoritmo de burbuja es el más simple pero no el más eficiente.", 5, 10, 0.7),
        ("Quicksort es mucho más rápido para grandes conjuntos de datos.", 10, 15, 0.9),
    ]
    
    full_text = ""
    for text, start, end, conf in transcriptions:
        trans = AudioTranscription(
            audio_session_id=audio1.id,
            segment_text=text,
            start_time=start,
            end_time=end,
            confidence_score=conf,
            sentiment='neutral'
        )
        db.session.add(trans)
        full_text += text + " "
    
    audio1.full_transcription = full_text.strip()
    audio1.transcription_completed = True
    audio1.average_confidence = sum(c[3] for c in transcriptions) / len(transcriptions)
    
    db.session.commit()
    print(f"  ✅ {len(transcriptions)} segmentos transcritos")
    
    print("\n" + "=" * 60)
    print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
    print("=" * 60)
    print(f"\nUsuario ID: {user.id}")
    print(f"Sesiones de video: 2")
    print(f"Sesiones de audio: 1")
    print(f"Total emociones: {len(emotions1) + len(emotions2)}")
    print(f"Total métricas: 2")
    print(f"Total transcripciones: {len(transcriptions)}")
    print("\n🎯 Ahora puedes probar:")
    print(f"GET http://localhost:5000/api/profile/{user.id}")
    print("=" * 60)
