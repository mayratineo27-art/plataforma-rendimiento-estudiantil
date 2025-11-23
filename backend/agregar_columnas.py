"""
Aplicar las columnas faltantes de forma manual
"""

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def aplicar_columnas():
    """Agrega las columnas faltantes una por una"""
    
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
            print("🔄 Agregando columnas faltantes...")
            print("="*70)
            
            # Verificar columnas existentes
            cursor.execute("DESCRIBE academic_courses")
            existing_columns = [col['Field'] for col in cursor.fetchall()]
            print(f"📋 Columnas existentes: {', '.join(existing_columns)}")
            
            # Lista de columnas a agregar
            columns_to_add = [
                ("code", "VARCHAR(50)", "NULL", "Código del curso"),
                ("category", "VARCHAR(50)", "'general'", "Categoría del curso"),
                ("icon", "VARCHAR(50)", "'BookOpen'", "Icono del curso"),
            ]
            
            for col_name, col_type, default, comment in columns_to_add:
                if col_name not in existing_columns:
                    try:
                        sql = f"ALTER TABLE academic_courses ADD COLUMN {col_name} {col_type} DEFAULT {default} COMMENT '{comment}'"
                        cursor.execute(sql)
                        connection.commit()
                        print(f"✅ Columna '{col_name}' agregada correctamente")
                    except Exception as e:
                        print(f"❌ Error al agregar '{col_name}': {e}")
                else:
                    print(f"⚠️  Columna '{col_name}' ya existe")
            
            print("="*70)
            
            # Verificar resultado final
            cursor.execute("DESCRIBE academic_courses")
            final_columns = cursor.fetchall()
            
            print("\n📊 Verificación final:")
            target_columns = ['code', 'category', 'icon', 'color']
            for col in target_columns:
                exists = any(c['Field'] == col for c in final_columns)
                symbol = "✅" if exists else "❌"
                print(f"{symbol} Columna '{col}': {'Existe' if exists else 'No encontrada'}")
            
            # Mostrar estructura completa
            print("\n📋 Estructura completa de academic_courses:")
            for col in final_columns:
                print(f"   - {col['Field']} ({col['Type']})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    aplicar_columnas()
