"""
Script para agregar columnas faltantes a la tabla timelines
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("=" * 80)
    print("🔧 AGREGANDO COLUMNAS FALTANTES A LA TABLA TIMELINES")
    print("=" * 80)
    
    # Obtener columnas actuales
    result = db.session.execute(text("SHOW COLUMNS FROM timelines"))
    current_columns = [row[0] for row in result]
    
    print(f"\n📋 Columnas actuales en 'timelines': {current_columns}")
    
    # Columnas que deben existir
    required_columns = {
        'end_date': "ALTER TABLE timelines ADD COLUMN end_date DATETIME NULL AFTER timeline_type",
        'is_visible': "ALTER TABLE timelines ADD COLUMN is_visible TINYINT(1) DEFAULT 1 AFTER steps_json",
        'is_completed': "ALTER TABLE timelines ADD COLUMN is_completed TINYINT(1) DEFAULT 0 AFTER is_visible",
        'completed_date': "ALTER TABLE timelines ADD COLUMN completed_date DATETIME NULL AFTER is_completed"
    }
    
    print("\n🔍 Verificando columnas requeridas...\n")
    
    added_columns = []
    skipped_columns = []
    
    for column_name, alter_query in required_columns.items():
        if column_name in current_columns:
            print(f"  ✅ '{column_name}' ya existe")
            skipped_columns.append(column_name)
        else:
            try:
                print(f"  ➕ Agregando '{column_name}'...")
                db.session.execute(text(alter_query))
                db.session.commit()
                print(f"  ✅ '{column_name}' agregada exitosamente")
                added_columns.append(column_name)
            except Exception as e:
                print(f"  ❌ Error agregando '{column_name}': {e}")
                db.session.rollback()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN")
    print("=" * 80)
    print(f"✅ Columnas que ya existían: {len(skipped_columns)}")
    print(f"➕ Columnas agregadas: {len(added_columns)}")
    
    if added_columns:
        print(f"\nColumnas nuevas: {', '.join(added_columns)}")
    
    # Verificar resultado final
    result = db.session.execute(text("SHOW COLUMNS FROM timelines"))
    final_columns = [row[0] for row in result]
    
    print(f"\n📋 Columnas finales en 'timelines': {final_columns}")
    
    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)
