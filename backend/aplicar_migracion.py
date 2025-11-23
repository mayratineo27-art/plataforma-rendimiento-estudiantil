"""
Aplicar migración de base de datos
Agrega nuevas columnas y tablas para las mejoras
"""

import pymysql
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def aplicar_migracion():
    """Ejecuta el script SQL de migración"""
    
    # Conectar a la base de datos
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'plataforma_estudiantil'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # Leer el archivo SQL
            sql_file = r"c:\Users\maley\Downloads\plataforma-rendimiento-estudiantil (1)\plataforma-rendimiento-estudiantilDis\database\migrations\mejoras_gestion_2025_11_23.sql"
            
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Dividir en comandos individuales
            commands = sql_script.split(';')
            
            print("🔄 Aplicando migración...")
            print("="*70)
            
            for i, command in enumerate(commands, 1):
                command = command.strip()
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                        print(f"✅ Comando {i} ejecutado correctamente")
                    except Exception as e:
                        # Ignorar errores de "ya existe"
                        if "already exists" in str(e) or "Duplicate" in str(e):
                            print(f"⚠️  Comando {i}: Ya existe (ignorando)")
                        else:
                            print(f"❌ Error en comando {i}: {e}")
            
            connection.commit()
            print("="*70)
            print("✅ Migración aplicada correctamente")
            
            # Verificar las nuevas columnas
            print("\n📊 Verificando cambios...")
            cursor.execute("DESCRIBE academic_courses")
            columns = cursor.fetchall()
            
            new_columns = ['code', 'category', 'icon', 'color']
            for col in new_columns:
                exists = any(c['Field'] == col for c in columns)
                symbol = "✅" if exists else "❌"
                print(f"{symbol} Columna '{col}': {'Existe' if exists else 'No encontrada'}")
            
            # Verificar nuevas tablas
            cursor.execute("SHOW TABLES LIKE 'syllabus_analysis'")
            syllabus_table = cursor.fetchone()
            print(f"{'✅' if syllabus_table else '❌'} Tabla 'syllabus_analysis': {'Existe' if syllabus_table else 'No encontrada'}")
            
            cursor.execute("SHOW TABLES LIKE 'timeline_steps'")
            steps_table = cursor.fetchone()
            print(f"{'✅' if steps_table else '❌'} Tabla 'timeline_steps': {'Existe' if steps_table else 'No encontrada'}")
            
    except Exception as e:
        print(f"❌ Error al aplicar migración: {e}")
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    aplicar_migracion()
