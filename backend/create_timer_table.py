"""
Script para crear la tabla study_timers
Ejecutar con: python backend/migrations/create_timer_table.py
"""

from app import create_app, db
from app.models.timer import StudyTimer

def create_timer_table():
    """Crea la tabla study_timers en la base de datos"""
    app = create_app()
    
    with app.app_context():
        try:
            # Crear todas las tablas (solo creará las que no existan)
            db.create_all()
            print("✅ Tabla 'study_timers' creada exitosamente")
            
            # Verificar que existe
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'study_timers' in tables:
                print("✅ Verificación exitosa: tabla 'study_timers' existe en la base de datos")
                
                # Mostrar columnas
                columns = inspector.get_columns('study_timers')
                print("\n📋 Columnas de la tabla:")
                for col in columns:
                    print(f"   - {col['name']}: {col['type']}")
            else:
                print("❌ Error: La tabla no se creó correctamente")
                
        except Exception as e:
            print(f"❌ Error al crear la tabla: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_timer_table()
