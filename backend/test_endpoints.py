"""
Script de prueba para verificar que los endpoints funcionen correctamente
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_create_course():
    """Prueba crear un curso"""
    print("\n🧪 Probando creación de curso...")
    data = {
        "user_id": 1,
        "name": "Curso de Prueba",
        "professor": "Prof. Test",
        "schedule_info": "Lunes 10-12",
        "color": "#3B82F6"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/academic/courses", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Curso creado exitosamente")
            return response.json()['id']
        else:
            print("❌ Error al crear curso")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_get_dashboard():
    """Prueba obtener dashboard"""
    print("\n🧪 Probando obtener dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/api/academic/user/1/dashboard")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Cursos: {len(data.get('courses', []))}")
        print(f"Tareas: {len(data.get('pending_tasks', []))}")
        
        if response.status_code == 200:
            print("✅ Dashboard obtenido exitosamente")
        else:
            print("❌ Error al obtener dashboard")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_mindmap():
    """Prueba generación de mapa mental"""
    print("\n🧪 Probando generación de mapa mental...")
    data = {
        "text": "Explica los conceptos fundamentales de programación orientada a objetos",
        "context": "Curso de POO"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/academic/tools/mindmap", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Mapa mental generado exitosamente")
            print(f"Root: {result.get('mindmap', {}).get('root', 'N/A')}")
        else:
            print(f"❌ Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_summary():
    """Prueba generación de resumen"""
    print("\n🧪 Probando generación de resumen...")
    data = {
        "text": "La inteligencia artificial es el campo de la ciencia que estudia cómo hacer que las máquinas piensen como humanos",
        "type": "general"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/academic/tools/summary", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resumen generado exitosamente")
            print(f"Longitud: {len(result.get('summary', ''))} caracteres")
        else:
            print(f"❌ Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_timeline():
    """Prueba generación de línea de tiempo"""
    print("\n🧪 Probando generación de línea de tiempo...")
    data = {
        "topic": "Desarrollo de tesis sobre machine learning",
        "type": "academic"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/academic/tools/timeline", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            timeline = result.get('timeline', {})
            print("✅ Línea de tiempo generada exitosamente")
            print(f"Título: {timeline.get('title', 'N/A')}")
            print(f"Milestones: {len(timeline.get('milestones', []))}")
        else:
            print(f"❌ Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_projects():
    """Prueba endpoints de proyectos"""
    print("\n🧪 Probando endpoints de proyectos...")
    
    # Crear un proyecto de prueba
    course_id = test_create_course()
    if not course_id:
        print("❌ No se pudo crear curso para probar proyectos")
        return
    
    data = {
        "course_id": course_id,
        "user_id": 1,
        "name": "Proyecto de Prueba",
        "description": "Proyecto para testing",
        "priority": "alta",
        "status": "en_progreso"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/projects/", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Proyecto creado exitosamente")
            project_id = response.json()['project']['id']
            
            # Probar iniciar sesión
            print("\n🧪 Probando iniciar sesión de tiempo...")
            response = requests.post(f"{BASE_URL}/api/projects/{project_id}/session/start", json={"user_id": 1})
            print(f"Status: {response.status_code}")
            
            if response.status_code == 201:
                print("✅ Sesión iniciada exitosamente")
        else:
            print(f"❌ Error: {response.json()}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 TESTING DE ENDPOINTS - MÓDULO 1")
    print("=" * 60)
    
    test_get_dashboard()
    test_create_course()
    test_mindmap()
    test_summary()
    test_timeline()
    test_projects()
    
    print("\n" + "=" * 60)
    print("✅ TESTS COMPLETADOS")
    print("=" * 60)
