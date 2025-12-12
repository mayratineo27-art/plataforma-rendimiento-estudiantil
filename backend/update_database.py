"""
Script para actualizar tablas de base de datos
Agrega columnas necesarias para audio y métricas de atención
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text

def update_database():
    app = create_app()
    
    with app.app_context():
        print("\n🔧 ACTUALIZANDO BASE DE DATOS\n")
        
        # Actualizar attention_metrics
        print("📊 Actualizando attention_metrics...")
        try:
            db.session.execute(text("""
                ALTER TABLE attention_metrics 
                ADD COLUMN IF NOT EXISTS face_presence_rate DECIMAL(5,2),
                ADD COLUMN IF NOT EXISTS confusion_percentage DECIMAL(5,2),
                ADD COLUMN IF NOT EXISTS confusion_peaks INT DEFAULT 0,
                ADD COLUMN IF NOT EXISTS comprehension_percentage DECIMAL(5,2),
                ADD COLUMN IF NOT EXISTS clarity_moments INT DEFAULT 0
            """))
            db.session.commit()
            print("   ✅ attention_metrics actualizada")
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
            db.session.rollback()
        
        # Crear audio_sessions si no existe
        print("\n📊 Verificando audio_sessions...")
        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS audio_sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    session_id INT,
                    user_id INT NOT NULL,
                    audio_file_path VARCHAR(500),
                    audio_file_size INT,
                    audio_duration_seconds INT,
                    audio_format VARCHAR(20),
                    processing_status ENUM('pending','processing','completed','failed') DEFAULT 'pending',
                    processing_started_at DATETIME,
                    processing_completed_at DATETIME,
                    error_message TEXT,
                    transcription_text TEXT,
                    transcription_confidence DECIMAL(5,2),
                    transcription_accuracy_percentage DECIMAL(5,2),
                    language_detected VARCHAR(10),
                    meta_info JSON,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES video_sessions(id) ON DELETE SET NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_session_id (session_id),
                    INDEX idx_user_id (user_id),
                    INDEX idx_status (processing_status)
                )
            """))
            db.session.commit()
            print("   ✅ audio_sessions verificada")
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
            db.session.rollback()
        
        # Crear audio_transcriptions si no existe
        print("\n📊 Verificando audio_transcriptions...")
        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS audio_transcriptions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    audio_session_id INT NOT NULL,
                    user_id INT NOT NULL,
                    start_time DECIMAL(10,3) NOT NULL,
                    end_time DECIMAL(10,3) NOT NULL,
                    duration_seconds DECIMAL(6,3),
                    text TEXT NOT NULL,
                    confidence DECIMAL(5,2),
                    sentiment VARCHAR(50),
                    sentiment_score DECIMAL(5,2),
                    keywords JSON,
                    language VARCHAR(10),
                    ai_analysis TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (audio_session_id) REFERENCES audio_sessions(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_audio_session_id (audio_session_id),
                    INDEX idx_time_range (start_time, end_time)
                )
            """))
            db.session.commit()
            print("   ✅ audio_transcriptions verificada")
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
            db.session.rollback()
        
        print("\n✅ ACTUALIZACIÓN COMPLETADA\n")

if __name__ == '__main__':
    update_database()
