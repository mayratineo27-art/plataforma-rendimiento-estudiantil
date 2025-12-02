"""
Script para añadir la columna course_topic a la tabla timelines
Permite crear líneas de tiempo sobre temas específicos de cursos
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("=" * 80)
    print("🔧 AÑADIENDO COLUMNA course_topic A TABLA timelines")
    print("=" * 80)
    
    try:
        # Verificar si la columna ya existe
        result = db.session.execute(text("""
            SELECT COUNT(*) as count
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'timelines' 
            AND COLUMN_NAME = 'course_topic'
        """))
        
        count = result.fetchone()[0]
        
        if count > 0:
            print("✅ La columna 'course_topic' ya existe en la tabla 'timelines'")
        else:
            print("📝 Añadiendo columna 'course_topic'...")
            
            # Añadir la columna
            db.session.execute(text("""
                ALTER TABLE timelines 
                ADD COLUMN course_topic VARCHAR(300) NULL
                COMMENT 'Tema específico del curso para timelines de tipo free'
            """))
            
            db.session.commit()
            print("✅ Columna 'course_topic' añadida exitosamente")
        
        # Verificar la estructura de la tabla
        print("\n📊 Estructura actual de la tabla 'timelines':")
        result = db.session.execute(text("""
            DESCRIBE timelines
        """))
        
        for row in result:
            print(f"  - {row[0]}: {row[1]}")
        
        print("\n" + "=" * 80)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
