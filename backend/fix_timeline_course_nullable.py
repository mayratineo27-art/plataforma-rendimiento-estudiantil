"""
Script para hacer la columna course_id nullable en la tabla timelines
Esto permite crear líneas de tiempo sin curso asociado
"""
from app import create_app, db
from sqlalchemy import text

def fix_timeline_course_nullable():
    """Modifica la columna course_id para permitir valores NULL"""
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar el estado actual
            print("Verificando estado actual de la columna course_id...")
            result = db.session.execute(text("""
                SELECT 
                    COLUMN_NAME,
                    IS_NULLABLE,
                    DATA_TYPE,
                    COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'timelines' 
                AND COLUMN_NAME = 'course_id'
            """))
            
            column_info = result.fetchone()
            if column_info:
                print(f"Estado actual: {column_info}")
                print(f"  - Columna: {column_info[0]}")
                print(f"  - Nullable: {column_info[1]}")
                print(f"  - Tipo: {column_info[2]}")
                
                if column_info[1] == 'NO':
                    print("\n⚠️  La columna course_id NO permite NULL")
                    print("Modificando columna para permitir NULL...")
                    
                    # Modificar la columna para permitir NULL
                    db.session.execute(text("""
                        ALTER TABLE timelines 
                        ALTER COLUMN course_id INT NULL
                    """))
                    
                    db.session.commit()
                    print("✅ Columna course_id ahora permite valores NULL")
                else:
                    print("✅ La columna course_id ya permite valores NULL")
            else:
                print("❌ No se encontró la columna course_id en la tabla timelines")
            
            # Verificar el cambio
            print("\nVerificando cambios...")
            result = db.session.execute(text("""
                SELECT 
                    COLUMN_NAME,
                    IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'timelines' 
                AND COLUMN_NAME = 'course_id'
            """))
            
            column_info = result.fetchone()
            if column_info:
                print(f"Estado final - Columna: {column_info[0]}, Nullable: {column_info[1]}")
                
        except Exception as e:
            print(f"❌ Error al modificar la columna: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("SCRIPT: Hacer course_id nullable en timelines")
    print("=" * 60)
    
    if fix_timeline_course_nullable():
        print("\n✅ Script ejecutado exitosamente")
    else:
        print("\n❌ El script encontró errores")
