"""Script para probar endpoint de evaluación de escritura"""
import requests
import os

API_URL = "http://localhost:5000/api/academic/tools/evaluate-writing"
TEST_FILE = "test_document.txt"

print("=" * 80)
print("🧪 PROBANDO ENDPOINT DE EVALUACIÓN DE ESCRITURA")
print("=" * 80)
print(f"URL: {API_URL}")
print(f"Archivo: {TEST_FILE}")
print()

# Verificar que el archivo existe
if not os.path.exists(TEST_FILE):
    print(f"❌ ERROR: No se encuentra el archivo {TEST_FILE}")
    exit(1)

try:
    # Preparar el archivo
    with open(TEST_FILE, 'rb') as f:
        files = {
            'document': (TEST_FILE, f, 'text/plain')
        }
        data = {
            'user_id': 1
        }
        
        print("📤 Enviando petición POST...")
        response = requests.post(
            API_URL,
            files=files,
            data=data,
            timeout=60
        )
    
    print(f"\n📊 STATUS CODE: {response.status_code}")
    print(f"📦 HEADERS: {dict(response.headers)}")
    
    if response.status_code == 200:
        print("\n✅ ¡ÉXITO! Endpoint funcionando correctamente")
        data = response.json()
        report = data.get('report', {})
        print(f"\n📝 REPORTE:")
        print(f"   Overall Score: {report.get('overall_score', 'N/A')}/100")
        print(f"   Word Count: {report.get('metrics', {}).get('word_count', 'N/A')}")
        print(f"   Readability: {report.get('metrics', {}).get('readability_score', 'N/A')}")
    else:
        print(f"\n❌ ERROR {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: No se puede conectar al backend")
    print("Verifica que el servidor esté corriendo en http://localhost:5000")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"Tipo: {type(e).__name__}")

print("\n" + "=" * 80)
