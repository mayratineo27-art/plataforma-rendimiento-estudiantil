"""
Script para agregar la columna end_date a la tabla timelines
"""

from app import create_app, db
from sqlalchemy import text

def add_end_date_column():
    """Agrega la columna end_date a la tabla timelines"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Verificando columna end_date en tabla timelines...")
            
            # Verificar si la columna ya existe
            result = db.session.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'timelines' 
                AND COLUMN_NAME = 'end_date'
                AND TABLE_SCHEMA = DATABASE()
            """))
            
            if result.fetchone():
                print("✅ La columna end_date ya existe")
                return True
            
            print("📝 Agregando columna end_date...")
            
            # Agregar la columna
            db.session.execute(text("""
                ALTER TABLE timelines 
                ADD COLUMN end_date DATETIME NULL
            """))
            
            db.session.commit()
            
            print("✅ Columna end_date agregada correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = add_end_date_column()
    if success:
        print("\n🎉 ¡Migración completada!")
    else:
        print("\n⚠️  Error en la migración")
