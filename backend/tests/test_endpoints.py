#!/usr/bin/env python
"""
test_endpoints.py - Script para verificar que los endpoints funcionan

Uso:
    python test_endpoints.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def print_result(test_name, response):
    """Imprimir resultado de prueba"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")

def test_health():
    """Probar endpoint de health"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_result("Health Check", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root():
    """Probar endpoint raíz"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print_result("Root Endpoint", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_video_test():
    """Probar endpoint de prueba de video"""
    try:
        response = requests.get(f"{BASE_URL}/api/video/test")
        print_result("Video Test Endpoint", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_audio_test():
    """Probar endpoint de prueba de audio"""
    try:
        response = requests.get(f"{BASE_URL}/api/audio/test")
        print_result("Audio Test Endpoint", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_start_video_session():
    """Probar inicio de sesión de video"""
    try:
        data = {
            "user_id": 1,
            "session_name": "Test Session",
            "session_type": "estudio",
            "course_name": "Test Course"
        }
        response = requests.post(f"{BASE_URL}/api/video/session/start", json=data)
        print_result("Start Video Session", response)
        
        if response.status_code == 201:
            return response.json().get('session', {}).get('id')
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE ENDPOINTS - MÓDULO 2")
    print("="*60 + "\n")
    
    results = {
        'health': False,
        'root': False,
        'video_test': False,
        'audio_test': False,
        'video_session': False
    }
    
    # Probar endpoints básicos
    print("🔍 Probando endpoints básicos...")
    results['health'] = test_health()
    results['root'] = test_root()
    
    # Probar endpoints de prueba
    print("\n🔍 Probando endpoints de prueba...")
    results['video_test'] = test_video_test()
    results['audio_test'] = test_audio_test()
    
    # Probar inicio de sesión
    print("\n🔍 Probando inicio de sesión de video...")
    session_id = test_start_video_session()
    results['video_session'] = session_id is not None
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE RESULTADOS")
    print("="*60)
    
    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test}: {'PASS' if result else 'FAIL'}")
    
    total = sum(results.values())
    print(f"\n{'='*60}")
    print(f"Total: {total}/{len(results)} pruebas pasadas")
    print(f"{'='*60}\n")
    
    if total == len(results):
        print("🎉 ¡TODOS LOS TESTS PASARON!")
    else:
        print("⚠️  Algunos tests fallaron. Revisa la configuración.")
    
    return total == len(results)

if __name__ == '__main__':
    main()