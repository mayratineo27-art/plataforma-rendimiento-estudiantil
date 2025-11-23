"""
Script para actualizar la tabla time_sessions con los campos del cronómetro inteligente
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def update_database():
    """Actualiza la base de datos con los nuevos campos"""
    try:
        # Conectar a MySQL
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'rendimiento_estudiantil'),
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        print("📋 Actualizando tabla time_sessions...")
        
        # Agregar columnas faltantes
        queries = [
            # is_paused
            """
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'time_sessions' 
            AND COLUMN_NAME = 'is_paused'
            """,
            """
            ALTER TABLE time_sessions 
            ADD COLUMN is_paused BOOLEAN DEFAULT FALSE AFTER is_active
            """,
            # resumed_at
            """
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'time_sessions' 
            AND COLUMN_NAME = 'resumed_at'
            """,
            """
            ALTER TABLE time_sessions 
            ADD COLUMN resumed_at DATETIME NULL AFTER paused_at
            """,
            # last_activity_at
            """
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'time_sessions' 
            AND COLUMN_NAME = 'last_activity_at'
            """,
            """
            ALTER TABLE time_sessions 
            ADD COLUMN last_activity_at DATETIME NULL AFTER resumed_at
            """,
            # ended_at
            """
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'time_sessions' 
            AND COLUMN_NAME = 'ended_at'
            """,
            """
            ALTER TABLE time_sessions 
            ADD COLUMN ended_at DATETIME NULL AFTER last_activity_at
            """
        ]
        
        db_name = os.getenv('DB_NAME', 'rendimiento_estudiantil')
        
        # Verificar y agregar is_paused
        cursor.execute(queries[0], (db_name,))
        if cursor.fetchone()[0] == 0:
            print("   Agregando columna is_paused...")
            cursor.execute(queries[1])
        else:
            print("   ✓ Columna is_paused ya existe")
        
        # Verificar y agregar resumed_at
        cursor.execute(queries[2], (db_name,))
        if cursor.fetchone()[0] == 0:
            print("   Agregando columna resumed_at...")
            cursor.execute(queries[3])
        else:
            print("   ✓ Columna resumed_at ya existe")
        
        # Verificar y agregar last_activity_at
        cursor.execute(queries[4], (db_name,))
        if cursor.fetchone()[0] == 0:
            print("   Agregando columna last_activity_at...")
            cursor.execute(queries[5])
        else:
            print("   ✓ Columna last_activity_at ya existe")
        
        # Verificar y agregar ended_at
        cursor.execute(queries[6], (db_name,))
        if cursor.fetchone()[0] == 0:
            print("   Agregando columna ended_at...")
            cursor.execute(queries[7])
        else:
            print("   ✓ Columna ended_at ya existe")
        
        # Actualizar valores por defecto
        print("   Actualizando valores por defecto...")
        cursor.execute("UPDATE time_sessions SET is_paused = FALSE WHERE is_paused IS NULL")
        cursor.execute("UPDATE time_sessions SET duration_seconds = 0 WHERE duration_seconds IS NULL")
        cursor.execute("UPDATE time_sessions SET last_activity_at = started_at WHERE last_activity_at IS NULL AND started_at IS NOT NULL")
        
        connection.commit()
        print("✅ Tabla time_sessions actualizada correctamente")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando base de datos: {e}")
        return False

if __name__ == '__main__':
    success = update_database()
    if success:
        print("\n🎉 ¡Migración completada exitosamente!")
    else:
        print("\n⚠️  Hubo errores durante la migración")
