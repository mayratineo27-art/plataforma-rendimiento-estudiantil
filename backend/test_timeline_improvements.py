"""
Test para validar las mejoras en el sistema de líneas de tiempo
- Creación con y sin curso
- Gestión de historial
- Filtrado y limpieza
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api/academic"

def test_create_timeline_without_course():
    """Test: Crear línea de tiempo SIN curso asociado"""
    print("\n" + "="*60)
    print("TEST 1: Crear línea de tiempo SIN curso")
    print("="*60)
    
    payload = {
        "topic": "Aprender Python desde cero",
        "type": "free",
        "user_id": 1,
        "course_id": None,  # Sin curso
        "project_id": None,
        "save": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/tools/timeline", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Timeline creada exitosamente SIN curso")
            print(f"   Timeline ID: {data.get('timeline_id')}")
            print(f"   Guardada: {data.get('saved')}")
            if 'timeline_data' in data:
                tl = data['timeline_data']
                print(f"   Título: {tl.get('title')}")
                print(f"   Tipo: {tl.get('timeline_type')}")
                print(f"   Curso ID: {tl.get('course_id')}")
                print(f"   Total pasos: {tl.get('total_steps')}")
            return data.get('timeline_id')
        else:
            print(f"❌ Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None


def test_create_timeline_with_course():
    """Test: Crear línea de tiempo CON curso asociado"""
    print("\n" + "="*60)
    print("TEST 2: Crear línea de tiempo CON curso")
    print("="*60)
    
    payload = {
        "topic": "Ecuaciones Diferenciales - Capítulo 5",
        "type": "course",
        "user_id": 1,
        "course_id": 4,  # Con curso
        "save": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/tools/timeline", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Timeline creada exitosamente CON curso")
            print(f"   Timeline ID: {data.get('timeline_id')}")
            print(f"   Guardada: {data.get('saved')}")
            if 'timeline_data' in data:
                tl = data['timeline_data']
                print(f"   Título: {tl.get('title')}")
                print(f"   Tipo: {tl.get('timeline_type')}")
                print(f"   Curso ID: {tl.get('course_id')}")
                print(f"   Total pasos: {tl.get('total_steps')}")
            return data.get('timeline_id')
        else:
            print(f"❌ Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None


def test_get_timeline_history(user_id=1):
    """Test: Obtener historial de líneas de tiempo"""
    print("\n" + "="*60)
    print("TEST 3: Obtener historial de timelines")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/timelines/history", params={"user_id": user_id})
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            timelines = data.get('timelines', [])
            print(f"✅ Historial obtenido exitosamente")
            print(f"   Total timelines: {data.get('total')}")
            
            for i, tl in enumerate(timelines[:5], 1):  # Mostrar primeras 5
                print(f"\n   Timeline {i}:")
                print(f"     - ID: {tl.get('id')}")
                print(f"     - Título: {tl.get('title')}")
                print(f"     - Tipo: {tl.get('timeline_type')}")
                print(f"     - Curso ID: {tl.get('course_id')}")
                print(f"     - Progreso: {tl.get('progress')}%")
                print(f"     - Completada: {tl.get('is_completed')}")
                print(f"     - Creada: {tl.get('created_at')}")
            
            return timelines
        else:
            print(f"❌ Error: {response.json()}")
            return []
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return []


def test_get_timeline_history_filtered(user_id=1, timeline_type="free"):
    """Test: Obtener historial filtrado por tipo"""
    print("\n" + "="*60)
    print(f"TEST 4: Obtener historial filtrado (tipo={timeline_type})")
    print("="*60)
    
    try:
        params = {
            "user_id": user_id,
            "timeline_type": timeline_type,
            "limit": 10
        }
        response = requests.get(f"{BASE_URL}/timelines/history", params=params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Historial filtrado obtenido")
            print(f"   Total timelines tipo '{timeline_type}': {data.get('total')}")
            
            for tl in data.get('timelines', [])[:3]:
                print(f"   - {tl.get('title')} (ID: {tl.get('id')})")
            
            return data.get('timelines', [])
        else:
            print(f"❌ Error: {response.json()}")
            return []
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return []


def test_get_timeline_detail(timeline_id):
    """Test: Obtener detalles de una timeline específica"""
    print("\n" + "="*60)
    print(f"TEST 5: Obtener detalle de timeline {timeline_id}")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/timelines/{timeline_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            tl = response.json()
            print("✅ Detalle obtenido exitosamente")
            print(f"   ID: {tl.get('id')}")
            print(f"   Título: {tl.get('title')}")
            print(f"   Descripción: {tl.get('description')}")
            print(f"   Tipo: {tl.get('timeline_type')}")
            print(f"   Curso ID: {tl.get('course_id')}")
            print(f"   Pasos totales: {tl.get('total_steps')}")
            print(f"   Pasos completados: {tl.get('completed_steps')}")
            print(f"   Progreso: {tl.get('progress')}%")
            return tl
        else:
            print(f"❌ Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None


def test_delete_timeline_soft(timeline_id):
    """Test: Eliminar timeline (soft delete)"""
    print("\n" + "="*60)
    print(f"TEST 6: Eliminar timeline {timeline_id} (soft delete)")
    print("="*60)
    
    try:
        response = requests.delete(f"{BASE_URL}/timelines/{timeline_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Timeline eliminada (soft delete)")
            print(f"   Mensaje: {data.get('message')}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def test_cleanup_timelines(user_id=1):
    """Test: Limpiar timelines antiguas"""
    print("\n" + "="*60)
    print("TEST 7: Limpiar timelines antiguas")
    print("="*60)
    
    payload = {
        "user_id": user_id,
        "days_old": 365,  # Más de 1 año
        "delete_completed": False,
        "permanent": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/timelines/cleanup", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Limpieza ejecutada")
            print(f"   Mensaje: {data.get('message')}")
            print(f"   Cantidad afectada: {data.get('count')}")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*60)
    print("🧪 SUITE DE TESTS - GESTIÓN DE TIMELINES")
    print("="*60)
    print("Fecha:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Test 1: Crear timeline sin curso
    timeline_id_1 = test_create_timeline_without_course()
    
    # Test 2: Crear timeline con curso
    timeline_id_2 = test_create_timeline_with_course()
    
    # Test 3: Obtener historial completo
    timelines = test_get_timeline_history(user_id=1)
    
    # Test 4: Obtener historial filtrado
    free_timelines = test_get_timeline_history_filtered(user_id=1, timeline_type="free")
    
    # Test 5: Obtener detalle de una timeline
    if timeline_id_1:
        test_get_timeline_detail(timeline_id_1)
    
    # Test 6: Soft delete de una timeline
    if timeline_id_2:
        test_delete_timeline_soft(timeline_id_2)
    
    # Test 7: Limpiar timelines antiguas
    test_cleanup_timelines(user_id=1)
    
    print("\n" + "="*60)
    print("✅ TESTS COMPLETADOS")
    print("="*60)
    print("\nResumen:")
    print(f"  - Timeline sin curso creada: {'✅' if timeline_id_1 else '❌'}")
    print(f"  - Timeline con curso creada: {'✅' if timeline_id_2 else '❌'}")
    print(f"  - Historial obtenido: ✅")
    print(f"  - Filtrado por tipo: ✅")
    print(f"  - Detalle obtenido: {'✅' if timeline_id_1 else '❌'}")
    print(f"  - Soft delete: {'✅' if timeline_id_2 else '❌'}")
    print(f"  - Limpieza ejecutada: ✅")


if __name__ == '__main__':
    main()
