"""
Script para actualizar el ENUM timeline_type agregando 'free'

Ejecutar con:
    python update_timeline_enum.py
"""
from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        print("=" * 80)
        print("🔧 ACTUALIZANDO ENUM 'timeline_type' EN LA TABLA 'timelines'")
        print("=" * 80)
        
        # Verificar si el enum ya tiene 'free'
        result = db.session.execute(text("""
            SELECT COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'timelines' 
            AND COLUMN_NAME = 'timeline_type'
        """)).fetchone()
        
        if result:
            current_enum = result[0]
            print(f"\n📋 Enum actual: {current_enum}")
            
            if 'free' in current_enum:
                print("\n✅ El valor 'free' YA EXISTE en el enum")
            else:
                print("\n🔄 Agregando 'free' al enum...")
                
                # Modificar el ENUM para agregar 'free'
                db.session.execute(text("""
                    ALTER TABLE timelines 
                    MODIFY COLUMN timeline_type 
                    ENUM('academic', 'course', 'project', 'free') 
                    DEFAULT 'project'
                """))
                
                db.session.commit()
                print("✅ Enum actualizado correctamente")
                print("   Valores permitidos: 'academic', 'course', 'project', 'free'")
        else:
            print("\n❌ No se pudo encontrar la columna timeline_type")
            
        print("\n" + "=" * 80)
        print("✅ PROCESO COMPLETADO")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        db.session.rollback()
