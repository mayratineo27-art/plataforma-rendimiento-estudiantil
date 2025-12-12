"""
Verificar datos del curso en la base de datos
"""
import pymysql
from app.config.settings import Config

# Conectar a la base de datos
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123',
    database='rendimiento_estudiantil',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # Ver el curso 7
        cursor.execute("SELECT * FROM academic_courses WHERE id = 7")
        result = cursor.fetchone()
        
        if result:
            print("=" * 70)
            print("DATOS DEL CURSO ID 7:")
            print("=" * 70)
            for key, value in result.items():
                print(f"{key:20s}: {value}")
        else:
            print("❌ No se encontró el curso ID 7")
            
        print("\n" + "=" * 70)
        print("TODOS LOS CURSOS:")
        print("=" * 70)
        cursor.execute("SELECT id, name, status, updated_at FROM academic_courses")
        courses = cursor.fetchall()
        
        for course in courses:
            print(f"ID {course['id']:2d}: {course['name']:30s} | Status: {course['status']} | Updated: {course['updated_at']}")

finally:
    connection.close()
