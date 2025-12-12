#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para agregar columna meta_info a la tabla reports
"""

from app import create_app, db
from sqlalchemy import text

def fix_reports_table():
    """Agregar columna meta_info a reports"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Verificando columna meta_info en tabla reports...")
            
            # Verificar si la columna existe
            result = db.session.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'reports' 
                AND COLUMN_NAME = 'meta_info'
            """))
            
            if result.fetchone():
                print("✅ La columna meta_info ya existe")
                return
            
            print("➕ Agregando columna meta_info...")
            
            # Agregar columna
            db.session.execute(text("""
                ALTER TABLE reports 
                ADD COLUMN meta_info JSON DEFAULT NULL COMMENT 'Metadatos adicionales del reporte'
            """))
            
            db.session.commit()
            
            print("✅ Columna meta_info agregada exitosamente")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    fix_reports_table()
