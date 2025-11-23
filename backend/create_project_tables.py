"""
Script para crear las tablas de Proyectos y Sesiones de Tiempo
Plataforma de Rendimiento Estudiantil - Módulo Digital
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.project import Project, TimeSession
from app.models.academic import AcademicCourse

def create_tables():
    """Crea las tablas de proyectos y sesiones de tiempo"""
    print("\n" + "="*60)
    print("  CREACIÓN DE TABLAS: PROYECTOS Y SESIONES DE TIEMPO")
    print("="*60 + "\n")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Intentar crear las tablas
            print("📋 Creando tablas...")
            
            # Verificar que exista la tabla de cursos primero
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'academic_courses' not in existing_tables:
                print("⚠️  ADVERTENCIA: La tabla 'academic_courses' no existe.")
                print("   Ejecuta primero el script de cursos académicos.")
                return
            
            # Crear las nuevas tablas
            Project.__table__.create(db.engine, checkfirst=True)
            TimeSession.__table__.create(db.engine, checkfirst=True)
            
            print("✅ Tabla 'projects' creada")
            print("✅ Tabla 'time_sessions' creada")
            
            # Verificar las tablas
            print("\n📊 Verificando estructura de las tablas:")
            
            projects_columns = inspector.get_columns('projects')
            print(f"\n   projects ({len(projects_columns)} columnas):")
            for col in projects_columns:
                print(f"      • {col['name']} ({col['type']})")
            
            sessions_columns = inspector.get_columns('time_sessions')
            print(f"\n   time_sessions ({len(sessions_columns)} columnas):")
            for col in sessions_columns:
                print(f"      • {col['name']} ({col['type']})")
            
            print("\n" + "="*60)
            print("✅ TABLAS CREADAS EXITOSAMENTE")
            print("="*60 + "\n")
            
            print("📌 Próximos pasos:")
            print("   1. Reinicia el backend: python run.py")
            print("   2. Prueba las rutas en /api/projects")
            print("   3. Crea un proyecto desde el frontend")
            print()
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            print(f"   Tipo: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return

if __name__ == '__main__':
    create_tables()
