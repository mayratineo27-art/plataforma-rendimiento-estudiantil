"""
Script para crear la tabla de evaluaciones de escritura
"""

from app import create_app, db
from app.models.writing_evaluation import WritingEvaluation

def create_writing_evaluation_table():
    app = create_app()
    
    with app.app_context():
        print("=" * 80)
        print("📊 CREANDO TABLA DE EVALUACIONES DE ESCRITURA")
        print("=" * 80)
        
        try:
            # Crear tabla
            WritingEvaluation.__table__.create(db.engine, checkfirst=True)
            print("✅ Tabla 'writing_evaluations' creada exitosamente")
            
            # Verificar
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            
            if 'writing_evaluations' in inspector.get_table_names():
                columns = inspector.get_columns('writing_evaluations')
                print(f"\n✅ Tabla verificada con {len(columns)} columnas:")
                for col in columns:
                    print(f"   - {col['name']}: {col['type']}")
            else:
                print("❌ Error: Tabla no encontrada después de creación")
                
        except Exception as e:
            print(f"❌ Error creando tabla: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_writing_evaluation_table()
