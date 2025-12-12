#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generador de Informe Detallado de Base de Datos
Plataforma de Rendimiento Estudiantil
"""

from app import create_app, db
from sqlalchemy import inspect, text
from datetime import datetime

def generate_database_report():
    """Genera un informe completo de la base de datos"""
    
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("="*100)
        print("📊 INFORME DETALLADO DE BASE DE DATOS - PLATAFORMA DE RENDIMIENTO ESTUDIANTIL")
        print("="*100)
        print(f"\n📅 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🗄️  Motor: {db.engine.url.drivername}")
        print(f"📦 Base de datos: {db.engine.url.database}")
        print(f"📊 Total de tablas: {len(tables)}\n")
        
        # Agrupar tablas por módulo
        modulo_nodo_digital = []
        modulo_video_audio = []
        modulo_academico = []
        modulo_proyectos = []
        modulo_usuarios = []
        modulo_reportes = []
        otras_tablas = []
        
        for table in sorted(tables):
            if table in ['users', 'student_profiles']:
                modulo_usuarios.append(table)
            elif table in ['video_sessions', 'emotion_data', 'audio_transcriptions', 'attention_metrics']:
                modulo_video_audio.append(table)
            elif table in ['writing_evaluations', 'courses', 'tasks', 'study_timers']:
                modulo_academico.append(table)
            elif table in ['projects', 'time_sessions', 'timelines']:
                modulo_proyectos.append(table)
            elif table in ['reports']:
                modulo_reportes.append(table)
            else:
                otras_tablas.append(table)
        
        # MÓDULO USUARIOS
        if modulo_usuarios:
            print("\n" + "="*100)
            print("👥 MÓDULO DE USUARIOS")
            print("="*100)
            for table in modulo_usuarios:
                print_table_details(inspector, table)
        
        # MÓDULO NODO DIGITAL (Académico)
        if modulo_academico:
            print("\n" + "="*100)
            print("📚 MÓDULO NODO DIGITAL - ACADÉMICO")
            print("="*100)
            for table in modulo_academico:
                print_table_details(inspector, table)
        
        # MÓDULO VIDEO/AUDIO
        if modulo_video_audio:
            print("\n" + "="*100)
            print("🎥 MÓDULO VIDEO & AUDIO - ANÁLISIS EN TIEMPO REAL")
            print("="*100)
            for table in modulo_video_audio:
                print_table_details(inspector, table)
        
        # MÓDULO PROYECTOS Y TIMELINES
        if modulo_proyectos:
            print("\n" + "="*100)
            print("📋 MÓDULO DE PROYECTOS Y LÍNEAS DE TIEMPO")
            print("="*100)
            for table in modulo_proyectos:
                print_table_details(inspector, table)
        
        # MÓDULO REPORTES
        if modulo_reportes:
            print("\n" + "="*100)
            print("📊 MÓDULO DE REPORTES")
            print("="*100)
            for table in modulo_reportes:
                print_table_details(inspector, table)
        
        # OTRAS TABLAS
        if otras_tablas:
            print("\n" + "="*100)
            print("🔧 OTRAS TABLAS DEL SISTEMA")
            print("="*100)
            for table in otras_tablas:
                print_table_details(inspector, table)
        
        # ESTADÍSTICAS DE DATOS
        print("\n" + "="*100)
        print("📈 ESTADÍSTICAS DE DATOS")
        print("="*100)
        
        try:
            # Contar registros en cada tabla
            for table in sorted(tables):
                result = db.session.execute(text(f"SELECT COUNT(*) FROM `{table}`"))
                count = result.scalar()
                status = "✅" if count > 0 else "⚪"
                print(f"{status} {table:30} → {count:6} registros")
        except Exception as e:
            print(f"⚠️  Error al contar registros: {e}")
        
        print("\n" + "="*100)
        print("✅ INFORME COMPLETADO")
        print("="*100)

def print_table_details(inspector, table_name):
    """Imprime detalles de una tabla específica"""
    
    columns = inspector.get_columns(table_name)
    pk_constraint = inspector.get_pk_constraint(table_name)
    fk_constraints = inspector.get_foreign_keys(table_name)
    indexes = inspector.get_indexes(table_name)
    
    print(f"\n📋 Tabla: {table_name}")
    print("-" * 100)
    
    # Primary Keys
    if pk_constraint and pk_constraint.get('constrained_columns'):
        pks = ', '.join(pk_constraint['constrained_columns'])
        print(f"🔑 Primary Key: {pks}")
    
    # Columnas
    print(f"\n📊 Columnas ({len(columns)}):")
    for col in columns:
        nullable = "NULL" if col['nullable'] else "NOT NULL"
        default = f" DEFAULT {col['default']}" if col['default'] else ""
        col_type = str(col['type'])
        
        # Marcar si es PK
        is_pk = ""
        if pk_constraint and col['name'] in pk_constraint.get('constrained_columns', []):
            is_pk = " 🔑"
        
        print(f"   • {col['name']:30} {col_type:20} {nullable:10}{default}{is_pk}")
    
    # Foreign Keys
    if fk_constraints:
        print(f"\n🔗 Foreign Keys ({len(fk_constraints)}):")
        for fk in fk_constraints:
            constrained = ', '.join(fk['constrained_columns'])
            referred = fk['referred_table']
            referred_cols = ', '.join(fk['referred_columns'])
            print(f"   • {constrained} → {referred}({referred_cols})")
    
    # Índices
    if indexes:
        print(f"\n📇 Índices ({len(indexes)}):")
        for idx in indexes:
            unique = "UNIQUE" if idx['unique'] else "INDEX"
            cols = ', '.join(idx['column_names'])
            print(f"   • {idx['name']:40} {unique:8} ({cols})")

if __name__ == '__main__':
    generate_database_report()
