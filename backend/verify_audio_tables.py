"""
Script para verificar y actualizar tablas de audio y atención
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import inspect, text

def check_and_update_tables():
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        print("\n" + "="*60)
        print("🔍 VERIFICANDO TABLAS DE AUDIO Y ATENCIÓN")
        print("="*60)
        
        # Verificar audio_sessions
        print("\n📊 Tabla: audio_sessions")
        if 'audio_sessions' in inspector.get_table_names():
            columns = {col['name']: col for col in inspector.get_columns('audio_sessions')}
            print(f"   ✅ Tabla existe con {len(columns)} columnas")
            
            # Verificar columnas necesarias
            required_cols = ['meta_info', 'processing_status', 'transcription_text']
            for col in required_cols:
                if col in columns:
                    print(f"   ✅ {col}: {columns[col]['type']}")
                else:
                    print(f"   ⚠️  {col}: FALTA")
                    
                    # Agregar columna faltante
                    try:
                        if col == 'meta_info':
                            db.session.execute(text(
                                'ALTER TABLE audio_sessions ADD COLUMN meta_info JSON'
                            ))
                        elif col == 'processing_status':
                            db.session.execute(text(
                                "ALTER TABLE audio_sessions ADD COLUMN processing_status "
                                "ENUM('pending','processing','completed','failed') DEFAULT 'pending'"
                            ))
                        elif col == 'transcription_text':
                            db.session.execute(text(
                                'ALTER TABLE audio_sessions ADD COLUMN transcription_text TEXT'
                            ))
                        db.session.commit()
                        print(f"      ➕ Columna {col} agregada")
                    except Exception as e:
                        print(f"      ❌ Error: {str(e)}")
                        db.session.rollback()
        else:
            print("   ❌ Tabla NO existe - creando...")
            db.session.execute(text("""
                CREATE TABLE audio_sessions (
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
            print("   ✅ Tabla creada")
        
        # Verificar audio_transcriptions
        print("\n📊 Tabla: audio_transcriptions")
        if 'audio_transcriptions' in inspector.get_table_names():
            columns = {col['name']: col for col in inspector.get_columns('audio_transcriptions')}
            print(f"   ✅ Tabla existe con {len(columns)} columnas")
            
            required_cols = ['audio_session_id', 'start_time', 'end_time', 'text']
            for col in required_cols:
                if col in columns:
                    print(f"   ✅ {col}: {columns[col]['type']}")
                else:
                    print(f"   ⚠️  {col}: FALTA")
        else:
            print("   ❌ Tabla NO existe - creando...")
            db.session.execute(text("""
                CREATE TABLE audio_transcriptions (
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
            print("   ✅ Tabla creada")
        
        # Verificar attention_metrics
        print("\n📊 Tabla: attention_metrics")
        if 'attention_metrics' in inspector.get_table_names():
            columns = {col['name']: col for col in inspector.get_columns('attention_metrics')}
            print(f"   ✅ Tabla existe con {len(columns)} columnas")
            
            # Verificar columnas nuevas
            new_cols = ['face_presence_rate', 'confusion_percentage', 'confusion_peaks', 
                       'comprehension_percentage', 'clarity_moments']
            for col in new_cols:
                if col not in columns:
                    print(f"   ⚠️  {col}: FALTA - agregando...")
                    try:
                        if 'percentage' in col or 'rate' in col:
                            db.session.execute(text(
                                f'ALTER TABLE attention_metrics ADD COLUMN {col} DECIMAL(5,2)'
                            ))
                        else:
                            db.session.execute(text(
                                f'ALTER TABLE attention_metrics ADD COLUMN {col} INT DEFAULT 0'
                            ))
                        db.session.commit()
                        print(f"      ➕ Columna {col} agregada")
                    except Exception as e:
                        print(f"      ❌ Error: {str(e)}")
                        db.session.rollback()
                else:
                    print(f"   ✅ {col}: {columns[col]['type']}")
        else:
            print("   ❌ Tabla NO existe - debe crearse con SQLAlchemy")
        
        print("\n" + "="*60)
        print("✅ VERIFICACIÓN COMPLETADA")
        print("="*60 + "\n")

if __name__ == '__main__':
    check_and_update_tables()
