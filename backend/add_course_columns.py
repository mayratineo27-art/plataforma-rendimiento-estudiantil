#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para añadir columnas status y updated_at a academic_courses
"""

from app import create_app, db
from sqlalchemy import text

def add_course_columns():
    """Añade columnas status y updated_at a la tabla academic_courses"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("🔧 AÑADIENDO COLUMNAS A academic_courses")
            print("=" * 60)
            
            # Verificar si las columnas ya existen
            result = db.session.execute(text("SHOW COLUMNS FROM academic_courses LIKE 'status'"))
            has_status = result.fetchone() is not None
            
            result = db.session.execute(text("SHOW COLUMNS FROM academic_courses LIKE 'updated_at'"))
            has_updated_at = result.fetchone() is not None
            
            # Añadir columna status si no existe
            if not has_status:
                print("\n📋 Añadiendo columna 'status'...")
                db.session.execute(text("""
                    ALTER TABLE academic_courses 
                    ADD COLUMN status VARCHAR(20) DEFAULT 'active' AFTER color
                """))
                print("✅ Columna 'status' añadida")
            else:
                print("ℹ️  Columna 'status' ya existe")
            
            # Añadir columna updated_at si no existe
            if not has_updated_at:
                print("\n📋 Añadiendo columna 'updated_at'...")
                db.session.execute(text("""
                    ALTER TABLE academic_courses 
                    ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at
                """))
                print("✅ Columna 'updated_at' añadida")
            else:
                print("ℹ️  Columna 'updated_at' ya existe")
            
            # Confirmar cambios
            db.session.commit()
            
            # Actualizar cursos existentes
            if not has_status:
                print("\n📋 Actualizando cursos existentes...")
                db.session.execute(text("UPDATE academic_courses SET status = 'active' WHERE status IS NULL"))
                db.session.commit()
                print("✅ Cursos actualizados")
            
            # Verificar cambios
            print("\n📊 VERIFICANDO ESTRUCTURA:")
            result = db.session.execute(text("DESCRIBE academic_courses"))
            columns = result.fetchall()
            
            for col in columns:
                field_name = col[0]
                field_type = col[1]
                if field_name in ['status', 'updated_at', 'created_at', 'color', 'icon', 'category']:
                    print(f"   ✓ {field_name:<20} {field_type}")
            
            print("\n" + "=" * 60)
            print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    add_course_columns()
