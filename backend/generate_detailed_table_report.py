#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generador de Informe Detallado por Tabla - Nodo Digital
Plataforma de Rendimiento Estudiantil
"""

from app import create_app, db
from sqlalchemy import inspect, text
from datetime import datetime

def generate_detailed_table_report():
    """Genera un informe DETALLADO tabla por tabla"""
    
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Tablas del Nodo Digital
        nodo_digital_tables = {
            'writing_evaluations': 'EVALUACIÓN DE ESCRITURA CON IA',
            'syllabus_analysis': 'ANÁLISIS DE SYLLABUS',
            'student_profiles': 'PERFIL ESTUDIANTIL AVANZADO',
            'timelines': 'LÍNEAS DE TIEMPO',
            'timeline_steps': 'PASOS DE LÍNEAS DE TIEMPO',
            'projects': 'PROYECTOS',
            'time_sessions': 'SESIONES DE TIEMPO',
            'academic_courses': 'CURSOS ACADÉMICOS',
            'academic_tasks': 'TAREAS ACADÉMICAS',
            'study_timers': 'CRONÓMETROS DE ESTUDIO',
            'ai_interactions': 'INTERACCIONES CON IA',
            'reports': 'REPORTES GENERADOS',
            'generated_templates': 'PLANTILLAS GENERADAS'
        }
        
        print("="*120)
        print("📊 INFORME DETALLADO DE TABLAS - NODO DIGITAL")
        print("="*120)
        print(f"\n📅 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🗄️  Base de datos: {db.engine.url.database}")
        print(f"🔗 Host: {db.engine.url.host}")
        print(f"📦 Total de tablas analizadas: {len(nodo_digital_tables)}\n")
        
        for table_name, description in nodo_digital_tables.items():
            print("\n" + "="*120)
            print(f"📋 TABLA: {table_name.upper()}")
            print(f"📝 Descripción: {description}")
            print("="*120)
            
            # Verificar si la tabla existe
            if table_name not in inspector.get_table_names():
                print(f"⚠️  TABLA NO ENCONTRADA EN LA BASE DE DATOS")
                continue
            
            # Obtener columnas
            columns = inspector.get_columns(table_name)
            pk_constraint = inspector.get_pk_constraint(table_name)
            fk_constraints = inspector.get_foreign_keys(table_name)
            
            # Contar registros
            try:
                result = db.session.execute(text(f"SELECT COUNT(*) FROM `{table_name}`"))
                record_count = result.scalar()
            except:
                record_count = "Error al contar"
            
            print(f"\n📊 ESTADÍSTICAS:")
            print(f"   • Total de columnas: {len(columns)}")
            print(f"   • Total de registros: {record_count}")
            print(f"   • Primary Keys: {len(pk_constraint.get('constrained_columns', [])) if pk_constraint else 0}")
            print(f"   • Foreign Keys: {len(fk_constraints)}")
            
            # Listar TODAS las columnas con TODOS los detalles
            print(f"\n📋 COLUMNAS DETALLADAS ({len(columns)}):")
            print("-"*120)
            print(f"{'#':<4} {'NOMBRE':<35} {'TIPO':<25} {'NULL':<8} {'DEFAULT':<20} {'EXTRAS'}")
            print("-"*120)
            
            pks = pk_constraint.get('constrained_columns', []) if pk_constraint else []
            
            for i, col in enumerate(columns, 1):
                # Información básica
                col_name = col['name']
                col_type = str(col['type'])
                nullable = "SÍ" if col['nullable'] else "NO"
                default = str(col['default'])[:18] if col['default'] else "-"
                
                # Extras
                extras = []
                if col_name in pks:
                    extras.append("🔑 PK")
                
                # Buscar si es FK
                for fk in fk_constraints:
                    if col_name in fk['constrained_columns']:
                        idx = fk['constrained_columns'].index(col_name)
                        referred_table = fk['referred_table']
                        referred_col = fk['referred_columns'][idx]
                        extras.append(f"🔗 FK → {referred_table}({referred_col})")
                
                extras_str = " | ".join(extras) if extras else ""
                
                print(f"{i:<4} {col_name:<35} {col_type:<25} {nullable:<8} {default:<20} {extras_str}")
            
            # Descripción de columnas clave
            print(f"\n💡 COLUMNAS DESTACADAS:")
            highlight_columns = {
                'writing_evaluations': [
                    ('overall_score', 'Puntuación general de 0-100 calculada por IA'),
                    ('grammar_score', 'Evaluación gramatical con Gemini'),
                    ('specific_errors', 'JSON con errores detectados y correcciones'),
                    ('suggestions', 'JSON con sugerencias personalizadas'),
                    ('tone_analysis', 'Tono del texto: académico/formal/informal'),
                    ('improvement_percentage', 'Porcentaje de mejora respecto a versión anterior')
                ],
                'student_profiles': [
                    ('thesis_readiness_score', 'Puntuación de preparación para tesis (0-100)'),
                    ('thesis_readiness_level', 'Nivel: no_preparado/inicial/intermedio/avanzado/listo'),
                    ('ai_profile_summary', 'Resumen del perfil generado por IA'),
                    ('ai_personalized_advice', 'Consejos personalizados de IA'),
                    ('academic_strengths', 'JSON con fortalezas académicas detectadas'),
                    ('areas_for_improvement', 'JSON con áreas a mejorar')
                ],
                'timelines': [
                    ('course_topic', '✅ NUEVO: Tema específico del curso'),
                    ('timeline_type', 'Tipo: project/course/custom/thesis'),
                    ('steps_json', 'JSON con los pasos de la línea de tiempo')
                ],
                'ai_interactions': [
                    ('interaction_type', 'Tipo: writing_eval/text_analysis/report_gen'),
                    ('model_used', 'Modelo de IA: gemini-2.5-flash, etc.'),
                    ('tokens_used', 'Tokens consumidos por la API'),
                    ('cost_estimate', 'Costo estimado en USD')
                ],
                'reports': [
                    ('report_type', 'Tipo: academic/writing/video/project/complete'),
                    ('personalization_profile', 'JSON con perfil del estudiante'),
                    ('charts_data', 'JSON con datos para gráficos'),
                    ('file_format', 'Formato: PDF/DOCX/PPTX')
                ]
            }
            
            if table_name in highlight_columns:
                for col_name, description in highlight_columns[table_name]:
                    print(f"   • {col_name:<35} → {description}")
            
            # Ejemplos de datos (si existen)
            if record_count > 0:
                print(f"\n📄 EJEMPLO DE DATOS (Primeros 3 registros):")
                try:
                    # Obtener nombres de columnas para mostrar
                    col_names = [col['name'] for col in columns[:5]]  # Primeras 5 columnas
                    cols_str = ', '.join([f"`{c}`" for c in col_names])
                    
                    result = db.session.execute(text(f"SELECT {cols_str} FROM `{table_name}` LIMIT 3"))
                    rows = result.fetchall()
                    
                    if rows:
                        print(f"   Mostrando columnas: {', '.join(col_names)}")
                        for row in rows:
                            row_data = []
                            for val in row:
                                if val is None:
                                    row_data.append("NULL")
                                elif isinstance(val, str) and len(val) > 30:
                                    row_data.append(val[:27] + "...")
                                else:
                                    row_data.append(str(val))
                            print(f"   → {' | '.join(row_data)}")
                except Exception as e:
                    print(f"   ⚠️  Error al obtener ejemplos: {e}")
        
        # Información de conexión
        print("\n" + "="*120)
        print("🔗 INFORMACIÓN DE CONEXIÓN A LA BASE DE DATOS")
        print("="*120)
        print(f"\n📍 Ubicación de la base de datos:")
        print(f"   • Motor: MySQL")
        print(f"   • Host: {db.engine.url.host or 'localhost'}")
        print(f"   • Puerto: {db.engine.url.port or 3306}")
        print(f"   • Base de datos: {db.engine.url.database}")
        print(f"   • Usuario: {db.engine.url.username}")
        print(f"\n📁 Archivo de configuración:")
        print(f"   • .env: backend/.env")
        print(f"   • Variables: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
        print(f"\n🔧 Herramientas para acceder:")
        print(f"   • phpMyAdmin: http://localhost/phpmyadmin (si tienes XAMPP/WAMP)")
        print(f"   • MySQL Workbench: Conexión directa a localhost:3306")
        print(f"   • Línea de comandos: mysql -u root -p {db.engine.url.database}")
        print(f"   • DBeaver: Herramienta universal de base de datos")
        
        print("\n" + "="*120)
        print("✅ INFORME DETALLADO COMPLETADO")
        print("="*120)

if __name__ == '__main__':
    generate_detailed_table_report()
