"""
Test rápido del endpoint de evaluación de escritura
"""
import requests
import os

# URL del endpoint
url = "http://localhost:5000/api/academic/tools/evaluate-writing"

print("=" * 80)
print("🧪 PROBANDO ENDPOINT DE EVALUACIÓN DE ESCRITURA")
print("=" * 80)

# Crear archivo de prueba
test_file_path = "test_document.txt"
with open(test_file_path, "w", encoding="utf-8") as f:
    f.write("""
La educación es fundamental para el desarrollo de las sociedades modernas.
A través del aprendizaje continuo, las personas pueden adquirir nuevas 
habilidades y conocimientos que les permiten enfrentar los desafíos del 
siglo XXI.

En este contexto, las nuevas tecnologías juegan un papel crucial. 
Las plataformas digitales facilitan el acceso a información y recursos
educativos que antes eran difíciles de obtener. Sin embargo, también 
presentan desafíos importantes relacionados con la equidad y el acceso.

Por lo tanto, es necesario desarrollar estrategias que garanticen que 
todos los estudiantes puedan beneficiarse de estas herramientas. Esto 
requiere inversión en infraestructura, capacitación docente y políticas
educativas inclusivas que no dejen a nadie atrás.
""")

print(f"📄 Archivo de prueba creado: {test_file_path}")

try:
    # Preparar datos
    with open(test_file_path, "rb") as f:
        files = {
            'document': ('test_document.txt', f, 'text/plain')
        }
        data = {
            'user_id': 1,
            'course_id': 1
        }
        
        print(f"\n📤 Enviando solicitud a: {url}")
        print(f"   User ID: {data['user_id']}")
        print(f"   Course ID: {data['course_id']}")
        
        response = requests.post(url, files=files, data=data, timeout=60)
        
        print(f"\n📥 Respuesta recibida:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ EVALUACIÓN EXITOSA")
            print(f"\n📊 Score General: {result['report']['evaluation']['overall_score']}/100")
            print(f"   - Gramática: {result['report']['evaluation']['grammar_score']}/100")
            print(f"   - Coherencia: {result['report']['evaluation']['coherence_score']}/100")
            print(f"   - Vocabulario: {result['report']['evaluation']['vocabulary_score']}/100")
            print(f"   - Estructura: {result['report']['evaluation']['structure_score']}/100")
            
            print(f"\n📈 Métricas:")
            metrics = result['report']['metrics']['current']
            print(f"   - Palabras: {metrics['word_count']}")
            print(f"   - Oraciones: {metrics['sentence_count']}")
            print(f"   - Vocabulario único: {metrics['vocabulary_size']}")
            print(f"   - Legibilidad: {metrics['readability_score']}/100")
            
            print(f"\n💪 Fortalezas:")
            for strength in result['report']['evaluation']['strengths'][:3]:
                print(f"   ✓ {strength}")
            
            print(f"\n⚠️  Áreas de mejora:")
            for weakness in result['report']['evaluation']['weaknesses'][:3]:
                print(f"   - {weakness}")
            
            print(f"\n💡 Recomendaciones:")
            for rec in result['report']['evaluation']['recommendations'][:3]:
                print(f"   → {rec}")
                
        elif response.status_code == 404:
            print(f"\n❌ ERROR 404: El endpoint no existe")
            print(f"\n🔧 SOLUCIÓN:")
            print(f"   1. Verifica que el backend esté corriendo")
            print(f"   2. REINICIA el backend (Ctrl+C y luego python run.py)")
            print(f"   3. Vuelve a intentar")
            
        elif response.status_code == 503:
            print(f"\n❌ ERROR 503: Servicio no disponible")
            print(f"   WritingEvaluator no se pudo importar")
            
        else:
            print(f"\n❌ ERROR {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
except requests.exceptions.ConnectionError:
    print(f"\n❌ ERROR: No se puede conectar al backend")
    print(f"\n🔧 SOLUCIÓN:")
    print(f"   1. Asegúrate de que el backend esté corriendo:")
    print(f"      cd backend")
    print(f"      python run.py")
    print(f"   2. Verifica que esté en http://localhost:5000")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Limpiar
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
        print(f"\n🧹 Archivo de prueba eliminado")

print("\n" + "=" * 80)
