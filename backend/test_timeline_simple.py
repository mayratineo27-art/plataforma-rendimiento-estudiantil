"""
Script de diagnóstico para verificar la creación de timeline
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.timeline import Timeline
from app.models.timeline_step import TimelineStep

app = create_app()

with app.app_context():
    print("=" * 80)
    print("🔍 DIAGNÓSTICO DE TIMELINE")
    print("=" * 80)
    
    # 1. Verificar que las tablas existen
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\n✅ Tablas en la base de datos: {len(tables)}")
        if 'timelines' in tables:
            print("  ✅ Tabla 'timelines' existe")
        else:
            print("  ❌ Tabla 'timelines' NO EXISTE")
        
        if 'timeline_steps' in tables:
            print("  ✅ Tabla 'timeline_steps' existe")
        else:
            print("  ❌ Tabla 'timeline_steps' NO EXISTE")
            
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
    
    # 2. Intentar crear un timeline simple
    print("\n" + "=" * 80)
    print("🧪 Probando crear timeline simple...")
    print("=" * 80)
    
    try:
        # Crear timeline de prueba
        test_timeline = Timeline(
            user_id=1,
            course_id=1,
            title="TEST - Timeline de Prueba",
            description="Este es un test",
            timeline_type='course'
        )
        
        print("  ✅ Objeto Timeline creado en memoria")
        
        db.session.add(test_timeline)
        print("  ✅ Timeline agregado a la sesión")
        
        db.session.flush()
        print(f"  ✅ Flush exitoso - ID asignado: {test_timeline.id}")
        
        # Crear un paso simple
        test_step = TimelineStep(
            timeline_id=test_timeline.id,
            title="Paso de prueba",
            description="Este es un paso de prueba",
            order=1
        )
        
        db.session.add(test_step)
        print("  ✅ TimelineStep agregado a la sesión")
        
        db.session.commit()
        print("  ✅ COMMIT EXITOSO - Timeline guardado en BD")
        
        print(f"\n✅ Timeline creado con ID: {test_timeline.id}")
        print(f"✅ Timeline tiene {len(test_timeline.steps)} pasos")
        
        # Limpiar - eliminar el timeline de prueba
        db.session.delete(test_timeline)
        db.session.commit()
        print("\n🧹 Timeline de prueba eliminado")
        
        print("\n" + "=" * 80)
        print("✅ TODAS LAS PRUEBAS PASARON - La BD está OK")
        print("=" * 80)
        print("\nEl problema debe estar en:")
        print("  1. Los datos que envía el frontend")
        print("  2. La validación de foreign keys (user_id o course_id inválidos)")
        print("  3. La API de Gemini (si usas generación con IA)")
        
    except Exception as e:
        print(f"\n❌ ERROR AL CREAR TIMELINE:")
        print(f"   {type(e).__name__}: {e}")
        
        import traceback
        print("\n📋 Traceback completo:")
        traceback.print_exc()
        
        db.session.rollback()
        
        print("\n" + "=" * 80)
        print("💡 POSIBLES CAUSAS:")
        print("=" * 80)
        print("  - user_id=1 no existe en la tabla 'users'")
        print("  - course_id=1 no existe en la tabla 'academic_courses'")
        print("  - Falta alguna columna en la tabla 'timelines'")
        print("  - Problema de tipos de datos (VARCHAR vs INT)")
