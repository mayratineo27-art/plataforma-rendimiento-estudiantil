"""
Script para añadir la columna course_topic a la tabla timelines
"""
from app import create_app, db
from sqlalchemy import text

def add_course_topic_column():
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si la columna ya existe
            result = db.session.execute(text("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'timelines'
                AND COLUMN_NAME = 'course_topic'
            """))
            
            exists = result.fetchone()[0] > 0
            
            if exists:
                print("✓ La columna 'course_topic' ya existe en la tabla 'timelines'")
                return
            
            # Añadir la columna course_topic
            db.session.execute(text("""
                ALTER TABLE timelines
                ADD COLUMN course_topic VARCHAR(255) NULL
                COMMENT 'Tema específico del curso para timelines tipo free'
            """))
            
            db.session.commit()
            print("✓ Columna 'course_topic' añadida exitosamente a la tabla 'timelines'")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error al añadir la columna: {str(e)}")
            raise

if __name__ == "__main__":
    add_course_topic_column()
