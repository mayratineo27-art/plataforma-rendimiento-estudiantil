"""
Código actualizado para __init__.py
Habilita el módulo de Video/Audio con TensorFlow 2.16.2
"""

# Este es el código que reemplazará la sección comentada en __init__.py (líneas 116-127)

# ========== MÓDULO 2: Video & Audio ========== 
try:
    from app.routes.video_routes import video_bp, audio_bp
    app.register_blueprint(video_bp, url_prefix='/api/video')
    app.register_blueprint(audio_bp, url_prefix='/api/audio')
    print("   ✅ Video routes: /api/video")
    print("   ✅ Audio routes: /api/audio")
    print("   📹 Análisis facial con DeepFace habilitado")
    print("   🎙️ Transcripción de audio habilitada")
except ImportError as e:
    print(f"   ⚠️  Video/Audio routes no disponibles: {str(e)[:100]}")
    print("   📝 Verifica que TensorFlow 2.16.2 esté instalado")
except Exception as e:
    print(f"   ❌ Error al registrar Video/Audio: {str(e)[:100]}")
    import traceback
    traceback.print_exc()
