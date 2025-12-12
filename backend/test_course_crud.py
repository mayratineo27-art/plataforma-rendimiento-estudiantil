"""
Script de prueba para verificar los endpoints CRUD de cursos
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/academic"

def test_course_crud():
    print("=" * 70)
    print("PRUEBA DE ENDPOINTS CRUD DE CURSOS")
    print("=" * 70)
    
    # 1. Crear un curso de prueba
    print("\n1️⃣ Creando curso de prueba...")
    new_course = {
        "user_id": 1,
        "name": "Curso de Prueba CRUD",
        "code": "TEST-001",
        "professor": "Dr. Test",
        "schedule": "Lunes 10:00-12:00",
        "category": "programacion",
        "icon": "Code",
        "color": "blue"
    }
    
    response = requests.post(f"{BASE_URL}/courses", json=new_course)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        course_data = response.json()
        course_id = course_data['course']['id']
        print(f"✅ Curso creado con ID: {course_id}")
        print(f"Nombre: {course_data['course']['name']}")
        print(f"Status: {course_data['course'].get('status', 'N/A')}")
        print(f"Updated At: {course_data['course'].get('updated_at', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")
        return
    
    # 2. Obtener el curso
    print(f"\n2️⃣ Obteniendo curso ID {course_id}...")
    response = requests.get(f"{BASE_URL}/courses/{course_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        course = response.json()['course']
        print(f"✅ Curso obtenido:")
        print(f"   Nombre: {course['name']}")
        print(f"   Profesor: {course['professor']}")
        print(f"   Status: {course.get('status', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")
    
    # 3. Actualizar el curso
    print(f"\n3️⃣ Actualizando curso ID {course_id}...")
    update_data = {
        "name": "Curso ACTUALIZADO",
        "professor": "Dr. Actualizado",
        "color": "purple",
        "icon": "Database"
    }
    
    response = requests.put(f"{BASE_URL}/courses/{course_id}", json=update_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        updated = response.json()['course']
        print(f"✅ Curso actualizado:")
        print(f"   Nombre: {updated['name']}")
        print(f"   Profesor: {updated['professor']}")
        print(f"   Color: {updated['color']}")
        print(f"   Icon: {updated['icon']}")
        print(f"   Status: {updated.get('status', 'N/A')}")
        print(f"   Updated At: {updated.get('updated_at', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")
    
    # 4. Listar todos los cursos
    print(f"\n4️⃣ Listando todos los cursos del usuario 1...")
    response = requests.get(f"{BASE_URL}/user/1/courses")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        courses = response.json()['courses']
        print(f"✅ Total de cursos: {len(courses)}")
        for c in courses:
            print(f"   - {c['name']} ({c['code']}) - Status: {c.get('status', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")
    
    # 5. Eliminar el curso de prueba
    print(f"\n5️⃣ Eliminando curso ID {course_id}...")
    response = requests.delete(f"{BASE_URL}/courses/{course_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✅ Curso eliminado exitosamente")
    else:
        print(f"❌ Error: {response.text}")
    
    # 6. Verificar eliminación
    print(f"\n6️⃣ Verificando eliminación...")
    response = requests.get(f"{BASE_URL}/courses/{course_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 404:
        print(f"✅ Verificado: El curso ya no existe")
    else:
        print(f"⚠️ El curso aún existe")
    
    print("\n" + "=" * 70)
    print("PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_course_crud()
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
